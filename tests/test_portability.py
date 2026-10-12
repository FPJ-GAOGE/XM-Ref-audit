"""Validate the portable artifact without pretending to run a Claude session."""
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("package_skill", ROOT / "tools/package_skill.py")
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


class PortabilityTests(unittest.TestCase):
    def test_common_frontmatter(self):
        content = (ROOT / "skills" / package.NAME / "SKILL.md").read_text(encoding="utf-8")
        metadata = content.split("---", 2)[1]
        fields = dict(line.split(":", 1) for line in metadata.strip().splitlines())
        self.assertEqual(set(fields), {"name", "description"})
        self.assertEqual(fields["name"].strip(), package.NAME)
        self.assertRegex(package.NAME, r"^[a-z0-9-]{1,64}$")
        self.assertLessEqual(len(fields["description"].strip()), 200)

    def test_archive_layout_and_relative_links(self):
        with tempfile.TemporaryDirectory() as folder:
            archive = package.build(Path(folder) / "skill.zip")
            with zipfile.ZipFile(archive) as z:
                names = set(z.namelist())
                self.assertIn(f"{package.NAME}/SKILL.md", names)
                self.assertTrue(all(n.startswith(package.NAME + "/") for n in names))
                self.assertFalse(any("agents/" in n or "__pycache__" in n for n in names))
                for name in names:
                    if not name.endswith(".md"):
                        continue
                    for link in re.findall(r"\]\(([^)]+)\)", z.read(name).decode("utf-8")):
                        if not link.startswith(("https:", "http:", "#")):
                            target = (Path(name).parent / link.split("#")[0]).as_posix()
                            self.assertIn(target, names)

    def test_helpers_run_outside_skill_directory(self):
        with tempfile.TemporaryDirectory(prefix="skill-portability-") as folder:
            root = Path(folder)
            unpacked = root / "路径 with spaces"
            with zipfile.ZipFile(package.build(root / "skill.zip")) as z:
                z.extractall(unpacked)
            scripts = unpacked / package.NAME / "scripts"
            measurements = root / "measurements.json"
            measurements.write_text(json.dumps({"page_limit": 8, "references_counted": True,
                "measurements": {"minimal": 7, "regular": 8, "detailed": 9}}), encoding="utf-8")
            result = subprocess.run([sys.executable, str(scripts / "select_mode.py"), str(measurements)],
                                    cwd=root, capture_output=True, text=True, check=True)
            self.assertEqual(json.loads(result.stdout)["mode"], "regular")
            invalid = root / "audit.json"
            invalid.write_text("{}", encoding="utf-8")
            result = subprocess.run([sys.executable, str(scripts / "check_audit.py"), str(invalid)],
                                    cwd=root, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["status"], "invalid_input")

    def test_build_is_reproducible(self):
        with tempfile.TemporaryDirectory() as folder:
            first = package.build(Path(folder) / "first.zip")
            second = package.build(Path(folder) / "second.zip")
            self.assertEqual(first.read_bytes(), second.read_bytes())


if __name__ == "__main__":
    unittest.main()
