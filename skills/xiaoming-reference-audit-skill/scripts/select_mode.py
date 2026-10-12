"""Select display density from measured pages; never estimate pagination."""
import argparse
import json
from pathlib import Path

MODES = ("minimal", "regular", "detailed")


def positive_int(value):
    return type(value) is int and value > 0


def select(data):
    requested = data.get("requested_mode", "auto")
    allowed = data.get("allowed_modes", list(MODES))
    limit = data.get("page_limit")
    counted = data.get("references_counted")
    measured = data.get("measurements", {})
    body = data.get("body_pages")
    if requested not in (*MODES, "auto"):
        raise ValueError("Invalid requested_mode")
    if not isinstance(allowed, list) or not allowed or any(m not in MODES for m in allowed) or len(set(allowed)) != len(allowed):
        raise ValueError("allowed_modes must contain unique known modes")
    if limit is not None and not positive_int(limit):
        raise ValueError("page_limit must be a positive integer or null")
    if counted is not None and type(counted) is not bool:
        raise ValueError("references_counted must be boolean or null")
    if not isinstance(measured, dict) or any(m not in MODES or not positive_int(p) for m, p in measured.items()):
        raise ValueError("measurements must contain positive integer page counts")
    if body is not None and not positive_int(body):
        raise ValueError("body_pages must be a positive integer")
    mode = requested if requested != "auto" else ("regular" if "regular" in allowed else next(m for m in reversed(MODES) if m in allowed))
    if mode not in allowed:
        return {"status": "style_conflict", "mode": mode}
    if limit is None:
        return {"status": "selected", "mode": mode, "reason": "No page limit supplied"}
    if counted is None:
        return {"status": "needs_scope", "provisional_mode": mode}
    if counted is False:
        if body is None:
            return {"status": "needs_measurement", "provisional_mode": mode, "needed": ["body_pages"]}
        return {"status": "selected" if body <= limit else "body_over_budget", "mode": mode, "body_pages": body, "over_by": max(0, body - limit)}
    if requested != "auto":
        if mode not in measured:
            return {"status": "needs_measurement", "provisional_mode": mode, "needed": [mode]}
        return {"status": "selected" if measured[mode] <= limit else "requested_over_budget", "mode": mode, "pages": measured[mode], "over_by": max(0, measured[mode] - limit)}
    for mode in reversed(MODES):
        if mode not in allowed:
            continue
        if mode not in measured:
            return {"status": "needs_measurement", "needed": [mode]}
        if measured[mode] <= limit:
            return {"status": "selected", "mode": mode, "pages": measured[mode]}
    mode = next(m for m in MODES if m in allowed)
    return {"status": "over_budget", "mode": mode, "pages": measured[mode], "over_by": measured[mode] - limit}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        result = select(json.loads(args.input.read_text(encoding="utf-8-sig")))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["status"] == "selected" else 1
    except (ValueError, OSError, TypeError, AttributeError) as exc:
        print(json.dumps({"status": "invalid_input", "error": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
