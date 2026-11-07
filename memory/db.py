"""
Memory Manager Module - SQLite + sqlite-vec (vec0) Episodic & Factual Storage.

Provides vector search and structured factual memory for Anki Vector.
Supports both native sqlite-vec C-extension and pure Python/NumPy cosine fallback.
"""

from __future__ import annotations

import json
import logging
import sqlite3
import struct
from pathlib import Path
from typing import Any, List, Optional, Tuple

import numpy as np

logger = logging.getLogger("vector.memory")

try:
    import sqlite_vec
    SQLITE_VEC_AVAILABLE = True
except ImportError:
    SQLITE_VEC_AVAILABLE = False
    logger.warning("sqlite-vec package not installed. Fallback cosine similarity will be used.")


def serialize_float32(vector: List[float] | np.ndarray) -> bytes:
    """Serializes a float vector into binary representation for sqlite-vec or storage."""
    if isinstance(vector, np.ndarray):
        vector = vector.astype(np.float32).tolist()
    return struct.pack(f"{len(vector)}f", *vector)


def deserialize_float32(blob: bytes) -> np.ndarray:
    """Deserializes binary blob into float numpy array."""
    count = len(blob) // 4
    return np.array(struct.unpack(f"{count}f", blob), dtype=np.float32)


class MemoryManager:
    """
    Episodic and factual memory database manager for Vector.
    Handles semantic embedding search and relational metadata storage.
    """

    def __init__(self, db_path: str = "vector_memory.db", vector_dim: int = 768):
        self.db_path = db_path
        self.vector_dim = vector_dim
        self.use_vec_extension = False
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        if SQLITE_VEC_AVAILABLE:
            try:
                conn.enable_load_extension(True)
                sqlite_vec.load(conn)
                conn.enable_load_extension(False)
                self.use_vec_extension = True
            except Exception as e:
                logger.warning(f"Failed to load sqlite-vec extension: {e}. Using numpy fallback.")
                self.use_vec_extension = False
        return conn

    def _init_db(self) -> None:
        """Initializes database tables and vec0 virtual table if available."""
        with self._get_connection() as conn:
            # 1. Standart metadata tablosu
            conn.execute("""
            CREATE TABLE IF NOT EXISTS memory_meta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fact TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                tags TEXT DEFAULT '',
                source TEXT DEFAULT 'user_dialog',
                confidence REAL DEFAULT 1.0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # 2. Ham vektör tablosu (fallback için)
            conn.execute("""
            CREATE TABLE IF NOT EXISTS memory_raw_vectors (
                id INTEGER PRIMARY KEY,
                embedding_blob BLOB NOT NULL,
                FOREIGN KEY(id) REFERENCES memory_meta(id) ON DELETE CASCADE
            );
            """)

            # 3. sqlite-vec vec0 sanal tablosu
            if self.use_vec_extension:
                try:
                    conn.execute(f"""
                    CREATE VIRTUAL TABLE IF NOT EXISTS vec_memories USING vec0(
                        id INTEGER PRIMARY KEY,
                        embedding float[{self.vector_dim}]
                    );
                    """)
                    logger.info(f"Initialized sqlite-vec vec0 virtual table (dim={self.vector_dim})")
                except Exception as e:
                    logger.warning(f"Could not create vec0 virtual table: {e}. Fallback will be active.")
                    self.use_vec_extension = False

    def store_memory(
        self,
        fact: str,
        embedding: List[float] | np.ndarray,
        category: str = "general",
        tags: str = "",
        source: str = "user_dialog",
        confidence: float = 1.0,
    ) -> int:
        """
        Stores a new fact and its embedding into long-term memory.
        Returns the created memory ID.
        """
        if len(embedding) != self.vector_dim:
            raise ValueError(
                f"Embedding dimension mismatch: expected {self.vector_dim}, got {len(embedding)}"
            )

        binary_vector = serialize_float32(embedding)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO memory_meta (fact, category, tags, source, confidence)
                VALUES (?, ?, ?, ?, ?)
                """,
                (fact, category, tags, source, confidence),
            )
            memory_id = cursor.lastrowid

            if memory_id is None:
                raise RuntimeError("Failed to insert memory metadata")

            # Always write to raw_vectors for fallback persistence
            cursor.execute(
                "INSERT INTO memory_raw_vectors (id, embedding_blob) VALUES (?, ?)",
                (memory_id, binary_vector),
            )

            # If sqlite-vec is active, write to vec_memories
            if self.use_vec_extension:
                try:
                    cursor.execute(
                        "INSERT INTO vec_memories (id, embedding) VALUES (?, ?)",
                        (memory_id, binary_vector),
                    )
                except Exception as e:
                    logger.error(f"Error inserting into vec_memories: {e}")

            conn.commit()
            logger.debug(f"Saved memory id={memory_id}: '{fact[:40]}...'")
            return memory_id

    def query_memories(
        self,
        query_embedding: List[float] | np.ndarray,
        limit: int = 5,
        category: Optional[str] = None,
    ) -> List[dict[str, Any]]:
        """
        Retrieves the top-k nearest memories based on cosine/Euclidean similarity.
        """
        if len(query_embedding) != self.vector_dim:
            raise ValueError(
                f"Query embedding dimension mismatch: expected {self.vector_dim}, got {len(query_embedding)}"
            )

        binary_query = serialize_float32(query_embedding)

        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Attempt 1: sqlite-vec vec0 query
            if self.use_vec_extension:
                try:
                    if category:
                        sql = """
                        SELECT m.id, m.fact, m.category, m.created_at, v.distance
                        FROM vec_memories v
                        JOIN memory_meta m ON m.id = v.id
                        WHERE v.embedding MATCH ? AND m.category = ?
                        ORDER BY v.distance ASC
                        LIMIT ?
                        """
                        cursor.execute(sql, (binary_query, category, limit))
                    else:
                        sql = """
                        SELECT m.id, m.fact, m.category, m.created_at, v.distance
                        FROM vec_memories v
                        JOIN memory_meta m ON m.id = v.id
                        WHERE v.embedding MATCH ?
                        ORDER BY v.distance ASC
                        LIMIT ?
                        """
                        cursor.execute(sql, (binary_query, limit))

                    rows = cursor.fetchall()
                    return [
                        {
                            "id": r["id"],
                            "fact": r["fact"],
                            "category": r["category"],
                            "created_at": r["created_at"],
                            "score": float(r["distance"]),
                        }
                        for r in rows
                    ]
                except Exception as e:
                    logger.warning(f"vec0 query failed: {e}. Executing numpy fallback search.")

            # Fallback: In-memory cosine similarity via numpy
            sql = """
            SELECT m.id, m.fact, m.category, m.created_at, r.embedding_blob
            FROM memory_meta m
            JOIN memory_raw_vectors r ON m.id = r.id
            """
            params: list[Any] = []
            if category:
                sql += " WHERE m.category = ?"
                params.append(category)

            cursor.execute(sql, params)
            rows = cursor.fetchall()

            if not rows:
                return []

            q_vec = np.array(query_embedding, dtype=np.float32)
            q_norm = np.linalg.norm(q_vec)
            if q_norm == 0:
                q_norm = 1.0

            scored = []
            for r in rows:
                v = deserialize_float32(r["embedding_blob"])
                v_norm = np.linalg.norm(v)
                if v_norm == 0:
                    v_norm = 1.0
                cosine_sim = float(np.dot(q_vec, v) / (q_norm * v_norm))
                # Distance = 1 - cosine similarity
                distance = 1.0 - cosine_sim
                scored.append(
                    {
                        "id": r["id"],
                        "fact": r["fact"],
                        "category": r["category"],
                        "created_at": r["created_at"],
                        "score": distance,
                    }
                )

            scored.sort(key=lambda x: x["score"])
            return scored[:limit]

    def get_recent_memories(self, limit: int = 10, category: Optional[str] = None) -> List[dict[str, Any]]:
        """Returns the most recent memories sorted chronologically."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if category:
                cursor.execute(
                    """
                    SELECT id, fact, category, tags, created_at
                    FROM memory_meta
                    WHERE category = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                    """,
                    (category, limit),
                )
            else:
                cursor.execute(
                    """
                    SELECT id, fact, category, tags, created_at
                    FROM memory_meta
                    ORDER BY created_at DESC
                    LIMIT ?
                    """,
                    (limit,),
                )
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def delete_memory(self, memory_id: int) -> bool:
        """Deletes a memory by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM memory_meta WHERE id = ?", (memory_id,))
            cursor.execute("DELETE FROM memory_raw_vectors WHERE id = ?", (memory_id,))
            if self.use_vec_extension:
                try:
                    cursor.execute("DELETE FROM vec_memories WHERE id = ?", (memory_id,))
                except Exception:
                    pass
            conn.commit()
            return cursor.rowcount > 0
