# Claude → ChatGPT/Codex 迁移记录

迁移日期：2026-10-15。

## 已迁移

- 原 Git 仓库及 `.git` 历史完整复制；原仓库当时在 `main`，工作区无未提交改动，基线提交 `3e6d39b`。
- Claude 文档「72V 水上推进器 · 系统学习路线」导出原件存于 `archive/claude/learning-route-export.md`；适配后的当前版本在 `docs/learning-route.md`。
- Claude Artifact「推进器实验记录」导出原件存于 `archive/claude/experiment-log-export.html`；脱离 Claude 数据库和下载接口的本地版本在 `tools/experiment-log.html`，使用浏览器本地存储并支持 CSV 导入/导出。
- 学习规则、README、项目指令及进度状态已指向当前仓库；`PROGRESS.md` 标明阶段零进行中。
- `PROJECT_CONTEXT.md` 是供 ChatGPT 项目上传的单文件知识包；项目指令放在 `CHATGPT_PROJECT_INSTRUCTIONS.md`。

## 数据和边界

- 迁移时 Claude 实验记录页面显示 0 条真实记录。页面中的 E3.1 卡片标为示例，不是用户的测试数据。
- 原 Claude 文档中有一个嵌入式阶段图，Markdown 导出将其简化为占位文本；当前 `docs/learning-route.md` 已用阶段表补齐其信息。
- 原文档有一条尚未解决的评论：电池是否为 20 串三元锂，或为磷酸铁锂。此问题未确认，所有按 20 串、满电 84V 推算的参数仍是示例。
- 课程文档中的设备参数、公式近似和安全做法尚未针对用户实物逐项验证。实际接线与参数设置需先核对型号、规格书和实测值。
- ChatGPT 云端项目不会自动读取本地 Git 仓库。云端使用时，需要上传 `PROJECT_CONTEXT.md` 与项目指令；进度变化后重新上传最新知识包，或改用能访问本地仓库的 Codex 项目。

## GitHub 集中保存（2026-10-15）

用户要求将项目资料集中保存到 GitHub。本次补齐完整课程、实验工具、来源归档和两端入口，并新增 `docs/github-sync.md`。本次未开展课程，学习位置和累计次数保持原记录。设备配置和真实实验记录仍待用户提供。是否上传成功以实际远端提交为准。
