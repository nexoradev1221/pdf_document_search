"""Read-only runtime diagnostics; no document indexing yet."""

import argparse
import json
import sqlite3

from pdf_document_search.config import load_config


def check_fts5() -> str:
    """Exercise actual full-text creation, insertion and matching in memory."""
    with sqlite3.connect(":memory:") as connection:
        connection.execute("CREATE VIRTUAL TABLE probe USING fts5(text)")
        connection.execute("INSERT INTO probe VALUES (?)", ("bearing repair",))
        result = connection.execute(
            "SELECT text FROM probe WHERE probe MATCH ?", ("bearing",)
        ).fetchone()
        if result != ("bearing repair",):
            raise RuntimeError("SQLite FTS5 probe failed")
    return sqlite3.sqlite_version


def main() -> None:
    parser = argparse.ArgumentParser(description="Диагностика локального поиска PDF")
    parser.add_argument("--config", help="Путь к файлу TOML")
    args = parser.parse_args()
    config = load_config(args.config)
    print(json.dumps({
        "sqlite_version": check_fts5(),
        "fts5": True,
        "host": config.host,
        "port": config.port,
        "data_dir": str(config.data_dir),
        "ocr_enabled": config.ocr_enabled,
        "semantic_enabled": config.semantic_enabled,
        "status": "Диагностика завершена. Индексация пока не реализована.",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
