"""Synthetic fixtures test decision gates, not real citation verification."""
import copy
from datetime import date
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / "skills" / "xm-ref-audit" / "scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


select = load("select_mode").select
check = load("check_audit").check


class ModeTests(unittest.TestCase):
    def setUp(self):
        self.data = {"page_limit": 8, "references_counted": True,
                     "measurements": {"minimal": 7, "regular": 8, "detailed": 9}}

    def test_best_fit(self):
        self.assertEqual(select(self.data)["mode"], "regular")

    def test_missing_measurement_is_not_estimated(self):
        del self.data["measurements"]["detailed"]
        self.assertEqual(select(self.data)["status"], "needs_measurement")

    def test_explicit_mode_is_not_silently_changed(self):
        self.data["requested_mode"] = "detailed"
        self.assertEqual(select(self.data)["status"], "requested_over_budget")

    def test_excluded_references_cannot_fix_body(self):
        self.data.update(references_counted=False, body_pages=9)
        self.assertEqual(select(self.data)["status"], "body_over_budget")

    def test_style_conflict(self):
        self.data.update(requested_mode="minimal", allowed_modes=["regular"])
        self.assertEqual(select(self.data)["status"], "style_conflict")

    def test_all_over_budget(self):
        self.data["page_limit"] = 6
        self.assertEqual(select(self.data)["status"], "over_budget")

    def test_unknown_scope(self):
        self.data["references_counted"] = None
        self.assertEqual(select(self.data)["status"], "needs_scope")

    def test_boolean_is_not_page_count(self):
        self.data["page_limit"] = True
        with self.assertRaises(ValueError):
            select(self.data)


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.data = {"document": "synthetic-fixture", "inventory": {"complete": True,
                     "reference_ids": ["r1"], "occurrence_ids": ["c1"]},
                     "references": [{"id": "r1", "identity": "verified", "metadata": "verified",
                         "publication_status": "checked_clear", "status_note": "Synthetic test only",
                         "evidence": [{"url": "https://example.org/synthetic", "accessed": date.today().isoformat(),
                             "kind": "primary", "supports": ["identity", "metadata", "status"],
                             "note": "Synthetic fixture; not a real publication"}], "changes": []}],
                     "occurrences": [{"id": "c1", "reference_id": "r1", "location": "paragraph 1",
                         "claim": "Synthetic assertion", "support": "supported", "evidence_url": "https://example.org/synthetic",
                         "source_locator": "section 1", "note": "Synthetic fixture"}], "issues": []}

    def test_complete_records(self):
        self.assertEqual(check(self.data)["status"], "records_complete")

    def test_doi_existence_alone_fails(self):
        self.data["references"][0]["evidence"][0]["supports"] = ["identity"]
        self.assertEqual(check(self.data)["status"], "needs_review")

    def test_partial_claim_fails(self):
        self.data["occurrences"][0]["support"] = "partial"
        self.assertEqual(check(self.data)["status"], "needs_review")

    def test_omitted_occurrence_fails(self):
        self.data["occurrences"] = []
        self.assertEqual(check(self.data)["status"], "needs_review")

    def test_retracted_fails(self):
        self.data["references"][0]["publication_status"] = "retracted"
        self.assertEqual(check(self.data)["status"], "needs_review")

    def test_duplicate_ids_rejected(self):
        self.data["references"].append(copy.deepcopy(self.data["references"][0]))
        with self.assertRaises(ValueError):
            check(self.data)

    def test_unread_change_evidence_fails(self):
        self.data["references"][0]["changes"] = [{"field": "year", "before": "2020", "after": "2021",
            "evidence_urls": ["https://example.org/unread"]}]
        self.assertEqual(check(self.data)["status"], "needs_review")

    def test_incomplete_input_fails(self):
        self.data["inventory"]["complete"] = False
        self.assertEqual(check(self.data)["status"], "needs_review")


if __name__ == "__main__":
    unittest.main()
