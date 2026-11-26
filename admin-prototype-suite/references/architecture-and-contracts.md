# Architecture & Contracts V1.2

## 1. 架构边界
目标为企业管理平台**可交互原型**，不是默认生产架构。采用 `AppShell → Page/Pattern → Component → State/Repository → Mock fixtures`。跨页共享数据通过 ID 和 selector 统一读取，UI 不持有互相矛盾的对象副本。

## 2. 设计权威
本轮用户明确要求 > 已确认决策 > 冻结 PRD/SRS/DESIGN.md > 现有源码 > 套件参考。新需求与旧业务安全控制冲突时记录风险、替代与待决，不直接绕过门禁。

## 3. 页面与组件契约
页面 `id/route/role/task/pattern/data/actions/states`；组件 `props/emits/slots/focus/error/loading`；领域动作 `input/guard/transition/feedback/rollback`；测试 `given/when/then/evidence`。详见 `prototype-interaction-contracts.md`。

## 4. 公共组件与代码复用
优先项目已有 `AppShell/PageHeader/DataTable/TableActions/Pagination/StatusBadge/Dialog/ConfirmDialog/Tabs/FormSection/InfoGrid/MultiSelect/Toast`。公共组件抽取需有真实复用或设计权威，不能为单个按钮建立抽象层。公共函数进 utils，领域逻辑进 domain/service，视图只做展示和事件转发。

## 5. 工程与运行
新工程优先 Vue3/TypeScript/Vite；项目既有 HTML/其它框架则原位维护。原型可在本地运行，不强制 Docker/K8s/真实后端。静态 HTML 不能长期靠附加覆盖脚本维护；对 render 入口、CSS 层叠和事件订阅做收敛。

## 6. 安全与真实性
前端 Mock 权限用于演示但不能宣称真实授权；凭证脱敏；动态 HTML 转义；发布/应用/实时指标与生产回执分离。任何 G0 静态工具均不能证明 G1-G4 通过。
