#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simplified RAG System V2 - Optimized for University Rules & Regulations
Removes academic level detection, adds structure-aware retrieval
Uses enhanced metadata from structure-aware chunking
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
    query_type: str
    related_articles: List[int]


class UniversityRulesRAG:
    """Simplified RAG system for university rules and regulations"""
    
    def __init__(self, 
                 index_dir: str = "./index",
                 env_path: str = "../.env"):
        """Initialize the RAG system"""
        
        # Load environment variables
        load_dotenv(env_path)

        # Get API key from environment or fallback
        api_key = os.getenv("OPENROUTER_API_KEY") or "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"
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment and no fallback provided")

        print("🔑 Loaded API key starts with:", api_key[:15])

        self.llm_model = os.getenv("LLM_MODEL", "openai/gpt-4o-mini")
        
        # Initialize OpenRouter client with required headers
        try:
            self.openai_client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
                default_headers={
                    "HTTP-Referer": "https://hadisadoghiyazdi1971.github.io",
                    "X-Title": "FUM University Rules RAG Chatbot",
                }
            )
            # Quick test to confirm authentication
            _ = self.openai_client.models.list()
            print(f"✅ Connected to OpenRouter with model: {self.llm_model}")
        except Exception as e:
            print(f"❌ Error connecting to OpenRouter: {e}")
            raise

        self.index_dir = Path(index_dir)
        
        # Load index summary
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
        
        # Build article index for quick lookup
        self._build_article_index()
        
        # RAG configuration
        self.max_context_length = 3000
        self.max_sources = 5
        
        # Query type patterns
        self.query_patterns = {
            'definitional': [r'چیست', r'تعریف', r'منظور از', r'مفهوم', r'یعنی چه', r'what is', r'define', r'meaning'],
            'procedural': [r'چگونه', r'چطور', r'نحوه', r'روش', r'مراحل', r'گام', r'فرآیند', r'how to', r'procedure', r'process', r'steps'],
            'eligibility': [r'آیا می\s*توانم', r'آیا مجاز', r'شرایط', r'ضوابط', r'الزامات', r'can I', r'may I', r'requirements', r'conditions', r'eligible'],
            'numerical': [r'چند', r'چقدر', r'میزان', r'درصد', r'تعداد', r'مبلغ', r'how much', r'how many', r'amount', r'percentage'],
            'exception': [r'تبصره', r'استثنا', r'مگر', r'به جز', r'موارد خاص', r'exception', r'special case', r'note'],
            'timeline': [r'مهلت', r'زمان', r'تاریخ', r'مدت', r'deadline', r'when', r'time']
        }
        
        print("✅ Simplified RAG system initialized")

    # ... ادامه تمام متدهای کلاس بدون تغییر ...


    
    def _build_article_index(self):
        """Build an index of chunks by article number for quick lookup"""
        self.article_to_chunks = {}
        
        for i, meta in enumerate(self.metadata):
            for article_num in meta.get('article_numbers', []):
                if article_num not in self.article_to_chunks:
                    self.article_to_chunks[article_num] = []
                self.article_to_chunks[article_num].append(i)
        
        print(f"📋 Built article index: {len(self.article_to_chunks)} unique articles")
    
    def detect_query_type(self, query: str) -> str:
        """Detect the type of query to optimize retrieval"""
        query_lower = query.lower()
        
        scores = {qtype: 0 for qtype in self.query_patterns.keys()}
        
        for qtype, patterns in self.query_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    scores[qtype] += 1
        
        # Return type with highest score, or 'general' if no match
        max_score = max(scores.values())
        if max_score == 0:
            return 'general'
        
        return max(scores, key=scores.get)
    
    def extract_article_mentions(self, query: str) -> List[int]:
        """Extract article numbers mentioned in the query"""
        article_numbers = []
        
        # Persian patterns
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
        """Retrieve relevant context with structure-aware filtering"""
        
        retrieval_start = time.time()
        
        # Extract mentioned articles
        mentioned_articles = self.extract_article_mentions(query)
        
        # Embed the query
        query_embedding = self.embedding_model.encode([query])[0].astype('float32')
        
        # Search in FAISS index - get more results for filtering
        k_search = min(top_k * 4, self.faiss_index.ntotal)
        distances, indices = self.faiss_index.search(
            query_embedding.reshape(1, -1), 
            k_search
        )
        
        # Process results
        candidate_sources = []
        related_articles = set(mentioned_articles)
        
        for idx, (distance, index) in enumerate(zip(distances[0], indices[0])):
            if index == -1 or index >= len(self.metadata):
                continue
            
            meta = self.metadata[index]
            
            # Convert L2 distance to similarity score
            similarity_score = 1.0 / (1.0 + distance)
            
            # Extract document info
            source_file = meta.get('source_file', '')
            document_id = source_file.replace('.txt', '') if source_file.endswith('.txt') else source_file
            
            # Boost score based on query type and chunk type
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
            
            # Boost if article is mentioned in query
            article_numbers = meta.get('article_numbers', [])
            if any(art in mentioned_articles for art in article_numbers):
                boost *= 1.5
            
            adjusted_score = similarity_score * boost
            
            source_data = {
                "score": float(adjusted_score),
                "original_score": float(similarity_score),
                "content": meta.get('chunk_text', ''),
                "document_title": meta.get('document_title', document_id),
                "document_file": source_file,
                "category": meta.get('chunk_type', 'general'),
                "chunk_type": chunk_type,
                "document_section": meta.get('document_section', ''),
                "article_numbers": article_numbers,
                "note_numbers": meta.get('note_numbers', []),
                "has_table": meta.get('has_table', False),
                "has_list": meta.get('has_list', False),
                "document_id": document_id,
                "chunk_id": meta.get('chunk_id', index),
                "metadata": meta.get('metadata', {})
            }
            
            candidate_sources.append(source_data)
            related_articles.update(article_numbers)
        
        # Sort by adjusted score and take top_k
        candidate_sources.sort(key=lambda x: x['score'], reverse=True)
        final_sources = candidate_sources[:top_k]
        
        # If we found specific articles mentioned, try to include related chunks
        if mentioned_articles and len(final_sources) < top_k:
            for article_num in mentioned_articles:
                if article_num in self.article_to_chunks:
                    for chunk_idx in self.article_to_chunks[article_num]:
                        if chunk_idx < len(self.metadata):
                            meta = self.metadata[chunk_idx]
                            # Check if not already included
                            if not any(s['chunk_id'] == chunk_idx for s in final_sources):
                                source_data = {
                                    "score": 0.9,  # High score for directly mentioned article
                                    "original_score": 0.9,
                                    "content": meta.get('chunk_text', ''),
                                    "document_title": meta.get('document_title', ''),
                                    "document_file": meta.get('source_file', ''),
                                    "category": meta.get('chunk_type', 'general'),
                                    "chunk_type": meta.get('chunk_type', 'general'),
                                    "document_section": meta.get('document_section', ''),
                                    "article_numbers": meta.get('article_numbers', []),
                                    "note_numbers": meta.get('note_numbers', []),
                                    "has_table": meta.get('has_table', False),
                                    "has_list": meta.get('has_list', False),
                                    "document_id": meta.get('source_file', '').replace('.txt', ''),
                                    "chunk_id": chunk_idx,
                                    "metadata": meta.get('metadata', {})
                                }
                                final_sources.append(source_data)
                                if len(final_sources) >= top_k:
                                    break
        
        retrieval_time = time.time() - retrieval_start
        
        print(f"✅ Retrieved {len(final_sources)} relevant chunks (query_type: {query_type})")
        
        return final_sources, retrieval_time, sorted(list(related_articles))
    
    def prepare_context_for_llm(
        self, 
        sources: List[Dict[str, Any]],
        query_type: str = 'general'
    ) -> str:
        """Prepare context string for LLM with enhanced metadata"""
        
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
            chunk_type = source.get('chunk_type', 'general')
            
            # Build metadata line
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
            
            # Check length limit
            if total_length + len(source_content) > self.max_context_length:
                break
            
            context_parts.append(source_content)
            total_length += len(source_content)
        
        context = "\n\n---\n\n".join(context_parts)
        return context
    
    def generate_answer_with_llm(
        self, 
        query: str, 
        context: str,
        query_type: str = 'general',
        related_articles: List[int] = None
    ) -> Tuple[str, str, float]:
        """Generate answer using LLM with query-type-aware prompts"""
        
        generation_start = time.time()
        
        # Query type specific instructions
        type_instructions = {
            'definitional': """
                1. ابتدا تعریف دقیق و رسمی را ارائه دهید
                2. توضیح مختصر و کاربردی بدهید
                3. در صورت وجود، شرایط یا الزامات را ذکر کنید
                4. اصطلاحات مرتبط را معرفی کنید
            """,
            'procedural': """
                1. مراحل انجام کار را به ترتیب شماره‌گذاری کنید
                2. مدارک و مستندات مورد نیاز را مشخص کنید
                3. مرجع مسئول یا واحد اجرایی را ذکر کنید
                4. زمان‌بندی یا مهلت‌ها را بیان کنید (در صورت وجود)
                5. نکات مهم و هشدارها را برجسته کنید
            """,
            'eligibility': """
                1. ابتدا پاسخ مستقیم (بله/خیر/در شرایط خاص) بدهید
                2. شرایط و الزامات را به صورت لیست ارائه دهید
                3. استثناها و موارد خاص را مشخص کنید
                4. به مواد و تبصره‌های مرتبط ارجاع دهید
            """,
            'numerical': """
                1. اعداد، درصدها یا مبالغ را به صورت برجسته بیان کنید
                2. در صورت وجود جدول، اطلاعات کلیدی را خلاصه کنید
                3. محدوده‌ها یا شرایط مختلف را توضیح دهید
                4. فرمول محاسبه را در صورت وجود ذکر کنید
            """,
            'exception': """
                1. ابتدا قاعده عمومی را بیان کنید
                2. استثناها و موارد خاص را مشخص کنید
                3. شرایط اعمال هر استثنا را توضیح دهید
                4. به تبصره‌های مربوط ارجاع دقیق دهید
            """,
            'timeline': """
                1. مهلت‌ها و زمان‌بندی‌ها را به صورت واضح بیان کنید
                2. نقاط شروع و پایان مهلت‌ها را مشخص کنید
                3. تبعات عدم رعایت مهلت را ذکر کنید
                4. موارد تمدید یا استثناء را توضیح دهید
            """,
            'general': """
                1. پاسخ جامع و کامل به سؤال بدهید
                2. نکات مهم را برجسته کنید
                3. به مواد و بخش‌های مرتبط ارجاع دهید
                4. در صورت نیاز، مثال یا توضیح تکمیلی ارائه دهید
            """
        }
        
        specific_instruction = type_instructions.get(query_type, type_instructions['general'])
        
        # Build article context if available
        article_context = ""
        if related_articles:
            articles_list = "، ".join([f"ماده {num}" for num in related_articles])
            article_context = f"\n\nمواد مرتبط شناسایی شده: {articles_list}"
        
        # Create prompt
        prompt = f"""شما یک مشاور قوانین و مقررات دانشگاه فردوسی مشهد هستید. بر اساس مقررات ارائه شده، به سؤال کاربر پاسخ دقیق و کاربردی بدهید.

نوع سؤال: {query_type}
{article_context}

مقررات دانشگاه:
{context}

سؤال کاربر: {query}

دستورالعمل پاسخ:
{specific_instruction}

نکات مهم:
- پاسخ را به زبان فارسی و رسمی ارائه دهید
- از منابع ارائه شده استفاده کنید و ارجاع دقیق دهید
- در صورت ابهام یا نیاز به بررسی بیشتر، صراحتاً اعلام کنید
- اگر چند حالت یا شرایط مختلف وجود دارد، همه را ذکر کنید
- از ساختار واضح و خوانا استفاده کنید (عنوان‌ها، فهرست، شماره‌گذاری)

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
                temperature=0.2  # Lower for more factual responses
            )
            
            answer_markdown = response.choices[0].message.content
            
            # Create plain text version
            answer_plain = answer_markdown.replace('**', '').replace('*', '')
            answer_plain = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', answer_plain)
            
            generation_time = time.time() - generation_start
            
            return answer_markdown, answer_plain, generation_time
            
        except Exception as e:
            generation_time = time.time() - generation_start
            error_answer = f"متأسفانه در تولید پاسخ خطایی رخ داد: {str(e)}\n\nبر اساس مقررات موجود:\n{context[:500]}..."
            return error_answer, error_answer, generation_time
    
    def answer_question(self, query: str, top_k: int = 5) -> RAGResponse:
        """Complete RAG pipeline: retrieve context and generate answer"""
        
        total_start = time.time()
        
        print(f"🔍 Processing query: {query}")
        
        # Detect query type
        query_type = self.detect_query_type(query)
        print(f"🎯 Query type detected: {query_type}")
        
        # Retrieve relevant context
        sources, retrieval_time, related_articles = self.retrieve_relevant_context(
            query, top_k, query_type
        )
        
        if not sources:
            total_time = time.time() - total_start
            return RAGResponse(
                query=query,
                answer="متأسفانه در پایگاه دانش موجود، اطلاعات مرتبطی برای این سؤال یافت نشد. لطفاً سؤال خود را بازنویسی کنید یا از کلمات کلیدی دیگری استفاده کنید.",
                answer_plain_text="متأسفانه در پایگاه دانش موجود، اطلاعات مرتبطی برای این سؤال یافت نشد.",
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
        
        # Prepare context for LLM
        context = self.prepare_context_for_llm(sources, query_type)
        
        # Generate answer with LLM
        answer_markdown, answer_plain, generation_time = self.generate_answer_with_llm(
            query, context, query_type, related_articles
        )
        
        total_time = time.time() - total_start
        
        # Calculate average confidence
        avg_confidence = (sum(source['score'] for source in sources) / len(sources)) if sources else 0.0
        
        # Get primary category
        primary_category = sources[0]['category'] if sources else "نامشخص"
        
        # Prepare source information
        source_info = []
        for source in sources:
            source_info.append({
                "source": source['document_title'],
                "document": source['document_title'],
                "category": source['category'],
                "section": source.get('document_section', ''),
                "confidence": source['score'],
                "score": source['score'],
                "document_id": source['document_id'],
                "chunk_type": source.get('chunk_type', 'general'),
                "article_numbers": source.get('article_numbers', []),
                "note_numbers": source.get('note_numbers', []),
                "has_table": source.get('has_table', False),
                "has_list": source.get('has_list', False)
            })
        
        print(f"✅ Response generated in {total_time:.2f}s (Retrieval: {retrieval_time:.2f}s, Generation: {generation_time:.2f}s)")
        print(f"🎯 Query type: {query_type}, Related articles: {related_articles}")
        
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
        """Get system performance statistics"""
        
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


def format_rag_response(response: RAGResponse) -> str:
    """Format RAG response for display"""
    
    formatted = f"""
{'='*80}
🔍 سؤال: {response.query}
🎯 نوع سؤال: {response.query_type}

🤖 پاسخ:
{response.answer}

📊 اطلاعات تکمیلی:
├── 🏷️ دسته‌بندی: {response.category}
├── 🎯 اعتماد: {response.confidence:.3f}
├── 📋 مواد مرتبط: {', '.join([f'ماده {a}' for a in response.related_articles]) if response.related_articles else 'ندارد'}
├── ⏱️ زمان کل: {response.total_time:.2f} ثانیه
├── 🔍 زمان جستجو: {response.retrieval_time:.2f} ثانیه
└── 🧠 زمان تولید: {response.generation_time:.2f} ثانیه

📚 منابع ({len(response.sources)} مورد):"""

    for i, source in enumerate(response.sources, 1):
        articles = f"مواد: {', '.join(map(str, source['article_numbers']))}" if source.get('article_numbers') else ""
        notes = f"تبصره‌ها: {', '.join(map(str, source['note_numbers']))}" if source.get('note_numbers') else ""
        
        formatted += f"""
   {i}. {source['document']} (اعتماد: {source['confidence']:.3f})
      نوع: {source['chunk_type']} | {articles} {notes}"""
    
    formatted += "\n" + "="*80
    
    return formatted


if __name__ == "__main__":
    print("University Rules RAG System V2 - Import this module")
    print("Example: from src.faiss_rag_v2 import UniversityRulesRAG")
