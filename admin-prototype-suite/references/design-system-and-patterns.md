# Design System & Interaction Patterns V1.2

## 权威与推荐
项目 DESIGN.md/Token 为唯一项目视觉权威；以下仅为缺失设计系统时的默认建议。主题色、字号、密度应统一经语义 Token 使用，避免页面硬编码不同蓝色。

## Foundations
字体层级：页标题 20–24px、区块标题 16–18px、正文 14px、辅助 12–13px（建议值）；间距采用 4px 基础步长；边框、圆角、阴影统一 Token；图标使用统一 Lucide 尺寸与语义。普通文字对比度目标 ≥4.5:1。

## 布局
导航、Header、工作区的职责清晰；页标题不重复。数据卡片按指标数量/视口决定列数，不为追求一行强制压缩可读性。表格始终受父容器约束，优先调整列宽/字段摘要/操作密度，最后才内部横向滚动。

## 高频组件
- `DataTable`：查询/表格/分页/空态/加载/操作列一体化，列宽与固定操作区有预算。
- `Dialog`：唯一标题、固定头尾、内容滚动、Esc/焦点恢复/未保存提醒。
- `FormSection`：字段分组、必填/帮助/错误/条件显隐与反馈。
- `InfoGrid`：只读双列字段卡片，长文本跨列，缺失显示“—”。
- `StatusBadge`：颜色+文字表达，不仅依赖颜色。
- `TableActions`：图标语义一致，危险动作独立，按操作数量决定是否折叠。

## 决策与验证
详细 Pattern 与取舍见 `management-platform-patterns.md`；事件与状态见 `prototype-interaction-contracts.md`。同视口、DPR、字体、缩放、主题、数据截图比对；先修 P0/P1，再处理装饰性偏差。
