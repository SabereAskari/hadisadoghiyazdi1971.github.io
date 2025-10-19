#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FAISS Index Creator V4 - Upgraded RAG Optimized
ایندکس‌سازی هوشمند با قابلیت‌های پیشرفته برای RAG و اسناد فارسی/قانونی
"""

import os
import json
import re
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import numpy as np
try:
    from sentence_transformers import SentenceTransformer
    import faiss
    from sklearn.preprocessing import normalize
    from sklearn.feature_extraction.text import TfidfVectorizer
    print("✅ همه کتابخانه‌های مورد نیاز با موفقیت وارد شدند")
except ImportError as e:
    print(f"❌ کتابخانه مفقوده: {e}")
    print("لطفا نصب کنید: pip install sentence-transformers faiss-cpu scikit-learn tqdm")
    exit(1)

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class AdvancedDocumentChunk:
    id: str
    text: str
    source_file: str
    chunk_type: str
    article_numbers: List[int]
    note_numbers: List[int]
    has_table: bool
    has_list: bool
    document_section: str
    document_title: str
    chunk_index: int
    keywords: List[str]
    embedding: Optional[np.ndarray] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if not self.id:
            self.id = self.generate_id()
    
    def generate_id(self) -> str:
        content = f"{self.source_file}_{self.chunk_index}_{self.text[:50]}"
        return hashlib.md5(content.encode()).hexdigest()

class AdvancedStructureAwareChunker:
    def __init__(self, max_chunk_size: int = 800, min_chunk_size: int = 150, overlap_size: int = 50):
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size
        self.overlap_size = overlap_size
        self.patterns = {
            'title': re.compile(r'^#\s+(.+)$', re.MULTILINE | re.UNICODE),
            'section': re.compile(r'^##\s+(.+)$', re.MULTILINE | re.UNICODE),
            'subsection': re.compile(r'^###\s+(.+)$', re.MULTILINE | re.UNICODE),
            'article': re.compile(r'(?:##\s*)?ماده\s+(\d+)[:-]?\s*(.+?)(?=\n|$)', re.MULTILINE | re.UNICODE),
            'note': re.compile(r'(?:\*+)?تبصره\s+(\d+):?\s*(.+?)(?=\n\n|\*+تبصره|\Z)', re.DOTALL | re.UNICODE),
            'regulation': re.compile(r'(?:##\s*)?(آیین نامه|دستورالعمل|بخشنامه|سیاست|قانون)\s*(.+?)(?=\n|$)', re.MULTILINE | re.UNICODE),
            'definition': re.compile(r'\*\*([^*]+):\*\*\s*(.+?)(?=\n-|\n\*\*|\n\n|\Z)', re.DOTALL | re.UNICODE),
            'list_item': re.compile(r'^-\s+(.+)$', re.MULTILINE | re.UNICODE),
            'table': re.compile(r'\|.+\|', re.MULTILINE | re.UNICODE),
            'numbered_list': re.compile(r'^\d+[-.)]\s+(.+)$', re.MULTILINE | re.UNICODE),
            'reference': re.compile(r'(به استناد|موضوع|طبق)\s+ماده\s+(\d+)', re.IGNORECASE | re.UNICODE),
        }
    
    def extract_document_structure(self, text: str) -> Dict[str, Any]:
        structure = {
            'title': self._extract_title(text),
            'sections': self._extract_sections(text),
            'articles': self._extract_articles(text),
            'notes': self._extract_notes(text),
            'regulations': self._extract_regulations(text),
            'tables': self._extract_tables(text)
        }
        return structure
    
    def _extract_title(self, text: str) -> str:
        match = self.patterns['title'].search(text)
        return match.group(1).strip() if match else "عنوان نامشخص"
    
    def _extract_sections(self, text: str) -> List[Dict]:
        sections = []
        for match in self.patterns['section'].finditer(text):
            sections.append({
                'title': match.group(1).strip(),
                'start_pos': match.start(),
                'end_pos': match.end()
            })
        return sections
    
    def _extract_articles(self, text: str) -> List[Dict]:
        articles = []
        for match in self.patterns['article'].finditer(text):
            articles.append({
                'number': int(match.group(1)),
                'title': match.group(2).strip(),
                'content_start': match.end()
            })
        return articles
    
    def _extract_notes(self, text: str) -> List[Dict]:
        notes = []
        for match in self.patterns['note'].finditer(text):
            notes.append({
                'number': int(match.group(1)),
                'content': match.group(2).strip()
            })
        return notes
    
    def _extract_regulations(self, text: str) -> List[Dict]:
        regulations = []
        for match in self.patterns['regulation'].finditer(text):
            regulations.append({
                'type': match.group(1).strip(),
                'title': match.group(2).strip()
            })
        return regulations
    
    def _extract_tables(self, text: str) -> List[Dict]:
        tables = []
        table_content = ""
        in_table = False
        for line in text.splitlines():
            if self.patterns['table'].match(line):
                in_table = True
                table_content += line + "\n"
            elif in_table:
                tables.append({'content': table_content.strip()})
                table_content = ""
                in_table = False
        if table_content:
            tables.append({'content': table_content.strip()})
        return tables
    
    def chunk_text(self, text: str, source_file: str) -> List[AdvancedDocumentChunk]:
        chunks = []
        structure = self.extract_document_structure(text)
        document_title = structure['title']
        positions = [0]
        for section in structure['sections']:
            positions.append(section['start_pos'])
        positions.append(len(text))
        
        chunk_index = 0
        for i in range(len(positions) - 1):
            section_text = text[positions[i]:positions[i+1]].strip()
            if len(section_text) < self.min_chunk_size:
                continue
            start = 0
            while start < len(section_text):
                end = min(start + self.max_chunk_size, len(section_text))
                if end < len(section_text):
                    sentence_end = section_text.rfind('.', start, end) + 1
                    if sentence_end > start:
                        end = sentence_end
                chunk_text = section_text[start:end]
                if len(chunk_text) < self.min_chunk_size:
                    break
                chunk_type = self._detect_chunk_type(chunk_text)
                keywords = self._extract_keywords(chunk_text)
                chunk = AdvancedDocumentChunk(
                    id="",
                    text=chunk_text,
                    source_file=source_file,
                    chunk_type=chunk_type,
                    article_numbers=self._get_article_numbers(chunk_text),
                    note_numbers=self._get_note_numbers(chunk_text),
                    has_table=bool(self.patterns['table'].search(chunk_text)),
                    has_list=bool(self.patterns['list_item'].search(chunk_text) or self.patterns['numbered_list'].search(chunk_text)),
                    document_section=structure['sections'][i]['title'] if i < len(structure['sections']) else "نامشخص",
                    document_title=document_title,
                    chunk_index=chunk_index,
                    keywords=keywords
                )
                quality_score = self._calculate_quality_score(chunk)
                chunk.metadata['quality_score'] = quality_score
                if quality_score > 0.3:
                    chunks.append(chunk)
                    chunk_index += 1
                start = end - self.overlap_size
        return chunks
    
    def _detect_chunk_type(self, text: str) -> str:
        if self.patterns['title'].search(text):
            return 'title'
        elif self.patterns['article'].search(text):
            return 'article'
        elif self.patterns['note'].search(text):
            return 'note'
        elif self.patterns['regulation'].search(text):
            return 'regulation'
        elif self.patterns['table'].search(text):
            return 'table'
        elif self.patterns['definition'].search(text):
            return 'definitions'
        else:
            return 'general'
    
    def _get_article_numbers(self, text: str) -> List[int]:
        return [int(m.group(1)) for m in self.patterns['article'].finditer(text)]
    
    def _get_note_numbers(self, text: str) -> List[int]:
        return [int(m.group(1)) for m in self.patterns['note'].finditer(text)]
    
    def _extract_keywords(self, text: str, top_n: int = 5) -> List[str]:
        vectorizer = TfidfVectorizer(max_features=100, stop_words=['و', 'از', 'به', 'در', 'که', 'با', 'این'])
        try:
            tfidf = vectorizer.fit_transform([text])
            indices = tfidf.toarray()[0].argsort()[-top_n:][::-1]
            return [vectorizer.get_feature_names_out()[i] for i in indices]
        except:
            return []
    
    def _calculate_quality_score(self, chunk: AdvancedDocumentChunk) -> float:
        score = 0.0
        length_score = min(len(chunk.text) / self.max_chunk_size, 1.0)
        score += length_score * 0.4
        if chunk.chunk_type in ['article', 'regulation', 'note']:
            score += 0.3
        if chunk.has_table or chunk.has_list:
            score += 0.1
        keyword_density = len(chunk.keywords) / len(chunk.text.split()) if chunk.text.split() else 0
        score += keyword_density * 0.2
        return min(score, 1.0)

class AdvancedFAISSIndexCreator:
    def __init__(self, documents_dir: str, index_dir: str, embedding_model: str = "intfloat/multilingual-e5-large", 
                 max_chunk_size: int = 800, min_chunk_size: int = 150, overlap_size: int = 50,
                 max_workers: int = 4, compression_dim: int = 64):
        self.documents_dir = Path(documents_dir)
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.embedding_model_name = embedding_model
        self.model = SentenceTransformer(embedding_model)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        self.chunker = AdvancedStructureAwareChunker(max_chunk_size, min_chunk_size, overlap_size)
        self.all_chunks: List[AdvancedDocumentChunk] = []
        self.max_workers = max_workers
        self.compression_dim = compression_dim
    
    def load_documents(self) -> List[Tuple[str, str]]:
        documents = []
        supported_extensions = ('.txt', '.md')
        for file_path in self.documents_dir.glob("*"):
            if file_path.suffix.lower() in supported_extensions:
                try:
                    text = file_path.read_text(encoding='utf-8')
                    documents.append((str(file_path), text))
                except Exception as e:
                    logger.warning(f"خطا در خواندن فایل {file_path}: {e}")
        return documents
    
    def process_document(self, doc_path: str, text: str) -> List[AdvancedDocumentChunk]:
        return self.chunker.chunk_text(text, doc_path)
    
    def process_documents_parallel(self):
        documents = self.load_documents()
        if not documents:
            raise ValueError("هیچ سندی یافت نشد!")
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self.process_document, doc_path, text) for doc_path, text in documents]
            for future in tqdm(as_completed(futures), total=len(futures), desc="پردازش اسناد"):
                try:
                    chunks = future.result()
                    self.all_chunks.extend(chunks)
                except Exception as e:
                    logger.error(f"خطا در پردازش سند: {e}")
        logger.info(f"✅ تعداد قطعات استخراج‌شده: {len(self.all_chunks)}")
    
    def create_embeddings_batch(self, batch_size: int = 32):
        texts = [chunk.text for chunk in self.all_chunks]
        embeddings = []
        for i in tqdm(range(0, len(texts), batch_size), desc="ایجاد embeddingها"):
            batch_texts = texts[i:i+batch_size]
            batch_emb = self.model.encode(batch_texts, normalize_embeddings=True)
            embeddings.extend(batch_emb)
        for chunk, emb in zip(self.all_chunks, embeddings):
            chunk.embedding = emb
        logger.info("✅ embeddingها با موفقیت ایجاد شدند")
    
    def create_optimized_faiss_index(self):
        embeddings = np.array([chunk.embedding for chunk in self.all_chunks if chunk.embedding is not None])
        if len(embeddings) == 0:
            raise ValueError("هیچ embeddingی موجود نیست!")
        d = self.embedding_dim
        nb = len(embeddings)
        nlist = max(1, int(np.sqrt(nb)))  # Dynamic nlist
        m = min(self.compression_dim, d // 4)
        m = m - (m % 4) if m % 4 != 0 else m  # Ensure m is divisible by 4
        bits = 4 if nb < 1000 else 8
        k = 2 ** bits
        if nb < k:
            logger.warning(f"Data too small ({nb} < {k}) for PQ. Using IndexHNSWFlat.")
            index = faiss.IndexHNSWFlat(d, 32)
            index.add(embeddings)
        else:
            quantizer = faiss.IndexFlatL2(d)
            index = faiss.IndexIVFPQ(quantizer, d, nlist, m, bits)
            try:
                index.train(embeddings)
                index.add(embeddings)
            except Exception as e:
                logger.error(f"Training failed: {e}. Using IndexFlatL2.")
                index = faiss.IndexFlatL2(d)
                index.add(embeddings)
        faiss.write_index(index, str(self.index_dir / "faiss_index_upgraded.index"))
        logger.info("✅ ایندکس FAISS با موفقیت ایجاد و ذخیره شد")
    
    def save_enhanced_metadata(self):
        metadata_list = [asdict(chunk) for chunk in self.all_chunks]
        for meta in metadata_list:
            meta.pop('embedding', None)
        metadata_path = self.index_dir / "enhanced_metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata_list, f, ensure_ascii=False, indent=2)
        logger.info(f"✅ متادیتا ذخیره شد در: {metadata_path}")
    
    def save_comprehensive_summary(self) -> Dict:
        total_words = sum(len(chunk.text.split()) for chunk in self.all_chunks)
        total_chars = sum(len(chunk.text) for chunk in self.all_chunks)
        chunk_lengths = [len(chunk.text) for chunk in self.all_chunks]
        quality_scores = [chunk.metadata.get('quality_score', 0) for chunk in self.all_chunks]
        chunk_types_dist = {chunk.chunk_type: 0 for chunk in self.all_chunks}
        for chunk in self.all_chunks:
            chunk_types_dist[chunk.chunk_type] = chunk_types_dist.get(chunk.chunk_type, 0) + 1
        summary = {
            "indexed_at": datetime.now().isoformat(),
            "total_documents": len(set(chunk.source_file for chunk in self.all_chunks)),
            "total_chunks": len(self.all_chunks),
            "total_words": total_words,
            "total_characters": total_chars,
            "embedding_model": self.embedding_model_name,
            "embedding_dimension": self.embedding_dim,
            "chunking_strategy": "advanced_structure_aware_upgraded",
            "chunk_size_stats": {
                "min": min(chunk_lengths) if chunk_lengths else 0,
                "max": max(chunk_lengths) if chunk_lengths else 0,
                "avg": sum(chunk_lengths) / len(chunk_lengths) if chunk_lengths else 0,
                "std": np.std(chunk_lengths) if chunk_lengths else 0
            },
            "quality_stats": {
                "min": min(quality_scores) if quality_scores else 0,
                "max": max(quality_scores) if quality_scores else 0,
                "avg": sum(quality_scores) / len(quality_scores) if quality_scores else 0
            },
            "chunk_types_distribution": chunk_types_dist,
            "document_details": self._get_document_details()
        }
        summary_path = self.index_dir / "comprehensive_summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        logger.info(f"✅ خلاصه جامع ذخیره شد در: {summary_path}")
        return summary
    
    def _get_document_details(self) -> List[Dict]:
        doc_details = {}
        for chunk in self.all_chunks:
            if chunk.source_file not in doc_details:
                doc_details[chunk.source_file] = {
                    "filename": chunk.source_file,
                    "title": chunk.document_title,
                    "chunk_count": 0,
                    "total_length": 0,
                    "total_words": 0,
                    "chunk_types": {},
                    "avg_quality_score": 0
                }
            doc = doc_details[chunk.source_file]
            doc["chunk_count"] += 1
            doc["total_length"] += len(chunk.text)
            doc["total_words"] += len(chunk.text.split())
            doc["chunk_types"][chunk.chunk_type] = doc["chunk_types"].get(chunk.chunk_type, 0) + 1
        for doc_file, doc_data in doc_details.items():
            doc_chunks = [chunk for chunk in self.all_chunks if chunk.source_file == doc_file]
            if doc_chunks:
                avg_quality = sum(chunk.metadata.get('quality_score', 0) for chunk in doc_chunks) / len(doc_chunks)
                doc_data["avg_quality_score"] = round(avg_quality, 3)
        return list(doc_details.values())
    
    def create_advanced_index(self):
        print("="*80)
        print("🚀 FAISS Index Creator V4 - Upgraded RAG Optimized")
        print("="*80)
        try:
            self.process_documents_parallel()
            self.create_embeddings_batch()
            self.create_optimized_faiss_index()
            self.save_enhanced_metadata()
            summary = self.save_comprehensive_summary()
            print("\n" + "="*80)
            print("✅ ایجاد ایندکس با موفقیت کامل شد!")
            print("="*80)
            self._print_final_summary(summary)
        except Exception as e:
            logger.error(f"خطا در ایجاد ایندکس: {e}")
            raise
    
    def _print_final_summary(self, summary: Dict):
        print(f"\n📊 خلاصه نهایی:")
        print(f"   📄 اسناد پردازش شده: {summary['total_documents']}")
        print(f"   ✂️  کل قطعات: {summary['total_chunks']}")
        print(f"   📝 کل کلمات: {summary['total_words']:,}")
        print(f"   🔤 کل کاراکترها: {summary['total_characters']:,}")
        print(f"   📏 اندازه متوسط قطعات: {summary['chunk_size_stats']['avg']:.0f} کاراکتر")
        print(f"   ⭐ میانگین امتیاز کیفیت: {summary['quality_stats']['avg']:.2f}")
        print(f"   🤖 مدل embedding: {summary['embedding_model']}")
        print(f"   📁 دایرکتوری ایندکس: {self.index_dir}")
        print("\nتوزیع انواع قطعات:")
        for typ, count in summary['chunk_types_distribution'].items():
            print(f"   - {typ}: {count}")
        print(f"\n📁 فایل‌های ایجاد شده:")
        for file_path in self.index_dir.glob("*"):
            size_mb = file_path.stat().st_size / (1024 * 1024)
            print(f"   📄 {file_path.name} ({size_mb:.2f} MB)")

def main():
    try:
        config = {
            "documents_dir": "./documents",
            "index_dir": "./index_v4_upgraded",
            "embedding_model": "intfloat/multilingual-e5-large",
            "max_chunk_size": 800,
            "min_chunk_size": 150,
            "overlap_size": 50,
            "max_workers": 8,
            "compression_dim": 16  # Reduced for small datasets
        }
        creator = AdvancedFAISSIndexCreator(**config)
        creator.create_advanced_index()
    except Exception as e:
        logger.error(f"خطا در اجرای برنامه: {e}")
        exit(1)

if __name__ == "__main__":
    main()