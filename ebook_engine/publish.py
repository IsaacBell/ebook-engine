#!/usr/bin/env python3
"""Publish ebook-engine to PyPI. Run under infisical: infisical run --env=dev -- python3 apps/ebook-engine/ebook_engine/publish.py"""
import os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.environ.setdefault("TWINE_USERNAME", "__token__")

# Build with uv (python-managed, PEP 668)
subprocess.run(["uv", "pip", "install", "-q", "build", "twine"], check=True)
subprocess.run([sys.executable, "-m", "build", "--outdir", str(ROOT / "dist")], cwd=ROOT, check=True)

# Upload
wheels = list((ROOT / "dist").glob("*.whl"))
tars = list((ROOT / "dist").glob("*.tar.gz"))
files = [str(f) for f in wheels + tars]
subprocess.run([sys.executable, "-m", "twine", "upload", *files], check=True)

print(f"Published {len(files)} package(s)")
