#!/usr/bin/env python3
"""Validate Codex skill structure, metadata, paths, references and executable scripts."""
import argparse, pathlib, re, sys, ast
import yaml
ROOT_SKILLS=['prototype-orchestrator','prototype-ux-design','prototype-frontend-engineer','prototype-quality-gate']
REQUIRED=['SKILL.md','README.md',*[f'skills/{s}/SKILL.md' for s in ROOT_SKILLS],
 'references/architecture-and-contracts.md','references/design-system-and-patterns.md',
 'references/acceptance-matrix.md','references/management-platform-patterns.md',
 'references/prototype-interaction-contracts.md','references/mock-data-and-state.md',
 'templates/page-spec.md','templates/interaction-test-cases.md','templates/change-request.md',
 'templates/impact-matrix.csv','templates/review-report.md',
 'scripts/audit_html.py','scripts/validate_suite.py','scripts/test_audit_html.py',
 'examples/maas-case-study.md','examples/v1071-static-audit.json']
REQUIRED_META={'name','description'}
def validate(root):
 root=pathlib.Path(root).resolve();errors=[];warnings=[];names=[]
 for rel in REQUIRED:
  if not (root/rel).is_file():errors.append(f'MISSING {rel}')
 for rel in ['SKILL.md',*[f'skills/{s}/SKILL.md' for s in ROOT_SKILLS]]:
  path=root/rel
  if not path.exists():continue
  txt=path.read_text(encoding='utf8')
  match=re.match(r'\A---\s*\n(.*?)\n---\s*\n',txt,re.S)
  if not match:errors.append(f'FRONTMATTER {rel}: missing or malformed');continue
  try:meta=yaml.safe_load(match.group(1))
  except yaml.YAMLError as e:errors.append(f'YAML {rel}: {e}');continue
  if not isinstance(meta,dict):errors.append(f'FRONTMATTER {rel}: not mapping');continue
  for key in REQUIRED_META:
   if not isinstance(meta.get(key),str) or not meta[key].strip():errors.append(f'META {rel}: invalid {key}')
  name=meta.get('name')
  if isinstance(name,str):
   names.append(name)
   if not re.fullmatch(r'[a-z][a-z0-9-]{1,63}',name):errors.append(f'NAME {rel}: invalid {name}')
  if rel!='SKILL.md' and name!=path.parent.name:errors.append(f'NAME {rel}: must equal directory name')
  # Only verify links that explicitly reference local shared assets.
  for link in re.findall(r'\]\(([^)]+)\)',txt):
   if link.startswith(('https:','http:','#','mailto:')):continue
   target=(path.parent/link.split('#')[0]).resolve()
   if not target.is_relative_to(root) or not target.exists():errors.append(f'LINK {rel}: {link}')
 if len(names)!=len(set(names)):errors.append('DUPLICATE skill names')
 for rel in ['scripts/audit_html.py','scripts/validate_suite.py','scripts/test_audit_html.py']:
  path=root/rel
  if path.is_file():
   try:ast.parse(path.read_text(encoding='utf8'))
   except SyntaxError as e:errors.append(f'PYTHON {rel}: {e}')
 for rel in ['templates/impact-matrix.csv','examples/v1071-static-audit.json']:
  path=root/rel
  if path.is_file() and not path.read_text(encoding='utf8').strip():errors.append(f'EMPTY {rel}')
 return errors,warnings
def main(argv=None):
 ap=argparse.ArgumentParser();ap.add_argument('root',nargs='?',default=str(pathlib.Path(__file__).resolve().parent.parent));a=ap.parse_args(argv)
 errors,warnings=validate(a.root)
 for item in errors:print('ERROR',item)
 for item in warnings:print('WARN',item)
 print(f'VALIDATE: {"FAIL" if errors else "PASS"}; errors={len(errors)} warnings={len(warnings)}')
 return 1 if errors else 0
if __name__=='__main__':sys.exit(main())
