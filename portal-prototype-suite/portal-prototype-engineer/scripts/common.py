"""Shared stdlib utilities; no project mutation."""
import hashlib, json
from pathlib import Path

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def files(root, suffixes=None):
    root=Path(root)
    if root.is_file(): return [root]
    skip={'.git','node_modules','dist','build','.venv','coverage','.next'}
    return sorted(p for p in root.rglob('*') if p.is_file() and not set(p.relative_to(root).parts)&skip and (suffixes is None or p.suffix.lower() in suffixes))

def emit(obj, output=None):
    s=json.dumps(obj,ensure_ascii=False,indent=2)
    if output: Path(output).write_text(s+'\n',encoding='utf-8')
    else: print(s)
