# PRD Writer V1.1

根据业务描述、纪要、截图或原 PRD 新写、补全及定向修订需求文档。入口为 `SKILL.md`，正文格式以 `references/prd-template.md` 为准。

## 文件

| 文件 | 用途 |
|---|---|
| `SKILL.md` | 触发、写作流程、交付和按需参考入口 |
| `references/prd-template.md` | PRD 正文、原型交接、交付前四项核对 |
| `references/prompts.md` | 会议纪要提取、功能归纳和多角色审视 |
| `references/feature-list-template.md` | 功能清单起草参考 |
| `references/quality-checklist.md` | 复杂需求按风险复核 |
| `references/prototype-guide.md` | 原型交接说明 |
| `scripts/check_contract.py` | 发布包基本结构核对 |

## 使用示例

- 根据会议纪要写一份企业后台 PRD，并补关键页面的 ASCII 线框及 Mermaid 动线。
- 只修改已冻结 PRD 的列表默认筛选，保留其他规则并同步受影响的验收。
- 将 PRD 的已确认范围交给原型能力，明确 Mock 入口、前置数据和受阻路径。

维护时可从包根运行 `python3 scripts/check_contract.py`。该检查只核对发布包版本、模板章节和关键资源。项目需求、历史编号、浏览器和真实联调按实际证据复核。

