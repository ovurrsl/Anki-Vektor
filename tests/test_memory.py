"""
Unit tests for Persistent Episodic Memory (MemoryManager & sqlite-vec).
"""

import os
import tempfile
import pytest
import numpy as np

from memory.db import MemoryManager


@pytest.fixture
def temp_db():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        path = f.name
    yield path
    if os.path.exists(path):
        os.remove(path)


def test_memory_storage_and_query(temp_db):
    dim = 8
    manager = MemoryManager(db_path=temp_db, vector_dim=dim)

    # Fact 1: coffee preference
    emb1 = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    id1 = manager.store_memory(
        fact="Kullanıcı kahvesini sade ve şekersiz sever.",
        embedding=emb1,
        category="preferences",
    )
    assert id1 > 0

    # Fact 2: car project
    emb2 = [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    id2 = manager.store_memory(
        fact="Scirocco far montajı ve CAN-bus kodlaması yapılıyor.",
        embedding=emb2,
        category="projects",
    )
    assert id2 > 0

    # Query closest to coffee (emb1)
    query_coffee = [0.95, 0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    results = manager.query_memories(query_coffee, limit=1)
    assert len(results) == 1
    assert results[0]["id"] == id1
    assert "kahve" in results[0]["fact"]

    # Recent memories test
    recent = manager.get_recent_memories(limit=10)
    assert len(recent) == 2

    # Delete test
    del_ok = manager.delete_memory(id1)
    assert del_ok is True
    assert len(manager.get_recent_memories()) == 1


def test_dimension_mismatch(temp_db):
    manager = MemoryManager(db_path=temp_db, vector_dim=8)
    with pytest.raises(ValueError):
        manager.store_memory("Invalid dim", [1.0, 2.0])
