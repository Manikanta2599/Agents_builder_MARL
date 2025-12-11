import os
import json
import sqlite3
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
from uuid import uuid4
from datetime import datetime

class MemoryStore:
    def __init__(self, persist_dir: str = "./antigravity_data/memory"):
        self.persist_dir = persist_dir
        os.makedirs(persist_dir, exist_ok=True)
        
        # Initialize Vector DB (Chroma)
        self.chroma_client = chromadb.PersistentClient(path=os.path.join(persist_dir, "chroma"))
        self.collection = self.chroma_client.get_or_create_collection(
            name="antigravity_memory",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize Relational DB (SQLite)
        self.sql_conn = sqlite3.connect(os.path.join(persist_dir, "metadata.db"), check_same_thread=False)
        self.init_sql_tables()

    def init_sql_tables(self):
        cursor = self.sql_conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                start_time TEXT,
                status TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_items (
                id TEXT PRIMARY KEY,
                session_id TEXT,
                type TEXT,
                content TEXT,
                timestamp TEXT,
                embedding_id TEXT
            )
        ''')
        self.sql_conn.commit()

    def add_memory(self, content: str, type: str, session_id: str, metadata: Dict[str, Any] = None) -> str:
        memory_id = str(uuid4())
        timestamp = datetime.now().isoformat()
        
        if metadata is None:
            metadata = {}
        
        # Enhance metadata for vector search
        metadata.update({
            "type": type,
            "session_id": session_id,
            "timestamp": timestamp
        })

        # Add to Vector DB
        try:
            self.collection.add(
                documents=[content],
                metadatas=[metadata],
                ids=[memory_id]
            )
        except Exception as e:
            print(f"Vector DB Add Error: {e}")

        # Add to SQLite
        cursor = self.sql_conn.cursor()
        cursor.execute(
            "INSERT INTO memory_items (id, session_id, type, content, timestamp, embedding_id) VALUES (?, ?, ?, ?, ?, ?)",
            (memory_id, session_id, type, content, timestamp, memory_id)
        )
        self.sql_conn.commit()
        return memory_id

    def search_memory(self, query: str, type_filter: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        where_filter = {}
        if type_filter:
            where_filter["type"] = type_filter
            
        # ChromaDB search
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=limit,
                where=where_filter if where_filter else None
            )
        except Exception as e:
            print(f"Vector DB Search Error: {e}")
            return []
        
        # Format results
        formatted_results = []
        if results['ids']:
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    "id": results['ids'][0][i],
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if results['distances'] else None
                })
                
        return formatted_results

    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        cursor = self.sql_conn.cursor()
        cursor.execute(
            "SELECT id, type, content, timestamp FROM memory_items WHERE session_id = ? ORDER BY timestamp ASC",
            (session_id,)
        )
        rows = cursor.fetchall()
        return [
            {"id": r[0], "type": r[1], "content": r[2], "timestamp": r[3]}
            for r in rows
        ]

    def close(self):
        self.sql_conn.close()
