"""Rebuild the thermal map dashboard and the STEP model.

Run from anywhere:  python dashboard/build.py

It regenerates the geometry, checks the STEP file, assembles the page, then copies
the two results to where the repository keeps them:
    docs/dashboard/index.html   (served by GitHub Pages)
    cad/Greenhouse1.step
"""
import shutil
import subprocess
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
root = here.parent
out = here / "out"
out.mkdir(exist_ok=True)


def run(*args):
    subprocess.run([sys.executable, *args], cwd=here, check=True)


run("build_model.py", "out")
run("verify_step.py", "out/greenhouse1.step")
run("build_page.py")

(root / "docs" / "dashboard").mkdir(parents=True, exist_ok=True)
(root / "cad").mkdir(exist_ok=True)
shutil.copyfile(out / "index.html", root / "docs" / "dashboard" / "index.html")
shutil.copyfile(out / "greenhouse1.step", root / "cad" / "Greenhouse1.step")
print("Wrote docs/dashboard/index.html and cad/Greenhouse1.step")
