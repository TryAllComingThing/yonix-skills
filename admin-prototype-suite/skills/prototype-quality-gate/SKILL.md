---
name: prototype-quality-gate
description: 企业管理平台原型专项质量验收；G0-G4、管理场景交互矩阵、Mock 数据一致性、同视口视觉对比、无障碍与缺陷闭环。
---
# Prototype Quality Gate V1.3｜管理平台专项验收专家

## 状态与证据
PASS=执行且有证据；FAIL=已执行失败；BLOCKED=依赖/环境阻断；NOT_RUN=未执行；N/A=说明原因后不适用。禁止把 BLOCKED/NOT_RUN 计入通过率。

## G0 源码/工程
运行 `scripts/validate_suite.py`（检查套件）及目标工程 lint/typecheck/build/test；单文件 HTML 可用 `scripts/audit_html.py --check-js --strict`。报告脚本、样式、重复 ID、render 覆盖、innerHTML 风险；静态检查不等于浏览器通过。
## G1 业务契约与 Mock
按 `references/prototype-interaction-contracts.md`、`references/mock-data-and-state.md` 验证 CRUD、字段必填、唯一性、状态机、引用关系、权限、草稿/取消、删除保护、发布快照、数据重置与重复提交。重点反例：同名跨对象、孤儿引用、保存失败、取消后污染、发布后草稿修改。
## G2 真实交互
浏览器实际点击导航、查询/清空、分页、详情/编辑/保存/取消、删除确认、Tabs 连续切换、弹窗焦点/滚动、失败反馈、跨页状态。记录步骤/预期/实际/日志/证据；不可运行标记 BLOCKED。
## G3 视觉
相同视口、DPR、字体、主题、缩放、语言、数据、动画状态截图；核查表格边界、卡片密度、标题重复、弹窗宽高、图标语义、文本溢出与响应式；区分功能遮挡 P0、布局失效 P1、局部偏差 P2。
## G4 易用性
键盘 Tab/Enter/Esc、焦点回归、表单错误提示、危险操作防误触、状态反馈、可读对比度与关键任务路径。自动化 axe 结果不能替代人工任务走查。

## 回归矩阵
以 `templates/interaction-test-cases.md` 为最小用例，新增功能需补正向/边界/异常/权限/跨页/回归。关键 G1/G2 FAIL 不得冻结；未执行 G3/G4 可交候选版但必须明确限制。

## 交付
`templates/review-report.md`：每门禁环境、输入 SHA256、命令、截图/日志路径、结果、缺陷编号、复测、风险、回滚；未验证项单独列出。

## V1.3 专家执行规则
G0 JS 语法失败必须使 G0 FAIL；检查未执行不得写 PASS。G1 测实体/状态/快照，G2 用浏览器测交互，G3 同条件视觉，G4 键盘与无障碍。每条证据对应测试 ID 和执行命令。
详细方法参考套件根目录 `references/expert-decision-method.md`；记录模板 `templates/decision-record.md`。
