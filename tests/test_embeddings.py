from agentic_edu.modules.embeddings import DatabaseEmbedder
import pytest


def test_add_table():
    db_embedder = DatabaseEmbedder()
    db_embedder.add_table("table1", "This is a test table")
    assert "table1" in db_embedder.map_name_to_embeddings
    assert "table1" in db_embedder.map_name_to_table_def


def test_compute_embeddings():
    db_embedder = DatabaseEmbedder()
    embeddings = db_embedder.compute_embeddings("This is a test sentence")
    assert embeddings.shape == (
        1,
        768,
    )  # the BERT model returns embeddings of shape (batch_size, embedding_size)


def test_get_similar_table_names_via_word_match():
    db_embedder = DatabaseEmbedder()
    db_embedder.add_table("table1", "This is a test table")
    tables = db_embedder.get_similar_table_names_via_word_match("table1")
    assert "table1" in tables


def test_get_similar_tables_via_embeddings():
    db_embedder = DatabaseEmbedder()
    db_embedder.add_table("table1", "This is a test table")
    tables = db_embedder.get_similar_tables_via_embeddings("test", 1)
    assert "table1" in tables


def test_get_similar_tables():
    db_embedder = DatabaseEmbedder()
    db_embedder.add_table("table1", "This is a test table")
    tables = db_embedder.get_similar_tables("test", 1)
    assert "table1" in tables


def test_get_table_definitions_from_names():
    db_embedder = DatabaseEmbedder()
    db_embedder.add_table("table1", "This is a test table")
    table_defs = db_embedder.get_table_definitions_from_names(["table1"])
    assert "This is a test table" in table_defs


def test_get_table_definitions_from_names_nonexistent():
    db_embedder = DatabaseEmbedder()
    db_embedder.add_table("table1", "This is a test table")
    with pytest.raises(KeyError):
        db_embedder.get_table_definitions_from_names(["nonexistent"])
