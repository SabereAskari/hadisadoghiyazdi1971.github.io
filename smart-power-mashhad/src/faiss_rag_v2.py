#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Updated RAG System V2 - Compatible with advanced_faiss_indexer1.py
استفاده از ایندکس V4 بروز شده
"""

import os
import json
import time
import re
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

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
    query_type: str
    related_articles: List[int]


class UniversityRulesRAG:
    """RAG system compatible with advanced_faiss_indexer1.py output"""
    
    def __init__(self, 
                 index_dir: str = "./index_v4_upgraded",
                 env_path: str = "./.env"):
        """Initialize the RAG system with V4 upgraded index"""
        
        load_dotenv(env_path)

        api_key = os.getenv("OPENROUTER_API_KEY") or "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"
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found")

        print("🔑 API key loaded")

        self.llm_model = os.getenv("LLM_MODEL", "openai/gpt-4o-mini")
        
        try:
            self.openai_client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
                default_headers={
                    "HTTP-Referer": "https://hadisadoghiyazdi1971.github.io",
                    "X-Title": "FUM University Rules RAG Chatbot",
                }
            )
            _ = self.openai_client.models.list()
            print(f"✅ Connected to OpenRouter with model: {self.llm_model}")
        except Exception as e:
            print(f"❌ Error connecting to OpenRouter: {e}")
            raise

        self.index_dir = Path(index_dir)
        
        # Load comprehensive summary from V4 index
        summary_path = self.index_dir / "comprehensive_summary.json"
        if not summary_path.exists():
            raise FileNotFoundError(f"Summary not found: {summary_path}")
        
        with open(summary_path, 'r', encoding='utf-8') as f:
            self.index_summary = json.load(f)
        
        self.embedding_model_name = self.index_summary.get(
            'embedding_model',
            'intfloat/multilingual-e5-large'
        )
        
        print(f"🤖 Loading embedding model: {self.embedding_model_name}")
        self.embedding_model = SentenceTransformer(self.embedding_model_name, device="cpu")
        self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()
        
        # Load FAISS index from V4
        index_path = self.index_dir / "faiss_index_upgraded.index"
        if not index_path.exists():
            raise FileNotFoundError(f"FAISS index not found: {index_path}")
        
        print(f"📚 Loading FAISS index from: {index_path}")
        self.faiss_index = faiss.read_index(str(index_path))
        print(f"✅ FAISS index loaded with {self.faiss_index.ntotal} vectors")
        
        # Load metadata from V4
        metadata_path = self.index_dir / "enhanced_metadata.json"
        if not metadata_path.exists():
            raise FileNotFoundError(f"Metadata not found: {metadata_path}")
        
        print(f"📚 Loading metadata from: {metadata_path}")
        with open(metadata_path, 'r', encoding='utf-8') as f:
            raw_metadata = json.load(f)
        
        # Transform metadata to compatible format
        self.metadata = self._transform_metadata(raw_metadata)
        print(f"✅ Loaded metadata for {len(self.metadata)} chunks")
        
        self._build_article_index()
        
        self.max_context_length = 3500
        self.max_sources = 5
        
        self.query_patterns = {
            'definitional': [r'چیست', r'تعریف', r'منظور از', r'مفهوم', r'یعنی چه', r'what is', r'define', r'meaning'],
            'procedural': [r'چگونه', r'چطور', r'نحوه', r'روش', r'مراحل', r'گام', r'فرآیند', r'how to', r'procedure', r'process', r'steps'],
            'eligibility': [r'آیا می\s*توانم', r'آیا مجاز', r'شرایط', r'ضوابط', r'الزامات', r'can I', r'may I', r'requirements', r'conditions', r'eligible'],
            'numerical': [r'چند', r'چقدر', r'میزان', r'درصد', r'تعداد', r'مبلغ', r'how much', r'how many', r'amount', r'percentage'],
            'exception': [r'تبصره', r'استثنا', r'مگر', r'به جز', r'موارد خاص', r'exception', r'special case', r'note'],
            'timeline': [r'مهلت', r'زمان', r'تاریخ', r'مدت', r'deadline', r'when', r'time']
        }
        
        print("✅ RAG system initialized successfully")

    def _transform_metadata(self, raw_metadata: List[Dict]) -> List[Dict]:
        """Transform V4 metadata to compatible format"""
        transformed = []
        
        for chunk in raw_metadata:
            transformed_chunk = {
                'chunk_id': chunk.get('id', ''),
                'chunk_text': chunk.get('text', ''),
                'source_file': chunk.get('source_file', ''),
                'document_title': chunk.get('document_title', ''),
                'document_section': chunk.get('document_section', ''),
                'chunk_type': chunk.get('chunk_type', 'general'),
                'article_numbers': chunk.get('article_numbers', []),
                'note_numbers': chunk.get('note_numbers', []),
                'has_table': chunk.get('has_table', False),
                'has_list': chunk.get('has_list', False),
                'keywords': chunk.get('keywords', []),
                'metadata': chunk.get('metadata', {})
            }
            transformed.append(transformed_chunk)
        
        return transformed

    def _build_article_index(self):
        """Build index for quick article lookup"""
        self.article_to_chunks = {}
        
        for i, meta in enumerate(self.metadata):
            for article_num in meta.get('article_numbers', []):
                if article_num not in self.article_to_chunks:
                    self.article_to_chunks[article_num] = []
                self.article_to_chunks[article_num].append(i)
        
        print(f"📋 Built article index: {len(self.article_to_chunks)} unique articles")
    
    def detect_query_type(self, query: str) -> str:
        """Detect query type"""
        query_lower = query.lower()
        scores = {qtype: 0 for qtype in self.query_patterns.keys()}
        
        for qtype, patterns in self.query_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    scores[qtype] += 1
        
        max_score = max(scores.values())
        return max(scores, key=scores.get) if max_score > 0 else 'general'
    
    def extract_article_mentions(self, query: str) -> List[int]:
        """Extract mentioned article numbers"""
        article_numbers = []
        patterns = [
            r'ماده\s+(\d+)',
            r'بند\s+(\d+)',
            r'تبصره\s+(\d+)'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, query)
            for match in matches:
                try:
                    num = int(match.group(1))
                    if num not in article_numbers:
                        article_numbers.append(num)
                except ValueError:
                    pass
        
        return sorted(article_numbers)
    
    def retrieve_relevant_context(
        self, 
        query: str, 
        top_k: int = 5,
        query_type: str = 'general'
    ) -> Tuple[List[Dict[str, Any]], float, List[int]]:
        """Retrieve relevant context with structure awareness"""
        
        retrieval_start = time.time()
        mentioned_articles = self.extract_article_mentions(query)
        
        query_embedding = self.embedding_model.encode([query])[0].astype('float32')
        
        k_search = min(top_k * 4, self.faiss_index.ntotal)
        distances, indices = self.faiss_index.search(
            query_embedding.reshape(1, -1), 
            k_search
        )
        
        candidate_sources = []
        related_articles = set(mentioned_articles)
        
        for idx, (distance, index) in enumerate(zip(distances[0], indices[0])):
            if index == -1 or index >= len(self.metadata):
                continue
            
            meta = self.metadata[index]
            similarity_score = 1.0 / (1.0 + distance)
            
            boost = 1.0
            chunk_type = meta.get('chunk_type', 'general')
            
            if query_type == 'definitional' and chunk_type == 'definitions':
                boost = 1.3
            elif query_type == 'procedural' and chunk_type == 'article':
                boost = 1.2
            elif query_type == 'numerical' and meta.get('has_table', False):
                boost = 1.3
            elif query_type == 'exception' and meta.get('note_numbers'):
                boost = 1.25
            
            if any(art in mentioned_articles for art in meta.get('article_numbers', [])):
                boost *= 1.5
            
            adjusted_score = similarity_score * boost
            
            source_data = {
                "score": float(adjusted_score),
                "original_score": float(similarity_score),
                "content": meta.get('chunk_text', ''),
                "document_title": meta.get('document_title', ''),
                "document_file": meta.get('source_file', ''),
                "category": meta.get('chunk_type', 'general'),
                "chunk_type": chunk_type,
                "document_section": meta.get('document_section', ''),
                "article_numbers": meta.get('article_numbers', []),
                "note_numbers": meta.get('note_numbers', []),
                "has_table": meta.get('has_table', False),
                "has_list": meta.get('has_list', False),
                "document_id": meta.get('source_file', '').replace('.txt', ''),
                "chunk_id": index,
                "metadata": meta.get('metadata', {})
            }
            
            candidate_sources.append(source_data)
            related_articles.update(meta.get('article_numbers', []))
        
        candidate_sources.sort(key=lambda x: x['score'], reverse=True)
        final_sources = candidate_sources[:top_k]
        
        retrieval_time = time.time() - retrieval_start
        
        print(f"✅ Retrieved {len(final_sources)} relevant chunks (type: {query_type})")
        
        return final_sources, retrieval_time, sorted(list(related_articles))
    
    def prepare_context_for_llm(
        self, 
        sources: List[Dict[str, Any]],
        query_type: str = 'general'
    ) -> str:
        """Prepare context for LLM"""
        
        if not sources:
            return "هیچ اطلاعات مرتبطی یافت نشد."
        
        context_parts = []
        total_length = 0
        
        for i, source in enumerate(sources, 1):
            content = source['content']
            document = source['document_title']
            section = source['document_section']
            article_nums = source.get('article_numbers', [])
            note_nums = source.get('note_numbers', [])
            
            metadata_parts = [f"منبع {i}: {document}"]
            
            if section and section != document:
                metadata_parts.append(f"بخش: {section}")
            
            if article_nums:
                articles_str = "، ".join([f"ماده {num}" for num in article_nums])
                metadata_parts.append(articles_str)
            
            if note_nums:
                notes_str = "، ".join([f"تبصره {num}" for num in note_nums])
                metadata_parts.append(notes_str)
            
            if source.get('has_table'):
                metadata_parts.append("📊 شامل جدول")
            
            metadata_line = " | ".join(metadata_parts)
            source_content = f"[{metadata_line}]\n{content}"
            
            if total_length + len(source_content) > self.max_context_length:
                break
            
            context_parts.append(source_content)
            total_length += len(source_content)
        
        return "\n\n---\n\n".join(context_parts)
    
    def generate_answer_with_llm(
        self, 
        query: str, 
        context: str,
        query_type: str = 'general',
        related_articles: List[int] = None
    ) -> Tuple[str, str, float]:
        """Generate answer using LLM"""
        
        generation_start = time.time()
        
        type_instructions = {
            'definitional': "۱. تعریف دقیق و رسمی را ارائه دهید\n۲. توضیح مختصر و کاربردی بدهید\n۳. شرایط یا الزامات را ذکر کنید\n۴. اصطلاحات مرتبط را معرفی کنید",
            'procedural': "۱. مراحل را به ترتیب شماره‌گذاری کنید\n۲. مدارک و مستندات مورد نیاز را مشخص کنید\n۳. مرجع مسئول را ذکر کنید\n۴. زمان‌بندی یا مهلت‌ها را بیان کنید\n۵. نکات مهم را برجسته کنید",
            'eligibility': "۱. پاسخ مستقیم (بله/خیر) بدهید\n۲. شرایط و الزامات را لیست کنید\n۳. استثناها و موارد خاص را مشخص کنید\n۴. به مواد مرتبط ارجاع دقیق دهید",
            'numerical': "۱. اعداد و درصدها را برجسته بیان کنید\n۲. اطلاعات جدولی را خلاصه کنید\n۳. محدودیت‌ها را توضیح دهید\n۴. فرمول محاسبه را ذکر کنید",
            'exception': "۱. قاعده عمومی را بیان کنید\n۲. استثناها را مشخص کنید\n۳. شرایط اعمال هر استثنا را توضیح دهید\n۴. به تبصره‌های مربوط ارجاع دقیق دهید",
            'timeline': "۱. مهلت‌ها و زمان‌بندی‌ها را واضح بیان کنید\n۲. نقاط شروع و پایان مهلت‌ها را مشخص کنید\n۳. تبعات عدم رعایت مهلت را ذکر کنید\n۴. موارد تمدید یا استثنا را توضیح دهید",
            'general': "۱. پاسخ جامع و کامل بدهید\n۲. نکات مهم را برجسته کنید\n۳. به مواد و بخش‌های مرتبط ارجاع دهید\n۴. در صورت نیاز مثال یا توضیح تکمیلی ارائه دهید"
        }
        
        specific_instruction = type_instructions.get(query_type, type_instructions['general'])
        
        article_context = ""
        if related_articles:
            articles_list = "، ".join([f"ماده {num}" for num in related_articles])
            article_context = f"\n\nموادمرتبط شناسایی شده: {articles_list}"
        
        prompt = f"""شما یک مشاور قوانین و مقررات  شرکت برق  هستید. بر اساس مقررات ارائه شده، به سؤال کاربر پاسخ دقیق و کاربردی بدهید.

نوع سؤال: {query_type}
{article_context}

مقررات شرکت برق:
{context}

سؤال کاربر: {query}

دستورالعمل پاسخ:
{specific_instruction}

نکات مهم:
- پاسخ را به زبان فارسی و رسمی ارائه دهید
- از منابع ارائه شده استفاده کنید و ارجاع دقیق دهید
- در صورت ابهام یا نیاز به بررسی بیشتر، صراحت‌آمیز اعلام کنید
- اگر چند حالت یا شرط مختلف وجود دارد، همه را ذکر کنید
- از ساختار واضح و خوانایی استفاده کنید (عنوان‌ها، فهرست، شماره‌گذاری)

پاسخ:"""

        try:
            response = self.openai_client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://github.com/FUM_RAG",
                    "X-Title": "FUM RAG System",
                },
                model=self.llm_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            
            answer_markdown = response.choices[0].message.content
            answer_plain = answer_markdown.replace('**', '').replace('*', '')
            answer_plain = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', answer_plain)
            
            generation_time = time.time() - generation_start
            return answer_markdown, answer_plain, generation_time
            
        except Exception as e:
            generation_time = time.time() - generation_start
            error_answer = f"متأسفانه خطایی در توليد پاسخ رخ داد: {str(e)}\n\nبر اساس مقررات موجود:\n{context[:500]}..."
            return error_answer, error_answer, generation_time
    
    def answer_question(self, query: str, top_k: int = 5) -> RAGResponse:
        """Complete RAG pipeline"""
        
        total_start = time.time()
        
        print(f"🔍 Processing query: {query}")
        
        query_type = self.detect_query_type(query)
        print(f"🎯 Query type: {query_type}")
        
        sources, retrieval_time, related_articles = self.retrieve_relevant_context(
            query, top_k, query_type
        )
        
        if not sources:
            total_time = time.time() - total_start
            return RAGResponse(
                query=query,
                answer="متأسفانه اطلاعات مرتبطی برای این سؤال در پایگاه دانش موجود نیست. لطفا سؤال خود را بازنویسی کنید.",
                answer_plain_text="متأسفانه اطلاعات مرتبطی یافت نشد",
                sources=[],
                confidence=0.0,
                generation_time=0.0,
                retrieval_time=retrieval_time,
                total_time=total_time,
                context_used="",
                category="نامشخص",
                query_type=query_type,
                related_articles=related_articles
            )
        
        context = self.prepare_context_for_llm(sources, query_type)
        answer_markdown, answer_plain, generation_time = self.generate_answer_with_llm(
            query, context, query_type, related_articles
        )
        
        total_time = time.time() - total_start
        avg_confidence = (sum(source['score'] for source in sources) / len(sources)) if sources else 0.0
        primary_category = sources[0]['category'] if sources else "نامشخص"
        
        source_info = []
        for source in sources:
            source_info.append({
                "document": source['document_title'],
                "section": source.get('document_section', ''),
                "category": source['category'],
                "confidence": source['score'],
                "chunk_type": source.get('chunk_type', 'general'),
                "article_numbers": source.get('article_numbers', []),
                "note_numbers": source.get('note_numbers', []),
                "has_table": source.get('has_table', False),
                "has_list": source.get('has_list', False)
            })
        
        print(f"✅ Response generated in {total_time:.2f}s")
        
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
            query_type=query_type,
            related_articles=related_articles
        )
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """Get system statistics"""
        
        stats = {
            "index_type": "FAISS",
            "total_chunks": len(self.metadata),
            "total_documents": self.faiss_index.ntotal,
            "embedding_model": self.embedding_model_name,
            "embedding_dimension": self.embedding_dim,
            "llm_model": self.llm_model,
            "max_context_length": self.max_context_length,
            "total_articles": len(self.article_to_chunks),
            "indexed_at": self.index_summary.get('indexed_at', 'unknown'),
            "chunking_strategy": self.index_summary.get('chunking_strategy', 'unknown'),
            "status": "active"
        }
        
        return stats