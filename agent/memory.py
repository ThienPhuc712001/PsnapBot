"""
Memory System for PSnapBOT - Local Persistent Development Agent
Handles SQLite database operations for sessions, build history, and project knowledge
"""
import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
from config import DATABASE_PATH, SIMILARITY_THRESHOLD


class MemorySystem:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize the SQLite database with required tables"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_input TEXT NOT NULL,
                    agent_response TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Build history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS build_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    error_text TEXT NOT NULL,
                    fix_applied TEXT NOT NULL,
                    related_files TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Project knowledge table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS project_knowledge (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT NOT NULL UNIQUE,
                    value TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def save_session(self, user_input: str, agent_response: str) -> int:
        """Save a user session interaction"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sessions (user_input, agent_response) VALUES (?, ?)",
                (user_input, agent_response)
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_recent_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent session history"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_input, agent_response, timestamp FROM sessions ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )
            return [
                {
                    "user_input": row[0],
                    "agent_response": row[1],
                    "timestamp": row[2]
                }
                for row in cursor.fetchall()
            ]
    
    def save_build_fix(self, error_text: str, fix_applied: str, related_files: List[str] = None) -> int:
        """Save a build error and its fix"""
        files_json = json.dumps(related_files) if related_files else None
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO build_history (error_text, fix_applied, related_files) VALUES (?, ?, ?)",
                (error_text, fix_applied, files_json)
            )
            conn.commit()
            return cursor.lastrowid
    
    def find_similar_build_errors(self, error_text: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Find similar build errors from history"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT error_text, fix_applied, related_files, timestamp FROM build_history ORDER BY timestamp DESC"
            )
            
            similar_errors = []
            for row in cursor.fetchall():
                stored_error, fix, files_json, timestamp = row
                similarity = self._calculate_similarity(error_text, stored_error)
                if similarity >= SIMILARITY_THRESHOLD:
                    related_files = json.loads(files_json) if files_json else []
                    similar_errors.append({
                        "error_text": stored_error,
                        "fix_applied": fix,
                        "related_files": related_files,
                        "timestamp": timestamp,
                        "similarity": similarity
                    })
            
            return sorted(similar_errors, key=lambda x: x["similarity"], reverse=True)[:limit]
    
    def save_knowledge(self, key: str, value: str) -> int:
        """Save project knowledge"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO project_knowledge (key, value) VALUES (?, ?)",
                (key, value)
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_knowledge(self, key: str) -> Optional[str]:
        """Get specific knowledge by key"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM project_knowledge WHERE key = ?", (key,))
            result = cursor.fetchone()
            return result[0] if result else None
    
    def get_all_knowledge(self) -> Dict[str, str]:
        """Get all project knowledge"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT key, value FROM project_knowledge")
            return {row[0]: row[1] for row in cursor.fetchall()}
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two text strings using simple word overlap"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def cleanup_old_sessions(self, days: int = 30):
        """Clean up old session data"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM sessions WHERE timestamp < datetime('now', '-{} days')".format(days)
            )
            conn.commit()