# Executable tests
Static suite: `python -m unittest discover -s tests -v` from skill root (stdlib only).
Browser scenario (requires Playwright and installed Chromium):
`python scripts/run_interaction_tests.py --html tests/fixtures/sample.html --scenario tests/scenarios/dialog.json --output interaction.json` (offline, no server) or serve the fixture over HTTP and pass `--url`. Optionally specify `--executable-path /usr/bin/chromium` for a system Chromium installation.
Visual regression (requires Pillow):
`python scripts/run_visual_regression.py --baseline baseline.png --candidate candidate.png --diff diff.png --output visual.json`
Without real baseline screenshots, do not report visual PASS.
