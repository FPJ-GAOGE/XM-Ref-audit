"""Build a deterministic portable skill ZIP for Claude and other skill hosts."""
import argparse
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAME = "xm-ref-audit"


def build(output):
    source = ROOT / "skills" / NAME
    # Only runtime instructions and helpers; no host UI metadata or personal files.
    files = [source / "SKILL.md"]
    for folder, extension in (("references", "*.md"), ("scripts", "*.py")):
        files.extend(sorted((source / folder).glob(extension)))
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            name = f"{NAME}/{path.relative_to(source).as_posix()}"
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            content = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
            archive.writestr(info, content.encode("utf-8"))
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist" / f"{NAME}.zip")
    args = parser.parse_args()
    print(build(args.output))
