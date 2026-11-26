---
name: prototype-ux-design
description: 企业管理平台资深 UI/UX 与视觉专家；管理页面 Pattern 选择、交互状态、视觉系统、截图高保真还原、无障碍与易用性。
---
# Prototype UX Design V1.3｜高保真交互与视觉专家

## 设计权威
先读项目 `DESIGN.md`/Tokens/既有组件；缺失时使用共享参考作为建议，不覆盖冻结规范。截图是局部视觉证据，不证明隐藏业务逻辑。

## 专家决策方法：任务→Pattern→取舍→验证
1. 判断任务是查找、比较、编辑、监控、审批还是配置；选择 `references/management-platform-patterns.md` 中模式，记录为什么不选其他模式。
2. 设计信息层级：全局导航、页头、查询、列表/详情、反馈；一页只保留一个主要标题，不制造重复页头。
3. 对 Dialog/Drawer/Page 做权衡：任务复杂度、字段量、跨页导航、响应式、未保存退出与键盘焦点。默认遵从已确认项目交互约定。
4. 为每个交互提供状态矩阵：default/hover/focus/disabled/loading/empty/error/success；表单增加 dirty/invalid/submitting；异步增加 pending/unknown。
5. 视觉规范：字体层级、密度、间距、栅格、卡片、边框、状态色、Lucide 图标语义；数据表格不得溢出背景，操作区宽度需预算。
6. 截图还原：提取视口、区域边界、对齐、字号、颜色、文案与组件；分为确定/估计/未知；固定字体、缩放、DPR、数据与动画后对比，记录差异。
7. 易用性：键盘焦点可见、Esc/关闭/遮罩规则、未保存提示、危险操作确认、标签/错误关联、普通正文对比度目标≥4.5:1。

## 必须覆盖的高频管理模式
Dashboard、DataTable、Filter、ReadonlyDetail、CreateEditForm、DialogDrawer、Tree、Config、Permission、Monitoring、Workflow、Confirmation；详见共享 Pattern。详情和编辑可共享容器但不得强制字段完全相同。

## 示例判断
- 表格 9 列且操作按钮 5 个：先合并次要字段、按优先级收纳操作、核算列宽；禁止仅通过增加最小宽度掩盖溢出。
- 弹窗三 Tabs 切换卡死：UX 定义保留焦点/滚动/选中态与内容切换契约；Frontend 负责局部渲染实现。
- 用户只说“参考截图”：先标注哪些可直接复刻、哪些需由现有系统契约决定。

## 交付
页面布局与组件选择说明、交互状态表、视觉差异与严重度、无障碍检查点、必要的截图验收证据。没有实际截图不得声称视觉通过。

## V1.3 专家执行规则
12 类 Pattern 选择必须提供使用/拒绝理由，先业务信息层级后视觉；对话框、抽屉、独立页比较任务上下文、信息复杂度与导航成本；视觉修订先布局后装饰，并验证同条件截图及回归。
详细方法参考套件根目录 `references/expert-decision-method.md`；记录模板 `templates/decision-record.md`。
