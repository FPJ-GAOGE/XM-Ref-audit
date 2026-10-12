import importlib.util
import json
from email.message import Message
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("fetch_doi", ROOT / "skills/xm-ref-audit/scripts/fetch_doi.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
DOI = "10.5555/synthetic-test"


class Response:
    def __init__(self, data):
        self.data = data.encode("utf-8")
        self.headers = Message()
        self.headers["Content-Type"] = "text/plain; charset=utf-8"
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False
    def read(self, limit):
        return self.data[:limit]
    def geturl(self):
        return "https://example.org/synthetic-metadata"


class FetchTests(unittest.TestCase):
    def test_doi_url_normalization(self):
        self.assertEqual(module.normalize_doi("https://doi.org/10.5555/synthetic-test"), DOI)
        self.assertEqual(module.normalize_doi("doi: " + DOI), DOI)

    def test_non_doi_url_rejected(self):
        with self.assertRaises(ValueError):
            module.normalize_doi("https://example.org/10.5555/synthetic-test")

    def test_wrong_doi_record_rejected(self):
        with self.assertRaises(ValueError):
            module.validate_payload(json.dumps({"DOI":"10.5555/other", "title":"Synthetic"}), "source.csl.json", DOI)

    def test_html_is_not_bibtex(self):
        with self.assertRaises(ValueError):
            module.validate_payload("<html>Login</html>", "source.bib", DOI)

    def test_success_never_claims_verified_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "new"
            responses = [Response("@article{synthetic,title={Synthetic}}"),
                         Response(json.dumps({"DOI":DOI,"title":"Synthetic"}))]
            with patch.object(module.urllib.request, "urlopen", side_effect=responses) as request:
                report = module.fetch(DOI, target)
            self.assertEqual(report["status"], "retrieved_unverified")
            self.assertFalse(report["identity_verified"])
            self.assertTrue((target / "source.bib").exists())
            self.assertEqual(request.call_args_list[0].args[0].get_header("Accept"), "application/x-bibtex")

    def test_partial_failure_preserves_bibtex(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "new"
            with patch.object(module.urllib.request, "urlopen", side_effect=[Response("@book{synthetic,title={Synthetic}}"), urllib.error.URLError("offline")]):
                report = module.fetch(DOI, target)
            self.assertEqual(report["status"], "incomplete")
            self.assertTrue((target / "source.bib").exists())
            self.assertEqual(report["items"][1]["status"], "failed")

    def test_existing_evidence_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(FileExistsError):
                module.fetch(DOI, directory)


if __name__ == "__main__":
    unittest.main()
