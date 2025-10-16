#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask Backend for University Rules RAG Chatbot
منطبق با ایندکس V4 بروز شده
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
from functools import lru_cache

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

# Import RAG system
from src.faiss_rag_v2 import UniversityRulesRAG, RAGResponse

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global RAG instance
rag_system = None

def initialize_rag():
    """Initialize RAG system with updated index"""
    global rag_system
    try:
        # Use the updated index directory
        index_dir = "./index_v4_upgraded"
        env_path = "./.env"
        
        logger.info(f"Initializing RAG system with index: {index_dir}")
        rag_system = UniversityRulesRAG(index_dir=index_dir, env_path=env_path)
        logger.info("✅ RAG system initialized successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Error initializing RAG system: {e}")
        return False

@app.route('/')
def index():
    """Serve main HTML page"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error serving index: {e}")
        return jsonify({"error": "Failed to load page"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    if rag_system is None:
        return jsonify({
            "status": "error",
            "message": "RAG system not initialized",
            "timestamp": datetime.now().isoformat()
        }), 503
    
    try:
        stats = rag_system.get_system_statistics()
        return jsonify({
            "status": "healthy",
            "rag_ready": True,
            "statistics": stats,
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint for answering questions"""
    
    if rag_system is None:
        return jsonify({
            "error": "RAG system not initialized",
            "answer": "سیستم هنوز آماده نیست. لطفا بعدا تلاش کنید."
        }), 503
    
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        user_message = data.get('message', '').strip()
        max_sources = data.get('max_sources', 5)
        
        if not user_message:
            return jsonify({"error": "Empty message"}), 400
        
        logger.info(f"Processing query: {user_message[:100]}")
        
        # Get answer from RAG system
        rag_response = rag_system.answer_question(user_message, top_k=max_sources)
        
        # Format response
        response_data = {
            "query": rag_response.query,
            "answer": rag_response.answer,
            "answer_plain_text": rag_response.answer_plain_text,
            "sources": [
                {
                    "title": source["document"],
                    "section": source.get("section", ""),
                    "category": source["category"],
                    "confidence": round(source["confidence"], 3),
                    "chunk_type": source.get("chunk_type", ""),
                    "article_numbers": source.get("article_numbers", []),
                    "note_numbers": source.get("note_numbers", []),
                    "has_table": source.get("has_table", False),
                    "has_list": source.get("has_list", False)
                }
                for source in rag_response.sources
            ],
            "metadata": {
                "query_type": rag_response.query_type,
                "category": rag_response.category,
                "confidence": round(rag_response.confidence, 3),
                "related_articles": rag_response.related_articles,
                "performance": {
                    "retrieval_time": round(rag_response.retrieval_time, 3),
                    "generation_time": round(rag_response.generation_time, 3),
                    "total_time": round(rag_response.total_time, 3)
                }
            },
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Query processed successfully in {rag_response.total_time:.2f}s")
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        return jsonify({
            "error": "Error processing request",
            "answer": f"خطا در پردازش درخواست: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """Get system statistics"""
    
    if rag_system is None:
        return jsonify({"error": "RAG system not initialized"}), 503
    
    try:
        stats = rag_system.get_system_statistics()
        return jsonify({
            "status": "success",
            "statistics": stats,
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/index-info', methods=['GET'])
def get_index_info():
    """Get detailed information about the index"""
    
    try:
        index_dir = Path("./index_v4_upgraded")
        
        # Read comprehensive summary
        summary_path = index_dir / "comprehensive_summary.json"
        if summary_path.exists():
            with open(summary_path, 'r', encoding='utf-8') as f:
                summary = json.load(f)
            return jsonify({
                "status": "success",
                "index_info": summary,
                "timestamp": datetime.now().isoformat()
            }), 200
        else:
            return jsonify({
                "error": "Index summary not found"
            }), 404
            
    except Exception as e:
        logger.error(f"Error getting index info: {e}")
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f"Server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Initialize RAG system
    if not initialize_rag():
        logger.error("Failed to initialize RAG system. Exiting.")
        exit(1)
    
    # Run Flask app
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 7000))
    
    logger.info(f"Starting Flask app on {host}:{port} (debug={debug_mode})")
    app.run(host=host, port=port, debug=debug_mode)