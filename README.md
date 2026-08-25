# pm-interview-transcript-review

面向 Codex 的产品经理面试复盘 Skill。它能把录音、视频或 Transcript 转换为可验证的问答实录、回答建议和 16 章复盘；本地保留完整原文，飞书固定知识库只删除前置问答中的候选人原回复，同时保留完整 16 章诊断。

## 最终使用体验

```text
自己的飞书机器人收到录音
  → 本机 faster-whisper 转写
  → 本机 codex exec 调用本 Skill
  → 使用当前系统用户自己的 ChatGPT/Codex 额度
  → 本地保存完整私密复盘
  → 生成并验证知识库脱敏版
  → 写入固定组织知识库（脱敏问题实录、建议、反问、完整 16 章诊断）
  → 飞书回复真实文档链接
```

每位使用者都是管理员并独立部署：使用自己的 Codex 登录、自己的飞书应用 App ID/Secret，但共享同一个组织知识库。项目不提供共享 OpenAI API Key，也不会把其他用户的 Codex 凭证复制到服务端。

## 安装 Skill

将仓库安装到当前用户的 Codex skills 目录：

```powershell
git clone https://github.com/liushuaikang12-ops/pm-interview-transcript-review.git "$HOME\.agents\skills\pm-interview-transcript-review"
cd "$HOME\.agents\skills\pm-interview-transcript-review"
python -m pip install -r requirements-feishu.txt
```

登录自己的 Codex 账号：

```powershell
codex login
codex login status
```

自动化只接受 `Logged in using ChatGPT`。即使系统里存在 `OPENAI_API_KEY`，桥接脚本也会在启动 Codex 子进程前移除它，避免误用组织共享 API 额度。

## 配置自己的飞书机器人

完整控制台步骤、权限和故障排查见 [`references/codex-feishu-automation.md`](references/codex-feishu-automation.md)。每位管理员需要：

1. 创建自己的企业自建应用并启用机器人。
2. 订阅 `im.message.receive_v1`，选择 WebSocket 长连接。
3. 开通收消息、下载消息资源、机器人回复、新版文档和知识库写入能力。
4. 发布应用版本。
5. 将自己的应用加入组织固定知识库并授予编辑权限。
6. 在自己的系统账户中设置 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET`。

固定知识库已内置为 `秋招知识库`（`vcnvx4cwol1n.feishu.cn` / `7677796340709133492`）。配置私聊和可选允许群：

```powershell
python scripts/setup_codex_feishu.py `
  --chat-id "oc_允许自动处理的群ID"
```

配置写到 `~/.pm-interview-review-os/config.json`。App Secret 不会写进该文件；`publish_candidate_answers` 固定为 `false`。

## 接入检查与启动

```powershell
python scripts/doctor.py
python scripts/codex_feishu_bridge.py
```

`doctor.py` 会检查：

- Codex 是否存在，并确认当前系统用户使用自己的 ChatGPT 登录；
- ffmpeg、faster-whisper、lark-channel-sdk 是否可用；
- 配置里没有保存密钥；
- App ID/Secret 能否获取 tenant token；
- 当前应用能否读取固定知识库。

启动后，直接给自己的机器人发送 `.mp3/.m4a/.wav/.ogg/.mp4/.mov/.mkv/.webm`，或发送 `.md/.txt/.vtt/.srt` Transcript。指定群无需每次 `@机器人`；未加入 allowlist 的群不会触发。任务目录中的 `review.private.md` 是完整本地备份，`review.feishu.md` 才是允许上传的脱敏版。

## 手动使用

在 Codex 中调用：

```text
$pm-interview-transcript-review 完整复盘这场面试，恢复追问树，并给出有证据约束的回答建议。
```

本地转写：

```powershell
python scripts/transcribe_media.py interview.mp4 --output-dir transcript-output --language zh --model small
```

本地历史：

```powershell
python scripts/interview_os.py init
python scripts/interview_os.py status
```

默认目录为 `~/.pm-interview-review-os/`，可用 `PM_INTERVIEW_REVIEW_HOME` 覆盖。

## 输出结构

本地私密报告在 16 章诊断前增加：

- 带可读 Surface Question 标题的面试官问题原文（不会退化成 `root / follow-up`）；
- 候选人实际回复；
- 追问与回复；
- 每个关键问题的回答建议；
- 候选人反问和面试官回答原文（存在时）。

飞书知识库版沿用相同的问题标题，只在第 1 节确定性删除候选人原回复和回答定位；回答建议、反问及后续完整 16 章诊断（包括评分和个人诊断）均保留。发布前若标题仍只是 `root / follow-up / administrative`、第 1 节仍含候选人回复或 16 章缺失，校验会直接拒绝上传。

之后包含 Executive Summary、Interview Structure、Complete Question Map、Follow-up Trees、Competency Mapping、Key Answer Reviews、Evidence & Quotes、Shortcoming Cards、Anti-patterns、Project Probe Depth、Role-specific Review（岗位专项复盘）、Interviewer Signals、Reverse Interview Intelligence、Shadow JD、Cross-interview Update 和 Next Interview Actions。

## 验证

```powershell
python scripts/validate_skill.py
python scripts/validate_review.py examples/test-run-output.md --automated
python scripts/publish_feishu_wiki.py examples/test-run-output.md --dry-run
```

真实飞书端到端测试需要每位管理员自己的 App ID/Secret 和固定知识库权限；离线测试不会创建文档。

## 隐私与额度边界

- ASR 默认在本机运行，不产生共享转写账单。
- 复盘由当前系统用户自己的 Codex 登录完成。
- 飞书写入由当前用户自己的企业自建应用执行。
- 默认不把原始录音上传知识库。
- Transcript、候选人信息和报告不会写进 Skill 安装目录或长期记忆。
- `message_id + file_key` 是任务幂等键；重试不会静默重复建文档。
