#!/usr/bin/env python3
"""Finaliza el repositorio Kodi: fija la URL de GitHub en el addon del repositorio y reconstruye
addons.xml, md5 y los ZIP. Uso:  python3 finalize_repo.py <usuario> <repo> [rama]"""
import hashlib, sys, zipfile
from pathlib import Path
user, repo = sys.argv[1], sys.argv[2]
branch = sys.argv[3] if len(sys.argv) > 3 else "main"
subpath = sys.argv[4].strip("/") if len(sys.argv) > 4 and sys.argv[4].strip("/") else ""
base = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/" + (f"{subpath}/" if subpath else "")
root = Path(__file__).resolve().parent
rid = "repository.iptv.flowproxy"
ax = root / rid / "addon.xml"
t = ax.read_text(encoding="utf-8")
import re
t = re.sub(r"https://raw\.githubusercontent\.com/[^<]+/", base, t)
ax.write_text(t, encoding="utf-8")
# rebuild ZIP del repositorio
z = root / rid / f"{rid}-1.0.0.zip"
with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as fh:
    fh.write(ax, f"{rid}/addon.xml")
# addons.xml + md5
parts = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<addons>\n']
for d in sorted(root.iterdir()):
    a = d / "addon.xml"
    if d.is_dir() and a.is_file():
        parts.append(a.read_text(encoding="utf-8").strip() + "\n")
parts.append("</addons>\n")
xml = "".join(parts)
(root / "addons.xml").write_text(xml, encoding="utf-8")
(root / "addons.xml.md5").write_text(hashlib.md5(xml.encode()).hexdigest(), encoding="utf-8")
print("OK. Base:", base)
