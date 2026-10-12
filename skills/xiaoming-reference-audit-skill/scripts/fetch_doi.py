"""Retrieve candidate BibTeX and CSL metadata from doi.org; never edit a manuscript."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request

MAX_BYTES = 1024 * 1024
FORMATS = (("source.bib", "application/x-bibtex"),
           ("source.csl.json", "application/vnd.citationstyles.csl+json"))


def normalize_doi(value):
    value = value.strip()
    if value.lower().startswith("doi:"):
        value = value[4:].strip()
    if value.lower().startswith(("https://", "http://")):
        parsed = urllib.parse.urlsplit(value)
        if parsed.netloc.lower() not in ("doi.org", "dx.doi.org") or parsed.query or parsed.fragment:
            raise ValueError("Use a bare DOI or a doi.org URL without query or fragment")
        value = urllib.parse.unquote(parsed.path.lstrip("/"))
    if not re.fullmatch(r"10\.\d{4,9}/[^\s]+", value) or any(ord(c) < 32 for c in value):
        raise ValueError("Invalid DOI syntax; provide the exact identifier without surrounding punctuation")
    return value


def validate_payload(payload, filename, doi):
    # Transport sanity checks only, not a BibTeX parser or identity verification.
    if filename.endswith(".bib"):
        if not re.match(r"\s*@[A-Za-z]+\s*[{(]", payload) or "<html" in payload.lower():
            raise ValueError("Response is not a recognizable BibTeX export")
    else:
        record = json.loads(payload)
        if not isinstance(record, dict) or not record.get("title"):
            raise ValueError("Response is not a CSL record with a title")
        returned = normalize_doi(str(record.get("DOI", "")))
        if returned.casefold() != doi.casefold():
            raise ValueError("Returned CSL DOI differs from the requested DOI")


def fetch(doi, output, timeout=20):
    doi = normalize_doi(doi)
    if not 1 <= timeout <= 60:
        raise ValueError("timeout must be between 1 and 60 seconds")
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    url = "https://doi.org/" + urllib.parse.quote(doi, safe="/")
    report = {"doi": doi, "identity_verified": False, "items": []}
    for filename, mime in FORMATS:
        item = {"file": filename, "request_url": url, "accept": mime,
                "accessed_at": datetime.now(timezone.utc).isoformat()}
        try:
            request = urllib.request.Request(url, headers={"Accept": mime,
                "User-Agent": "xiaoming-reference-audit-skill/1.0"})
            with urllib.request.urlopen(request, timeout=timeout) as response:
                item["response_url"] = response.geturl()
                item["content_type"] = response.headers.get("Content-Type", "")
                raw = response.read(MAX_BYTES + 1)
                if len(raw) > MAX_BYTES:
                    raise ValueError("Metadata response exceeds 1 MiB")
                payload = raw.decode(response.headers.get_content_charset() or "utf-8-sig")
            validate_payload(payload, filename, doi)
            (output / filename).write_text(payload, encoding="utf-8")
            item["status"] = "retrieved_unverified"
        except (urllib.error.URLError, OSError, ValueError, UnicodeError, LookupError) as exc:
            item.update(status="failed", error=str(exc))
        report["items"].append(item)
    count = sum(i["status"] == "retrieved_unverified" for i in report["items"])
    report["status"] = "retrieved_unverified" if count == len(FORMATS) else "incomplete"
    report["limitation"] = "Match the intended title, authors and version before merging; retrieval is not verification."
    (output / "retrieval.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("doi")
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--timeout", type=int, default=20)
    args = parser.parse_args()
    try:
        report = fetch(args.doi, args.out, args.timeout)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["status"] == "retrieved_unverified" else 1
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "invalid_input_or_output", "error": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
