#!/usr/bin/env python3
"""Read-only HTML static inventory. Exit 2 on deterministic HTML ID/parser failures in --strict mode.
This tool cannot verify runtime interactions, business contracts, or visual quality.
"""
import argparse
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import shutil
import subprocess

class Inventory(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = Counter()
        self.scripts = []
        self.styles = 0
        self.inline_handlers = 0
        self.external = []
        self.inline_js = []
        self.script_types = []
        self._current_script_type = ''
        self._inside_script = False
        self._script_data = []
        self._script_external = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids[a['id']] += 1
        self.inline_handlers += sum(k.lower().startswith('on') for k, _ in attrs)
        if tag == 'script':
            self.scripts.append(a)
            self._inside_script = True
            self._current_script_type = a.get('type', '').strip().lower()
            self._script_external = bool(a.get('src'))
            self._script_data = []
            if a.get('src'):
                self.external.append(a['src'])
        elif tag == 'style':
            self.styles += 1
        elif tag == 'link' and a.get('href'):
            self.external.append(a['href'])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag == 'script':
            self.handle_endtag(tag)

    def handle_data(self, data):
        if self._inside_script:
            self._script_data.append(data)

    def handle_endtag(self, tag):
        if tag == 'script' and self._inside_script:
            if not self._script_external:
                self.inline_js.append(''.join(self._script_data))
                self.script_types.append(self._current_script_type)
            self._inside_script = False
            self._script_data = []

def check_js_syntax(scripts, script_types, node_path=None):
    node = node_path or shutil.which('node')
    if not node:
        return {'status':'NOT_RUN','reason':'Node.js not found','checked':0,'errors':[]}
    errors=[];checked=0
    for i,(js,typ) in enumerate(zip(scripts,script_types),start=1):
        if typ not in ('','text/javascript','application/javascript','module') or not js.strip():
            continue
        # Node --check reads from stdin, module mode uses --input-type=module.
        cmd=[node, '--input-type=module' if typ=='module' else '--input-type=commonjs','--check']
        try:
            result=subprocess.run(cmd,input=js,text=True,capture_output=True,timeout=8)
            checked+=1
            if result.returncode:
                errors.append({'script_index':i,'error':(result.stderr or result.stdout)[-1200:]})
        except (OSError,subprocess.TimeoutExpired) as exc:
            errors.append({'script_index':i,'error':str(exc)})
    return {'status':'FAIL' if errors else 'PASS','checked':checked,'errors':errors}

def audit(source, file_label='<memory>', check_js=False, node_path=None):
    p = Inventory()
    errors = []
    try:
        p.feed(source)
        p.close()
    except Exception as exc:
        errors.append(f'HTML parser exception: {exc}')
    duplicate_ids = {key: n for key, n in sorted(p.ids.items()) if n > 1}
    if duplicate_ids:
        errors.append(f'duplicate DOM IDs: {len(duplicate_ids)}')
    if p._inside_script:
        errors.append('unclosed script tag')
    js = '\n'.join(p.inline_js)
    warnings = []
    render_overrides = len(re.findall(r'\b(?:window\.|globalThis\.)render\s*=', js))
    render_functions = len(re.findall(r'\bfunction\s+render\s*\(', js))
    if render_overrides:
        warnings.append('global render assignment detected; inspect override chain manually')
    if len(p.scripts) > 30 or p.styles > 30:
        warnings.append('many inline script/style tags; inspect maintainability and cascade')
    if p.inline_handlers:
        warnings.append('inline event attributes detected; inspect escaping and event binding')
    if 'innerHTML' in js:
        warnings.append('innerHTML usage detected; inspect untrusted data escaping')
    js_syntax = check_js_syntax(p.inline_js,p.script_types,node_path) if check_js else {'status':'NOT_RUN','reason':'--check-js not requested','checked':0,'errors':[]}
    return {
        'js_syntax':js_syntax,
        'file': file_label,
        'bytes': len(source.encode('utf-8')),
        'script_tags': len(p.scripts),
        'inline_script_tags': len(p.inline_js),
        'style_tags': p.styles,
        'inline_event_handlers': p.inline_handlers,
        'duplicate_ids': duplicate_ids,
        'external_dependencies': p.external,
        'global_render_definitions': render_functions,
        'render_assignments': render_overrides,
        'innerHTML_mentions': js.count('innerHTML'),
        'errors': errors,
        'warnings': warnings,
        'gate_g0': 'FAIL' if errors or js_syntax['status']=='FAIL' else 'BLOCKED' if check_js and js_syntax['status']=='NOT_RUN' else 'PASS_WITH_WARNINGS' if warnings else 'PASS',
        'scope': 'static structural audit only; G1-G4 NOT_RUN',
    }

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('html', help='input HTML file')
    ap.add_argument('--out', help='write JSON report')
    ap.add_argument('--strict', action='store_true', help='exit 2 on deterministic errors')
    ap.add_argument('--check-js', action='store_true', help='check inline JS with Node.js')
    ap.add_argument('--require-js', action='store_true', help='require JS syntax check to run (implies --check-js)')
    args = ap.parse_args(argv)
    path = Path(args.html)
    if not path.is_file():
        ap.error(f'file not found: {path}')
    result = audit(path.read_text(encoding='utf-8', errors='replace'), str(path), check_js=args.check_js or args.require_js)
    output = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.out:
        Path(args.out).write_text(output, encoding='utf-8')
    print(output, end='')
    if args.require_js and result['js_syntax']['status']=='NOT_RUN': return 3
    if args.strict and (result['errors'] or result['js_syntax']['status']=='FAIL'): return 2
    return 0

if __name__ == '__main__':
    sys.exit(main())
