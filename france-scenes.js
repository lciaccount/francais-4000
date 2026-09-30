/* Optional illustrated French culture notebook. Facts are linked to source pages. */
(() => {
  'use strict';
  const scenes = [
    {id:'eiffel',name:'埃菲尔铁塔',fr:'La tour Eiffel',place:'Paris · 巴黎',source:'https://www.toureiffel.paris/fr/le-monument/exposition-universelle',
      lines:[
        {fr:"La tour Eiffel a été construite pour l'Exposition universelle de 1889.",zh:'埃菲尔铁塔是为 1889 年世界博览会建造的。',structure:'主语 + 被动语态 + 目的状语',grammar:'a été construite 是 être 的复合过去时加过去分词，表示“被建造”；pour 引出目的。',gloss:{tour:'塔',construite:'建造的',universelle:'世界性的'}},
        {fr:'Elle est devenue un symbole de Paris.',zh:'它已成为巴黎的象征。',structure:'主语 + devenir 的复合过去时 + 表语',grammar:'est devenue 用 être 作助动词；devenue 与阴性主语 elle 保持一致。',gloss:{devenue:'变成',symbole:'象征'}}]},
    {id:'soleil',name:'太阳王',fr:'Le Roi-Soleil',place:'Louis XIV · 路易十四',source:'https://www.chateauversailles.fr/decouvrir/histoire/grands-personnages/louis-xiv',
      lines:[
        {fr:'Louis XIV était surnommé le Roi-Soleil.',zh:'路易十四被称为“太阳王”。',structure:'主语 + 未完成过去时被动结构 + 称号',grammar:'était surnommé 描述过去持续存在的称号；surnommé 意为“被称作”。',gloss:{surnommé:'被称为',roi:'国王',soleil:'太阳'}},
        {fr:'Il a fait de Versailles le centre de sa cour.',zh:'他使凡尔赛成为其宫廷的中心。',structure:'faire de A B：使 A 成为 B',grammar:'a fait 是 faire 的复合过去时；de Versailles le centre de sa cour 是固定结构。',gloss:{fait:'使；做',centre:'中心',cour:'宫廷'}}]},
    {id:'fleur',name:'鸢尾花',fr:'La fleur de lys',place:'Symbole · 纹章',source:'https://www.chateauversailles.fr/sites/default/files/web-exe-maquette-livret-versailles-rigaud.pdf',
      lines:[
        {fr:'La fleur de lys était un symbole de la monarchie française.',zh:'鸢尾花纹章曾是法国王权的象征。',structure:'主语 + 未完成过去时 + 表语',grammar:'était 表示过去的状态；de la monarchie française 修饰 symbole。',gloss:{fleur:'花',lys:'百合纹章',symbole:'象征',monarchie:'君主制'}},
        {fr:'On la voit sur le manteau royal de Louis XIV.',zh:'在路易十四的王室披风上可以看到这种纹章。',structure:'on + 宾语代词 + 动词 + 地点',grammar:'la 指代阴性名词 fleur；on 在这里相当于“人们”。',gloss:{voit:'看见',manteau:'披风',royal:'王室的'}}]},
    {id:'louvre',name:'卢浮宫',fr:'Le Louvre',place:'Paris · 巴黎',source:'https://www.louvre.fr/se-former-et-transmettre/rencontres-et-formations/decouvrir-le-louvre-du-palais-au-musee-0',
      lines:[
        {fr:'Le Louvre était autrefois un palais royal.',zh:'卢浮宫从前是一座王宫。',structure:'主语 + 未完成过去时 + 表语',grammar:'était 讲述过去的状态；autrefois 意为“从前”。',gloss:{autrefois:'从前',palais:'宫殿',royal:'王室的'}},
        {fr:"Aujourd'hui, il abrite un grand musée.",zh:'今天，它容纳着一座大型博物馆。',structure:'时间状语 + 主语 + 动词 + 宾语',grammar:'abrite 是 abriter 的现在时，表示“容纳、庇护”。',gloss:{"aujourd'hui":'今天',abrite:'容纳',musée:'博物馆'}}]},
    {id:'versailles',name:'凡尔赛宫',fr:'Le château de Versailles',place:'Versailles · 凡尔赛',source:'https://www.chateauversailles.fr/decouvrir/histoire',
      lines:[
        {fr:'Louis XIV a installé sa cour à Versailles en 1682.',zh:'路易十四于 1682 年将宫廷迁至凡尔赛。',structure:'主语 + 动词 + 宾语 + 地点 + 时间',grammar:'a installé 是复合过去时；à Versailles 是地点，en 1682 是年份。',gloss:{installé:'安置；迁入',cour:'宫廷'}},
        {fr:'Le château est entouré de jardins et de fontaines.',zh:'宫殿周围环绕着花园和喷泉。',structure:'主语 + 被动结构 + 补语',grammar:'est entouré de 表示“被……环绕”；jardins 与 fontaines 并列。',gloss:{château:'城堡；宫殿',entouré:'被环绕',jardins:'花园',fontaines:'喷泉'}}]},
    {id:'cote-azur',name:'蔚蓝海岸',fr:"La Côte d'Azur",place:'Méditerranée · 地中海',source:'https://www.france.fr/fr/destination/cote-dazur/',
      lines:[
        {fr:"La Côte d'Azur borde la mer Méditerranée.",zh:'蔚蓝海岸濒临地中海。',structure:'主语 + 动词 + 宾语',grammar:'borde 是 border 的现在时；la mer Méditerranée 是地中海。',gloss:{côte:'海岸',azur:'蔚蓝',borde:'毗邻',mer:'海'}},
        {fr:'Ses plages et ses villages attirent de nombreux visiteurs.',zh:'它的海滩和村庄吸引许多游客。',structure:'并列主语 + 动词 + 宾语',grammar:'plages et villages 是复数主语，因此动词用 attirent。',gloss:{plages:'海滩',villages:'村庄',attirent:'吸引',visiteurs:'游客'}}]},
    {id:'bourgogne',name:'勃艮第',fr:'La Bourgogne',place:'Vignobles · 葡萄园',source:'https://www.france.fr/fr/destination/bourgogne/',
      lines:[
        {fr:'La Bourgogne est connue pour ses vignobles et sa gastronomie.',zh:'勃艮第以葡萄园和美食闻名。',structure:'主语 + être connu pour + 名词',grammar:'est connue pour 表示“以……闻名”；connue 与阴性主语保持一致。',gloss:{connue:'闻名的',vignobles:'葡萄园',gastronomie:'美食文化'}},
        {fr:'Dijon est une ville historique de la région.',zh:'第戎是这个地区的一座历史名城。',structure:'主语 + 系动词 + 表语',grammar:'historique 修饰阴性名词 ville；de la région 指明所属地区。',gloss:{ville:'城市',historique:'历史悠久的',région:'地区'}}]},
    {id:'normandie',name:'诺曼底',fr:'La Normandie',place:'Falaises · 海岸',source:'https://www.france.fr/fr/destination/normandie/',
      lines:[
        {fr:'La Normandie possède des falaises, des plages et des vergers.',zh:'诺曼底有悬崖、海滩和果园。',structure:'主语 + 动词 + 并列宾语',grammar:'possède 是 posséder 的现在时；三个 des 引出复数名词。',gloss:{possède:'拥有',falaises:'悬崖',plages:'海滩',vergers:'果园'}},
        {fr:'Ses paysages ont inspiré de nombreux peintres impressionnistes.',zh:'它的风景启发了许多印象派画家。',structure:'主语 + 复合过去时 + 宾语',grammar:'ont inspiré 是复合过去时；de nombreux 表示“许多”。',gloss:{paysages:'风景',inspiré:'启发',peintres:'画家',impressionnistes:'印象派的'}}]},
    {id:'pantheon',name:'先贤祠',fr:'Le Panthéon',place:'Quartier latin · 拉丁区',source:'https://www.paris-pantheon.fr/decouvrir/histoire-du-pantheon',
      lines:[
        {fr:'Le Panthéon se trouve dans le Quartier latin de Paris.',zh:'先贤祠位于巴黎拉丁区。',structure:'主语 + se trouver + 地点',grammar:'se trouve 是代词式动词 se trouver 的现在时，在这里表示“位于”。',gloss:{trouve:'位于',quartier:'街区',latin:'拉丁的'}},
        {fr:'Ce monument honore de grandes figures de la nation.',zh:'这座纪念建筑向国家的重要人物致敬。',structure:'主语 + 动词 + 宾语',grammar:'Ce 修饰阳性单数名词 monument；honore 表示“尊崇、纪念”。',gloss:{monument:'纪念建筑',honore:'纪念',figures:'人物',nation:'国家'}}]},
    {id:'champs-elysees',name:'香榭丽舍大街',fr:'Les Champs-Élysées',place:'Paris · 巴黎',source:'https://mairie08.paris.fr/pages/l-histoire-du-8e-arrondissement-9134',
      lines:[
        {fr:"L'avenue des Champs-Élysées mène vers l'Arc de Triomphe.",zh:'香榭丽舍大街通向凯旋门。',structure:'主语 + 动词 + 方向补语',grammar:'mène vers 表示“通向”；des 是 de + les 的缩合。',gloss:{avenue:'大街',mène:'通向',arc:'拱门',triomphe:'凯旋'}},
        {fr:'Cette avenue est bordée de commerces et de jardins.',zh:'大街两侧分布着商店和花园。',structure:'主语 + 被动结构 + 补语',grammar:'est bordée de 表示“两旁排列着”；bordée 与阴性 avenue 一致。',gloss:{avenue:'大街',bordée:'两旁有',commerces:'商店',jardins:'花园'}}]}
  ];
  const dialog = document.querySelector('#sceneDialog');
  const choices = document.querySelector('#sceneChoices');
  const content = document.querySelector('#sceneContent');
  const safeIds = new Set(scenes.map(s => s.id));
  let selected = localStorage.getItem('fr4000-scene') || 'none';
  if (!safeIds.has(selected)) selected = 'none';
  let active = scenes.find(s => s.id === selected) || scenes[0];
  let lookup = null;
  let returnFocus = null;

  function applyBackground() {
    document.documentElement.dataset.scene = selected;
    document.documentElement.style.setProperty('--scene-image',selected === 'none' ? 'none' : `url("./backgrounds/${selected}.webp")`);
    const banner = document.querySelector('#sceneBanner');
    banner.hidden = selected === 'none';
    if (selected !== 'none') document.querySelector('#sceneBannerName').textContent = (scenes.find(s => s.id === selected) || active).name;
    localStorage.setItem('fr4000-scene',selected);
    if (!dialog.hidden) renderChoices();
  }
  function renderChoices() {
    choices.innerHTML = `<button class="sceneChoice none" type="button" data-scene="none" aria-pressed="${selected === 'none'}"><span>纯色背景<br>关闭插画</span></button>` + scenes.map(s => `<button class="sceneChoice" type="button" data-scene="${s.id}" aria-pressed="${selected === s.id}" title="${escapeHtml(s.name)}"><img src="./backgrounds/${s.id}.webp" alt="" loading="lazy"><span>${escapeHtml(s.name)}</span></button>`).join('');
  }
  function wordButtons(fr) {
    return fr.split(/([A-Za-zÀ-ÖØ-öø-ÿŒœ]+(?:[’'-][A-Za-zÀ-ÖØ-öø-ÿŒœ]+)*)/u).map(part => /^[A-Za-zÀ-ÖØ-öø-ÿŒœ]/u.test(part) ? `<button class="sceneWord" type="button" data-word="${escapeHtml(part)}" aria-label="查询并点读 ${escapeHtml(part)}">${escapeHtml(part)}</button>` : escapeHtml(part)).join('');
  }
  function renderContent() {
    const s = active;
    document.querySelector('#sceneTitle').textContent = s.name;
    content.innerHTML = `<div class="sceneHero" style="background-image:url('./backgrounds/${s.id}.webp')"><div><small>${escapeHtml(s.place)}</small><h3>${escapeHtml(s.fr)}</h3><p>${escapeHtml(s.name)}</p></div></div><p class="sceneSource">内容参考：<a href="${s.source}" target="_blank" rel="noopener noreferrer">查看原始资料 ↗</a> · 插画为 AI 创作，非实景照片。</p><p class="sceneAudioNote">介绍句使用设备的法语／中文语音朗读，不属于三种内置音色；语音可用性取决于设备。</p><div class="sceneLines">${s.lines.map((line,i) => `<article class="sceneLine" data-line="${i}"><div class="sceneFrench" lang="fr">${wordButtons(line.fr)}</div><div class="sceneChinese" lang="zh-CN">${escapeHtml(line.zh)}</div><div class="sceneLineActions"><button type="button" data-action="play-fr">▶ 法语</button><button type="button" data-action="play-zh">中文朗读</button><button type="button" data-action="explain" aria-expanded="false">句子讲解</button></div><div class="sceneExplanation" hidden><div><strong>句型：</strong>${escapeHtml(line.structure)}</div><div><strong>解析：</strong>${escapeHtml(line.grammar)}</div></div></article>`).join('')}</div><div class="sceneFooter"><button class="scenePlayAll" type="button" data-action="play-all">▶ 连读介绍</button><span>点击法语单词查词并循环听发音</span></div>`;
  }
  function play(text,lang,all=false) {
    stopAll(true);
    hideDictionaryVisual();
    state.mode = 'scene';
    const token = ++state.token;
    const lines = all ? active.lines.map(x => x.fr) : [text];
    let i = 0;
    setStatus(`法国漫游 · ${active.name} · 朗读中`);
    const next = () => {
      if (state.mode !== 'scene' || state.token !== token) return;
      if (i >= lines.length) {state.mode = null; setStatus(`法国漫游 · ${active.name} · 朗读完成`); return;}
      speakOnce(lines[i++],lang,next,{onerror:() => {state.mode = null; setStatus('设备语音未能播放；请检查系统语音与静音设置。');}});
    };
    next();
  }
  function open() {
    returnFocus = document.activeElement;
    renderChoices();
    renderContent();
    dialog.hidden = false;
    document.body.classList.add('scene-open');
    document.querySelector('#sceneClose').focus();
  }
  function close() {
    if (dialog.hidden) return;
    if (state.mode === 'scene' || state.mode === 'word' || state.mode === 'word-preview') stopAll(true);
    hideDictionaryVisual();
    dialog.hidden = true;
    document.body.classList.remove('scene-open');
    lookup = null;
    returnFocus?.focus();
  }
  choices.onclick = event => {
    const button = event.target.closest('[data-scene]');
    if (!button) return;
    selected = button.dataset.scene;
    if (selected !== 'none') active = scenes.find(s => s.id === selected);
    applyBackground();
    renderContent();
  };
  content.onclick = event => {
    const word = event.target.closest('[data-word]');
    if (word) {
      const line = active.lines[Number(word.closest('.sceneLine').dataset.line)];
      lookup = {title:active.name,fr:line.fr,zh:line.zh,gloss:line.gloss};
      startWordLoop(word.dataset.word);
      return;
    }
    const button = event.target.closest('[data-action]');
    if (!button) return;
    const action = button.dataset.action;
    if (action === 'play-all') {play('', 'fr-FR', true); return;}
    const article = button.closest('.sceneLine');
    const line = active.lines[Number(article.dataset.line)];
    if (action === 'play-fr') play(line.fr,'fr-FR');
    if (action === 'play-zh') play(line.zh,'zh-CN');
    if (action === 'explain') {
      const box = article.querySelector('.sceneExplanation');
      box.hidden = !box.hidden;
      button.setAttribute('aria-expanded',String(!box.hidden));
      button.textContent = box.hidden ? '句子讲解' : '收起讲解';
    }
  };
  dialog.onclick = event => {if (event.target === dialog) close();};
  document.querySelector('#sceneOpen').onclick = open;
  document.querySelector('#sceneBanner').onclick = open;
  document.querySelector('#sceneClose').onclick = close;
  document.addEventListener('keydown',event => {
    if (dialog.hidden) return;
    if (event.key === 'Escape' && !document.querySelector('#dictionary').classList.contains('show')) {event.preventDefault();event.stopImmediatePropagation();close();}
    if (event.key === 'Tab' && !document.querySelector('#dictionary').classList.contains('show')) {
      const focusable = [...dialog.querySelectorAll('button,a[href]')].filter(el => el.getClientRects().length);
      if (event.shiftKey && document.activeElement === focusable[0]) {event.preventDefault();focusable.at(-1).focus();}
      else if (!event.shiftKey && document.activeElement === focusable.at(-1)) {event.preventDefault();focusable[0].focus();}
    }
  },true);
  applyBackground();
  window.FranceScenes = {lookupContext(raw) {
    if (dialog.hidden || !lookup) return null;
    const key = String(raw).toLocaleLowerCase('fr').replace(/[’']/g,"'");
    return {title:lookup.title,fr:lookup.fr,zh:lookup.zh,meaning:lookup.gloss[key] || ''};
  }};
})();
