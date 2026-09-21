# 日常法语 4000 句 · 交流优先版

这是在原 `french-2000` 界面和交互基础上重做语料后的版本。页面布局、收藏、掌握标记、搜索、分类、分页、连续播放、单句循环、播放间隔、点词词典、内置讲解、PWA 等使用方式保持原样；核心数据从 2000 句扩展为 4000 句。

## 本版改了什么

- 20 个主题，每个主题 200 句，共 **4000 句**；ID 连续 1–4000。
- 删除了旧语料中“把两条独立寒暄机械拼成一句”的生成方式。例如不会再出现 `À bientôt, ravi de vous voir.` 这种语义互相冲突的组合。
- 语料围绕与法国人实际交流：问候礼貌、自我介绍、家庭、住房、作息、日期时间、天气、购物、餐厅、交通、酒店、问路、工作、学习、健康、数码、休闲、邀约、情绪、求助等。
- 中文释义与新句子同步；页面的内置语法讲解仍由当前句子动态生成，因此会跟随 4000 句更新。
- 点词词典同步扩充；当前内置点读索引为 **914 个**词形/词条。
- 源码包不伪装成“已经带完整语音”：`audio/voice-manifest.json` 默认不启用任何内置音频。运行本地生成脚本成功后，3 路内置音色才会自动启用。

## 本地生成全部内置语音

需要：Linux / WSL、Python 3、`python3-venv`、`ffmpeg`，以及可访问 Microsoft Edge TTS 服务的网络。

在项目根目录执行：

```bash
bash build-french-4000-neural.sh "$PWD"
```

脚本会生成：

- 4000 个句子 × 3 个音色
- 914 个点读词条 × 3 个音色
- 合计 **14,742 个 MP3**

固定使用三个 `fr-FR` 法国法语单语神经音色：

- `fr-FR-HenriNeural`
- `fr-FR-EloiseNeural`
- `fr-FR-DeniseNeural`

脚本开始时会在线读取音色清单，并验证三个音色的 `Locale` 必须等于 `fr-FR`；不使用 Multilingual 音色，也不自动切换语言。这样能显著降低 `Wi-Fi`、`Bluetooth`、`parking` 等拼写像英语的词被按英语口音朗读的风险。

### 首尾静音

每个 TTS 原始 MP3 生成后立即经过 `ffmpeg`：

1. 只裁掉**开头和结尾**的静音，不裁句中自然停顿；
2. 默认首尾各保留 **20 ms** 保护空白；
3. `FRENCH_EDGE_PAD_MS` 被脚本强制限制在 **0–50 ms**，所以不会超过你要求的 0.05 秒。

因此页面把“句子间隔”设为 `0s` 时，不会再叠加 TTS 文件本身常见的长首尾空白。

如希望恰好保留 50 ms：

```bash
FRENCH_EDGE_PAD_MS=50 bash build-french-4000-neural.sh "$PWD"
```

如希望尽量贴边：

```bash
FRENCH_EDGE_PAD_MS=0 bash build-french-4000-neural.sh "$PWD"
```

脚本支持断点续跑：已经存在且大小正常的目标 MP3 会跳过。全部成功后会把 `audio/voice-manifest.json` 的 `availableSlots` 写为 `[1,2,3]`。

## 语料与词典源文件

- `sentences-4000.json`：4000 句法语、中文、IPA、分类与 ID。
- `extra-words-4000.json`：新语料补充词典。
- `build_corpus_4000.py`：重建语料和 IPA 的离线脚本。
- `build_extra_dictionary.py`：检查/生成新增词典数据。
- `apply_4000_update.py`：把语料和词典同步写回 `index.html`。
- `build-french-4000-neural.sh`：本地生成三路纯 `fr-FR` 内置音频，并裁首尾静音。

## 说明

本项目仍是学习材料，不把模板数量当成质量指标。新增句子按具体交际场景约束生成，并进行了重复、数量、词典覆盖和明显机械拼接的静态检查。IPA 用离线法语 eSpeak 生成，主要用于页面辅助显示；实际内置音频以 `fr-FR` Edge Neural TTS 为准。
