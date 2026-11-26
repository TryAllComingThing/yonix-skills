---
name: prototype-expert-skills
description: Engineering Validation Edition V1.3 协调入口：企业管理软件高保真交互原型，从零创建、增量迭代、截图还原；四专业 Skill 协作、契约驱动、G0-G4 验收。
---
# Prototype Expert Skills V1.3 — Engineering Validation Edition

> **定位**：为企业后台、运营、数据、知识、AI 与配置管理平台创建可运行、可演示、可持续修改的高保真原型。交付的核心是业务正确的交互系统，不是静态图、生产后端或通用网站生成器。根 SKILL.md 是**协调入口**，四个专业 `skills/*/SKILL.md` 是专业能力；不增加第五个专业 Skill。

## 0. 输入、权威与启动判定
- 先定位当前任务的真实源文件、截图、PRD/SRS、DESIGN.md、现有组件、技术栈和可运行命令；不虚构源文件或测试。
- 权威优先级：本轮明确要求 > 本轮已确认决策 > 项目冻结设计/契约 > 现有实现 > 通用参考。若与安全/数据完整性冲突，明确风险及替代方案，不默默移除控制。
- 按任务选择模式：**A 从零创建**、**B 现有原型迭代**、**C 截图/参考还原**；组合任务可先 C 取设计约束再 B 修改，不另起重复工程。
- 默认保留项目技术栈。新工程优先 Vue3 + TypeScript + Vite + 既有 UI 组件/设计系统；用户指定 HTML 时交付 HTML；原型使用 Mock，不宣称生产接口真实生效。

## 1. 总控路由与四专家协作
1. `prototype-orchestrator`：业务对象/角色/权限/流程 → 菜单 IA、页面矩阵、字段、动作、状态、页面规格与影响分析；交付 `templates/page-spec.md`、`templates/change-request.md`。
2. `prototype-ux-design`：从任务选择管理平台 Pattern，明确列表/详情/编辑/弹窗/抽屉的决策理由、视觉 Token、交互状态与截图还原标准。
3. `prototype-frontend-engineer`：先查可复用组件/函数；实现 Mock 数据、实体 ID、交互状态、跨页联动、持久化边界；禁止无计划的尾部覆盖脚本。
4. `prototype-quality-gate`：G0 源码，G1 业务契约，G2 真实浏览器，G3 同条件视觉，G4 易用性；证据不足写 NOT_RUN/BLOCKED。

## 2. 三种模式的标准工作流
### A 从零创建（A0—A6）
A0 收集目标/角色/边界/参考/交付介质 → A1 业务实体与任务流、权限/状态 → A2 菜单/页面矩阵/关键流程 → A3 选择 Pattern、视觉基线和组件 → A4 Mock 数据/状态契约 → A5 前端实现（先壳层和公共组件，后业务页）→ A6 G0—G4 与演示脚本。不得跳过页面矩阵直接堆砌界面。
### B 持续迭代（B0—B6）
B0 基线指纹、路由、渲染入口 → B1 定位需求与截图目标 → B2 影响矩阵（正向、反向、保留项）→ B3 UX 决策与复用搜索 → B4 在权威源码原位修改、保留状态边界 → B5 业务/交互/视觉回归 → B6 差异、风险与回滚。小改动按比例执行，不能省略必要验证。
### C 截图还原（C0—C5）
C0 确认参考图及目标页面 → C1 提取布局、层级、尺寸、文字、交互控件与未知项 → C2 与项目 DESIGN.md 对齐，识别局部覆盖 → C3 映射现有组件、实现 → C4 固定视口/数据/字体截图对比 → C5 差异修复与验收。截图无法证明的隐藏状态不得臆造。

## 3. 专家判断的强制产物（不是仅列清单）
- 每个关键页面至少说明：**为什么选这个模式、舍弃哪些方案、有哪些失败/空态、如何验证**。
- `references/management-platform-patterns.md`：12 类管理页面 Pattern 和选择准则。
- `references/prototype-interaction-contracts.md`：字段/操作/状态/焦点/导航/保存等契约。
- `references/mock-data-and-state.md`：Mock 主键、数据关系、状态机、草稿隔离和持久化边界。
- 产物：页面规格、交互用例、影响矩阵、可运行代码、分层验收报告；不是只有截图或解释。

## 4. 不可突破的边界
- 修改 UI ≠ 修改业务安全规则；保存 ≠ 发布/生效；确认 ≠ 恢复；Mock ≠ 实时；静态语法 PASS ≠ G2/G3 PASS。
- 同名实体不得代替稳定 ID；发布快照不可被草稿编辑原位污染；取消不得泄漏草稿；Tabs 不得因无必要的全局重绘卡死。
- 有效设计系统与共享组件优先，避免新建同义组件；不因小改动迁移框架或引入无关依赖。
- AI 专家组评审应明确为模拟角色评审，不冒称真人参与。

## 5. 交付门禁
运行 `python3 scripts/validate_suite.py .` 和适用的 `python3 scripts/audit_html.py <prototype.html> --check-js --strict --out <report.json>`；Vue 工程执行已有 lint/typecheck/build/test。G1—G4 按 `references/acceptance-matrix.md` 与 `templates/interaction-test-cases.md` 记录，无法运行明确标记。交付说明需列版本指纹、变更范围、实际执行命令、证据、遗留缺陷、回滚方式。

## 6. V1.3 执行契约与专家判断
- 必须执行 `references/expert-decision-method.md` 的观察→约束→候选→权衡→决定→反证→证据；复杂决策填写 `templates/decision-record.md`。
- 技能发现、共享路径、阶段路由按 `references/codex-execution-contract.md`；不能将文件校验冒充 Codex 原生验收。
- Mock 最小状态与可复现浏览器断言见 `references/mock-test-contract.md`。
- 原生 A/B/C 评测记录采用 `templates/native-evaluation.md`，缺少 Codex 环境写 BLOCKED_ENV。
