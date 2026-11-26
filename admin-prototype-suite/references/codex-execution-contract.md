# Codex 执行契约 V1.3

## 安装与发现（需要实机验收）
- **推荐**：将完整 `prototype-expert-skills/` 放在项目 `.codex/skills/prototype-expert-skills/`，保持所有相对路径。根 `SKILL.md` 是一个可发现的总控 Skill；四个子目录为总控通过相对路径显式读取的专业能力文档。
- **可选**：若希望四个专业 Skill 也独立发现，将其各自目录链接到 `.codex/skills/`，但共享规范依然以完整套件根目录为权威。避免复制多份导致版本分叉。
- Codex 的技能扫描规则因 CLI 版本和配置不同可能不同；**静态目录 PASS 不等于发现 PASS**。在目标环境运行 `codex --version`、实际开启会话并尝试明确调用总控 Skill；记录 CLI 输出与加载路径。
- `AGENTS.md` 仅作为项目约定补充，不应替代总控技能的可发现安装。

## 路由契约
- A 从零：Orchestrator→UX→Frontend→Quality；B 迭代：Orchestrator 影响分析→UX/Frontend→Quality；C 截图：UX 定位→Orchestrator 确认变更边界→Frontend→Quality。
- 总控读取 `skills/<name>/SKILL.md` 后再加载所需 `references/`，不把四专业文档的职责重复写进总控。
- 各阶段输出必须标记 `INPUT / DECISION / ARTIFACT / TEST / STATUS`；每一阶段完成前检查上阶段产物是否存在。
- 对未授权的删除/覆盖、不可逆操作、缺失源文件或重要设计冲突，先询问；其余按已有约束推进。

## 验证脚本不等于原生验证
- `validate_suite.py` 只校验文件/Frontmatter/引用和 Python 语法；不声称验证 Codex 技能发现。
- 原生测试必须留存：Codex CLI 版本、启动命令、技能发现证据、任务输入、操作轨迹、修改文件、构建/浏览器证据、人工干预次数。
- 若目标环境无 `codex`，标记 `BLOCKED_ENV`，不得把模拟多角色阅读冒称为真实 Codex 协作。
