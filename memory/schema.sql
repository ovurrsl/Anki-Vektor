-- ================================================
-- Vector Hybrid AI Architecture - Memory Schema
-- SQLite + sqlite-vec (vec0) Episodic & Factual DB
-- ================================================

-- İlişkisel Hafıza ve Metadata Tablosu
CREATE TABLE IF NOT EXISTS memory_meta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fact TEXT NOT NULL,
    category TEXT DEFAULT 'general',
    tags TEXT DEFAULT '',
    source TEXT DEFAULT 'user_dialog',
    confidence REAL DEFAULT 1.0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Fallback (sqlite-vec uzantısı yoksa kullanılacak ham embedding tablosu)
CREATE TABLE IF NOT EXISTS memory_raw_vectors (
    id INTEGER PRIMARY KEY,
    embedding_blob BLOB NOT NULL,
    FOREIGN KEY(id) REFERENCES memory_meta(id) ON DELETE CASCADE
);

-- İndeksler
CREATE INDEX IF NOT EXISTS idx_memory_category ON memory_meta(category);
CREATE INDEX IF NOT EXISTS idx_memory_created_at ON memory_meta(created_at);
