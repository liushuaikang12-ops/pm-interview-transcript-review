# Local Media → Timestamped Transcript

## 1. Capability Check

优先本地处理。依次检查：

```bash
ffmpeg -version
ffprobe -version
python -c "import faster_whisper; print('faster-whisper available')"
```

本 Skill 自带 `scripts/transcribe_media.py`，需要 ffmpeg + faster-whisper。模型首次使用会下载；网络不可用、模型未缓存或资源不足时应明确失败，不得伪造 Transcript。

## 2. Command

```bash
python scripts/transcribe_media.py INPUT_MEDIA --output-dir OUTPUT_DIR --language zh --model small
```

产出：

- `audio.16k.mono.wav`：供 ASR 的中间音频
- `transcript.segments.json`：segment start/end/text
- `transcript.vtt`：标准时间戳
- `transcript.txt`：纯文本
- `transcript.md`：`[HH:MM:SS–HH:MM:SS] Unknown Speaker: ...`
- `transcription-metadata.json`：模型、语言、duration、运行参数

ASR 脚本不做 speaker diarization，因此初始 speaker 必须是 `Unknown Speaker`。后续由 Agent 结合轮次与内容标注；不确定仍保留 Unknown。

## 3. Model Choice

- `tiny/base`：快速预览，中文准确率有限。
- `small`：本地默认，准确率/资源折中。
- `medium/large-v3`：更准但下载、内存与耗时显著增加。

默认 `device=auto`、CPU 使用 `int8`，CUDA 可用时使用 `float16`。不要在未检查资源时盲目用 large。

## 4. Existing Transcript

输入为 `.md/.txt/.vtt/.srt` 时不要重新 ASR：

1. 原文件只读保留。
2. 创建 normalized Markdown。
3. 有 timestamp 时保留；没有时使用稳定段落号，随后映射 Q&A ID。
4. 删除 filler/ASR 重复只发生在 clean copy；Evidence 需要时回引 raw。

## 5. Cleanup Rules

允许：

- 去掉不改变语义的“呃、啊、嗯”。
- 合并明显重复口吃。
- 修复上下文可唯一确定的 ASR 同音词，并在首次出现处记录 `[ASR correction]`。

禁止：

- 改数字、百分比、时间、项目名。
- 添加否定或删除否定。
- 把“我们”改成“我”。
- 把相关性润色成因果。
- 将不确定 speaker 强行标注。

## 6. Quality Gate

抽查至少：开头、自我介绍、最长项目追问、数字密集段、反问环节。若专有名词/数字错误明显，先用简历/JD 建 glossary 再重跑或人工修正。报告中保存 ASR quality 与修订说明。

## 7. Expression Metrics

时间指标从 segment timing 计算，前提是 speaker 已可靠标注。VTT 无重叠轨道时不能判断 interruption。文本词数不能冒充 speaking time。中文 filler rate 建议按每千字；阈值必须在报告中声明。

## 8. Failure Handling

- ffmpeg 缺失：列出检测结果，停止媒体链路。
- faster-whisper 缺失：说明可安装依赖或请用户提供 Transcript；不要自动上传云 ASR。
- 模型下载失败：尝试用户已有缓存/更小模型；仍失败则报告。
- 视频损坏/无音轨：用 ffprobe 验证并报告真实错误。
- ASR 成功但 speaker 失败：继续 Q&A 前先标 Unknown，不猜。

所有外部上传必须得到用户明确同意；默认 local-only。