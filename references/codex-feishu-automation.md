# Codex + 飞书自动归档

仅在用户配置、检查或运行飞书自动复盘时读取。本流程假设每位使用者都是组织管理员：每人创建自己的飞书应用、使用自己的 Codex 登录，并将最终文档写入同一个固定组织知识库。

## 1. 责任边界

```text
飞书 Channel：接收事件、下载录音、回复状态
本地 ASR：把媒体转成带时间戳 Transcript
Codex：使用当前系统用户的 ChatGPT/Codex 额度完成复盘
飞书 OpenAPI：创建 Wiki Docx、写入 blocks、回读验证
```

不得引入中央 OpenAI Key、共享 Codex 登录或组织统一模型账户。桥接进程必须运行在完成 `codex login` 的同一系统账户中。

## 2. 每位管理员首次接入

### 2.1 准备本机运行环境

要求 Python 3.10+、Git、Codex CLI 和 ffmpeg。先确认：

```powershell
python --version
git --version
codex --version
ffmpeg -version
```

未安装 Codex CLI 时使用 OpenAI 官方安装页：<https://developers.openai.com/codex/cli>。Windows 可用 `winget install Git.Git` 安装 Git、`winget install Gyan.FFmpeg` 安装 ffmpeg；Python 可从 python.org 或受管软件中心安装。安装后必须重新打开终端并重新运行上面的四个检查。

将 Skill 安装到当前用户目录并安装 Python 依赖：

```powershell
git clone https://github.com/liushuaikang12-ops/pm-interview-transcript-review.git "$HOME\.agents\skills\pm-interview-transcript-review"
Set-Location "$HOME\.agents\skills\pm-interview-transcript-review"
python -m pip install -r requirements-feishu.txt
```

若目录已存在，不要再次 clone；在原目录执行 `git pull --ff-only` 和依赖安装。

### 2.2 Codex 个人登录

1. 执行 `codex login`，在浏览器登录自己的 ChatGPT/Codex 账号。
2. 执行 `codex login status`，必须显示 ChatGPT 登录。
3. 如果显示 API key 登录，先执行 `codex logout`，再重新执行 `codex login` 并选择 ChatGPT 登录。

桥接使用 `codex exec` 非交互模式。启动子进程时会移除 `OPENAI_API_KEY`、`OPENAI_BASE_URL` 和 `OPENAI_API_BASE`，确保任务不误用环境中的共享 API 配置。

### 2.3 创建自己的飞书应用

1. 在飞书开放平台创建企业自建应用。
2. 启用机器人能力。
3. 在事件订阅中选择 WebSocket 长连接。
4. 订阅 `im.message.receive_v1`。
5. 在权限管理中开通以下能力：
   - 接收私聊消息；
   - 接收群消息。若指定群不要求 `@机器人`，必须开通读取群内全部消息的对应权限；
   - 获取消息中的资源，用于下载录音/视频/文件；
   - 以机器人身份发送或回复消息；
   - 创建和编辑新版文档；
   - 查看、编辑和管理知识库。
6. 发布应用版本。所有使用者都是管理员，因此由本人完成发布与审批。

飞书控制台要求先建立一次真实长连接，才允许验证并保存 WebSocket 订阅方式。凭证已写入用户环境变量后，在 Skill 目录运行：

```powershell
$env:FEISHU_APP_ID = [Environment]::GetEnvironmentVariable("FEISHU_APP_ID", "User")
$env:FEISHU_APP_SECRET = [Environment]::GetEnvironmentVariable("FEISHU_APP_SECRET", "User")
python scripts/feishu_websocket_probe.py
```

保持该进程运行，在控制台点击“验证”并保存订阅方式；完成后按 `Ctrl+C` 停止探针。探针不得输出 App Secret。

飞书控制台可能调整权限显示名称。不要仅凭权限名称声称接入成功；以 `doctor.py` 的真实 token、Wiki 读取和首次写入结果为准。

### 2.4 配置个人应用凭证

Windows 推荐使用 Skill 自带的掩码输入脚本，避免 Secret 出现在命令历史：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/set_feishu_credentials.ps1 -AppId "cli_xxx"
```

脚本会提示输入 App Secret，输入过程不回显，并将 App ID/Secret 写入当前 Windows 用户环境变量。macOS/Linux 或无法运行该脚本时，再在每位用户自己的系统环境中设置：

```powershell
[Environment]::SetEnvironmentVariable("FEISHU_APP_ID", "cli_xxx", "User")
[Environment]::SetEnvironmentVariable("FEISHU_APP_SECRET", "xxx", "User")
```

关闭并重新打开终端。运行 `$env:FEISHU_APP_ID` 只能用于确认 App ID；不要打印 App Secret。不得把 Secret 写入 JSON、README、日志、报告、Git 或终端命令历史。

### 2.5 固定知识库

1. 打开组织约定的知识库。
2. 将知识库可见范围限定为组织成员或组织内指定成员，不启用互联网公开分享。
3. 将自己的应用/机器人加入该知识库，并给予目标父节点编辑权限。
4. 本 Skill 的目标已固定为组织知识库 `秋招知识库`：域名 `vcnvx4cwol1n.feishu.cn`，`space_id` 为 `7677796340709133492`，根目录发布。不得改投其他知识库；这些标识不包含 App Secret。
   应用发布并加入知识库后运行 `python scripts/list_feishu_wikis.py`，确认应用真实可见该 `space_id`，不要只凭 URL 判断。
5. 在 Skill 目录运行：

```powershell
python scripts/setup_codex_feishu.py `
  --chat-id "oc_允许自动处理的群ID"
```

6. 运行 `python scripts/doctor.py`。只有全部 PASS 才启动桥接；该检查验证登录、依赖、tenant token 和 Wiki 读取，首次测试录音再验证真实写入。

Wiki 的 `node_token` 用于生成用户链接；`obj_token` 是底层 Docx 标识，用于写文档 blocks。两者不能混用。

新建文档位于该 Wiki 内，继承知识库的组织内访问边界。首次验收应分别用组织账号和非组织账号测试链接：组织用户能打开，非组织用户不能打开。

## 3. 自动任务契约

1. 只处理私聊或 `allowed_chat_ids` 中的群。
2. 从消息资源中选择 audio/video/file；拒绝未知扩展名。
3. 用 `message_id + file_key` 生成稳定 job id。
4. 下载到 `~/.pm-interview-review-os/jobs/<job-id>/`。
5. 媒体先经本地 ASR；已有 transcript 不重复 ASR。
6. 运行当前用户的 `codex exec --ephemeral --sandbox workspace-write`，显式调用 `$pm-interview-transcript-review`。
7. 要求 Codex 把完整结果写到本地 `review.private.md`，不能只在 stdout 回复摘要。
8. 在验证私密全量版前，先把裸 `root / follow-up / administrative` 标题按问题原文确定性恢复为 `Qxx/Axx — <Surface Question>`，并同步回答建议标题；`validate_review.py --automated` 通过后，再由 `build_feishu_review.py` 确定性生成 `review.feishu.md`。知识库版只在第 0.1 节删除候选人原回复和回答定位；第 0.2 节回答建议、第 0.3 节反问及面试官回答、后续 1–16 章完整保留。若标题仍不可读、前置问答仍泄露候选人回复或 16 章不完整，发布器必须拒绝上传。
9. 发布器拒绝 Full Review，只接受通过隐私契约校验的 `review.feishu.md`；创建 Wiki Docx 后立即保存 node/obj token，再分批写入 blocks。
10. 完整分页回读文档 blocks；只有内容和隐私校验都成功后才回复文档链接。

如果节点已创建但正文写入失败，`publication.json` 保留 `node-created` 状态。不得直接再次创建新节点；先人工检查该 manifest 和飞书节点。

## 4. 固定知识库与自动授权

管理员在首次部署时已经明确授权允许群/私聊的录音自动处理和归档，因此每条录音无需再次确认。授权不扩展到其他群、其他文件类型或上传原始录音。

本地默认保存：问题原文、候选人回复、追问、回答建议、反问原文、面试官回答原文和 16 章复盘。

飞书默认发布：第 0.1 节的面试官问题原文与追问（删除候选人原回复和回答定位）、第 0.2 节回答建议、第 0.3 节候选人反问与面试官回答，以及后续完整 1–16 章诊断。评分、个人表现诊断、Shortcoming Cards 和 Anti-patterns 属于后续诊断，允许写入固定组织知识库；原始录音仍禁止上传。第 0.1 节的候选人原回复脱敏边界不可通过配置关闭。

## 5. 启动与常驻

先前台验证：

```powershell
python scripts/codex_feishu_bridge.py
```

Windows 常驻应创建“仅当前用户”的登录触发任务，并让任务在该用户账户下运行；否则读取不到该用户的 Codex 登录。任务命令指向该用户安装目录中的 Python 和 `codex_feishu_bridge.py`。不要以共享系统服务账户运行。

Windows 任务计划程序设置：

1. 选择“创建任务”，名称填 `PM Interview Review Feishu Bridge`。
2. “常规”选择当前用户，并选择“仅当用户登录时运行”；不要改成共享服务账号。
3. “触发器”新增“登录时”，指定当前用户。
4. “操作”新增“启动程序”：程序填 `Get-Command python` 显示的完整 Python 路径；参数填 Skill 目录下 `scripts\codex_feishu_bridge.py` 的完整路径；“起始于”填 Skill 根目录。
5. “设置”启用失败后每 1 分钟重启、最多 3 次，并取消短时间后强制停止任务。
6. 手动运行任务后发送一段无隐私测试录音；在任务历史、飞书回复和 `~/.pm-interview-review-os/jobs/` 中同时核对结果。

macOS/Linux 同理：launchd/systemd user service 必须属于完成 `codex login` 的用户。

## 6. 故障定位

| 现象 | 首查 | 停止条件 |
|---|---|---|
| `codex login status` 不是 ChatGPT | 当前系统用户是否登录 | 不启动桥接 |
| 收不到消息 | 事件订阅、机器人能力、应用是否发布 | 看到真实消息事件 |
| 群里必须 @ | 是否有读取群内全部消息权限；群是否在 allowlist | 不放宽到所有群 |
| 下载失败 | file_key 是否属于该 message_id；消息资源权限 | 不猜文件内容 |
| token 成功但 Wiki 失败 | 应用是否为知识库成员、父节点是否可编辑 | 读写权限真实通过 |
| 生成了本地报告但没链接 | publication.json 和 Feishu log_id | 回读 blocks 成功才宣布完成 |
| 重发后出现重复文档 | job id/manifest 是否被删除或绕过 | 不使用 `--force-new` 自动重试 |

## 7. 验收

用一段不含真实候选人隐私的测试录音执行：发送消息、下载、转写、Codex 生成、脱敏、双版本校验、创建节点、写 blocks、完整分页回读、返回链接。确认本地私密版含完整复盘；飞书版第 1 节不含候选人原回复和回答定位，但后续 1–16 章完整存在；同一消息再次送达时只返回已有链接，不创建第二篇文档。
