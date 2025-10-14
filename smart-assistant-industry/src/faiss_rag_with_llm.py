#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced RAG System with FAISS Integration
Complete RAG pipeline with FAISS vector database and LLM generation
Adapted from Qdrant-based system to use local FAISS index
"""

import os
import json
import time
import numpy as np
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import re

# Import required packages
try:
    from sentence_transformers import SentenceTransformer
    import faiss
    from openai import OpenAI
    print("✅ All required packages imported successfully")
except ImportError as e:
    print(f"❌ Missing required package: {e}")
    print("Please install: pip install sentence-transformers faiss-cpu python-dotenv openai")
    exit(1)

@dataclass
class RAGResponse:
    """Structured response from RAG system"""
    query: str
    answer: str
    answer_plain_text: str
    sources: List[Dict[str, Any]]
    confidence: float
    generation_time: float
    retrieval_time: float
    total_time: float
    context_used: str
    category: str
    cross_references: List[str]
    detected_academic_level: str = 'general'  # New field for academic level
    academic_level_confidence: float = 0.0    # New field for confidence

class UniversityRulesRAGWithLLM:
    def __init__(self, 
                 index_dir: str = "./index",
                 env_path: str = ".env"):
        """Initialize the enhanced RAG system with FAISS"""
        
        # Load environment variables
        load_dotenv(env_path)
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set or empty. Please set it in .env or environment.")
        self.llm_model = os.getenv("LLM_MODEL", "openai/gpt-4o-mini")
        
        if not self.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")
        
        self.index_dir = Path(index_dir)
        
        # Load index summary to get configuration
        summary_path = self.index_dir / "index_summary.json"
        if not summary_path.exists():
            raise FileNotFoundError(f"Index summary not found: {summary_path}")
        
        with open(summary_path, 'r', encoding='utf-8') as f:
            self.index_summary = json.load(f)
        
        # Get embedding model from summary
        self.embedding_model_name = self.index_summary.get(
            'embedding_model',
            'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
        )
        
        # Initialize embedding model
        print(f"🤖 Loading embedding model: {self.embedding_model_name}")
        self.embedding_model = SentenceTransformer(self.embedding_model_name, device="cpu")
        self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()
        
        # Load FAISS index
        index_path = self.index_dir / "faiss_index.bin"
        if not index_path.exists():
            raise FileNotFoundError(f"FAISS index not found: {index_path}")
        
        print(f"📂 Loading FAISS index from: {index_path}")
        self.faiss_index = faiss.read_index(str(index_path))
        print(f"✅ FAISS index loaded with {self.faiss_index.ntotal} vectors")
        
        # Load metadata
        metadata_path = self.index_dir / "metadata.json"
        if not metadata_path.exists():
            raise FileNotFoundError(f"Metadata not found: {metadata_path}")
        
        print(f"📂 Loading metadata from: {metadata_path}")
        with open(metadata_path, 'r', encoding='utf-8') as f:
            self.metadata = json.load(f)
        print(f"✅ Loaded metadata for {len(self.metadata)} chunks")
        
        # Import PDF URLs configuration (optional)
        try:
            from src.pdf_urls_config import get_pdf_url, get_document_title, get_document_category
            self.get_pdf_url = get_pdf_url
            self.get_document_title = get_document_title  
            self.get_document_category = get_document_category
            print("✅ PDF URLs configuration loaded")
        except ImportError:
            print("⚠️ PDF URLs configuration not found, using metadata fallback")
            self.get_pdf_url = lambda doc_id: ""
            self.get_document_title = lambda doc_id: doc_id
            self.get_document_category = lambda doc_id: "نامشخص"
        
        # Initialize OpenRouter client (OpenAI-compatible)
        print("🧠 Connecting to OpenRouter...")
        self.openai_client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.openrouter_api_key,
        )
        print(f"✅ Connected to OpenRouter with model: {self.llm_model}")
        
        # RAG configuration
        self.max_context_length = 2000  # Max characters for context
        self.max_sources = 5  # Maximum number of sources to retrieve
        self.min_confidence = 0.0  # Minimum confidence threshold
        
        # Academic level mapping for enhanced filtering
        self.academic_levels = {
            'کاردانی': 'associate_bachelor',
            'کارشناسی': 'associate_bachelor', 
            'کارشناسی ارشد': 'masters',
            'ارشد': 'masters',
            'دکتری': 'phd',
            'دکتری تخصصی': 'phd',
            'عمومی': 'general'
        }
        
        # Academic level keywords for query analysis
        self.level_keywords = {
            'associate_bachelor': ['کاردانی', 'کارشناسی', 'لیسانس', 'bachelor', 'دانشجوی جدید', 'ترم اول'],
            'masters': ['کارشناسی ارشد', 'ارشد', 'فوق لیسانس', 'پایان‌نامه', 'master', 'استاد راهنما'],
            'phd': ['دکتری', 'رساله', 'آزمون جامع', 'phd', 'doctorate'],
            'general': ['عمومی', 'کلی', 'همه', 'تمام دوره‌ها']
        }
        
        print("✅ Enhanced RAG system with FAISS and LLM initialized")
    
    def get_available_categories(self) -> List[str]:
        """Get a list of unique categories from the knowledge base"""
        try:
            from src.pdf_urls_config import get_all_categories
            return get_all_categories()
        except (ImportError, AttributeError):
            # Extract unique categories from metadata
            categories = set()
            for meta in self.metadata:
                if 'category' in meta:
                    categories.add(meta['category'])
                if 'document_type' in meta:
                    categories.add(meta['document_type'])
            return sorted(list(categories)) if categories else ["عمومی"]

    def detect_academic_level(self, query: str) -> tuple[str, float]:
        """Detect the academic level from the query with confidence score"""
        query_lower = query.lower()
        
        level_scores = {}
        
        # Score each academic level based on keyword matches
        for level, keywords in self.level_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in query_lower:
                    # Give higher weight to exact matches
                    if keyword == query_lower.strip():
                        score += 10
                    else:
                        score += len(keyword.split())  # Multi-word keywords get higher scores
            level_scores[level] = score
        
        # Special case: check for combined "کارشناسی ارشد" pattern
        if 'کارشناسی' in query_lower and 'ارشد' in query_lower:
            level_scores['masters'] = max(level_scores.get('masters', 0), 15)  # High score for masters
            level_scores['associate_bachelor'] = 0  # Reset bachelor's score
        
        # Find the level with highest score
        if not level_scores or max(level_scores.values()) == 0:
            return 'general', 0.0
        
        best_level = max(level_scores, key=level_scores.get)
        max_score = level_scores[best_level]
        confidence = min(max_score / 15.0, 1.0)  # Normalize to 0-1 range
        
        return best_level, confidence
    
    def retrieve_relevant_context(self, query: str, top_k: int = 5) -> tuple[List[Dict[str, Any]], float, str]:
        """Retrieve relevant context from FAISS index with academic level filtering"""
        
        retrieval_start = time.time()
        
        # Detect academic level first
        detected_level, level_confidence = self.detect_academic_level(query)
        print(f"🎯 Detected academic level: {detected_level} (confidence: {level_confidence:.2f})")
        
        # Embed the query
        query_embedding = self.embedding_model.encode([query])[0].astype('float32')
        
        # Search in FAISS index - get more results for filtering
        k_search = min(top_k * 3, self.faiss_index.ntotal)
        distances, indices = self.faiss_index.search(
            query_embedding.reshape(1, -1), 
            k_search
        )
        
        # Process and filter results by academic level
        filtered_sources = []
        general_sources = []
        other_sources = []
        
        for idx, (distance, index) in enumerate(zip(distances[0], indices[0])):
            if index == -1:  # Invalid index
                continue
            
            # Get metadata for this chunk
            if index >= len(self.metadata):
                continue
                
            meta = self.metadata[index]
            
            # Convert L2 distance to similarity score (inverse)
            # Lower distance = higher similarity
            # Normalize to 0-1 range (approximate)
            similarity_score = 1.0 / (1.0 + distance)
            
            # Extract document info
            source_file = meta.get('source_file', '')
            document_id = source_file.replace('.txt', '') if source_file.endswith('.txt') else source_file
            
            chunk_level = meta.get('academic_level', 'general')
            
            source_data = {
                "score": float(similarity_score),
                "content": meta.get('chunk_text', ''),
                "document_title": self.get_document_title(document_id),
                "document_file": source_file,
                "category_persian": meta.get('document_type', meta.get('category', 'عمومی')),
                "chunk_summary": meta.get('chunk_text', '')[:200] + '...',
                "key_topics": meta.get('main_topics', meta.get('keywords', [])),
                "cross_references": meta.get('keywords', []),
                "document_id": document_id,
                "chunk_id": meta.get('chunk_id', index),
                "pdf_url": self.get_pdf_url(document_id),
                "academic_level": chunk_level,
                "article_number": meta.get('article_number', 0),
                "note_number": meta.get('note_number', 0),
                "chunk_type": meta.get('chunk_type', 'unknown'),
                "chunk_index": meta.get('chunk_index', 0)
            }
            
            # Categorize by academic level
            if chunk_level == detected_level:
                filtered_sources.append(source_data)
            elif chunk_level == 'general':
                general_sources.append(source_data)
            else:
                other_sources.append(source_data)
        
        # Combine results: prioritize detected level, then general, then others
        final_sources = filtered_sources[:top_k]
        
        # If we don't have enough results from the detected level, add general sources
        if len(final_sources) < top_k:
            needed = top_k - len(final_sources)
            final_sources.extend(general_sources[:needed])
        
        # If still not enough, add from other levels
        if len(final_sources) < top_k:
            needed = top_k - len(final_sources)
            final_sources.extend(other_sources[:needed])
        
        retrieval_time = time.time() - retrieval_start
        
        print(f"✅ Retrieved {len(final_sources)} relevant chunks")
        
        return final_sources, retrieval_time, detected_level
    
    def prepare_context_for_llm(self, sources: List[Dict[str, Any]], detected_level: str = 'general') -> tuple[str, List[str]]:
        """Prepare context string for LLM with source tracking and academic level information"""
        
        if not sources:
            return "هیچ اطلاعات مرتبطی یافت نشد.", []
        
        context_parts = []
        cross_references = set()
        total_length = 0
        
        for i, source in enumerate(sources, 1):
            content = source['content']
            category = source['category_persian']
            document = source['document_title']
            document_id = source['document_id']
            pdf_url = source['pdf_url']
            academic_level = source.get('academic_level', 'general')
            article_number = source.get('article_number', 0)
            note_number = source.get('note_number', 0)
            
            # Enhanced source metadata with academic level and article information
            level_info = f" - مقطع: {category}" if category else ""
            article_info = f" - ماده {article_number}" if article_number > 0 else ""
            note_info = f" - تبصره {note_number}" if note_number > 0 else ""
            
            # Create proper hyperlink if PDF URL is available
            if pdf_url and pdf_url != "PDF_URL":
                pdf_link_text = f" - [مشاهده PDF]({pdf_url})"
            else:
                pdf_link_text = " - [PDF در دسترس نیست]"
            
            source_info = f"[منبع {i}: {document}{level_info}{article_info}{note_info}{pdf_link_text}]"
            source_content = f"{source_info}\n{content}"
            
            # Check length limit
            if total_length + len(source_content) > self.max_context_length:
                break
            
            context_parts.append(source_content)
            total_length += len(source_content)
            
            # Collect cross-references
            cross_references.update(source.get('cross_references', []))
        
        context = "\n\n".join(context_parts)
        return context, list(cross_references)
    
    def generate_answer_with_llm(self, query: str, context: str, cross_references: List[str], detected_level: str = 'general') -> tuple[str, str, float]:
        """Generate answer using LLM via OpenRouter with academic level awareness"""
        
        generation_start = time.time()
        
        # Prepare cross-reference information
        cross_ref_info = ""
        if cross_references:
            cross_ref_info = f"\n\nمقررات مرتبط: {', '.join(cross_references)}"
        
        # Academic level specific context and instructions
        level_context = {
            'associate_bachelor': 'دانشجویان کاردانی و کارشناسی',
            'masters': 'دانشجویان کارشناسی ارشد',
            'phd': 'دانشجویان دکتری تخصصی',
            'general': 'تمام دانشجویان'
        }
        
        level_specific_info = {
            'associate_bachelor': 'توجه کنید که این پاسخ مخصوص دانشجویان کاردانی و کارشناسی است. مواردی مانند پایان‌نامه، رساله، یا آزمون جامع مربوط به مقاطع بالاتر است.',
            'masters': 'توجه کنید که این پاسخ مخصوص دانشجویان کارشناسی ارشد است. دانشجویان این مقطع باید پایان‌نامه انجام دهند و استاد راهنما انتخاب کنند.',
            'phd': 'توجه کنید که این پاسخ مخصوص دانشجویان دکتری تخصصی است. دانشجویان این مقطع باید رساله انجام دهند و آزمون جامع بگذرانند.',
            'general': 'این پاسخ شامل مقررات عمومی برای تمام دانشجویان است.'
        }
        
        target_audience = level_context.get(detected_level, 'تمام دانشجویان')
        level_instruction = level_specific_info.get(detected_level, '')
        
        # Create enhanced academic-level-aware prompt
        prompt = f"""شما یک مشاور قوانین و مقررات دانشگاه فردوسی مشهد هستید. بر اساس مقررات ارائه شده، به سؤال کاربر پاسخ کاملی بدهید.

مخاطب هدف: {target_audience}
{level_instruction}

مقررات دانشگاه:
{context}
{cross_ref_info}

سؤال کاربر: {query}

دستورالعمل پاسخ:
1. پاسخ را به زبان فارسی و مخصوص {target_audience} ارائه دهید
2. اگر سؤال مربوط به مقطع تحصیلی دیگری است، صراحت اعلام کنید
3. پاسخ باید عملی، مفید و قابل اجرا باشد
4. نکات مهم را به صورت شماره‌گذاری شده ارائه دهید
5. در پاسخ، به جای لینک‌های کامل PDF، از عبارات کوتاه مانند "[مشاهده PDF]" یا "([منبع])" استفاده کنید
6. اگر چندین بخش مرتبط وجود دارد، همه را ذکر کنید
7. در صورت وجود نکات مهم یا استثناها، آنها را برجسته کنید
8. در متن پاسخ، لینک‌ها را به صورت ساده مانند ([منبع X]) نمایش دهید

پاسخ:"""

        try:
            # Generate response using OpenRouter
            response = self.openai_client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://github.com/FUM_RAG",
                    "X-Title": "FUM RAG System",
                },
                model=self.llm_model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3  # Slightly higher for more natural responses
            )
            
            answer_markdown = response.choices[0].message.content
            
            # Create a plain text version for copy-pasting
            answer_plain = answer_markdown.replace('**', '').replace('*', '')
            answer_plain = answer_plain.replace('[مشاهده PDF]', '').replace('([منبع])', '')
            
            generation_time = time.time() - generation_start
            
            return answer_markdown, answer_plain, generation_time
            
        except Exception as e:
            generation_time = time.time() - generation_start
            error_answer = f"متأسفانه در تولید پاسخ خطایی رخ داد: {str(e)}\n\nبر اساس مقررات موجود:\n{context[:500]}..."
            return error_answer, error_answer, generation_time
    
    def answer_question(self, query: str, top_k: int = 5) -> RAGResponse:
        """Complete RAG pipeline: retrieve context and generate answer with academic level awareness"""
        
        total_start = time.time()
        
        print(f"🔍 Processing query: {query}")
        
        # Step 1: Retrieve relevant context with academic level filtering
        sources, retrieval_time, detected_level = self.retrieve_relevant_context(query, top_k)
        
        # Get academic level confidence for response
        detected_level_with_confidence, level_confidence = self.detect_academic_level(query)
        
        if not sources:
            total_time = time.time() - total_start
            return RAGResponse(
                query=query,
                answer="متأسفانه در پایگاه دانش موجود، اطلاعات مرتبطی برای این سؤال یافت نشد. لطفاً سؤال خود را بازنویسی کنید یا از کلمات کلیدی دیگری استفاده کنید.",
                answer_plain_text="متأسفانه در پایگاه دانش موجود، اطلاعات مرتبطی برای این سؤال یافت نشد. لطفاً سؤال خود را بازنویسی کنید یا از کلمات کلیدی دیگری استفاده کنید.",
                sources=[],
                confidence=0.0,
                generation_time=0.0,
                retrieval_time=retrieval_time,
                total_time=total_time,
                context_used="",
                category="نامشخص",
                cross_references=[],
                detected_academic_level=detected_level,
                academic_level_confidence=level_confidence
            )
        
        # Step 2: Prepare context for LLM with academic level information
        context, cross_references = self.prepare_context_for_llm(sources, detected_level)
        
        # Step 3: Generate answer with LLM and academic level awareness
        answer_markdown, answer_plain, generation_time = self.generate_answer_with_llm(
            query,
            context,
            cross_references,
            detected_level
        )
        
        # Linkify inline references like ([منبع 1]) using the retrieved sources
        answer_markdown = self._linkify_references(answer_markdown, sources)
        
        total_time = time.time() - total_start
        
        # Calculate average confidence from sources
        avg_confidence = (sum(source['score'] for source in sources) / len(sources)) if sources else 0.0
        
        # Get primary category from best source
        primary_category = sources[0]['category_persian'] if sources else "نامشخص"
        
        # Prepare source information for response
        source_info = []
        for source in sources:
            source_info.append({
                "source": source['document_title'],  # For compatibility
                "document": source['document_title'],
                "category": source['category_persian'], 
                "confidence": source['score'],
                "score": source['score'],
                "topics": source['key_topics'],
                "document_id": source['document_id'],
                "pdf_url": source['pdf_url'],
                "academic_level": source.get('academic_level', 'general'),
                "article_number": source.get('article_number', 0),
                "note_number": source.get('note_number', 0)
            })
        
        print(f"✅ Response generated in {total_time:.2f}s (Retrieval: {retrieval_time:.2f}s, Generation: {generation_time:.2f}s)")
        print(f"🎯 Academic level: {detected_level}")
        
        return RAGResponse(
            query=query,
            answer=answer_markdown,
            answer_plain_text=answer_plain,
            sources=source_info,
            confidence=avg_confidence,
            generation_time=generation_time,
            retrieval_time=retrieval_time,
            total_time=total_time,
            context_used=context,
            category=primary_category,
            cross_references=cross_references,
            detected_academic_level=detected_level,
            academic_level_confidence=level_confidence
        )
    
    def batch_answer_questions(self, queries: List[str]) -> List[RAGResponse]:
        """Answer multiple questions in batch"""
        
        print(f"🔄 Processing {len(queries)} queries in batch...")
        responses = []
        
        for i, query in enumerate(queries, 1):
            print(f"\n📝 Query {i}/{len(queries)}: {query[:50]}...")
            response = self.answer_question(query)
            responses.append(response)
            
            # Small delay to avoid rate limiting
            time.sleep(0.5)
        
        print(f"✅ Batch processing complete")
        return responses
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """Get system performance statistics"""
        
        stats = {
            "index_type": "FAISS",
            "total_documents": self.faiss_index.ntotal,
            "total_chunks": len(self.metadata),
            "embedding_model": self.embedding_model_name,
            "embedding_dimension": self.embedding_dim,
            "llm_model": self.llm_model,
            "max_context_length": self.max_context_length,
            "min_confidence_threshold": self.min_confidence,
            "indexed_at": self.index_summary.get('indexed_at', 'unknown'),
            "status": "active"
        }
        
        return stats
    
    def _linkify_references(self, answer_markdown: str, sources: List[Dict[str, Any]]) -> str:
        """Turn inline reference markers like ([منبع 1]) or [منبع 1] into markdown links using sources order."""
        if not answer_markdown or not sources:
            return answer_markdown
        
        # Build index -> url map (1-based)
        index_to_url = {}
        for i, s in enumerate(sources, start=1):
            url = s.get('pdf_url') or ''
            if url and isinstance(url, str) and url.startswith(('http://', 'https://')):
                index_to_url[i] = url
        
        if not index_to_url:
            return answer_markdown
        
        # Replace ([منبع N]) first
        def repl_paren(m):
            idx = int(m.group(1))
            url = index_to_url.get(idx)
            return f"[منبع {idx}]({url})" if url else m.group(0)
        
        result = re.sub(r"\(\[منبع\s+(\d+)\]\)", repl_paren, answer_markdown)
        
        # Replace bare [منبع N] not already linked (no immediate '(')
        def repl_bare(m):
            idx = int(m.group(1))
            url = index_to_url.get(idx)
            return f"[منبع {idx}]({url})" if url else m.group(0)
        
        result = re.sub(r"\[منبع\s+(\d+)\](?!\()", repl_bare, result)
        
        return result

def format_rag_response(response: RAGResponse) -> str:
    """Format RAG response for display"""
    
    formatted = f"""
{'='*80}
🔍 سؤال: {response.query}

🤖 پاسخ هوش مصنوعی:
{response.answer}

📊 اطلاعات تکمیلی:
├── 🏷️ دسته‌بندی: {response.category}
├── 🎯 اعتماد: {response.confidence:.3f}
├── 🎓 مقطع تحصیلی: {response.detected_academic_level} ({response.academic_level_confidence:.2f})
├── ⏱️ زمان کل: {response.total_time:.2f} ثانیه
├── 🔍 زمان جستجو: {response.retrieval_time:.2f} ثانیه
└── 🧠 زمان تولید: {response.generation_time:.2f} ثانیه

📚 منابع ({len(response.sources)} مورد):"""

    for i, source in enumerate(response.sources, 1):
        pdf_link = ""
        if source.get('pdf_url'):
            pdf_link = f" 📄 [مشاهده PDF]({source['pdf_url']})"
        
        formatted += f"""
   {i}. {source['document']} (اعتماد: {source['confidence']:.3f}){pdf_link}
      دسته‌بندی: {source['category']}
      مقطع: {source.get('academic_level', 'general')}"""
    
    if response.cross_references:
        formatted += f"""

🔗 مقررات مرتبط: {', '.join(response.cross_references)}"""
    
    formatted += "\n" + "="*80
    
    return formatted

# Usage and testing functions
def test_faiss_rag_system():
    """Test the FAISS-based RAG system"""
    
    print("🧪 Testing FAISS-based RAG System")
    print("="*80)
    
    # Initialize system
    rag = UniversityRulesRAGWithLLM()
    
    # Test queries
    test_queries = [
        "نویسنده مسئول کیست و چه وظایفی دارد؟",
        "چگونه نشانی دانشگاه فردوسی مشهد را در مقالات درج کنم؟",
        "قوانین مربوط به مقالات مستخرج از پایان‌نامه چیست؟"
    ]
    
    # Process queries
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        response = rag.answer_question(query)
        print(format_rag_response(response))
        print("\n")
    
    # System statistics
    stats = rag.get_system_statistics()
    print("📊 System Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    return rag

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_faiss_rag_system()
    else:
        print("FAISS RAG System - Import this module or use --test flag")
        print("Example: from src.faiss_rag_with_llm import UniversityRulesRAGWithLLM")
