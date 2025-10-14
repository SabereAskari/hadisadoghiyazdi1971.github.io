#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced RAG System with Qwen LLM Integration
Complete RAG pipeline with retrieval and generation using Qwen2.5-72B-Instruct via OpenRouter
"""

import os
import json
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv
import re

# Import required packages
try:
    from sentence_transformers import SentenceTransformer
    from qdrant_client import QdrantClient
    from openai import OpenAI
    print("✅ All required packages imported successfully")
except ImportError as e:
    print(f"❌ Missing required package: {e}")
    print("Please install: pip install sentence-transformers qdrant-client python-dotenv openai")
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
    def __init__(self, env_path: str = ".env"):
        """Initialize the enhanced RAG system with LLM"""
        
        # Load environment variables
        load_dotenv(env_path)
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.qwen_model = os.getenv("QWEN_MODEL", "openai/gpt-4o-mini")
        
        if not all([self.qdrant_url, self.qdrant_api_key, self.openrouter_api_key]):
            raise ValueError("Required environment variables not found")
        
        # Import PDF URLs configuration
        try:
            from .pdf_urls_config import get_pdf_url, get_document_title, get_document_category
            self.get_pdf_url = get_pdf_url
            self.get_document_title = get_document_title  
            self.get_document_category = get_document_category
            print("✅ PDF URLs configuration loaded")
        except ImportError:
            print("⚠️ PDF URLs configuration not found, using fallback URLs")
            # Fallback URLs (your existing ones)
            self.document_urls = {
                "rules_01": "https://vpr.um.ac.ir/images/32/stories/moavenat/maghalat/87.1.18-darj-sahih-neshani-daneshgah-dar-maghale2.pdf",
                "rules_02": "https://vpr.um.ac.ir/images/32/stories/moavenat/maghalat/91.10.16-tartibe-asami-va-nahve-darj-neshani4.pdf",
                "rules_03": "https://vpr.um.ac.ir/images/32/stories/moavenat/maghalat/93.3.17-darje-neshani-post-electronic.pdf",
                "rules_04": "https://vpr.um.ac.ir/images/32/stories/moavenat/tahsilat-takmili/9333-tartibe-asami-nevisandegan-maghalat-va-nevisande-masool.pdf",
                "rules_05": "https://vpr.um.ac.ir/images/32/stories/moavenat/mosavabat/heyat-raeese/13980702comission.pdf",
                "rules_06": "https://vpr.um.ac.ir/images/32/stories/moavenat/maghalat/letter.pdf",
                "rules_07": "https://vpr.um.ac.ir/images/32/stories/moavenat/tahsilat-takmili/shora-pajoheshi-1400-03-25.pdf"
            }
            self.get_pdf_url = lambda doc_id: self.document_urls.get(doc_id, "")
            self.get_document_title = lambda doc_id: doc_id
            self.get_document_category = lambda doc_id: "نامشخص"
        
        # Initialize embedding model
        print("🤖 Loading sentence-transformers model...")
        self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', device="cpu")
        
        # Initialize Qdrant client
        print("🔗 Connecting to Qdrant...")
        self.qdrant_client = QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
        )
        
        # Initialize OpenRouter client (OpenAI-compatible)
        print("🧠 Connecting to OpenRouter...")
        self.openai_client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.openrouter_api_key,
        )
        self.model_name = self.qwen_model
        print(f"✅ Connected to OpenRouter with model: {self.model_name}")
        self.collection_name = "university_rules"
        
        # RAG configuration
        self.max_context_length = 2000  # Max characters for context
        self.max_sources = 5  # Maximum number of sources to retrieve
        self.min_confidence = 0.0  # Minimum confidence threshold (lowered to allow more results)
        
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
        
        print("✅ Enhanced RAG system with LLM and Academic Level Awareness initialized")
    
    def get_available_categories(self) -> List[str]:
        """Get a list of unique categories from the knowledge base"""
        # This is a placeholder. In a real scenario, you might query Qdrant
        # or have a pre-compiled list of categories.
        # For now, we'll use the categories from the pdf_urls_config.
        try:
            from src.pdf_urls_config import get_all_categories
            return get_all_categories()
        except (ImportError, AttributeError):
             # Fallback if the function doesn't exist
            return [
                "قوانین انتشار پایان‌نامه",
                "سیاست پست الکترونیک",
                "مقررات تحصیلات تکمیلی",
                "قوانین نویسندگی",
                "سیاست‌های به‌روز نویسندگی",
                "انعطاف نویسندگی",
                "الزامات نشانی"
            ]

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
        """Retrieve relevant context from knowledge base with academic level filtering"""
        
        retrieval_start = time.time()
        
        # Detect academic level first
        detected_level, level_confidence = self.detect_academic_level(query)
        print(f"🎯 Detected academic level: {detected_level} (confidence: {level_confidence:.2f})")
        
        # Embed the query
        query_embedding = self.model.encode([query])[0].tolist()
        
        # Search in Qdrant with more results to allow filtering
        search_results = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=top_k * 3,  # Get more results to filter by academic level
            with_payload=True,
            score_threshold=self.min_confidence
        )
        
        # Process and filter results by academic level
        filtered_sources = []
        general_sources = []
        other_sources = []
        
        for result in search_results.points:
            payload = result.payload
            source_file = payload.get('source_file', '')
            
            # Extract document ID from source file (remove .txt extension if present)
            document_id = source_file.replace('.txt', '') if source_file.endswith('.txt') else source_file
            
            chunk_level = payload.get('academic_level', 'general')
            
            source_data = {
                "score": result.score,
                "content": payload.get('text', ''),
                "document_title": self.get_document_title(document_id),
                "document_file": source_file,  # Keep original filename for reference
                "category_persian": payload.get('academic_level_persian', payload.get('document_type', '')),
                "chunk_summary": payload.get('text_snippet', ''),
                "key_topics": payload.get('main_topics', payload.get('key_topics', [])),
                "cross_references": payload.get('keywords', []),
                "document_id": document_id,
                "chunk_id": payload.get('chunk_id', ''),
                "pdf_url": self.get_pdf_url(document_id),
                "academic_level": chunk_level,
                "article_number": payload.get('article_number', 0),
                "note_number": payload.get('note_number', 0),
                "chunk_type": payload.get('chunk_type', 'unknown')
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
        """Generate answer using Qwen LLM via OpenRouter with academic level awareness"""
        
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
            # Generate response using OpenRouter (Qwen model)
            response = self.openai_client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://github.com/FUM_RAG",  # Optional
                    "X-Title": "FUM RAG System",  # Optional
                },
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            answer_markdown = response.choices[0].message.content
            
            # Create a plain text version for copy-pasting
            answer_plain = answer_markdown.replace('**', '').replace('*', '')
            answer_plain = answer_plain.replace('[مشاهده PDF]', '').replace('([منبع])', '')
            
            # Note: Linkification is applied later in answer_question where sources are available
            
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
                cross_references=[]
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
                "source": source['document_title'],  # For compatibility with test script
                "document": source['document_title'],
                "category": source['category_persian'], 
                "confidence": source['score'],
                "score": source['score'],  # For compatibility with test script
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
        
        try:
            collection_info = self.qdrant_client.get_collection(self.collection_name)
            
            stats = {
                "collection_name": self.collection_name,
                "total_documents": collection_info.points_count,
                "embedding_model": "paraphrase-multilingual-MiniLM-L12-v2",
                "llm_model": self.qwen_model,
                "max_context_length": self.max_context_length,
                "min_confidence_threshold": self.min_confidence,
                "status": "active"
            }
            
            return stats
            
        except Exception as e:
            return {"error": str(e), "status": "error"}
    
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
      دسته‌بندی: {source['category']}"""
    
    if response.cross_references:
        formatted += f"""

🔗 مقررات مرتبط: {', '.join(response.cross_references)}"""
    
    formatted += "\n" + "="*80
    
    return formatted

# Usage and testing functions
def test_rag_system_with_llm():
    """Test the enhanced RAG system with comprehensive queries"""
    
    print("🧪 Testing Enhanced RAG System with Qwen LLM")
    print("="*80)
    
    # Initialize system
    rag = UniversityRulesRAGWithLLM()
    
    # Test queries with varying complexity
    test_queries = [
        "نویسنده مسئول کیست و چه وظایفی دارد؟",
        "چگونه نشانی دانشگاه فردوسی مشهد را در مقالات درج کنم؟",
        "قوانین مربوط به مقالات مستخرج از پایان‌نامه چیست؟",
        "آیا استفاده از ایمیل دانشگاه در مقالات الزامی است؟",
        "در همکاری با پژوهشگران خارجی چه نکاتی باید رعایت شود؟",
        "ترتیب اسامی نویسندگان در مقالات چگونه تعیین می‌شود؟",
        "اگر بخواهم یک نویسنده را به مقاله اضافه کنم چه کنم؟",
        "قوانین مربوط به دانشجویان بین‌المللی چیست؟"
    ]
    
    # Process queries
    responses = rag.batch_answer_questions(test_queries)
    
    # Display results
    for response in responses:
        print(format_rag_response(response))
        print("\n")
    
    # System statistics
    stats = rag.get_system_statistics()
    print("📊 System Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    return responses

def performance_benchmark():
    """Benchmark system performance"""
    
    print("⚡ Performance Benchmark")
    print("="*50)
    
    rag = UniversityRulesRAGWithLLM()
    
    # Quick queries for speed testing
    quick_queries = [
        "نویسنده مسئول چیست؟",
        "نشانی دانشگاه",
        "ایمیل دانشگاه", 
        "پایان‌نامه",
        "همکاری خارجی"
    ]
    
    total_time = 0
    retrieval_times = []
    generation_times = []
    
    for query in quick_queries:
        response = rag.answer_question(query, top_k=3)  # Smaller top_k for speed
        
        total_time += response.total_time
        retrieval_times.append(response.retrieval_time)
        generation_times.append(response.generation_time)
        
        print(f"✅ '{query}' - {response.total_time:.2f}s (Confidence: {response.confidence:.3f})")
    
    # Calculate averages
    avg_total = total_time / len(quick_queries)
    avg_retrieval = sum(retrieval_times) / len(retrieval_times)
    avg_generation = sum(generation_times) / len(generation_times)
    
    print(f"\n📊 Performance Summary:")
    print(f"   Average Total Time: {avg_total:.2f}s")
    print(f"   Average Retrieval Time: {avg_retrieval:.2f}s") 
    print(f"   Average Generation Time: {avg_generation:.2f}s")
    print(f"   Total Queries Processed: {len(quick_queries)}")

def interactive_mode_with_llm():
    """Interactive mode with enhanced LLM responses"""
    
    rag = UniversityRulesRAGWithLLM()
    
    print("\n🎯 حالت تعاملی RAG با هوش مصنوعی - برای خروج 'quit' تایپ کنید")
    print("="*70)
    
    while True:
        query = input("\n❓ سؤال خود را بپرسید: ").strip()
        
        if query.lower() in ['quit', 'exit', 'خروج']:
            print("👋 خداحافظ!")
            break
        
        if not query:
            continue
        
        try:
            response = rag.answer_question(query)
            print(format_rag_response(response))
            
        except Exception as e:
            print(f"❌ خطا: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--interactive":
            interactive_mode_with_llm()
        elif sys.argv[1] == "--benchmark":
            performance_benchmark()
        else:
            print("Usage: python enhanced_rag_with_llm.py [--interactive|--benchmark]")
    else:
        test_rag_system_with_llm()