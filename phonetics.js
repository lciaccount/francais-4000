/* Pronunciation lab: shares the application's playback token and audio owner. */
(() => {
  'use strict';
  const data = window.PHONETICS_DATA;
  const credits = window.PHONETICS_SOURCES || {};
  const panel = $('#phoneticsPanel');
  const lab = {tab: 'letters', group: 'all', selected: data.letters[0], active: null, timer: null};
  const isOpen = () => !panel.hidden;
  const isLetter = item => !item.group;
  const itemKey = item => `${isLetter(item) ? 'letter' : 'sound'}-${item.id}`;
  const label = item => isLetter(item) ? `字母 ${item.symbol}` : `音标 /${item.symbol}/`;
  const items = () => lab.tab === 'letters' ? data.letters : data.sounds.filter(s => lab.group === 'all' || s.group === lab.group);
  const repeatLimit = () => $('#singleRepeat').value === 'inf' ? Infinity : Math.max(1, Number($('#singleRepeat').value) || 1);
  const mobile = matchMedia('(max-width:640px)');
  let returnFocus = null;

  function closeDetail(restore = true) {
    $('#phoneticsDetail').classList.remove('expanded');
    $('#phoneticsDetail').removeAttribute('aria-modal');
    $('#phoneticsDetail').removeAttribute('role');
    $('#phoneticsBackdrop').hidden = true;
    if (restore && returnFocus?.isConnected) returnFocus.focus({preventScroll: true});
  }

  function revealDetail() {
    if (!mobile.matches) return;
    const detail = $('#phoneticsDetail');
    if (!detail.classList.contains('expanded')) {
      returnFocus = document.activeElement;
      detail.classList.add('expanded');
      detail.setAttribute('role', 'dialog');
      detail.setAttribute('aria-modal', 'true');
      $('#phoneticsBackdrop').hidden = false;
      $('#phoneticsClose').focus({preventScroll: true});
    }
  }

  function setView(view) {
    const open = view === 'phonetics';
    stopAll(true);
    hideDictionaryVisual();
    closeDetail(false);
    panel.hidden = !open;
    $('#sentencePanel').hidden = open;
    document.body.classList.toggle('phonetics-open', open);
    document.querySelectorAll('[data-study-view]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.studyView === view)));
    $('#mPrev').textContent = open ? '← 上一个' : '← 上一句';
    $('#mNext').textContent = open ? '下一个 →' : '下一句 →';
    document.querySelector('label[for="singleRepeat"]').textContent = open ? '点读重复次数' : '单句重复次数';
    $('#mobileSingleRepeat').setAttribute('aria-label', open ? '点读重复次数' : '单句重复次数');
    document.querySelector('.mobileRepeat .repeatLabel').textContent = open ? '点读重复' : '单句重复';
    setStatus(open ? '点击字母或音标开始点读。' : '待播放。点击任意句子开始单句循环。');
    if (open) {
      render();
      $('#mobileNowPlaying .nowPlayingText').textContent = '发音基础 · 点击字母或音标开始';
    }
  }

  function render() {
    document.querySelectorAll('[data-phon-tab]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.phonTab === lab.tab)));
    const letters = lab.tab === 'letters';
    $('#phoneticsIntro').textContent = letters
      ? '这里读的是字母名称。字母在单词中的发音，要结合拼写组合判断；重音字母 é、è、ç 等不是额外的字母。'
      : '这里听的是语音，不是字母名称。IPA 真人参考音固定音色；部分辅音带辅助元音，法语例词可另行点读。';
    $('#phoneticsListTitle').textContent = letters ? 'L’alphabet · 字母表' : 'Les sons · 法语语音';
    $('#phoneticsFilters').hidden = letters;
    $('#phoneticsFilters').innerHTML = [['all', '全部 37'], ...Object.entries(data.groups).map(([k, v]) => [k, `${v} ${data.sounds.filter(s => s.group === k).length}`])]
      .map(([k, v]) => `<button type="button" class="phonFilter" data-phon-group="${k}" aria-pressed="${lab.group === k}">${v}</button>`).join('');
    const groupHtml = (list, title = '') => `<div class="phoneticsGroup">${title ? `<h4>${title}</h4>` : ''}<div class="phoneticsGrid">${list.map(item =>
      `<button type="button" class="phonTile" data-phon-key="${itemKey(item)}" aria-label="点读${label(item)}" aria-pressed="${itemKey(item) === itemKey(lab.selected)}"><span class="phonTileSymbol" lang="fr">${escapeHtml(item.symbol)}${isLetter(item) ? `<small>${item.symbol.toLowerCase()}</small>` : ''}</span><span class="phonTileSub">${isLetter(item) ? `/${item.ipa}/` : escapeHtml(item.example)}</span>${item.variant ? '<span class="phonVariant">变体 / 借词</span>' : ''}<span class="phonTilePlay" aria-hidden="true">▶</span></button>`).join('')}</div></div>`;
    $('#phoneticsGrid').innerHTML = letters ? groupHtml(data.letters) : Object.entries(data.groups).filter(([k]) => lab.group === 'all' || lab.group === k).map(([k, title]) => groupHtml(data.sounds.filter(s => s.group === k), title)).join('');
    renderDetail();
    updateControls();
  }

  function renderDetail() {
    const item = lab.selected, letter = isLetter(item), example = data.examples[item.example], source = credits[item.id];
    const repeat = repeatLimit();
    const focused = $('#phoneticsDetail').contains(document.activeElement) ? document.activeElement.id : null;
    $('#phoneticsDetail').innerHTML = `<button id="phoneticsClose" class="phoneticsClose" type="button" aria-label="关闭发音讲解">×</button><div class="phonDetailTop"><div><div class="phoneticsEyebrow">${letter ? '字母名称' : data.groups[item.group] + ' · IPA'}</div><h3 class="phonDetailSymbol" lang="fr">${letter ? item.symbol + ' <small>' + item.symbol.toLowerCase() + '</small>' : '/' + item.symbol + '/'}</h3></div><div class="phonDetailName">${letter ? `/${item.ipa}/` : item.name}${item.variant ? '<span class="phonDetailVariant">含口音差异或借词用音</span>' : ''}</div></div>
      <div id="phoneticsPlayState" class="phoneticsPlayState" role="status" aria-live="polite">点击卡片开始点读</div>
      <div class="phonDetailActions"><button id="phoneticsLoop" type="button" class="phonButton primary">▶ ${repeat === Infinity ? '循环点读' : `点读 ${repeat} 次`}</button><button id="phoneticsSlow" type="button" class="phonButton">◔ 0.75× 慢读</button><button id="phoneticsStop" type="button" class="phonButton" disabled>■ 停止</button></div>
      <div class="phonExplanation"><h4>怎么发音</h4><p>${escapeHtml(item.tip)}</p>${item.spelling ? `<h4>常见拼写</h4><p>${escapeHtml(item.spelling)}</p>` : ''}</div>
      <div class="phonExample"><div class="phoneticsEyebrow">放进单词里听</div><button id="phoneticsExample" type="button" class="phonExampleButton" aria-label="播放例词 ${escapeHtml(item.example)}"><span><strong lang="fr">${escapeHtml(item.example)}</strong><span class="phonExampleIPA">/${escapeHtml(example.ipa)}/</span><span class="phonExampleZh">${escapeHtml(example.zh)}</span></span><span aria-hidden="true">▶</span></button></div>
      <p class="phonSourceNote">${letter ? '字母名与例词跟随所选音色；循环次数、速度和间隔沿用播放设置。' : '参考音固定原录音音色，不随音色设置切换。' + (['consonant', 'glide'].includes(item.group) ? '录音可能带 /a/ 等辅助元音；请听其中的目标音，再对照法语例词。' : '')}</p>
      ${!letter && source ? `<details class="phonSource"><summary>这条录音的来源</summary><p>${escapeHtml(source.author)} · <a href="${escapeHtml(source.page)}" target="_blank" rel="noopener noreferrer">原录音</a> · <a href="${escapeHtml(source.licenseUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(source.license)}</a><br>已转为 MP3 并裁去首尾静音；衍生音频沿用原许可。</p></details>` : ''}`;
    $('#phoneticsLoop').onclick = () => start(lab.selected);
    $('#phoneticsSlow').onclick = () => start(lab.selected, {slow: true});
    $('#phoneticsStop').onclick = () => stopAll();
    $('#phoneticsExample').onclick = () => start(lab.selected, {example: true});
    $('#phoneticsClose').onclick = () => {stopAll(true); closeDetail();};
    if (focused) document.getElementById(focused)?.focus({preventScroll: true});
  }

  function updateControls(message = '') {
    const busy = state.mode === 'phonetics' && !!lab.active;
    const active = lab.active;
    const status = $('#phoneticsPlayState');
    if (status) status.textContent = message || (busy ? `${active.slow ? '0.75× 慢读' : active.sequence ? '顺序点读' : active.example ? '例词示范' : '正在点读'} · ${active.example ? lab.selected.example : label(lab.selected)}${!active.slow && !active.example && !active.sequence ? ` · 第 ${active.count + 1} 次` : ''}` : '已停止 · 可点读、慢读或听例词');
    if ($('#phoneticsStop')) $('#phoneticsStop').disabled = !busy;
    if ($('#phoneticsSlow')) $('#phoneticsSlow').classList.toggle('listening', !!(busy && active.slow));
    document.querySelectorAll('.phonTile').forEach(b => {
      const selected = b.dataset.phonKey === itemKey(lab.selected);
      b.setAttribute('aria-pressed', String(selected));
      b.classList.toggle('playing', busy && selected && !active.example);
      b.querySelector('.phonTilePlay').textContent = busy && selected && !active.example ? '■' : '▶';
    });
  }

  function stopLab() {
    clearTimeout(lab.timer);
    lab.timer = null;
    lab.active = null;
    updateControls();
    if (isOpen()) $('#mobileNowPlaying .nowPlayingText').textContent = '发音基础 · 已停止';
  }

  // Never send IPA symbols to speech synthesis: those are often spoken as letters.
  function referenceAudio(item, token, rate, done, onerror = null) {
    const audio = new Audio(`audio/phonetics/ipa/${item.id}.mp3`);
    state.audio = audio;
    audio.playbackRate = rate;
    let settled = false;
    const current = () => !settled && state.token === token && state.audio === audio;
    onAudioFinished(audio, () => {
      if (!current()) return;
      settled = true;
      state.audio = null;
      done();
    });
    const fail = () => {
      if (!current()) return;
      settled = true;
      if (onerror) {onerror(); return;}
      stopAll(true);
      const message = '参考音频未能播放，请联网重试或先下载本栏离线音频。';
      updateControls(message);
      setStatus(message);
    };
    audio.onerror = fail;
    audio.play().catch(fail);
  }

  function start(item, options = {}) {
    stopAll(true);
    hideDictionaryVisual();
    lab.selected = item;
    renderDetail();
    revealDetail();
    state.mode = 'phonetics';
    const token = ++state.token;
    const active = lab.active = {...options, count: 0, turn: 0, queue: options.sequence ? [...items()] : [item]};
    const valid = () => token === state.token && state.mode === 'phonetics';
    const limit = options.slow || options.example ? 1 : repeatLimit();
    const cycle = () => {
      if (!valid()) return;
      const current = lab.selected;
      const title = options.example ? `例词 · ${current.example}` : label(current);
      updateControls();
      updatePlaybackUI(null, `${options.slow ? '慢读 · ' : ''}${title}`);
      setStatus(title);
      const done = () => {
        if (!valid()) return;
        active.count++;
        if (options.sequence) {
          if (active.count >= active.queue.length) return complete();
          lab.selected = active.queue[active.count];
          renderDetail();
        } else if (active.count >= limit) return complete();
        lab.timer = setTimeout(cycle, Math.max(0, Number($('#gap').value) || 0));
      };
      const rate = options.slow ? .75 : Number($('#speed').value);
      if (!isLetter(current) && !options.example) referenceAudio(current, token, rate, done);
      else speakOnce(options.example ? current.example : current.name, 'fr-FR', done, {
        asset: {kind: options.example ? 'phonetics' : 'alphabet', id: options.example ? data.examples[current.example].id : current.id},
        voiceTurn: active.turn++, rate
      });
    };
    const complete = () => {
      if (!valid()) return;
      stopAll(true);
      const message = options.sequence ? '当前分组已顺序播放一遍。' : `已完成${options.example ? '例词' : options.slow ? '慢读' : '点读'}：${options.example ? item.example : label(item)}`;
      updateControls(message);
      setStatus(message);
    };
    cycle();
  }

  function step(delta) {
    const list = items(), index = list.findIndex(s => itemKey(s) === itemKey(lab.selected));
    start(list[(Math.max(0, index) + delta + list.length) % list.length]);
  }

  async function downloadAudio() {
    const button = $('#phoneticsDownload'), info = $('#phoneticsOffline');
    if (!('serviceWorker' in navigator) || !/^https?:$/.test(location.protocol)) {
      info.textContent = '本地文件模式直接使用随项目附带的音频；网站离线下载需要 HTTPS 或 localhost。';
      return;
    }
    if (!navigator.serviceWorker.controller) {
      info.textContent = '离线功能正在准备，请稍后刷新页面再试。';
      return;
    }
    button.disabled = true;
    button.textContent = '正在下载…';
    const channel = new MessageChannel();
    let timeout;
    const finish = message => {
      clearTimeout(timeout);
      channel.port1.close();
      button.disabled = false;
      button.textContent = '↓ 检查 / 补全离线音频';
      info.textContent = message;
    };
    const resetTimeout = () => {clearTimeout(timeout); timeout = setTimeout(() => finish('下载暂未完成，已保存的音频会保留。请联网后重试；若刚更新网页，请刷新一次。'), 45000);};
    resetTimeout();
    channel.port1.onmessage = e => {
      const m = e.data;
      resetTimeout();
      if (m.error) finish(`下载未完成：${m.error}。已缓存的音频会保留，可重试补全。`);
      else if (m.done) finish(`✓ 本栏 ${m.total} 个音频已缓存。离线时字母和例词请选择内置音色；音标可直接播放。`);
      else info.textContent = `正在缓存本栏音频 ${m.loaded} / ${m.total}…`;
    };
    navigator.serviceWorker.controller.postMessage({type: 'CACHE_PHONETICS'}, [channel.port2]);
  }

  $('#phoneticsGrid').onclick = e => {
    const button = e.target.closest('[data-phon-key]');
    if (!button) return;
    const item = items().find(s => itemKey(s) === button.dataset.phonKey);
    if (!item) return;
    if (state.mode === 'phonetics' && !lab.active?.example && itemKey(item) === itemKey(lab.selected)) stopAll();
    else start(item);
  };
  $('#phoneticsFilters').onclick = e => {
    const button = e.target.closest('[data-phon-group]');
    if (!button) return;
    stopAll(true);
    lab.group = button.dataset.phonGroup;
    if (!items().includes(lab.selected)) lab.selected = items()[0];
    render();
  };
  document.querySelectorAll('[data-study-view]').forEach(b => b.onclick = () => setView(b.dataset.studyView));
  document.querySelectorAll('[data-phon-tab]').forEach(b => b.onclick = () => {
    if (lab.tab === b.dataset.phonTab) return;
    stopAll(true);
    lab.tab = b.dataset.phonTab;
    lab.selected = items()[0];
    render();
  });
  $('#phoneticsSequence').onclick = () => start(items()[0], {sequence: true});
  $('#phoneticsDownload').onclick = downloadAudio;
  $('#phoneticsBackdrop').onclick = () => {stopAll(true); closeDetail();};
  mobile.addEventListener('change', () => closeDetail(false));
  document.addEventListener('keydown', e => {
    if (!mobile.matches || !$('#phoneticsDetail').classList.contains('expanded')) return;
    if (e.key === 'Escape') {e.preventDefault(); e.stopPropagation(); stopAll(true); closeDetail();}
    if (e.key === 'Tab') {
      const focusable = [...$('#phoneticsDetail').querySelectorAll('button:not(:disabled),summary,a[href]')].filter(el => el.getClientRects().length);
      const first = focusable[0], last = focusable[focusable.length - 1];
      if (e.shiftKey && (document.activeElement === first || !$('#phoneticsDetail').contains(document.activeElement))) {e.preventDefault(); last?.focus();}
      else if (!e.shiftKey && (document.activeElement === last || !$('#phoneticsDetail').contains(document.activeElement))) {e.preventDefault(); first?.focus();}
    }
  }, true);
  window.addEventListener('playbackstop', stopLab);
  for (const id of ['singleRepeat', 'mobileSingleRepeat']) $('#'+id).addEventListener('change', () => {
    if (isOpen()) {stopAll(true); renderDetail(); updateControls();}
  });
  // Restart the current item on an explicit source change; no stale old-voice loop.
  for (const id of ['voiceMode', 'mobileVoiceMode']) $('#'+id).addEventListener('change', () => {
    if (state.mode === 'phonetics') start(lab.selected, {slow: lab.active?.slow, example: lab.active?.example});
  });
  $('#phoneticsCredits').innerHTML = data.sounds.map(s => {
    const c = credits[s.id];
    return c ? `<p><strong>/${s.symbol}/</strong> · ${escapeHtml(c.author)} · <a href="${escapeHtml(c.page)}" target="_blank" rel="noopener noreferrer">原文件</a> · <a href="${escapeHtml(c.licenseUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(c.license)}</a></p>` : '';
  }).join('') + '<p>处理：转为单声道 24 kHz MP3，裁除首尾静音，不额外添加留白；参考音内部用于展示发音的停顿保留。</p>';
  window.Phonetics = {isOpen, step, closeDetail, referenceAudio,
    getContext: () => ({kind: lab.tab === 'letters' ? 'letter' : 'sound', items: [...items()], selected: lab.selected,
      label: lab.tab === 'letters' ? '26 个字母' : (data.groups[lab.group] || '全部音标')})};
  render();
})();
