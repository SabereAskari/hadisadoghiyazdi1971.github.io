#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FAISS Index Creator V3 - Advanced RAG Optimized
ایندکس‌سازی هوشمند با قابلیت‌های پیشرفته برای RAG
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

try:
    from sentence_transformers import SentenceTransformer
    import faiss
    import numpy as np
    from sklearn.preprocessing import normalize
    print("✅ همه کتابخانه‌های مورد نیاز با موفقیت وارد شدند")
except ImportError as e:
    print(f"❌ کتابخانه مفقوده: {e}")
    print("لطفا نصب کنید: pip install sentence-transformers faiss-cpu scikit-learn")
    exit(1)

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class AdvancedDocumentChunk:
    """قطعه سند پیشرفته با متادیتای غنی"""
    id: str
    text: str
    source_file: str
    chunk_type: str  # 'title', 'introduction', 'article', 'definitions', 'table', 'conclusion', 'regulation'
    article_numbers: List[int]
    note_numbers: List[int]
    has_table: bool
    has_list: bool
    document_section: str
    document_title: str
    chunk_index: int
    embedding: Optional[np.ndarray] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if not self.id:
            self.id = self.generate_id()
    
    def generate_id(self) -> str:
        """ایجاد شناسه یکتا برای قطعه"""
        content = f"{self.source_file}_{self.chunk_index}_{self.text[:50]}"
        return hashlib.md5(content.encode()).hexdigest()

class AdvancedStructureAwareChunker:
    """قطعه‌بند پیشرفته با درک ساختار سند"""
    
    def __init__(self, max_chunk_size: int = 800, min_chunk_size: int = 150, overlap_size: int = 50):
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size
        self.overlap_size = overlap_size
        
        # الگوهای پیشرفته برای تشخیص ساختار
        self.patterns = {
            'title': re.compile(r'^#\s+(.+)$', re.MULTILINE),
            'section': re.compile(r'^##\s+(.+)$', re.MULTILINE),
            'subsection': re.compile(r'^###\s+(.+)$', re.MULTILINE),
            'article': re.compile(r'##\s*ماده\s+(\d+)[:-]?\s*(.+?)(?=\n|$)', re.MULTILINE),
            'note': re.compile(r'\*\*تبصره\s+(\d+):\*\*\s*(.+?)(?=\n\n|\*\*تبصره|\Z)', re.DOTALL),
            'regulation': re.compile(r'##\s*(آیین نامه|دستورالعمل|بخشنامه)\s*(.+?)(?=\n|$)', re.MULTILINE),
            'definition': re.compile(r'\*\*([^*]+):\*\*\s*(.+?)(?=\n-|\n\*\*|\n\n|\Z)', re.DOTALL),
            'list_item': re.compile(r'^-\s+(.+)$', re.MULTILINE),
            'table': re.compile(r'\|.+\|', re.MULTILINE),
            'numbered_list': re.compile(r'^\d+[-.)]\s+(.+)$', re.MULTILINE),
            'reference': re.compile(r'(به استناد|موضوع|طبق)\s+ماده\s+(\d+)', re.IGNORECASE),
        }
    
    def extract_document_structure(self, text: str) -> Dict[str, Any]:
        """استخراج ساختار کامل سند"""
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
        """استخراج عنوان اصلی"""
        match = self.patterns['title'].search(text)
        return match.group(1).strip() if match else "عنوان نامشخص"
    
    def _extract_sections(self, text: str) -> List[Dict]:
        """استخراج بخش‌های سند"""
        sections = []
        for match in self.patterns['section'].finditer(text):
            sections.append({
                'title': match.group(1).strip(),
                'start_pos': match.start(),
                'end_pos': match.end()
            })
        return sections
    
    def _extract_articles(self, text: str) -> List[Dict]:
        """استخراج مواد قانونی"""
        articles = []
        for match in self.patterns['article'].finditer(text):
            articles.append({
                'number': int(match.group(1)),
                'title': match.group(2).strip(),
                'content_start': match.end()
            })
        return articles
    
    def _extract_notes(self, text: str) -> List[Dict]:
        """استخراج تبصره‌ها"""
        notes = []
        for match in self.patterns['note'].finditer(text):
            notes.append({
                'number': int(match.group(1)),
                'content': match.group(2).strip()
            })
        return notes
    
    def _extract_regulations(self, text: str) -> List[Dict]:
        """استخراج آیین‌نامه‌ها و دستورالعمل‌ها"""
        regulations = []
        for match in self.patterns['regulation'].finditer(text):
            regulations.append({
                'type': match.group(1).strip(),
                'title': match.group(2).strip()
            })
        return regulations
    
    def _extract_tables(self, text: str) -> List[Dict]:
        """استخراج جداول"""
        tables = []
        for match in self.patterns['table'].finditer(text):
            tables.append({
                'content': match.group(0),
                'start_pos': match.start()
            })
        return tables
    
    def intelligent_chunking(self, text: str, source_file: str) -> List[AdvancedDocumentChunk]:
        """قطعه‌بندی هوشمند با حفظ زمینه"""
        chunks = []
        document_title = self._extract_title(text)
        structure = self.extract_document_structure(text)
        
        # پردازش بر اساس ساختار
        current_pos = 0
        chunk_index = 0
        
        # پردازش عنوان و مقدمه
        title_chunk = self._create_title_chunk(text, source_file, document_title, chunk_index)
        if title_chunk:
            chunks.append(title_chunk)
            chunk_index += 1
            current_pos = len(title_chunk.text)
        
        # پردازش بخش‌ها
        for section in structure['sections']:
            section_text = self._extract_section_text(text, section['start_pos'])
            section_chunks = self._process_section(section_text, source_file, document_title, 
                                                 section['title'], chunk_index)
            chunks.extend(section_chunks)
            chunk_index += len(section_chunks)
        
        # بهینه‌سازی قطعات کوچک
        chunks = self._optimize_small_chunks(chunks)
        
        return chunks
    
    def _create_title_chunk(self, text: str, source_file: str, document_title: str, chunk_index: int) -> Optional[AdvancedDocumentChunk]:
        """ایجاد قطعه عنوان"""
        title_match = self.patterns['title'].search(text)
        if not title_match:
            return None
        
        title_text = title_match.group(0)
        remaining = text[title_match.end():].strip()
        
        # اگر مقدمه کوتاه است، با عنوان ادغام کن
        if remaining and len(remaining) < 300:
            combined_text = f"{title_text}\n\n{remaining}"
            return AdvancedDocumentChunk(
                id="",
                text=combined_text,
                source_file=source_file,
                chunk_type="title_intro",
                document_title=document_title,
                document_section="عنوان و مقدمه",
                chunk_index=chunk_index,
                article_numbers=[],
                note_numbers=[],
                has_table=False,
                has_list=False,
                metadata={'combined': True}
            )
        else:
            return AdvancedDocumentChunk(
                id="",
                text=title_text,
                source_file=source_file,
                chunk_type="title",
                document_title=document_title,
                document_section="عنوان",
                chunk_index=chunk_index,
                article_numbers=[],
                note_numbers=[],
                has_table=False,
                has_list=False
            )
    
    def _extract_section_text(self, text: str, start_pos: int) -> str:
        """استخراج متن بخش"""
        next_section = re.search(r'\n##\s+', text[start_pos:])
        if next_section:
            return text[start_pos:start_pos + next_section.start()]
        return text[start_pos:]
    
    def _process_section(self, section_text: str, source_file: str, document_title: str, 
                        section_name: str, start_index: int) -> List[AdvancedDocumentChunk]:
        """پردازش یک بخش"""
        chunks = []
        
        # تشخیص نوع بخش
        section_type = self._classify_section_type(section_text, section_name)
        
        if section_type == "article_section":
            # پردازش بخش مواد قانونی
            chunks.extend(self._process_article_section(section_text, source_file, document_title, 
                                                      section_name, start_index))
        elif section_type == "regulation":
            # پردازش آیین‌نامه‌ها
            chunks.extend(self._process_regulation_section(section_text, source_file, document_title, 
                                                         section_name, start_index))
        else:
            # پردازش بخش عادی
            if len(section_text) <= self.max_chunk_size:
                chunks.append(self._create_chunk(section_text, source_file, document_title, 
                                               section_name, section_type, start_index))
            else:
                # تقسیم بخش بزرگ
                sub_chunks = self._split_large_section(section_text, source_file, document_title, 
                                                     section_name, section_type, start_index)
                chunks.extend(sub_chunks)
        
        return chunks
    
    def _classify_section_type(self, text: str, section_name: str) -> str:
        """طبقه‌بندی نوع بخش"""
        text_lower = text.lower()
        section_lower = section_name.lower()
        
        if any(word in section_lower for word in ['ماده', 'اصل', 'مادۀ']):
            return "article_section"
        elif any(word in section_lower for word in ['آیین', 'دستورالعمل', 'بخشنامه']):
            return "regulation"
        elif any(word in section_lower for word in ['تعریف', 'تعاریف']):
            return "definitions"
        elif any(word in section_lower for word in ['جدول', 'فرم']):
            return "table_section"
        elif any(word in section_lower for word in ['مقدمه', 'پیشگفتار']):
            return "introduction"
        elif any(word in section_lower for word in ['نتیجه', 'پایان', 'تصویب']):
            return "conclusion"
        else:
            return "general"
    
    def _process_article_section(self, section_text: str, source_file: str, document_title: str, 
                               section_name: str, start_index: int) -> List[AdvancedDocumentChunk]:
        """پردازش بخش مواد قانونی"""
        chunks = []
        
        # تقسیم بر اساس مواد و تبصره‌ها
        parts = re.split(r'(\*\*تبصره\s+\d+:\*\*)', section_text)
        
        current_chunk = ""
        current_index = start_index
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            if part.startswith('**تبصره'):
                # اگر تبصره است
                if current_chunk and len(current_chunk) + len(part) < self.max_chunk_size:
                    # ادغام با قطعه قبلی
                    current_chunk += f"\n\n{part}"
                else:
                    # ذخیره قطعه قبلی و شروع جدید
                    if current_chunk:
                        chunks.append(self._create_chunk(current_chunk, source_file, document_title, 
                                                       section_name, "article", current_index))
                        current_index += 1
                    current_chunk = part
            else:
                # متن اصلی ماده
                if current_chunk:
                    current_chunk += f"\n\n{part}"
                else:
                    current_chunk = part
            
            # اگر قطعه بزرگ شد، ذخیره کن
            if len(current_chunk) >= self.max_chunk_size:
                chunks.append(self._create_chunk(current_chunk, source_file, document_title, 
                                               section_name, "article", current_index))
                current_index += 1
                current_chunk = ""
        
        # ذخیره قطعه نهایی
        if current_chunk:
            chunks.append(self._create_chunk(current_chunk, source_file, document_title, 
                                           section_name, "article", current_index))
        
        return chunks
    
    def _process_regulation_section(self, section_text: str, source_file: str, document_title: str, 
                                  section_name: str, start_index: int) -> List[AdvancedDocumentChunk]:
        """پردازش بخش آیین‌نامه‌ها"""
        # برای آیین‌نامه‌ها از قطعه‌بندی دقیق‌تر استفاده می‌کنیم
        return self._split_by_logical_units(section_text, source_file, document_title, 
                                          section_name, "regulation", start_index)
    
    def _split_by_logical_units(self, text: str, source_file: str, document_title: str, 
                              section_name: str, chunk_type: str, start_index: int) -> List[AdvancedDocumentChunk]:
        """تقسیم بر اساس واحدهای منطقی"""
        chunks = []
        
        # تقسیم بر اساس پاراگراف‌های منطقی
        paragraphs = re.split(r'\n\s*\n', text)
        
        current_chunk = ""
        current_index = start_index
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # اگر پاراگراف خیلی بزرگ است، خودش یک قطعه شود
            if len(para) > self.max_chunk_size * 0.7:
                if current_chunk:
                    chunks.append(self._create_chunk(current_chunk, source_file, document_title, 
                                                   section_name, chunk_type, current_index))
                    current_index += 1
                    current_chunk = ""
                
                # تقسیم پاراگراف بزرگ
                sub_chunks = self._split_large_paragraph(para, source_file, document_title, 
                                                       section_name, chunk_type, current_index)
                chunks.extend(sub_chunks)
                current_index += len(sub_chunks)
            else:
                # بررسی امکان ادغام
                if len(current_chunk) + len(para) + 2 <= self.max_chunk_size:
                    if current_chunk:
                        current_chunk += f"\n\n{para}"
                    else:
                        current_chunk = para
                else:
                    # ذخیره قطعه فعلی
                    if current_chunk:
                        chunks.append(self._create_chunk(current_chunk, source_file, document_title, 
                                                       section_name, chunk_type, current_index))
                        current_index += 1
                    current_chunk = para
        
        # ذخیره قطعه نهایی
        if current_chunk:
            chunks.append(self._create_chunk(current_chunk, source_file, document_title, 
                                           section_name, chunk_type, current_index))
        
        return chunks
    
    def _split_large_section(self, section_text: str, source_file: str, document_title: str, 
                           section_name: str, chunk_type: str, start_index: int) -> List[AdvancedDocumentChunk]:
        """تقسیم بخش بزرگ"""
        return self._split_by_logical_units(section_text, source_file, document_title, 
                                          section_name, chunk_type, start_index)
    
    def _split_large_paragraph(self, paragraph: str, source_file: str, document_title: str, 
                             section_name: str, chunk_type: str, start_index: int) -> List[AdvancedDocumentChunk]:
        """تقسیم پاراگراف بزرگ"""
        chunks = []
        
        # تقسیم بر اساس جملات
        sentences = re.split(r'[.!?]+\s+', paragraph)
        
        current_chunk = ""
        current_index = start_index
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            if len(current_chunk) + len(sentence) + 2 <= self.max_chunk_size:
                if current_chunk:
                    current_chunk += f". {sentence}"
                else:
                    current_chunk = sentence
            else:
                if current_chunk:
                    chunks.append(self._create_chunk(current_chunk, source_file, document_title, 
                                                   section_name, chunk_type, current_index))
                    current_index += 1
                current_chunk = sentence
        
        if current_chunk:
            chunks.append(self._create_chunk(current_chunk, source_file, document_title, 
                                           section_name, chunk_type, current_index))
        
        return chunks
    
    def _create_chunk(self, text: str, source_file: str, document_title: str, 
                     section_name: str, chunk_type: str, chunk_index: int) -> AdvancedDocumentChunk:
        """ایجاد قطعه سند"""
        
        article_numbers = self._extract_article_numbers(text)
        note_numbers = self._extract_note_numbers(text)
        has_table = bool(self.patterns['table'].search(text))
        has_list = bool(self.patterns['list_item'].search(text) or 
                       self.patterns['numbered_list'].search(text))
        
        metadata = {
            'has_definitions': '**' in text and ':' in text,
            'has_references': bool(self.patterns['reference'].search(text)),
            'sentence_count': len(re.findall(r'[.!?]+', text)),
            'word_count': len(text.split()),
            'char_count': len(text),
            'quality_score': self._calculate_quality_score(text)
        }
        
        return AdvancedDocumentChunk(
            id="",
            text=text,
            source_file=source_file,
            chunk_type=chunk_type,
            document_title=document_title,
            document_section=section_name,
            chunk_index=chunk_index,
            article_numbers=article_numbers,
            note_numbers=note_numbers,
            has_table=has_table,
            has_list=has_list,
            metadata=metadata
        )
    
    def _extract_article_numbers(self, text: str) -> List[int]:
        """استخراج شماره مواد"""
        numbers = []
        for match in self.patterns['article'].finditer(text):
            try:
                numbers.append(int(match.group(1)))
            except (ValueError, IndexError):
                pass
        
        # استخراج ارجاعات به مواد
        for match in self.patterns['reference'].finditer(text):
            try:
                num = int(match.group(2))
                if num not in numbers:
                    numbers.append(num)
            except (ValueError, IndexError):
                pass
        
        return sorted(list(set(numbers)))
    
    def _extract_note_numbers(self, text: str) -> List[int]:
        """استخراج شماره تبصره‌ها"""
        numbers = []
        for match in self.patterns['note'].finditer(text):
            try:
                numbers.append(int(match.group(1)))
            except (ValueError, IndexError):
                pass
        return sorted(numbers)
    
    def _calculate_quality_score(self, text: str) -> float:
        """محاسبه امتیاز کیفیت قطعه"""
        score = 0.0
        
        # امتیاز بر اساس طول
        if self.min_chunk_size <= len(text) <= self.max_chunk_size:
            score += 0.3
        elif len(text) > 50:  # حداقل طول قابل قبول
            score += 0.1
        
        # امتیاز بر اساس ساختار
        if any(marker in text for marker in ['**', '##', 'ماده', 'تبصره']):
            score += 0.3
        
        # امتیاز بر اساس کامل بودن جملات
        sentences = re.findall(r'[^.!?]+[.!?]', text)
        if len(sentences) >= 1:
            score += 0.2
        
        # امتیاز بر اساس تنوع محتوا
        words = text.split()
        unique_words = len(set(words))
        if len(words) > 0:
            diversity = unique_words / len(words)
            score += diversity * 0.2
        
        return min(score, 1.0)
    
    def _optimize_small_chunks(self, chunks: List[AdvancedDocumentChunk]) -> List[AdvancedDocumentChunk]:
        """بهینه‌سازی قطعات کوچک"""
        if not chunks:
            return chunks
        
        optimized = []
        i = 0
        
        while i < len(chunks):
            current = chunks[i]
            
            # اگر قطعه خیلی کوچک است و قطعه بعدی وجود دارد
            if (len(current.text) < self.min_chunk_size and 
                i < len(chunks) - 1 and 
                chunks[i+1].chunk_type == current.chunk_type):
                
                next_chunk = chunks[i+1]
                combined_text = f"{current.text}\n\n{next_chunk.text}"
                
                if len(combined_text) <= self.max_chunk_size:
                    # ادغام قطعات
                    merged_chunk = AdvancedDocumentChunk(
                        id="",
                        text=combined_text,
                        source_file=current.source_file,
                        chunk_type=current.chunk_type,
                        document_title=current.document_title,
                        document_section=current.document_section,
                        chunk_index=current.chunk_index,
                        article_numbers=list(set(current.article_numbers + next_chunk.article_numbers)),
                        note_numbers=list(set(current.note_numbers + next_chunk.note_numbers)),
                        has_table=current.has_table or next_chunk.has_table,
                        has_list=current.has_list or next_chunk.has_list,
                        metadata={
                            'merged': True,
                            'original_chunks': [current.chunk_index, next_chunk.chunk_index],
                            'quality_score': (current.metadata.get('quality_score', 0) + 
                                            next_chunk.metadata.get('quality_score', 0)) / 2
                        }
                    )
                    optimized.append(merged_chunk)
                    i += 2  # دو قطعه را پرش کن
                    continue
            
            optimized.append(current)
            i += 1
        
        return optimized

class AdvancedFAISSIndexCreator:
    """ایجاد کننده ایندکس FAISS پیشرفته"""
    
    def __init__(
        self,
        documents_dir: str = "./documents",
        index_dir: str = "./index_v3",
        embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        max_chunk_size: int = 800,
        min_chunk_size: int = 150
    ):
        self.documents_dir = Path(documents_dir)
        self.index_dir = Path(index_dir)
        self.embedding_model_name = embedding_model
        
        # ایجاد دایرکتوری ایندکس
        self.index_dir.mkdir(parents=True, exist_ok=True)
        
        # راه‌اندازی کامپوننت‌ها
        logger.info(f"🤖 در حال بارگذاری مدل embedding: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model, device="cpu")
        self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()
        
        self.chunker = AdvancedStructureAwareChunker(
            max_chunk_size=max_chunk_size,
            min_chunk_size=min_chunk_size
        )
        
        # ذخیره‌سازی
        self.all_chunks: List[AdvancedDocumentChunk] = []
        self.embeddings: np.ndarray = None
    
    def process_documents_parallel(self, max_workers: int = 4):
        """پردازش موازی اسناد"""
        logger.info(f"📂 پردازش اسناد از: {self.documents_dir}")
        
        txt_files = list(self.documents_dir.glob("*.txt"))
        
        if not txt_files:
            raise FileNotFoundError(f"هیچ فایل .txt در {self.documents_dir} یافت نشد")
        
        logger.info(f"📄 تعداد اسناد یافت شده: {len(txt_files)}")
        
        # پردازش موازی
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(self._process_single_document, file_path): file_path 
                for file_path in sorted(txt_files)
            }
            
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    chunks = future.result()
                    logger.info(f"✅ پردازش کامل: {file_path.name} - {len(chunks)} قطعه")
                except Exception as exc:
                    logger.error(f"❌ خطا در پردازش {file_path.name}: {exc}")
        
        logger.info(f"✅ مجموع قطعات ایجاد شده: {len(self.all_chunks)}")
        
        # آمار
        self._print_statistics()
    
    def _process_single_document(self, file_path: Path) -> List[AdvancedDocumentChunk]:
        """پردازش یک سند"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # ایجاد قطعات
            chunks = self.chunker.intelligent_chunking(text, file_path.name)
            
            # افزودن به مجموعه کلی
            self.all_chunks.extend(chunks)
            
            return chunks
            
        except Exception as e:
            logger.error(f"خطا در پردازش {file_path}: {e}")
            return []
    
    def _print_statistics(self):
        """چاپ آمار قطعات"""
        chunk_types = {}
        quality_scores = []
        
        for chunk in self.all_chunks:
            chunk_types[chunk.chunk_type] = chunk_types.get(chunk.chunk_type, 0) + 1
            quality_scores.append(chunk.metadata.get('quality_score', 0))
        
        logger.info("\n📊 توزیع قطعات:")
        for chunk_type, count in sorted(chunk_types.items()):
            percentage = (count / len(self.all_chunks)) * 100
            logger.info(f"   {chunk_type}: {count} ({percentage:.1f}%)")
        
        if quality_scores:
            avg_quality = sum(quality_scores) / len(quality_scores)
            logger.info(f"   میانگین امتیاز کیفیت: {avg_quality:.2f}")
    
    def create_embeddings_batch(self, batch_size: int = 64):
        """ایجاد embedding به صورت batch"""
        logger.info(f"🧠 ایجاد embedding برای {len(self.all_chunks)} قطعه...")
        
        texts = [chunk.text for chunk in self.all_chunks]
        
        # ایجاد embedding برای همه متن‌ها
        all_embeddings = self.embedding_model.encode(
            texts, 
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        
        # نرمال‌سازی embeddingها
        self.embeddings = normalize(all_embeddings, norm='l2', axis=1)
        
        logger.info(f"✅ ایجاد {len(self.embeddings)} embedding انجام شد")
    
    def create_optimized_faiss_index(self):
        """ایجاد ایندکس FAISS بهینه‌شده"""
        logger.info("📊 ایجاد ایندکس FAISS...")
        
        if self.embeddings is None:
            raise ValueError("ابتدا باید embeddingها ایجاد شوند")
        
        # ایجاد ایندکس HNSW برای کارایی بهتر
        index = faiss.IndexHNSWFlat(self.embedding_dim, 32)
        
        # افزودن embeddingها به ایندکس
        index.add(self.embeddings.astype('float32'))
        
        # ذخیره ایندکس
        index_path = self.index_dir / "faiss_index_optimized.bin"
        faiss.write_index(index, str(index_path))
        logger.info(f"✅ ایندکس FAISS ذخیره شد در: {index_path}")
        
        return index
    
    def save_enhanced_metadata(self):
        """ذخیره متادیتای پیشرفته"""
        logger.info("💾 ذخیره متادیتا...")
        
        metadata_list = []
        
        for i, chunk in enumerate(self.all_chunks):
            chunk_data = {
                "chunk_id": chunk.id,
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
                "word_count": len(chunk.text.split()),
                "quality_score": chunk.metadata.get('quality_score', 0),
                "chunk_text": chunk.text,
                "metadata": chunk.metadata,
                "indexed_at": datetime.now().isoformat()
            }
            metadata_list.append(chunk_data)
        
        # ذخیره متادیتا
        metadata_path = self.index_dir / "enhanced_metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata_list, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ متادیتا ذخیره شد در: {metadata_path}")
    
    def save_comprehensive_summary(self):
        """ذخیره خلاصه جامع"""
        logger.info("📋 ذخیره خلاصه جامع...")
        
        # محاسبه آمار پیشرفته
        total_words = sum(len(chunk.text.split()) for chunk in self.all_chunks)
        total_chars = sum(len(chunk.text) for chunk in self.all_chunks)
        
        chunk_lengths = [len(chunk.text) for chunk in self.all_chunks]
        quality_scores = [chunk.metadata.get('quality_score', 0) for chunk in self.all_chunks]
        
        summary = {
            "indexed_at": datetime.now().isoformat(),
            "total_documents": len(set(chunk.source_file for chunk in self.all_chunks)),
            "total_chunks": len(self.all_chunks),
            "total_words": total_words,
            "total_characters": total_chars,
            "embedding_model": self.embedding_model_name,
            "embedding_dimension": self.embedding_dim,
            "chunking_strategy": "advanced_structure_aware",
            "chunk_size_stats": {
                "min": min(chunk_lengths),
                "max": max(chunk_lengths),
                "avg": sum(chunk_lengths) / len(chunk_lengths),
                "std": np.std(chunk_lengths) if chunk_lengths else 0
            },
            "quality_stats": {
                "min": min(quality_scores) if quality_scores else 0,
                "max": max(quality_scores) if quality_scores else 0,
                "avg": sum(quality_scores) / len(quality_scores) if quality_scores else 0
            },
            "document_details": self._get_document_details()
        }
        
        # ذخیره خلاصه
        summary_path = self.index_dir / "comprehensive_summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ خلاصه جامع ذخیره شد در: {summary_path}")
        
        return summary
    
    def _get_document_details(self) -> List[Dict]:
        """دریافت جزئیات اسناد"""
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
        
        # محاسبه میانگین امتیاز کیفیت
        for doc_file, doc_data in doc_details.items():
            doc_chunks = [chunk for chunk in self.all_chunks if chunk.source_file == doc_file]
            if doc_chunks:
                avg_quality = sum(chunk.metadata.get('quality_score', 0) for chunk in doc_chunks) / len(doc_chunks)
                doc_data["avg_quality_score"] = round(avg_quality, 3)
        
        return list(doc_details.values())
    
    def create_advanced_index(self):
        """متد اصلی برای ایجاد ایندکس پیشرفته"""
        print("="*80)
        print("🚀 FAISS Index Creator V3 - Advanced RAG Optimized")
        print("="*80)
        
        try:
            # پردازش اسناد
            self.process_documents_parallel()
            
            # ایجاد embeddingها
            self.create_embeddings_batch()
            
            # ایجاد ایندکس FAISS
            self.create_optimized_faiss_index()
            
            # ذخیره متادیتا
            self.save_enhanced_metadata()
            
            # ذخیره خلاصه
            summary = self.save_comprehensive_summary()
            
            print("\n" + "="*80)
            print("✅ ایجاد ایندکس با موفقیت کامل شد!")
            print("="*80)
            
            # چاپ خلاصه نهایی
            self._print_final_summary(summary)
            
        except Exception as e:
            logger.error(f"خطا در ایجاد ایندکس: {e}")
            raise
    
    def _print_final_summary(self, summary: Dict):
        """چاپ خلاصه نهایی"""
        print(f"\n📊 خلاصه نهایی:")
        print(f"   📄 اسناد پردازش شده: {summary['total_documents']}")
        print(f"   ✂️  کل قطعات: {summary['total_chunks']}")
        print(f"   📝 کل کلمات: {summary['total_words']:,}")
        print(f"   🔤 کل کاراکترها: {summary['total_characters']:,}")
        print(f"   📏 اندازه متوسط قطعات: {summary['chunk_size_stats']['avg']:.0f} کاراکتر")
        print(f"   ⭐ میانگین امتیاز کیفیت: {summary['quality_stats']['avg']:.2f}")
        print(f"   🤖 مدل embedding: {summary['embedding_model']}")
        print(f"   📁 دایرکتوری ایندکس: {self.index_dir}")
        
        print(f"\n📁 فایل‌های ایجاد شده:")
        for file_path in self.index_dir.glob("*"):
            size_mb = file_path.stat().st_size / (1024 * 1024)
            print(f"   📄 {file_path.name} ({size_mb:.2f} MB)")

def main():
    """تابع اصلی"""
    try:
        # پیکربندی
        config = {
            "documents_dir": "./documents",
            "index_dir": "./index_v3_advanced",
            "embedding_model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            "max_chunk_size": 800,
            "min_chunk_size": 150
        }
        
        # ایجاد ایندکس
        creator = AdvancedFAISSIndexCreator(**config)
        creator.create_advanced_index()
        
    except Exception as e:
        logger.error(f"خطا در اجرای برنامه: {e}")
        exit(1)

if __name__ == "__main__":
    main()