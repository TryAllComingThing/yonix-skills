# PPT Master Plus 协同契约 V1.2-R3
## 基线与证据
用户上传 main ZIP，SHA256 0d6bb566fb73fac5ada997f1c1a7fae2e8449ebf74d141f4f1dfed335e2ff381；无 Git commit，源码声明集成 PPT Master 5.1。依据 SKILL.md、workflows/routing.md、references/strategist.md、references/ppt-master-capability-overlay.md。实际项目初始化通过；上游契约测试24/24，能力测试20/24，Flask及skia-pathops缺失。Codex与PowerPoint未验证。
## 路由与所有权
仅三条公开路线：generate_pptx（svg_generate，faithful_beautify/image_to_pptx为profile）、edit_native_pptx（edit_native）、import_brand_pptx（无制作引擎）。品牌导入须明确用户PPTX，独立注册Brand及确认Page Kit，不创建项目；内容页仅保留Master/Layout壳，不复用示例内容。原件定向编辑采用原生计划确认与roundtrip。Presentation Kit不复制上游资产。
## Generate交接
W0-W3/G1在上游Step1之前完成领域Brief；将其作为Markdown内容输入，与权威来源分开标识。实际命令：python scripts/project_manager.py init <单一项目名> --format ppt169；python scripts/project_manager.py import-sources <project_path> <brief.md> --copy。Brief不是上游API；禁止假定自动解析。Step3自由设计或明确模板路径。Step4读取references/strategist.md及templates/design_spec_reference.md，先确认Tier1（canvas、brand、audience、core message、content divergence、delivery purpose、mode、visual style），再按实际选择派生Tier2（页数、颜色、字体、图标、公式、图片、generation_mode、transition、refine）。Confirm UI不可用时采用两轮聊天确认。不得伪造result.json。确认后按I-XI结构编写design_spec.md及spec_lock.md，G2检查Locked/Required映射，不改变原生确认顺序。Step5按需图片；Step6主Agent逐页手写SVG、每页重读spec_lock、先Live Preview；gated逐页确认，continuous不逐页等待；Step7质量检查、finalize、导出。禁止批量脚本生成SVG及--quick-generate。Quick仅简化Presentation Kit专业分析。
## 原生对象及模板
原生图表/表格需按references/ppt-master-core/native-data-interface.md显式data-pptx-replace-with标记及--native-charts-and-tables；结构化Master/Layout仅验证的structured Layout，默认flat。E4连接行为仍需PowerPoint实际测试。原生fixture已通过图表、表格、公式、超链接XML检查及roundtrip测试，不等于客户成品验证。品牌注册命令 scripts/import_brand.py <file> --brand-id <id>，需Brand Import Web确认，不可静默导入。模板保真按实际路线与确认范围验收。
## 回归与记忆
Locked变化需批准；Required检查语义及覆盖；Flexible可调整。V1视觉、V2表达、V3结构、V4专业、V5事实分别回归。偏好仅生成候选，不覆盖用户确认的上游spec_lock。W8仅确认后写入长期记忆。缺依赖时明确降级；不得绕过门禁。升级重跑测试并记录版本。

## V1.4 集成补充
Presentation Kit 的专业 Profile 不等于上游 Generate Profile。Brief 的 Effective Profile 仅为本次推荐与约束；上游 Tier 确认及 Spec Lock 是制作权威。上游不直接读取个人记忆。已锁定专业事实变更回到 Brief 审批；视觉变更遵循上游确认与回归。历史测试证据不代表本版本运行通过。
