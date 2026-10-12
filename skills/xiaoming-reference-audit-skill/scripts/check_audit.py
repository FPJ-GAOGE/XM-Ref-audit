"""Validate audit completeness, not the truth of recorded evidence."""
import argparse
from datetime import date
import json
from pathlib import Path


def text(value):
    return isinstance(value, str) and bool(value.strip())


def unique_ids(values, label):
    if not isinstance(values, list) or any(not text(v) for v in values) or len(values) != len(set(values)):
        raise ValueError(f"{label}: expected unique nonempty string IDs")
    return set(values)


def check(data):
    problems = []
    if not text(data.get("document")):
        raise ValueError("document is required")
    inventory = data["inventory"]
    if type(inventory.get("complete")) is not bool:
        raise ValueError("inventory.complete must be boolean")
    if not inventory["complete"]:
        problems.append("Input inventory is incomplete")
    expected_refs = unique_ids(inventory["reference_ids"], "reference_ids")
    expected_occ = unique_ids(inventory["occurrence_ids"], "occurrence_ids")
    refs, occurrences = data["references"], data["occurrences"]
    if not isinstance(refs, list) or not isinstance(occurrences, list):
        raise ValueError("references and occurrences must be lists")
    actual_refs = unique_ids([r["id"] for r in refs], "references")
    actual_occ = unique_ids([o["id"] for o in occurrences], "occurrences")
    if actual_refs != expected_refs:
        problems.append("Reference inventory coverage mismatch")
    if actual_occ != expected_occ:
        problems.append("Citation occurrence coverage mismatch")
    if not expected_refs:
        problems.append("No references inventoried; cannot certify a reference audit")
    verified = supported = 0
    for ref in refs:
        before = len(problems)
        rid = ref["id"]
        for field in ("identity", "metadata"):
            if ref.get(field) not in ("verified", "unresolved", "conflict"):
                raise ValueError(f"{rid}: invalid {field}")
            if ref[field] != "verified":
                problems.append(f"{rid}: {field} {ref[field]}")
        status = ref.get("publication_status")
        if status not in ("checked_clear", "corrected", "retracted", "expression_of_concern", "unresolved"):
            raise ValueError(f"{rid}: invalid publication_status")
        if status not in ("checked_clear", "corrected") or not text(ref.get("status_note")):
            problems.append(f"{rid}: publication status unresolved or requires explicit review")
        evidence = ref.get("evidence")
        changes = ref.get("changes")
        if not isinstance(evidence, list) or not isinstance(changes, list):
            raise ValueError(f"{rid}: evidence and changes must be lists")
        coverage = set()
        has_primary = False
        urls = set()
        for item in evidence:
            if not text(item.get("url")) or not text(item.get("note")):
                raise ValueError(f"{rid}: evidence requires URL/path and note")
            checked = date.fromisoformat(item["accessed"])
            if checked > date.today():
                problems.append(f"{rid}: evidence access date is in the future")
            kind = item.get("kind")
            if kind not in ("primary", "registry", "catalog", "secondary"):
                raise ValueError(f"{rid}: invalid evidence kind")
            roles = item.get("supports")
            if not isinstance(roles, list) or not roles or any(r not in ("identity", "metadata", "status") for r in roles):
                raise ValueError(f"{rid}: invalid evidence supports")
            urls.add(item["url"])
            if kind != "secondary":
                coverage.update(roles)
            has_primary |= kind == "primary"
        if not has_primary or not {"identity", "metadata", "status"} <= coverage:
            problems.append(f"{rid}: missing primary or identity/metadata/status evidence")
        for change in changes:
            if not text(change.get("field")) or "before" not in change or "after" not in change:
                raise ValueError(f"{rid}: invalid change record")
            links = change.get("evidence_urls")
            if not isinstance(links, list) or not links or any(not text(u) for u in links):
                problems.append(f"{rid}: change lacks evidence")
            elif any(u not in urls for u in links) and not change.get("style_only", False):
                problems.append(f"{rid}: change evidence is absent from read evidence records")
        verified += len(problems) == before
    for occurrence in occurrences:
        before = len(problems)
        oid = occurrence["id"]
        if occurrence.get("reference_id") not in expected_refs:
            problems.append(f"{oid}: unknown reference_id")
        if occurrence.get("support") not in ("supported", "partial", "unsupported", "unresolved"):
            raise ValueError(f"{oid}: invalid support")
        if occurrence["support"] != "supported":
            problems.append(f"{oid}: claim support {occurrence['support']}")
        for field in ("location", "claim", "evidence_url", "source_locator", "note"):
            if not text(occurrence.get(field)):
                problems.append(f"{oid}: missing {field}")
        supported += len(problems) == before
    issues = data["issues"]
    if not isinstance(issues, list) or any(not text(i) for i in issues):
        raise ValueError("issues must be a list of nonempty strings")
    problems.extend(issues)
    return {"status": "records_complete" if not problems else "needs_review", "references_checked": verified,
            "references_expected": len(expected_refs), "occurrences_supported": supported,
            "occurrences_expected": len(expected_occ), "problems": problems,
            "limitation": "Checks recorded coverage only; does not authenticate sources or assess scientific truth."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        result = check(json.loads(args.input.read_text(encoding="utf-8-sig")))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["status"] == "records_complete" else 1
    except (ValueError, KeyError, TypeError, AttributeError, OSError) as exc:
        print(json.dumps({"status": "invalid_input", "error": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
