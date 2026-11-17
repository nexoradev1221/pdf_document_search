import hashlib
import json
from pathlib import Path

import pymupdf
import pytest

from scripts.generate_corpus import generate

CORPUS = Path(__file__).resolve().parents[1] / "sample_data" / "corpus"


def test_manifest_documents_and_exact_pages():
    manifest = json.loads((CORPUS / "manifest.json").read_text(encoding="utf-8"))
    assert len(manifest["documents"]) == 15
    assert len(list(CORPUS.rglob("*.pdf"))) == 15
    for record in manifest["documents"]:
        path = CORPUS / record["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"]
        with pymupdf.open(path) as doc:
            assert doc.page_count == 3
            assert doc.metadata["author"] == "PDF Document Search synthetic corpus"
            for expected, page in zip(record["pages"], doc, strict=True):
                text = page.get_text()
                if expected["image_only"]:
                    assert not text.strip()
                    assert page.get_images()
                else:
                    assert text.strip()
                    assert (record["reference"]["code"] in text) == (
                        expected["page"] == record["reference"]["page"]
                    )
            if "russian" not in record["path"] and "учебное" not in record["path"]:
                continue
            assert "перегрев подшипника" in doc[1].get_text()


def test_generator_is_reproducible_and_preserves_existing_output(tmp_path):
    first, second = tmp_path / "first", tmp_path / "second"
    manifest = generate(first)
    assert generate(second) == manifest
    for path in first.rglob("*"):
        if path.is_file():
            assert path.read_bytes() == (second / path.relative_to(first)).read_bytes()
    sentinel = first / "user.txt"
    sentinel.write_text("preserve me", encoding="utf-8")
    with pytest.raises(FileExistsError):
        generate(first)
    assert sentinel.read_text(encoding="utf-8") == "preserve me"


def test_corrupt_pdf_is_rejected():
    fixture = Path(__file__).parent / "fixtures" / "corrupt.pdf"
    with pytest.raises(pymupdf.FileDataError):
        pymupdf.open(fixture)
