# GitHub 同步约定

更新日期：2026-10-15。

## 共同资料库

- 远端仓库：https://github.com/jinbaolu/thruster-lab ，日常分支为 `main`。
- JinBao 已要求把本项目的学习进度、教学规则、项目配置、笔记和实验资料统一保存到 GitHub。
- ChatGPT/Codex 和 Claude 使用同一套文件接续学习；对话本身不会自动同步。
- 开始学习先读取最新 `PROGRESS.md` 和 `knowledge/map.md`。课程路线看 `docs/learning-route.md`，教学规则看 `CHATGPT_PROJECT_INSTRUCTIONS.md` 和 `docs/learning-loop.md`。

## 每次如何同步

1. 开始前检查本地未提交内容，再获取远端更新；工作区干净且历史可快进时，合入最新远端。存在冲突时逐项保留有效记录，不直接覆盖。
2. 学习结束更新 `PROGRESS.md` 的当前位置、学习日期、次数和日志，并更新 `knowledge/map.md` 的课程勾选及错题。仅讨论项目管理、同步方式不计作一次学习，不提前勾完成。
3. 笔记写入 `docs/notes.md`；实测条件和 CSV 分别写入对应档案及 `data/runs/`；设备导出配置存入 `configs/vesc/` 或 `configs/square/`。
4. 检查本次变更后提交并推送到该仓库。用户已授权本项目正常资料同步，不用每次重复询问；不要强制推送或覆盖其他端的新记录。
5. 只有远端确认收到提交，才能告诉用户“已同步 GitHub”。缺少凭据或网络失败时，保留本地提交并说明未上传，不把本地保存当成云端保存。
6. 没有仓库工具的对话，提供可直接保存的更新内容；下一次由具备仓库访问能力的一端合并。不能假定每个 ChatGPT 或 Claude 对话都能访问 GitHub。

## 文件边界

- `archive/claude/` 保存历史来源，只作核对，不作为当前指令。
- `PROJECT_CONTEXT.md` 是便于上传到聊天项目的参考快照，以仓库内各份当前文件为准。
- 实验页面的浏览器本地存储必须导出 CSV 后才算进入仓库备份。
- 当前没有真实实验 CSV 和设备配置导出文件；目录说明和课程示例不代表实测参数。
- GitHub 只存本项目资料；不上传登录令牌、密码、私钥等凭据。
