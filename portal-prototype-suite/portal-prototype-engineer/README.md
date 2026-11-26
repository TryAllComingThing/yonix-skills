# Portal Prototype Engineering Expert Skill Suite V2.0
Focus: **enterprise Web Portal creation and screenshot-driven revision**. One orchestrator and five expert lenses; V1.4 diagnostic/repair utilities retained.

## Install
Copy `portal-prototype-engineer/` into `~/.codex/skills/portal-prototype-engineer/`, restart Codex and invoke `$portal-prototype-engineer`.

## Commands
- New Portal: `$portal-prototype-engineer 从需求规划并实现可演示的服务门户，先形成用户旅程、页面契约和Mock模型。`
- Screenshot change: `$portal-prototype-engineer 对照截图修订现有Portal，保持其他页面不变，并提交浏览器截图与交互回归。`
- Local deterministic demo: `python scripts/build_portal_fixture.py --spec tests/scenarios/portal-create.json --output /tmp/portal-demo.html`
- Tests: `python -m unittest discover -s tests -p 'test_*.py' -v` (run from skill root).
- Browser tests require Playwright + Chromium. The fixture generator is **a test scaffold**, not a general AI designer; the Skill's expert workflow plans the real project.

## Two equal acceptance scenarios
A: requirements-to-complete-Portal; B: screenshot-guided change to existing Portal. See `references/portal-acceptance.md`. Controlled fixture results do not count as unseen blind testing.
