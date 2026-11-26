# Prototype Expert Skills V1.3 — Engineering Validation Edition

**用途**：企业管理平台高保真交互原型的产品建模、设计决策、Mock 业务实现、工程迭代与 G0—G4 验收。不是生产系统自动交付器。

## 结构与安装
**推荐完整安装**：将 `prototype-expert-skills/` 放入项目 `.codex/skills/` 下；保持总控 `SKILL.md` 和所有共享资源同目录。四个子技能由总控按相对路径加载。若要单独发现专业 Skill，可额外建立指向其目录的软链接，但不要复制并维护多份。

安装后的**必要实测**：在目标机器检查 `codex --version`，启动 Codex 会话，明确调用 `prototype-expert-skills` 并检查四个子技能及共享文档是否可读取。CLI 版本和配置可能改变发现行为；仅目录校验不能证明原生发现。具体见 `references/codex-execution-contract.md`。

## 三种模式
- A 从零创建：`请用 Prototype Expert Skills 模式 A，为集团设备管理平台设计可运行的 Vue3 高保真原型。先给出业务实体、角色、菜单页面矩阵和关键交互契约，再实现与验收。`
- B 持续迭代：`请用模式 B，在现有项目中将用户管理详情改为居中弹窗。保留原有数据与权限，先查复用，再修订并执行回归。`
- C 截图还原：`请用模式 C 参考截图还原配额规则弹窗。对齐当前 DESIGN.md，固定视口截图比对并记录差异。`

## 使用与检查
```bash
python3 scripts/validate_suite.py .
python3 -m unittest discover -s scripts -p 'test_*.py' -v
python3 scripts/audit_html.py /path/to/prototype.html --check-js --strict --out /tmp/prototype-audit.json
```
`audit_html.py` 是只读静态检查，不能证明交互、视觉或业务正确。`validate_suite.py` 仅验证套件完整性。`--require-js` 需要 Node.js；缺失时应报告无法执行。

## 决策顺序与边界
用户最新明确要求 > 已确认决策 > 项目设计权威 > 既有实现 > 通用 Pattern。默认尊重现有技术栈和组件。原型中 Mock 数据需可追溯、确定性、避免虚构真实网关成功或监控数据。变更交付需列 G0—G4 逐项状态，禁止将 NOT_RUN 写成 PASS。

## 目录
- `skills/` 四个专业角色
- `references/` 六份共享规范
- `templates/` 变更、影响、评审、页面规格、交互测试模板
- `scripts/` 静态审计、套件验证及其单测（不新增自动化工具）
- `examples/` MaaS 历史案例与原型设计示例（示例不是通用业务约束）

## V1.3 评测说明
- 真实 Codex 原生 A/B/C 任务仍需目标环境执行，见 `templates/native-evaluation.md`。
- 内置最小 Mock 浏览器测试夹具在 `examples/mock-management-fixture/`，不依赖生产后端。
- `scripts/` 保留原有三类工具，补充其自身单测 `test_validate_suite.py`，不引入新的自动化功能脚本。
- 新增专家判断与安装契约在 `references/`，所有示例是参考，不是管理平台业务强制规则。

## 实测证据
详见 `examples/v13-validation-report.md`。M0/M1 静态基线和 M2 Mock 浏览器已验证，M3 Codex 原生任务受环境阻塞，未宣布正式冻结。
