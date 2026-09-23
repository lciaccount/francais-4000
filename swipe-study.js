/* One visible card, one audio owner. No 4000-node feed or background players. */
(() => {
  'use strict';
  const KEY = 'fr4000-swipe-v1';
  const stored = (() => {try {return JSON.parse(localStorage.getItem(KEY) || '{}') || {};} catch {return {};}})();
  const integer = (value, fallback, max) => Number.isInteger(value) && value >= 1 && value <= max ? value : fallback;
  const prefs = {details: stored.details === true, hideTranslation: stored.hideTranslation === true,
    auto: stored.auto === true, repeats: integer(stored.repeats, 3, 100), range: stored.range === true,
    start: integer(stored.start, 1, SENTENCES.length), end: integer(stored.end, SENTENCES.length, SENTENCES.length), loop: stored.loop === true,
    positions: typeof stored.positions === 'object' && stored.positions ? stored.positions : {}};
  if (prefs.start > prefs.end) [prefs.start, prefs.end] = [prefs.end, prefs.start];
  const feed = {open: false, kind: 'sentence', list: [], index: 0, contexts: {}, playing: false,
    slow: false, details: false, revealed: false, turn: 0, count: 0, timer: null, preview: false,
    returnFocus: null, inert: [], scroll: [0, 0], fullscreen: false, gesture: null, locked: false, completed: false};
  const save = () => {try {localStorage.setItem(KEY, JSON.stringify(prefs));} catch { /* Private mode / quota: keep the in-memory settings. */ }};
  const current = () => feed.list[feed.index];
  const title = item => !item ? '暂无内容' : feed.kind === 'sentence' ? `句子 #${item.id}` : feed.kind === 'letter' ? `字母 ${item.symbol}` : `音标 /${item.symbol}/`;
  document.body.insertAdjacentHTML('beforeend', `
    <section id="swipeStudy" class="swipeStudy" role="dialog" aria-modal="true" aria-labelledby="swipeTitle" hidden>
      <header class="swipeHeader"><div><h2 id="swipeTitle">滑屏学习</h2><span id="swipeScopeLabel"></span></div>
        <label class="swipeKindLabel"><span class="swipeSrOnly">学习内容</span><select id="swipeKind"><option value="sentence">句子</option><option value="letter">字母</option><option value="sound">音标</option></select></label>
        <button id="swipeLock" type="button" aria-pressed="false">锁定</button>
        <button id="swipeExit" type="button" aria-label="退出滑屏学习">× <span>退出</span></button></header>
      <div class="swipeSettings"><div class="swipePreferences"><label><input id="swipeDefaultDetails" type="checkbox" role="switch">默认显示详解</label><label><input id="swipeHideTranslation" type="checkbox" role="switch">先隐藏译文</label><label id="swipeAllLabel"><input id="swipeAll" type="checkbox">全部 4000 句</label></div>
        <details id="swipeAutoSettings"><summary id="swipeAutoSummary">自动切换与区间 · 未开启</summary>
          <form id="swipeAutoForm" class="swipeAutoForm" novalidate>
            <label><input id="swipeAuto" type="checkbox" role="switch">自动切换</label>
            <label>每句 <input id="swipeRepeats" type="number" min="1" max="100" step="1" inputmode="numeric" required> 遍</label>
            <label><input id="swipeRange" type="checkbox">指定句子区间</label>
            <div class="swipeRangeFields"><label>起始编号 <input id="swipeRangeStart" type="number" min="1" max="${SENTENCES.length}" step="1" inputmode="numeric" required></label><span>—</span><label>结束编号 <input id="swipeRangeEnd" type="number" min="1" max="${SENTENCES.length}" step="1" inputmode="numeric" required></label></div>
            <label><input id="swipeRangeLoop" type="checkbox">到末尾循环回第一条</label><button type="submit">应用并开始</button>
            <p class="swipeAutoNote">仅用于句子；指定区间后按全库编号学习，不受原分类或搜索限制。一遍包含当前设置的完整播放组合。</p>
            <p id="swipeAutoError" role="alert" hidden></p>
          </form>
        </details>
      </div>
      <div class="swipeProgress"><span id="swipeCounter" aria-live="polite"></span><div role="progressbar" id="swipeProgressBar" aria-label="当前列表位置"><i id="swipeProgressFill"></i></div><span>↑ 下一条 · ↓ 上一条</span></div>
      <div id="swipeStage" class="swipeStage"><article id="swipeCard" class="swipeCard" tabindex="-1"></article></div>
      <footer class="swipeFooter"><div class="swipeAudioRow"><span id="swipePlayState" role="status" aria-live="polite"></span><div class="swipeAudioControls"><label class="swipeSpeedLabel"><span class="swipeSrOnly">播放倍速（0.50 至 2.00，步长 0.05）</span><select id="swipeSpeed">${Array.from({length:31}, (_,i) => {const rate=((50+i*5)/100).toFixed(2); return `<option value="${rate}">${rate}×</option>`;}).join('')}</select></label><label class="swipeVoiceLabel"><span class="swipeSrOnly">播放音色（音标参考音固定）</span><select id="swipeVoice"></select></label></div></div>
        <div class="swipeActions"><button id="swipePrev" type="button" aria-label="上一条">↑ <span>上一条</span></button><button id="swipePause" type="button" class="swipePrimary">暂停</button><button id="swipeSlow" type="button" aria-pressed="false">0.75× <span>慢读</span></button><button id="swipeDetails" type="button" aria-expanded="false" aria-controls="swipeExplanation">详解</button><button id="swipeNext" type="button" aria-label="下一条">↓ <span>下一条</span></button></div>
        <div id="swipeHint" class="swipeHint">上下滑切换 · 当前条目无限循环 · 空格暂停 · Esc 退出</div></footer>
    </section>`);
  const root = $('#swipeStudy'), stage = $('#swipeStage'), card = $('#swipeCard');
  const autoEnabled = () => feed.kind === 'sentence' && prefs.auto;
  const playbackRate = () => feed.slow ? .75 : Number($('#speed').value);

  function fillAutoSettings() {
    $('#swipeAuto').checked = prefs.auto;
    $('#swipeRepeats').value = prefs.repeats;
    $('#swipeRange').checked = prefs.range;
    $('#swipeRangeStart').value = prefs.start;
    $('#swipeRangeEnd').value = prefs.end;
    $('#swipeRangeLoop').checked = prefs.loop;
    $('#swipeAutoError').hidden = true;
    syncRangeFields();
  }
  function syncRangeFields() {
    for (const id of ['swipeRangeStart', 'swipeRangeEnd']) $('#'+id).disabled = !$('#swipeRange').checked;
  }
  function syncLock() {
    root.classList.toggle('is-locked', feed.locked);
    $('#swipeLock').textContent = feed.locked ? '解锁' : '锁定';
    $('#swipeLock').setAttribute('aria-pressed', String(feed.locked));
    for (const el of root.querySelectorAll('.swipeKindLabel,#swipeExit,.swipeSettings,.swipeActions,.swipeAudioRow label')) el.inert = feed.locked;
    for (const el of card.querySelectorAll('button,a')) {
      if (el.tagName === 'BUTTON') el.disabled = feed.locked;
      if (feed.locked) el.setAttribute('tabindex', '-1'); else el.removeAttribute('tabindex');
    }
    if ($('#swipeExplanation')) $('#swipeExplanation').tabIndex = feed.locked ? -1 : 0;
    $('#swipeHint').textContent = feed.locked ? '已锁定 · 仅可上下滑切换 · 点右上角解锁' : '上下滑切换 · 详解内可滚动 · 空格暂停 · Esc 退出';
  }
  function advanceAutomatically() {
    if (feed.index < feed.list.length - 1) {step(1, 'auto'); return;}
    if (prefs.loop) {
      stopAll(true); feed.index = 0; feed.turn = 0;
      renderCard(1); startPlayback();
    } else {
      feed.completed = true;
      pause('本轮已完成，已到列表末尾。点继续可重听当前句。');
    }
  }

  function sentenceExplanation(item) {
    const a = sentenceLearning(item);
    const list = values => `<ul>${values.map(t => `<li>${escapeHtml(t)}</li>`).join('')}</ul>`;
    return `<h3>句子详解</h3><h4>句型结构</h4><p>${escapeHtml(a.structure || '')}</p>${renderGrammarParts(a.parts || [])}
      ${a.subparts?.length ? `<h4>从句拆分</h4>${renderGrammarParts(a.subparts)}` : ''}
      <h4>时态 / 语气</h4><p>${escapeHtml(a.tense || '')}</p>${list((a.tenseEvidence || []).map(e => `${(e.words || []).join('、')}：${e.text}`))}
      <h4>语态</h4><p>${escapeHtml(a.voice || '')} · ${escapeHtml(a.voiceText || '')}</p>
      ${a.notes?.length ? `<h4>语法要点</h4>${list(a.notes)}` : ''}
      ${a.phrases?.length ? `<h4>固定表达</h4>${list(a.phrases.map(p => `${p.text}：${p.meaning}`))}` : ''}
      ${a.keywords?.length ? `<h4>重点词语</h4>${list(a.keywords.map(w => `${w.raw}：${w.currentMeaning || w.meaning || ''}${w.lemma && normWord(w.lemma) !== normWord(w.raw) ? `（原形 ${w.lemma}）` : ''}${w.morph?.length ? ' · ' + w.morph.join('、') : ''}`))}` : ''}
      <p class="swipeFinePrint">预生成离线分析，用于辅助学习；${a.confidence === 'high' ? '自动分析可信度较高' : '请结合具体语境核对'}。</p>`;
  }

  function soundExplanation(item) {
    const source = feed.kind === 'sound' ? window.PHONETICS_SOURCES?.[item.id] : null;
    return `<h3>发音详解</h3><h4>怎么发音</h4><p>${escapeHtml(item.tip)}</p>
      ${item.spelling ? `<h4>常见拼写</h4><p>${escapeHtml(item.spelling)}</p>` : ''}
      ${item.variant ? '<p class="swipeFinePrint">这个音含口音差异或借词用音，请结合上面的说明学习。</p>' : ''}
      ${source ? `<p class="swipeFinePrint">IPA 使用固定真人参考音，部分辅音带辅助元音；请听其中的目标音，再对照法语例词。</p><p class="swipeFinePrint">${escapeHtml(source.author)} · <a href="${escapeHtml(source.page)}" target="_blank" rel="noopener noreferrer">原录音</a> · <a href="${escapeHtml(source.licenseUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(source.license)}</a>。音频已转为 MP3 并裁去首尾静音，沿用原许可。</p>` : '<p class="swipeFinePrint">字母名称与单词中的实际发音不一定相同；字母和例词跟随所选音色。</p>'}`;
  }

  function renderCard(direction = 0) {
    const item = current();
    feed.details = prefs.details;
    feed.revealed = !prefs.hideTranslation;
    feed.count = 0;
    feed.completed = false;
    $('#swipeKind').value = feed.kind;
    $('#swipeAllLabel').hidden = feed.kind !== 'sentence' || prefs.range;
    $('#swipeAutoSettings').hidden = feed.kind !== 'sentence';
    $('#swipeAutoSummary').textContent = `自动切换与区间 · ${prefs.auto ? `每句 ${prefs.repeats} 遍` : '手动切换'}${prefs.range ? ` · #${prefs.start}–${prefs.end}` : ''}${prefs.auto && prefs.loop ? ' · 循环' : ''}`;
    $('#swipeScopeLabel').textContent = feed.kind === 'sentence' && prefs.range ? `句子区间 #${prefs.start}–${prefs.end}` : feed.kind === 'sentence' && $('#swipeAll').checked ? '全部句子' : feed.contexts[feed.kind].label;
    $('#swipeCounter').textContent = item ? `${feed.index + 1} / ${feed.list.length}` : '0 / 0';
    $('#swipeProgressFill').style.width = item ? `${(feed.index + 1) / feed.list.length * 100}%` : '0%';
    $('#swipeProgressBar').setAttribute('aria-valuenow', item ? feed.index + 1 : 0);
    $('#swipeProgressBar').setAttribute('aria-valuemin', 0);
    $('#swipeProgressBar').setAttribute('aria-valuemax', feed.list.length);
    if (!item) {
      delete card.dataset.id;
      card.dataset.kind = feed.kind;
      card.classList.remove('with-details');
      card.innerHTML = '<div class="swipeHero"><h3>当前列表还没有内容</h3><p>可勾选“全部 4000 句”，或切换到字母、音标。</p></div>';
      syncControls();
      return;
    }
    const sentence = feed.kind === 'sentence', example = sentence ? null : PHONETICS_DATA.examples[item.example];
    const translation = sentence ? item.zh : example.zh;
    card.dataset.kind = feed.kind;
    card.dataset.id = item.id;
    card.innerHTML = `<div class="swipeHero swipeScrollable"><div class="swipeEyebrow">${escapeHtml(title(item))}${feed.kind === 'sound' ? ' · ' + PHONETICS_DATA.groups[item.group] : ''}</div>
      <h3 class="swipeMainText ${sentence ? 'swipeSentenceText' : 'swipeSymbol'}" lang="fr">${sentence ? escapeHtml(item.fr) : feed.kind === 'letter' ? `${item.symbol}<small>${item.symbol.toLowerCase()}</small>` : `/${item.symbol}/`}</h3>
      <div class="swipeIPA">${sentence || feed.kind === 'letter' ? `/${escapeHtml(item.ipa)}/` : escapeHtml(item.name)}</div>
      ${!sentence ? `<button class="swipeExample" id="swipeExample" type="button" aria-label="点读例词 ${escapeHtml(item.example)}"><strong lang="fr">${escapeHtml(item.example)}</strong><span>/${escapeHtml(example.ipa)}/</span><span aria-hidden="true">▶</span></button>` : ''}
      <p id="swipeTranslation" class="swipeTranslation" ${feed.revealed ? '' : 'hidden'}>${escapeHtml(translation)}</p><button id="swipeReveal" class="swipeReveal" type="button" ${feed.revealed ? 'hidden' : ''}>点一下，查看${sentence ? '中文' : '例词释义'}</button>
      ${sentence ? '<div class="swipeMarks"><button id="swipeFavorite" type="button"></button><button id="swipeMastered" type="button"></button></div>' : ''}</div>
      <section id="swipeExplanation" class="swipeExplanation swipeScrollable" aria-label="当前条目详解" tabindex="0" ${feed.details ? '' : 'hidden'}>${sentence ? sentenceExplanation(item) : soundExplanation(item)}</section>`;
    card.classList.toggle('with-details', feed.details);
    if (direction && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
      card.getAnimations().forEach(a => a.cancel());
      card.animate([{opacity: .3, transform: `translateY(${direction > 0 ? 40 : -40}px)`}, {opacity: 1, transform: 'translateY(0)'}], {duration: 190, easing: 'ease-out'});
    }
    prefs.positions[feed.kind] = item.id;
    save();
    syncControls();
  }

  function syncControls(message = '') {
    const item = current(), busy = feed.playing && state.mode === 'swipe';
    $('#swipePause').textContent = busy ? 'Ⅱ 暂停' : '▶ 继续';
    $('#swipePause').setAttribute('aria-label', busy ? '暂停当前条目' : '继续循环当前条目');
    $('#swipePause').disabled = !item;
    $('#swipeSlow').disabled = !item;
    $('#swipeSlow').setAttribute('aria-pressed', String(feed.slow));
    $('#swipeSpeed').value = (feed.slow ? .75 : Number($('#speed').value)).toFixed(2);
    $('#swipeDetails').disabled = !item;
    $('#swipeDetails').setAttribute('aria-expanded', String(feed.details && !!item));
    $('#swipeDetails').textContent = feed.details ? '收起详解' : '显示详解';
    $('#swipePrev').disabled = !item || feed.index === 0;
    $('#swipeNext').disabled = !item || feed.index >= feed.list.length - 1;
    const audioLabel = feed.kind === 'sound' && !feed.preview ? '固定参考音' : '所选音色';
    $('#swipePlayState').textContent = message || (!item ? '请选择其他列表' : !busy ? '已暂停' : feed.preview ? '例词点读中' : `↻ 循环中 · ${feed.count + 1} 遍 · ${feed.slow ? '0.75×' : Number($('#speed').value) + '×'} · ${audioLabel}`);
    root.classList.toggle('is-playing', busy);
    if (!message && busy && !feed.preview && autoEnabled()) $('#swipePlayState').textContent = `自动切换 · 第 ${Math.min(feed.count + 1, prefs.repeats)}/${prefs.repeats} 遍 · ${feed.slow ? '0.75' : $('#speed').value}×`;
    if ($('#swipeFavorite') && item) {
      $('#swipeFavorite').textContent = progress.favorites.has(item.id) ? '★ 已收藏' : '☆ 收藏';
      $('#swipeFavorite').setAttribute('aria-pressed', String(progress.favorites.has(item.id)));
      $('#swipeMastered').textContent = progress.mastered.has(item.id) ? '✓ 已掌握' : '○ 标为掌握';
      $('#swipeMastered').setAttribute('aria-pressed', String(progress.mastered.has(item.id)));
    }
    syncLock();
  }

  function startPlayback(example = false) {
    if (!feed.open || !current()) return;
    const resumeAfterExample = feed.playing;
    stopAll(true);
    const item = current(), token = ++state.token;
    state.mode = 'swipe';
    feed.playing = true;
    feed.preview = example;
    if (feed.completed) {feed.count = 0; feed.completed = false;}
    const valid = () => feed.open && feed.playing && state.mode === 'swipe' && state.token === token;
    const fail = error => {if (valid()) pause(error?.name === 'NotAllowedError' ? '浏览器阻止了自动播放，请点继续授权播放（锁定时先解锁）。' : '音频未能播放。请检查网络后点继续，将重试当前音色；离线时需先缓存音频。');};
    const onloading = message => {if (valid()) syncControls(message);};
    const cycle = () => {
      if (!valid()) return;
      if (!example && autoEnabled() && feed.count >= prefs.repeats) {advanceAutomatically(); return;}
      syncControls();
      const done = () => {
        if (!valid()) return;
        if (example) {
          if (resumeAfterExample) startPlayback();
          else pause('例词已播放，点继续可循环当前条目。');
          return;
        }
        feed.count++;
        feed.turn++;
        feed.timer = setTimeout(cycle, Math.max(0, Number($('#gap').value) || 0));
      };
      // Failed or interrupted attempts must retry the same voice, not skip it.
      const rate = feed.slow ? .75 : Number($('#speed').value), turn = feed.turn;
      if (example) speakOnce(item.example, 'fr-FR', done, {asset: {kind: 'phonetics', id: PHONETICS_DATA.examples[item.example].id}, voiceTurn: turn, getRate: playbackRate, onerror: fail, onloading});
      else if (feed.kind === 'sentence') sequenceFor(item, done, token, turn, {getRate: playbackRate, onerror: fail, onloading});
      else if (feed.kind === 'letter') speakOnce(item.name, 'fr-FR', done, {asset: {kind: 'alphabet', id: item.id}, voiceTurn: turn, getRate: playbackRate, onerror: fail, onloading});
      else Phonetics.referenceAudio(item, token, rate, done, fail);
    };
    if (feed.kind === 'sentence' && !example) {try {markStudied(item.id);} catch { /* Storage can be full; playback still works. */ }}
    cycle();
  }

  function pause(message) {
    stopAll(true);
    feed.preview = false;
    syncControls(message);
  }

  function selectKind(kind, preferredId = null) {
    stopAll(true);
    feed.kind = kind;
    feed.list = kind === 'sentence' && prefs.range ? SENTENCES.filter(s => s.id >= prefs.start && s.id <= prefs.end) : kind === 'sentence' && $('#swipeAll').checked ? [...SENTENCES] : [...feed.contexts[kind].items];
    const id = preferredId ?? prefs.positions[kind];
    feed.index = Math.max(0, feed.list.findIndex(item => String(item.id) === String(id)));
    feed.turn = 0;
    renderCard();
    if (feed.open) startPlayback();
  }

  function open(sentenceId = null) {
    if (feed.open) return;
    const phonetic = Phonetics.getContext(), sentences = filteredSentences();
    const initialKind = sentenceId != null ? 'sentence' : Phonetics.isOpen() ? phonetic.kind : 'sentence';
    const sentenceIndex = Math.min(Math.max(0, (state.page - 1) * state.pageSize), sentences.length - 1);
    const remembered = sentences.find(s => String(s.id) === String(prefs.positions.sentence));
    const initialId = initialKind === 'sentence' ? sentenceId ?? state.currentId ?? remembered?.id ?? sentences[sentenceIndex]?.id : phonetic.selected.id;
    feed.contexts = {
      sentence: {items: sentences, label: state.search ? '搜索结果 · 当前筛选' : `${CATEGORIES.find(c => c.id === state.cat)?.name || '当前分类'} · 当前筛选`},
      letter: {items: PHONETICS_DATA.letters, label: '26 个字母'},
      sound: {items: PHONETICS_DATA.sounds, label: '全部音标'}
    };
    if (Phonetics.isOpen()) feed.contexts[phonetic.kind] = phonetic;
    feed.returnFocus = document.activeElement;
    feed.scroll = [window.scrollX, window.scrollY];
    feed.bodyTop = document.body.style.top;
    stopAll(true);
    hideDictionaryVisual();
    Phonetics.closeDetail(false);
    feed.open = true;
    feed.slow = false;
    feed.fullscreen = false;
    feed.locked = false;
    root.hidden = false;
    $('#swipeDefaultDetails').checked = prefs.details;
    $('#swipeHideTranslation').checked = prefs.hideTranslation;
    $('#swipeAll').checked = false;
    fillAutoSettings();
    $('#swipeAutoSettings').open = false;
    $('#swipeVoice').innerHTML = $('#voiceMode').innerHTML;
    $('#swipeVoice').value = currentVoiceMode();
    document.body.classList.add('swipe-study-open');
    document.body.style.top = `-${feed.scroll[1]}px`;
    feed.inert = [...document.body.children].filter(el => el !== root && !['SCRIPT', 'STYLE'].includes(el.tagName)).map(el => [el, el.inert]);
    feed.inert.forEach(([el]) => {el.inert = true;});
    selectKind(initialKind, initialId);
    card.focus({preventScroll: true});
    // Fullscreen is optional: iPhone/embedded browsers still get a viewport-filling mode.
    if (root.requestFullscreen && !document.fullscreenElement) {
      root.requestFullscreen({navigationUI: 'hide'}).then(() => {
        if (!feed.open && document.fullscreenElement === root) document.exitFullscreen().catch(() => {});
      }).catch(() => {});
    }
  }

  function close() {
    if (!feed.open || feed.locked) return;
    feed.open = false;
    stopAll(true);
    feed.gesture = null;
    stage.style.transform = '';
    if (document.fullscreenElement === root) document.exitFullscreen().catch(() => {});
    root.hidden = true;
    feed.inert.forEach(([el, previous]) => {el.inert = previous;});
    feed.inert = [];
    document.body.classList.remove('swipe-study-open');
    document.body.style.top = feed.bodyTop;
    render();
    window.scrollTo({left: feed.scroll[0], top: feed.scroll[1], behavior: 'instant'});
    const focus = feed.returnFocus?.isConnected && feed.returnFocus.getClientRects().length ? feed.returnFocus : $('#swipeEnter');
    focus.focus({preventScroll: true});
  }

  function step(delta, source = 'control') {
    if (!feed.open || !current() || (feed.locked && !['gesture', 'auto'].includes(source))) return;
    const next = Math.max(0, Math.min(feed.list.length - 1, feed.index + delta));
    if (next === feed.index) {$('#swipeHint').textContent = delta > 0 ? '已经是最后一条，可向下滑返回。' : '已经是第一条，可向上滑继续。'; return;}
    stopAll(true);
    feed.index = next;
    feed.turn = 0;
    renderCard(delta);
    $('#swipeHint').textContent = '上下滑切换 · 详解内可滚动，到边缘后再滑切条目';
    startPlayback();
  }

  function toggleDetails() {
    if (!current()) return;
    feed.details = !feed.details;
    $('#swipeExplanation').hidden = !feed.details;
    card.classList.toggle('with-details', feed.details);
    syncControls();
  }

  // If a gesture began inside scrollable explanations, let that entire gesture
  // finish scrolling. Only a NEW gesture at the boundary may change the item.
  function canScroll(el, delta) {
    return el && el.scrollHeight > el.clientHeight + 2 && (delta > 0 ? el.scrollTop + el.clientHeight < el.scrollHeight - 2 : el.scrollTop > 2);
  }
  stage.addEventListener('touchstart', e => {
    feed.gesture = null;
    if (e.touches.length !== 1 || e.target.closest('input,select')) return;
    const t = e.touches[0];
    const scroll = e.target.closest('.swipeScrollable');
    feed.gesture = {x: t.clientX, y: t.clientY, dy: 0, mode: '', scroll, scrollTop: scroll?.scrollTop || 0};
  }, {passive: true});
  stage.addEventListener('touchmove', e => {
    const g = feed.gesture;
    if (!g || e.touches.length !== 1) {feed.gesture = null; stage.style.transform = ''; return;}
    const dx = e.touches[0].clientX - g.x, dy = e.touches[0].clientY - g.y;
    if (!g.mode && Math.max(Math.abs(dx), Math.abs(dy)) > 10) g.mode = Math.abs(dx) > Math.abs(dy) * .85 ? 'ignore' : !feed.locked && canScroll(g.scroll, -dy) ? 'scroll' : 'swipe';
    if (g.mode === 'scroll') {
      if (e.cancelable) e.preventDefault();
      g.scroll.scrollTop = g.scrollTop - dy;
      return;
    }
    if (g.mode !== 'swipe') return;
    if (e.cancelable) e.preventDefault();
    g.dy = dy;
    stage.style.transform = `translateY(${Math.max(-65, Math.min(65, dy * .22))}px)`;
  }, {passive: false});
  stage.addEventListener('touchend', e => {
    const g = feed.gesture;
    feed.gesture = null;
    stage.style.transform = '';
    if (['scroll', 'swipe', 'ignore'].includes(g?.mode) && e.cancelable) e.preventDefault();
    if (g?.mode === 'swipe' && Math.abs(g.dy) >= Math.max(55, Math.min(85, stage.clientHeight * .12))) step(g.dy < 0 ? 1 : -1, 'gesture');
  });
  stage.addEventListener('touchcancel', () => {feed.gesture = null; stage.style.transform = '';});
  let wheelLast = 0, wheelSum = 0, wheelLocked = false, wheelScrolling = false;
  stage.addEventListener('wheel', e => {
    if (e.ctrlKey || Math.abs(e.deltaX) > Math.abs(e.deltaY) || e.target.closest('select,input')) return;
    const now = performance.now(), fresh = now - wheelLast > 220;
    wheelLast = now;
    if (fresh) {wheelLocked = false; wheelSum = 0; wheelScrolling = false;}
    const scroll = e.target.closest('.swipeScrollable');
    if (!feed.locked && canScroll(scroll, e.deltaY)) {wheelScrolling = true; return;}
    e.preventDefault();
    if (wheelLocked || wheelScrolling) return;
    const delta = e.deltaY * (e.deltaMode === 1 ? 20 : e.deltaMode === 2 ? stage.clientHeight : 1);
    if (Math.sign(delta) !== Math.sign(wheelSum)) wheelSum = 0;
    wheelSum += delta;
    if (Math.abs(wheelSum) >= 70) {wheelLocked = true; step(wheelSum > 0 ? 1 : -1, 'gesture');}
  }, {passive: false});

  $('#swipeEnter').onclick = () => open();
  $('#swipeLock').onclick = () => {
    feed.locked = !feed.locked;
    feed.gesture = null; stage.style.transform = '';
    wheelLocked = false; wheelScrolling = false; wheelSum = 0;
    syncLock(); (feed.locked ? card : $('#swipeLock')).focus({preventScroll: true});
  };
  // Block delegated clicks too; disabling only the visible buttons is not enough.
  for (const type of ['click', 'change', 'input', 'submit', 'contextmenu']) root.addEventListener(type, e => {
    if (feed.locked && !e.target.closest('#swipeLock')) {e.preventDefault(); e.stopImmediatePropagation();}
  }, true);
  $('#swipeRange').onchange = syncRangeFields;
  $('#swipeAutoForm').onsubmit = e => {
    e.preventDefault();
    const repeats = Number($('#swipeRepeats').value), start = Number($('#swipeRangeStart').value), end = Number($('#swipeRangeEnd').value), range = $('#swipeRange').checked;
    const error = !integer(repeats, 0, 100) ? '每句播放次数须为 1–100 的整数。' : range && (!integer(start, 0, SENTENCES.length) || !integer(end, 0, SENTENCES.length)) ? `句子编号须为 1–${SENTENCES.length} 的整数。` : range && start > end ? '起始编号不能大于结束编号。' : '';
    $('#swipeAutoError').textContent = error; $('#swipeAutoError').hidden = !error;
    if (error) return;
    Object.assign(prefs, {auto: $('#swipeAuto').checked, repeats, range, loop: $('#swipeRangeLoop').checked});
    if (range) {prefs.start = start; prefs.end = end;}
    save(); fillAutoSettings();
    $('#swipeAutoSettings').open = false;
    selectKind('sentence', range ? start : current()?.id);
    card.focus({preventScroll: true});
  };
  $('#swipeExit').onclick = close;
  $('#swipePrev').onclick = () => step(-1);
  $('#swipeNext').onclick = () => step(1);
  $('#swipePause').onclick = () => feed.playing ? pause() : startPlayback();
  $('#swipeSlow').onclick = () => {feed.slow = !feed.slow; if (feed.playing) startPlayback(); else syncControls();};
  $('#swipeSpeed').onchange = e => {
    const rate = Number(e.target.value);
    if (!Number.isFinite(rate) || rate < .5 || rate > 2) return;
    feed.slow = false;
    $('#speed').value = rate;
    $('#speed').dispatchEvent(new Event('input'));
    // Update MP3 playback in place: no restart, no extra counted repeat.
    if (state.audio) {state.audio.defaultPlaybackRate = rate; state.audio.playbackRate = rate;}
    syncControls();
  };
  $('#swipeDetails').onclick = toggleDetails;
  $('#swipeKind').onchange = e => selectKind(e.target.value);
  $('#swipeAll').onchange = () => selectKind('sentence', current()?.id);
  $('#swipeDefaultDetails').onchange = e => {prefs.details = e.target.checked; save(); if (feed.details !== prefs.details) toggleDetails();};
  $('#swipeHideTranslation').onchange = e => {
    prefs.hideTranslation = e.target.checked; save(); feed.revealed = !prefs.hideTranslation;
    if ($('#swipeTranslation')) {$('#swipeTranslation').hidden = !feed.revealed; $('#swipeReveal').hidden = feed.revealed;}
  };
  $('#swipeVoice').onchange = e => {
    $('#voiceMode').value = e.target.value;
    $('#voiceMode').dispatchEvent(new Event('change'));
    feed.turn = 0;
    if (feed.playing) startPlayback();
  };
  card.onclick = e => {
    const button = e.target.closest('button');
    if (!button) return;
    if (button.id === 'swipeReveal') {feed.revealed = true; $('#swipeTranslation').hidden = false; button.hidden = true;}
    else if (button.id === 'swipeExample') startPlayback(true);
    else if (button.id === 'swipeFavorite' || button.id === 'swipeMastered') {
      const set = button.id === 'swipeFavorite' ? progress.favorites : progress.mastered;
      const id = current().id;
      set.has(id) ? set.delete(id) : set.add(id);
      try {saveAll();} catch {}
      renderProgress(); syncControls();
    }
  };
  window.addEventListener('playbackstop', () => {clearTimeout(feed.timer); feed.timer = null; feed.playing = false; if (feed.open) syncControls();});
  document.addEventListener('visibilitychange', () => {if (feed.open && document.hidden) pause('切到后台已暂停，回到页面后点继续。');});
  document.addEventListener('fullscreenchange', () => {
    if (document.fullscreenElement === root) feed.fullscreen = true;
    else if (feed.open && feed.fullscreen) {feed.fullscreen = false; if (!feed.locked) close();}
  });
  document.addEventListener('keydown', e => {
    if (!feed.open) return;
    if (feed.locked) {
      e.stopImmediatePropagation();
      if (e.key === 'Tab') {e.preventDefault(); $('#swipeLock').focus();}
      else if (!(e.target === $('#swipeLock') && ['Enter', ' '].includes(e.key))) e.preventDefault();
      return;
    }
    if (e.key === 'Escape') {e.preventDefault(); e.stopImmediatePropagation(); close(); return;}
    // Prevent the normal sentence keyboard shortcuts from running under the overlay.
    e.stopImmediatePropagation();
    if (e.key === 'Tab') {
      const focusable = [...root.querySelectorAll('button:not(:disabled),input:not(:disabled),select,summary,a[href],[tabindex="0"]')].filter(el => el.getClientRects().length);
      const first = focusable[0], last = focusable[focusable.length - 1];
      if (!focusable.includes(document.activeElement)) {e.preventDefault(); (e.shiftKey ? last : first)?.focus();}
      else if (e.shiftKey && document.activeElement === first) {e.preventDefault(); last?.focus();}
      else if (!e.shiftKey && document.activeElement === last) {e.preventDefault(); first?.focus();}
      return;
    }
    if (e.target.closest('input,select,textarea') || e.ctrlKey || e.metaKey || e.altKey) return;
    if (['ArrowDown', 'PageDown', 'ArrowUp', 'PageUp'].includes(e.key)) {
      const delta = ['ArrowDown', 'PageDown'].includes(e.key) ? 1 : -1;
      if (canScroll(e.target.closest('.swipeScrollable'), delta)) return;
      e.preventDefault(); if (!e.repeat) step(delta);
    } else if (e.code === 'Space' && !e.target.closest('button,a,summary')) {e.preventDefault(); if (!e.repeat) feed.playing ? pause() : startPlayback();}
  }, true);

  // Contextual entry buttons survive list pagination and the mobile phonetic drawer.
  function addEntries() {
    document.querySelectorAll('#sentenceList .sentenceActions').forEach(actions => {
      if (actions.querySelector('[data-swipe-sentence]')) return;
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'iconBtn'; b.textContent = '↕ 滑屏';
      b.dataset.swipeSentence = actions.closest('.sentence').dataset.id;
      b.setAttribute('aria-label', `从第 ${b.dataset.swipeSentence} 句开始滑屏学习`);
      actions.append(b);
    });
    const actions = $('#phoneticsDetail .phonDetailActions');
    if (actions && !actions.querySelector('[data-swipe-phonetics]')) {
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'phonButton'; b.textContent = '↕ 滑屏学习'; b.dataset.swipePhonetics = '';
      actions.append(b);
    }
  }
  new MutationObserver(addEntries).observe($('#sentenceList'), {childList: true});
  new MutationObserver(addEntries).observe($('#phoneticsDetail'), {childList: true});
  document.addEventListener('click', e => {
    const b = e.target.closest('[data-swipe-sentence],[data-swipe-phonetics]');
    if (b) open(b.hasAttribute('data-swipe-sentence') ? Number(b.dataset.swipeSentence) : null);
  });
  addEntries();
  window.SwipeStudy = {isOpen: () => feed.open, step, close};
})();
