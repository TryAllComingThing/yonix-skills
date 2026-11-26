# YONIX Memory V1.5 安装与使用指南

适用 macOS、Codex、WorkBuddy；依据 Memory Expert V1.5、Contract V1.1。客户端运行尚未验证。

## 1. 安装
解压集成包，在包含 personal-memory 和 yonix-memory-expert 的目录打开终端。首次初始化：

```bash
umask 077
mkdir -p "$HOME/.yonix"
chmod 700 "$HOME/.yonix"
if [ ! -e "$HOME/.yonix/memory" ] && [ ! -L "$HOME/.yonix/memory" ]; then
  cp -R personal-memory "$HOME/.yonix/memory"
  chmod 700 "$HOME/.yonix/memory"
else
  echo '已有记忆库，不覆盖'
fi
```

Codex（支持用户级 Skill 的版本）：

```bash
mkdir -p "$HOME/.agents/skills"
if [ ! -e "$HOME/.agents/skills/yonix-memory-expert" ] && [ ! -L "$HOME/.agents/skills/yonix-memory-expert" ]; then
  cp -R yonix-memory-expert "$HOME/.agents/skills/"
else
  echo '已有 Skill，请先备份升级'
fi
```

WorkBuddy：通过实际客户端的本地 Skill 导入功能导入完整 yonix-memory-expert 目录，允许访问同一个 ~/.yonix/memory/。不要导入 personal-memory 为 Skill。无需安装其他运行依赖。客户端不支持本地访问时报告限制，不创建替代库。

## 2. 目录与职责
- MEMORY.md：权威读写契约。
- profile.md：全局专业画像；preferences.md：全局偏好；lessons.md：跨领域经验。
- domains/：领域与场景记忆；organizations/：明确授权的组织规范；inbox.md：经授权保存的候选，不作为执行依据。
- Skill 的 references/knowledge 为专业方法，evaluation 为隔离测试案例，不属于用户记忆。

## 3. 首次检查
在两个客户端分别输入：请使用 yonix-memory-expert，检查 Skill 发现、版本、共享记忆绝对路径、Contract V1.1 及读取权限；仅检查，不写入。输出实际证据和 PASS/FAIL/NOT_VERIFIED。

## 4. 日常使用指令
- 初始化画像：请根据我明确提供的专业背景、工作领域和工作方法提取画像候选，标注依据和范围，等待确认，不写入。
- 明确记忆：请记住，今后客户汇报优先突出业务价值，适用范围仅为客户汇报。写入后重读验证。
- 使用记忆：请加载与本次任务相关的已确认专业记忆，忽略候选与无关领域；当前任务要求优先于普通历史偏好。
- 反思：请从本次真实反馈及验收结果提取最多三条可复用经验候选，等待确认。
- 导入：请仅分析我授权的历史资料，区分项目事实与长期记忆，先提出去重后的候选，不写入。
- 更正：请查找指定偏好，确认作用域，按我的明确修改要求更新并验证。
- 删除：请删除指定本地记忆及派生引用，报告实际文件变更和无法处理的外部副本。

## 5. 专业套件协同
任务识别 → 读取契约及相关 Confirmed 记录 → 专业套件执行 → 实际反馈 → Memory Expert 提取候选 → 用户确认 → 定向写入并验证。Presentation Kit 将有效偏好纳入 Brief 的 Effective Profile，PPT Master Plus 按原生确认和 Spec Lock 制作。其他套件可直接按契约只读，不必强制调用 Memory Expert。专业默认策略、项目事实及锁定配置不自动成为记忆。

## 6. 可选全局指令
专业任务按需读取 ~/.yonix/memory/MEMORY.md 及相关已确认记忆；复杂提取、归纳、更正、删除使用 yonix-memory-expert；不创建替代库，不自动同步原生记忆；重要任务结束后按需提出最多三条候选，未经授权不写入。Codex 可追加到已有 ~/.codex/AGENTS.md，WorkBuddy 使用实际支持的长期指令功能，不覆盖原配置。

## 7. 升级与安全
关闭两个客户端，备份真实记忆及旧 Skill 到私有非发现目录；审查合并 MEMORY.md、README.md，缺失 learning.md 才补充，保留所有用户记录。备份移出旧 Skill 后安装新版，更新旧 ID 引用。回滚时保留新增用户记录。单写者约定，不保证并发锁或跨文件事务。明确长期记忆请求只授权指定范围；推断候选及候选持久化均需授权。不得保存编程偏好、凭据、客户秘密或原始聊天。磁盘本地不等于模型推理本地。无后台自动提取或原生记忆同步。

## 8. 验收
先在隔离测试库执行 Skill 的 references/evaluation/memory-cases.md。测试空库、确认与候选隔离、场景偏好、当前要求覆盖、授权写入、删除、跨客户隔离、双客户端顺序读写。记录实际文件差异；未经验证不得标 PASS。真实客户端安装及语义测试仍待本地执行。
