#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Structure-Aware FAISS Index Creator V2
Creates a better index by understanding document structure (articles, notes, tables)
Reduces chunks while maintaining complete context
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple
from datetime import datetime
from dataclasses import dataclass

try:
    from sentence_transformers import SentenceTransformer
    import faiss
    import numpy as np
    print("✅ All required packages imported successfully")
except ImportError as e:
    print(f"❌ Missing required package: {e}")
    print("Please install: pip install sentence-transformers faiss-cpu")
    exit(1)


@dataclass
class DocumentChunk:
    """Structured chunk with rich metadata"""
    text: str
    source_file: str
    chunk_type: str  # 'title', 'introduction', 'article', 'definitions', 'table', 'conclusion'
    article_numbers: List[int]  # Articles present in this chunk
    note_numbers: List[int]  # Notes (تبصره) present in this chunk
    has_table: bool
    has_list: bool
    document_section: str  # e.g., "ماده 2- نحوه محاسبه"
    document_title: str
    chunk_index: int
    metadata: Dict[str, Any]


class StructureAwareChunker:
    """Chunks documents based on logical structure"""
    
    def __init__(self, max_chunk_size: int = 1000, min_chunk_size: int = 200):
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size
        
        # Regex patterns for structure detection
        self.patterns = {
            'title': re.compile(r'^#\s+(.+)$', re.MULTILINE),
            'section': re.compile(r'^##\s+(.+)$', re.MULTILINE),
            'subsection': re.compile(r'^###\s+(.+)$', re.MULTILINE),
            'article': re.compile(r'##\s*ماده\s+(\d+)[:-]?\s*(.+?)(?=\n|$)', re.MULTILINE),
            'note': re.compile(r'\*\*تبصره\s+(\d+):\*\*\s*(.+?)(?=\n\n|\*\*تبصره|\Z)', re.DOTALL),
            'explanation': re.compile(r'\*\*توضیح\s+(\d+):\*\*\s*(.+?)(?=\n\n|\*\*توضیح|\Z)', re.DOTALL),
            'definition': re.compile(r'\*\*([^*]+):\*\*\s*(.+?)(?=\n-|\n\*\*|\n\n|\Z)', re.DOTALL),
            'list_item': re.compile(r'^-\s+(.+)$', re.MULTILINE),
            'table': re.compile(r'\|.+\|', re.MULTILINE),
            'numbered_list': re.compile(r'^\d+[-.)]\s+(.+)$', re.MULTILINE),
        }
    
    def extract_document_title(self, text: str) -> str:
        """Extract main title from document"""
        match = self.patterns['title'].search(text)
        if match:
            return match.group(1).strip()
        return "عنوان نامشخص"
    
    def detect_chunk_type(self, text: str, section_name: str) -> str:
        """Determine the type of chunk based on content"""
        text_lower = text.lower()
        section_lower = section_name.lower()
        
        if 'مقدمه' in section_lower:
            return 'introduction'
        elif 'تعاریف' in section_lower or 'تعریف' in section_lower:
            return 'definitions'
        elif self.patterns['table'].search(text):
            return 'table'
        elif 'ماده' in section_lower:
            return 'article'
        elif 'بخش' in section_lower:
            return 'section'
        elif any(end in section_lower for end in ['اجرایی است', 'تصویب', 'مصوب']):
            return 'conclusion'
        else:
            return 'general'
    
    def extract_article_numbers(self, text: str) -> List[int]:
        """Extract all article numbers mentioned in text"""
        article_numbers = []
        
        # Find article declarations (## ماده X)
        for match in self.patterns['article'].finditer(text):
            try:
                article_numbers.append(int(match.group(1)))
            except (ValueError, IndexError):
                pass
        
        # Find article references (به استناد ماده X, موضوع ماده Y)
        ref_pattern = re.compile(r'ماده\s+(\d+)', re.IGNORECASE)
        for match in ref_pattern.finditer(text):
            try:
                num = int(match.group(1))
                if num not in article_numbers:
                    article_numbers.append(num)
            except (ValueError, IndexError):
                pass
        
        return sorted(article_numbers)
    
    def extract_note_numbers(self, text: str) -> List[int]:
        """Extract all note numbers (تبصره) mentioned in text"""
        note_numbers = []
        
        # Find note declarations
        for match in self.patterns['note'].finditer(text):
            try:
                note_numbers.append(int(match.group(1)))
            except (ValueError, IndexError):
                pass
        
        # Find note references
        ref_pattern = re.compile(r'تبصره\s+(\d+)', re.IGNORECASE)
        for match in ref_pattern.finditer(text):
            try:
                num = int(match.group(1))
                if num not in note_numbers:
                    note_numbers.append(num)
            except (ValueError, IndexError):
                pass
        
        return sorted(note_numbers)
    
    def split_by_structure(self, text: str, source_file: str) -> List[DocumentChunk]:
        """Split document into logical chunks based on structure"""
        
        chunks = []
        document_title = self.extract_document_title(text)
        
        # Split by main sections (##)
        sections = re.split(r'\n(?=##\s)', text)
        
        # First section is usually title + introduction
        if sections:
            title_and_intro = sections[0]
            
            # Split title from introduction if both exist
            title_match = self.patterns['title'].search(title_and_intro)
            if title_match:
                title_text = title_match.group(0)
                remaining = title_and_intro[title_match.end():].strip()
                
                # Create title chunk (small, so combine with intro if exists)
                if remaining:
                    combined = f"{title_text}\n\n{remaining}"
                    if len(combined) < self.max_chunk_size:
                        chunks.append(self._create_chunk(
                            text=combined,
                            source_file=source_file,
                            document_title=document_title,
                            section_name="عنوان و مقدمه",
                            chunk_index=0
                        ))
                    else:
                        # Title chunk
                        chunks.append(self._create_chunk(
                            text=title_text,
                            source_file=source_file,
                            document_title=document_title,
                            section_name="عنوان",
                            chunk_index=0
                        ))
                        # Introduction chunk
                        chunks.append(self._create_chunk(
                            text=remaining,
                            source_file=source_file,
                            document_title=document_title,
                            section_name="مقدمه",
                            chunk_index=1
                        ))
                else:
                    chunks.append(self._create_chunk(
                        text=title_text,
                        source_file=source_file,
                        document_title=document_title,
                        section_name="عنوان",
                        chunk_index=0
                    ))
        
        # Process remaining sections
        for section_text in sections[1:]:
            section_text = section_text.strip()
            if not section_text:
                continue
            
            # Extract section name
            section_match = self.patterns['section'].search(section_text)
            section_name = section_match.group(1) if section_match else "بخش نامشخص"
            
            # Check if this is an article with notes
            article_match = self.patterns['article'].search(section_text)
            
            if article_match:
                # This is an article - keep it with its notes
                chunks.extend(self._process_article_section(
                    section_text=section_text,
                    source_file=source_file,
                    document_title=document_title,
                    section_name=section_name,
                    start_index=len(chunks)
                ))
            else:
                # Regular section - check if it needs splitting
                if len(section_text) <= self.max_chunk_size:
                    # Keep as single chunk
                    chunks.append(self._create_chunk(
                        text=section_text,
                        source_file=source_file,
                        document_title=document_title,
                        section_name=section_name,
                        chunk_index=len(chunks)
                    ))
                else:
                    # Split large section intelligently
                    chunks.extend(self._split_large_section(
                        section_text=section_text,
                        source_file=source_file,
                        document_title=document_title,
                        section_name=section_name,
                        start_index=len(chunks)
                    ))
        
        return chunks
    
    def _process_article_section(
        self,
        section_text: str,
        source_file: str,
        document_title: str,
        section_name: str,
        start_index: int
    ) -> List[DocumentChunk]:
        """Process an article section with its notes"""
        
        chunks = []
        
        # Try to split by notes
        note_pattern = re.compile(r'\n(?=\*\*تبصره\s+\d+:\*\*)')
        parts = note_pattern.split(section_text)
        
        if len(parts) == 1:
            # No notes, or article is small enough
            if len(section_text) <= self.max_chunk_size:
                chunks.append(self._create_chunk(
                    text=section_text,
                    source_file=source_file,
                    document_title=document_title,
                    section_name=section_name,
                    chunk_index=start_index
                ))
            else:
                # Article is too large, split it
                chunks.extend(self._split_large_section(
                    section_text=section_text,
                    source_file=source_file,
                    document_title=document_title,
                    section_name=section_name,
                    start_index=start_index
                ))
        else:
            # Article with notes
            # Keep article main content with first note if possible
            current_chunk = parts[0]
            
            for i, part in enumerate(parts[1:], 1):
                part = part.strip()
                if not part:
                    continue
                
                # Check if we can add this note to current chunk
                if len(current_chunk) + len(part) + 2 <= self.max_chunk_size:
                    current_chunk = f"{current_chunk}\n\n{part}"
                else:
                    # Save current chunk
                    if current_chunk.strip():
                        chunks.append(self._create_chunk(
                            text=current_chunk,
                            source_file=source_file,
                            document_title=document_title,
                            section_name=section_name,
                            chunk_index=start_index + len(chunks)
                        ))
                    current_chunk = part
            
            # Add final chunk
            if current_chunk.strip():
                chunks.append(self._create_chunk(
                    text=current_chunk,
                    source_file=source_file,
                    document_title=document_title,
                    section_name=section_name,
                    chunk_index=start_index + len(chunks)
                ))
        
        return chunks
    
    def _split_large_section(
        self,
        section_text: str,
        source_file: str,
        document_title: str,
        section_name: str,
        start_index: int
    ) -> List[DocumentChunk]:
        """Split a large section into smaller chunks at paragraph boundaries"""
        
        chunks = []
        
        # Split by double newline (paragraphs)
        paragraphs = section_text.split('\n\n')
        
        current_chunk = ""
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # Check if adding this paragraph exceeds limit
            if len(current_chunk) + len(para) + 2 <= self.max_chunk_size:
                if current_chunk:
                    current_chunk = f"{current_chunk}\n\n{para}"
                else:
                    current_chunk = para
            else:
                # Save current chunk if it meets minimum size
                if current_chunk.strip() and len(current_chunk) >= self.min_chunk_size:
                    chunks.append(self._create_chunk(
                        text=current_chunk,
                        source_file=source_file,
                        document_title=document_title,
                        section_name=section_name,
                        chunk_index=start_index + len(chunks)
                    ))
                    current_chunk = para
                else:
                    # Current chunk is too small, force add this paragraph
                    if current_chunk:
                        current_chunk = f"{current_chunk}\n\n{para}"
                    else:
                        current_chunk = para
        
        # Add final chunk
        if current_chunk.strip():
            chunks.append(self._create_chunk(
                text=current_chunk,
                source_file=source_file,
                document_title=document_title,
                section_name=section_name,
                chunk_index=start_index + len(chunks)
            ))
        
        return chunks
    
    def _create_chunk(
        self,
        text: str,
        source_file: str,
        document_title: str,
        section_name: str,
        chunk_index: int
    ) -> DocumentChunk:
        """Create a DocumentChunk with metadata"""
        
        chunk_type = self.detect_chunk_type(text, section_name)
        article_numbers = self.extract_article_numbers(text)
        note_numbers = self.extract_note_numbers(text)
        has_table = bool(self.patterns['table'].search(text))
        has_list = bool(self.patterns['list_item'].search(text) or 
                       self.patterns['numbered_list'].search(text))
        
        # Extract key information
        metadata = {
            'has_definitions': '**' in text and ':' in text,
            'has_numbers': any(char.isdigit() for char in text),
            'has_references': 'به استناد' in text or 'موضوع ماده' in text,
            'length': len(text),
            'word_count': len(text.split())
        }
        
        return DocumentChunk(
            text=text,
            source_file=source_file,
            chunk_type=chunk_type,
            article_numbers=article_numbers,
            note_numbers=note_numbers,
            has_table=has_table,
            has_list=has_list,
            document_section=section_name,
            document_title=document_title,
            chunk_index=chunk_index,
            metadata=metadata
        )


class FAISSIndexCreatorV2:
    """Create FAISS index with structure-aware chunking"""
    
    def __init__(
        self,
        documents_dir: str = "./documents",
        index_dir: str = "./index",
        embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    ):
        self.documents_dir = Path(documents_dir)
        self.index_dir = Path(index_dir)
        self.embedding_model_name = embedding_model
        
        # Create index directory
        self.index_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        print(f"🤖 Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model, device="cpu")
        self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()
        
        self.chunker = StructureAwareChunker(max_chunk_size=1000, min_chunk_size=200)
        
        # Storage
        self.all_chunks: List[DocumentChunk] = []
        self.embeddings: List[np.ndarray] = []
    
    def process_documents(self):
        """Process all documents in the documents directory"""
        
        print(f"\n📂 Processing documents from: {self.documents_dir}")
        
        txt_files = list(self.documents_dir.glob("*.txt"))
        
        if not txt_files:
            raise FileNotFoundError(f"No .txt files found in {self.documents_dir}")
        
        print(f"📄 Found {len(txt_files)} document(s)")
        
        for file_path in sorted(txt_files):
            print(f"\n📖 Processing: {file_path.name}")
            self._process_single_document(file_path)
        
        print(f"\n✅ Total chunks created: {len(self.all_chunks)}")
        
        # Statistics
        chunk_types = {}
        for chunk in self.all_chunks:
            chunk_types[chunk.chunk_type] = chunk_types.get(chunk.chunk_type, 0) + 1
        
        print("\n📊 Chunk distribution:")
        for chunk_type, count in sorted(chunk_types.items()):
            print(f"   {chunk_type}: {count}")
    
    def _process_single_document(self, file_path: Path):
        """Process a single document"""
        
        # Read document
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Create chunks
        chunks = self.chunker.split_by_structure(text, file_path.name)
        
        print(f"   ✂️  Created {len(chunks)} chunks")
        
        # Add to collection
        self.all_chunks.extend(chunks)
    
    def create_embeddings(self):
        """Create embeddings for all chunks"""
        
        print(f"\n🧠 Creating embeddings for {len(self.all_chunks)} chunks...")
        
        texts = [chunk.text for chunk in self.all_chunks]
        
        # Create embeddings in batches
        batch_size = 32
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            embeddings = self.embedding_model.encode(batch, show_progress_bar=False)
            self.embeddings.extend(embeddings)
            
            if (i + batch_size) % 100 == 0:
                print(f"   Progress: {min(i + batch_size, len(texts))}/{len(texts)}")
        
        print(f"✅ Created {len(self.embeddings)} embeddings")
    
    def create_faiss_index(self):
        """Create and save FAISS index"""
        
        print(f"\n📊 Creating FAISS index...")
        
        # Convert embeddings to numpy array
        embeddings_array = np.array(self.embeddings).astype('float32')
        
        # Create FAISS index (L2 distance)
        index = faiss.IndexFlatL2(self.embedding_dim)
        index.add(embeddings_array)
        
        # Save index
        index_path = self.index_dir / "faiss_index.bin"
        faiss.write_index(index, str(index_path))
        print(f"✅ FAISS index saved to: {index_path}")
        
        return index
    
    def save_metadata(self):
        """Save chunk metadata to JSON"""
        
        print(f"\n💾 Saving metadata...")
        
        metadata_list = []
        
        for i, chunk in enumerate(self.all_chunks):
            metadata_list.append({
                "chunk_id": i,
                "source_file": chunk.source_file,
                "document_title": chunk.document_title,
                "chunk_index": chunk.chunk_index,
                "chunk_type": chunk.chunk_type,
                "document_section": chunk.document_section,
                "article_numbers": chunk.article_numbers,
                "note_numbers": chunk.note_numbers,
                "has_table": chunk.has_table,
                "has_list": chunk.has_list,
                "chunk_length": len(chunk.text),
                "chunk_text": chunk.text,
                "metadata": chunk.metadata,
                "indexed_at": datetime.now().isoformat()
            })
        
        # Save metadata
        metadata_path = self.index_dir / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata_list, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Metadata saved to: {metadata_path}")
    
    def save_index_summary(self):
        """Save index summary information"""
        
        print(f"\n📋 Saving index summary...")
        
        summary = {
            "indexed_at": datetime.now().isoformat(),
            "total_documents": len(set(chunk.source_file for chunk in self.all_chunks)),
            "total_chunks": len(self.all_chunks),
            "embedding_model": self.embedding_model_name,
            "embedding_dimension": self.embedding_dim,
            "documents": [],
            "chunking_strategy": "structure_aware",
            "chunk_size_stats": {
                "min": min(len(chunk.text) for chunk in self.all_chunks),
                "max": max(len(chunk.text) for chunk in self.all_chunks),
                "avg": sum(len(chunk.text) for chunk in self.all_chunks) / len(self.all_chunks)
            }
        }
        
        # Document statistics
        doc_chunks = {}
        for chunk in self.all_chunks:
            if chunk.source_file not in doc_chunks:
                doc_chunks[chunk.source_file] = {
                    "filename": chunk.source_file,
                    "title": chunk.document_title,
                    "chunk_count": 0,
                    "total_length": 0
                }
            doc_chunks[chunk.source_file]["chunk_count"] += 1
            doc_chunks[chunk.source_file]["total_length"] += len(chunk.text)
        
        summary["documents"] = list(doc_chunks.values())
        
        # Save summary
        summary_path = self.index_dir / "index_summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Index summary saved to: {summary_path}")
    
    def create_index(self):
        """Main method to create complete index"""
        
        print("="*80)
        print("🚀 FAISS Index Creator V2 - Structure-Aware Chunking")
        print("="*80)
        
        # Process documents
        self.process_documents()
        
        # Create embeddings
        self.create_embeddings()
        
        # Create FAISS index
        self.create_faiss_index()
        
        # Save metadata
        self.save_metadata()
        
        # Save summary
        self.save_index_summary()
        
        print("\n" + "="*80)
        print("✅ Index creation completed successfully!")
        print("="*80)
        
        # Print summary
        print(f"\n📊 Summary:")
        print(f"   Documents processed: {len(set(chunk.source_file for chunk in self.all_chunks))}")
        print(f"   Total chunks: {len(self.all_chunks)}")
        print(f"   Index location: {self.index_dir}")
        print(f"   Embedding model: {self.embedding_model_name}")
        print(f"   Embedding dimension: {self.embedding_dim}")


def main():
    """Main execution function"""
    
    # Configuration
    DOCUMENTS_DIR = "./documents"
    INDEX_DIR = "./index"
    EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    
    # Create index
    creator = FAISSIndexCreatorV2(
        documents_dir=DOCUMENTS_DIR,
        index_dir=INDEX_DIR,
        embedding_model=EMBEDDING_MODEL
    )
    
    creator.create_index()


if __name__ == "__main__":
    main()
