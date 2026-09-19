# 日常法语 2000 句 · v5 修正版

这版针对手机界面、内置法语发音和点词词典做了集中修正。

## 1. 手机端不再被控制区占满

- 手机宽度 `<= 800px` 时，完整播放设置默认折叠成一条 **“⚙ 播放设置”** 按钮，需要时再展开。
- 学习进度在手机端压缩为一行，隐藏进度条和次要统计。
- 搜索框、清除按钮、筛选器放在同一行。
- 手机底部固定栏只保留 **上一句 / 停止 / 下一句**，重复次数与音色选择回到可折叠播放设置中。
- 分类栏、句子卡片、边距和字号同步压缩，首屏会优先显示真正的学习内容。

## 2. 内置语音全部改为法国法语单语音色

旧版前两路使用 `fr-FR-VivienneMultilingualNeural` 和 `fr-FR-RemyMultilingualNeural`。多语种音色遇到很短或拼写跨语言的词时，可能自动采用非预期语言读法。

v5 生成器改为：

- `v1` → `fr-FR-HenriNeural`
- `v2` → `fr-FR-JacquelineNeural`
- `v3` → `fr-FR-DeniseNeural`

三路都固定为 `fr-FR`。脚本启动时还会读取 Edge TTS 音色列表，检查这三个 ShortName 是否存在、Locale 是否确实为 `fr-FR`。

### 为什么源码包里先只启用 Denise？

本次运行环境不能联网调用 Edge TTS 批量生成 8000 多个 MP3，所以我没有把旧的 Vivienne/Remy 音频冒充成“修复后音频”。安全源码包只保留旧版已经是 `DeniseNeural` 的 v3，并通过 `audio/voice-manifest.json` 暂时禁用 Henri/Jacqueline。运行下面的 v5 生成脚本后，三路会全部自动启用。

### 生成完整三音色

Linux / WSL 下，在项目目录执行：

```bash
bash build-french-2000-neural-v5.sh "$PWD"
```

默认会复用已有的 Denise 音频，只重新生成 Henri、Jacqueline，以及新加入的连字符复合词音频。当前数据量是：

- 2000 个句子
- 691 个可点读词形/词条
- 完整三音色共 8073 个 MP3
- 若可复用旧 Denise：复用 2669 个，本次生成 5404 个

需要强制三路全部重做时：

```bash
FRENCH_REBUILD_ALL=1 bash build-french-2000-neural-v5.sh "$PWD"
```

脚本支持断点续跑。全部成功后会写入 `audio/voice-manifest.json`，替换旧 `audio/`，并在家目录打包生成：

```text
~/french-2000-fr-only-v5.zip
```

## 3. 词典改成“词义”和“例句用法”分开

旧数据里很多条目其实是从句子翻译反推出来的上下文提示，却被显示成了“固定表达 / 名词短语 / 动词短语”等，容易让人误以为那是这个单词真正的词性和定义。

v5 做了三层修复：

1. 对原来的 640 个规范词条逐项兜底：其中 448 个原先只有上下文短语标签的词条补充/纠正了核心词义；其余已有正常词性词义的条目保留。因此现在 640 个原始词条都至少有一个真正的词义/词性区块。
2. 原先的“固定表达、名词短语、动词短语、天气表达、症状表达、时间表达”等不再冒充词性，统一放到 **“例句用法”** 区域。
3. 点击单词时同时显示它所在的法语原句和中文句意，方便区分“这个词本身是什么意思”和“在这一句里怎么理解”。

例如 `Enchanté` 现在显示为：

- **形容词 / 过去分词**
- 高兴的；荣幸的
- 用于见面寒暄时：很高兴认识你/您
- 动词原形：`enchanter`

而不是把“固定表达”当成它的词性。

另外修复了 `week-end`、`rendez-vous`、`petit-déjeuner`、`après-midi`、`Wi-Fi`、`grand-père` 等 22 个常见连字符复合词：它们现在会作为一个完整词条点击和点读；`allez-vous`、`pouvez-vous` 这类倒装结构仍会拆成独立单词。

## 其他修复

- Service Worker 缓存版本升级到 v5。
- 修复旧 `sw.js` 预缓存一个实际不存在的 `audio/word-index.json` 的问题，改为缓存 `audio/voice-manifest.json`，避免 PWA 安装阶段因为缺失资源而失败。
- 内置音频 URL 的缓存参数改为 `fronly5`，避免浏览器继续命中旧版多语种 MP3。
- 系统语音模式仍只优先选择 `fr-*`，并强制 `SpeechSynthesisUtterance.lang = 'fr-FR'`。

## 文件说明

- `index.html`：手机布局、词典、复合词、语音选择逻辑的主要修复。
- `sw.js`：v5 缓存和离线修复。
- `manifest.webmanifest`：新版说明。
- `audio/voice-manifest.json`：标记当前内置音色是否已准备好。
- `build-french-2000-neural-v5.sh`：重新生成三路法国法语神经音频的脚本。

## 已做的静态检查

- `index.html` 中的 JavaScript 已通过 `node --check`。
- 生成脚本已通过 `bash -n`。
- 生成脚本内嵌 Python 已通过 `compile()`。
- 验证 2000 句完整、691 个点读音频索引连续且无重复。
- 验证原 640 个词条都至少有一个核心词义/词性区块；另有 22 个连字符复合词进入新版词典/索引。

当前容器里的 Chromium 无法正常完成 headless 截图（DBus/进程环境卡住），所以没有把“浏览器截图”当作已完成测试来声称；移动端布局是按 CSS/DOM 和语法检查完成的。
