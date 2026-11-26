# V1.1 验证记录

运行 `python3 -m unittest discover -s scripts -p 'test_*.py' -v`、`python3 scripts/validate_suite.py .` 与 `python3 scripts/audit_html.py <MaaS V10.71> --check-js --strict --out <report>`。

`v1071-static-audit.json` 为 V1.0 历史报告，不应伪装为本轮复测结果。V1.1 的真实报告为 `v1071-v11-static-audit.json`。

G1—G4 没有真实业务/浏览器测试，均为 NOT_RUN；不宣称交互与视觉验收通过。
