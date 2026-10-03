/* Further event-rich bilingual reading for the sixteen stages. Each row is French | Chinese | language note. */
const parseHistoryDeep = raw => raw.trim().split('\n').map(row => row.trim().split('|'));
window.FRANCE_HISTORY_DEEP = {
  0: parseHistoryDeep(`Massalia, fondée par des Grecs vers 600 avant notre ère, reliait le littoral gaulois aux échanges méditerranéens.|约公元前 600 年希腊人建立的马赛，将高卢海岸接入地中海贸易网络。|fondée 是过去分词，补充 Massalia 的来历。
Les peuples gaulois possédaient des institutions, des monnaies et des réseaux commerciaux différents selon les régions.|高卢各部在制度、铸币和商贸网络方面存在地区差异。|selon 表示“依据、因……而异”。
Rome a d'abord dominé une province du sud avant de chercher à contrôler toute la Gaule.|罗马先控制高卢南部行省，然后才试图掌控整个高卢。|d'abord...avant de... 表示先后步骤。
En 58 avant notre ère, César a utilisé les mouvements des Helvètes comme point de départ de ses campagnes.|公元前 58 年，恺撒以赫尔维蒂人的迁徙为军事行动的起点。|comme point de départ 表示“作为起点”。
Les sièges, les négociations et les alliances ont autant compté que les batailles rangées.|围城、谈判和结盟与正面会战同样重要。|autant que 表示“与……同样”。
La victoire de César à Alésia en 52 avant notre ère a brisé une grande coalition, sans achever immédiatement toutes les résistances.|公元前 52 年阿莱西亚之战击溃一大联盟，却未立即结束所有抵抗。|sans + 动词原形表示“但未……”。
Les destructions et les déplacements de population ont pesé lourdement sur les communautés conquises.|破坏与人口迁移使被征服社群付出沉重代价。|ont pesé sur 表示“对……造成负担”。
Les récits romains éclairent cette histoire, mais donnent rarement la parole directe aux vaincus.|罗马记述帮助我们了解这段历史，却很少让战败者直接发声。|mais 引出史料的局限。
Le mot « Gaule » désigne un ensemble de territoires et non un État national déjà constitué.|“高卢”指多片地区，并非一个已成形的民族国家。|et non 用于纠正误解。
L'archéologie permet de comparer les textes de César avec les traces des habitats, des objets et des fortifications.|考古可将恺撒的叙述与聚落、器物和防御工事的遗迹对照。|comparer A avec B 表示比较两类证据。`),
  1: parseHistoryDeep(`Lugdunum a été fondée en 43 avant notre ère et a pris une place importante dans l'administration des Gaules.|卢格杜努姆建于公元前 43 年，后来在高卢行政中占据重要地位。|a été fondée 是被动语态。
Les routes romaines facilitaient le déplacement des soldats, des marchandises et des décisions impériales.|罗马道路便利了军队、货物和帝国命令的流通。|三个 des 引出并列宾语。
Les élites locales ont souvent conservé une influence en participant aux institutions municipales.|地方精英常借参与城市机构保有影响力。|en + 现在分词表示方式。
La diffusion du latin fut inégale et les langues gauloises n'ont pas disparu partout au même rythme.|拉丁语传播并不均衡，高卢语言也非在各地同时消失。|ne...pas partout 表示“并非处处”。
Les thermes, les aqueducs et les théâtres montrent des investissements urbains, mais ils ne résument pas la vie des campagnes.|浴场、水道和剧场体现城市建设，却不足以概括乡村生活。|mais 引出城市遗迹与整体社会的区别。
L'édit de 212 a étendu la citoyenneté romaine à beaucoup d'hommes libres de l'Empire.|212 年的法令将罗马公民权扩大至帝国内众多自由男子。|a étendu...à... 表示将权利扩展给某群体。
L'économie reposait aussi sur le travail agricole, l'artisanat, les échanges et différentes formes de dépendance.|经济同样依赖农业劳动、手工业、交换及不同形式的人身依附。|reposer sur 表示“以……为基础”。
Le christianisme s'est implanté progressivement, sans remplacer d'un seul coup les pratiques religieuses antérieures.|基督教逐步扎根，并未一下取代早期宗教实践。|sans + 动词原形限制前句含义。
Au cours de l'Antiquité tardive, les frontières et les centres de pouvoir ont été réorganisés plusieurs fois.|古代晚期，边界和权力中心经历多次重组。|au cours de 表示“在……期间”。
Parler de « romanisation » ne doit pas faire oublier que les habitants ont aussi adapté et transformé les modèles romains.|谈“罗马化”不能忘记当地居民也主动改造了罗马模式。|ne doit pas faire oublier 表示“不能让人忘记”。`),
  2: parseHistoryDeep(`Au quatrième siècle, les autorités romaines ont intégré certains groupes germaniques dans leurs armées et leurs accords politiques.|4 世纪，罗马当局把部分日耳曼群体纳入军队及政治协定。|ont intégré...dans... 表示纳入。
La Gaule a connu des invasions et des guerres civiles, mais aussi des arrangements négociés entre chefs.|高卢经历入侵和内战，也出现首领间的协商安排。|mais aussi 补充另一面。
En 418, des Wisigoths ont reçu un établissement dans le sud-ouest de la Gaule dans le cadre d'un accord avec l'Empire.|418 年，西哥特人在与帝国协议框架下获得高卢西南部的定居地。|dans le cadre de 表示“在……框架下”。
Les structures impériales n'ont pas cessé de fonctionner partout en même temps.|帝国机构并非在各地同时停止运作。|ne...pas partout en même temps 避免一刀切。
En 476, la déposition du dernier empereur d'Occident est devenue un repère chronologique, non une disparition instantanée du monde romain.|476 年西罗马末代皇帝被废成为年代标志，而非罗马世界瞬间消失。|non 表示否定后面的简单化解释。
Les évêques et les aristocrates gallo-romains ont parfois servi d'intermédiaires entre anciens et nouveaux pouvoirs.|主教和高卢—罗马贵族有时成为新旧权力之间的中介。|servir d'intermédiaire 表示充当中介。
Les Francs formaient plusieurs groupes dont les chefs entretenaient des rapports variables avec Rome.|法兰克人由多个群体组成，各首领与罗马的关系并不相同。|dont 引出这些群体的首领。
Les lois, les titres et les habitudes administratives ont souvent été réemployés par les royaumes qui se formaient.|形成中的王国常沿用旧有法律、头衔和行政习惯。|qui 引导关系从句，修饰 royaumes。
Cette période ne se comprend ni comme une simple chute ni comme une transition paisible.|这一时期既不能简化为单纯崩溃，也不能描述成和平过渡。|ni...ni... 表示既不……也不……。
Comparer les sources écrites aux découvertes archéologiques aide à distinguer les ruptures des continuités.|对照文献与考古发现，有助于区分断裂与延续。|aider à + 动词原形表示帮助。`),
  3: parseHistoryDeep(`Clovis a d'abord gouverné un ensemble franc relativement limité avant d'étendre son autorité.|克洛维起初统治的法兰克地盘相对有限，后来才扩张权力。|d'abord...avant de... 表示扩张过程。
La victoire sur Syagrius vers 486 lui a ouvert l'accès à une grande partie du nord de la Gaule.|约 486 年战胜西阿格里乌斯，使他取得高卢北部大片地区。|ouvrir l'accès à 表示获得进入或控制机会。
La bataille de Vouillé en 507 a affaibli les Wisigoths au nord des Pyrénées.|507 年武耶之战削弱了比利牛斯山以北的西哥特势力。|a affaibli 是“削弱”的复合过去时。
Les récits de sa conversion ont été écrits après les faits et ne permettent pas de fixer aisément une date unique.|其皈依故事写于事件之后，难以据此确定唯一准确日期。|ne permettent pas de 表示“不足以”。
Après la mort de Clovis en 511, ses fils se sont partagé des territoires sans effacer l'idée d'un héritage dynastique commun.|511 年克洛维去世后，诸子分地，但共同的王朝继承观念并未消失。|sans effacer 表示“不抹去”。
Les capitales et les lieux de pouvoir mérovingiens ont varié avec les partages et les rivalités.|墨洛温时代的都城与权力中心随分治和竞争而变化。|avec 表示“随着”。
Les reines pouvaient exercer une influence politique considérable, même si les sources les décrivaient souvent de façon hostile.|王后可能拥有重要政治影响力，尽管史料常以敌意描绘她们。|même si 引出让步。
Les grands propriétaires et les évêques négociaient avec les rois et défendaient leurs propres intérêts.|大地主和主教与国王协商，同时维护自身利益。|两个动词并列，说明双重角色。
La royauté ne contrôlait pas chaque région de manière uniforme ni sans l'aide des aristocraties locales.|王权对各地区的控制并不均衡，也离不开地方贵族。|ne...pas...ni... 构成双重否定。
Qualifier cette époque de simple déclin masquerait la création de nouveaux réseaux politiques et religieux.|把这一时期只称为衰落，会遮蔽新政治与宗教网络的形成。|条件式 masquerait 表示假设后果。`),
  4: parseHistoryDeep(`Le maire du palais gérait d'abord la maison du roi, puis certains titulaires ont acquis un pouvoir militaire et politique.|宫相最初管理王室事务，后来部分宫相取得军政大权。|d'abord...puis... 表示职位演变。
La famille des Pippinides a construit sa puissance grâce aux terres, aux clientèles et aux alliances.|丕平家族依靠土地、依附网络和联盟建立实力。|grâce à 表示促成原因。
Charles Martel a consolidé ce pouvoir au début du huitième siècle, sans se faire couronner roi.|查理·马特在 8 世纪初巩固权力，却没有称王。|sans se faire couronner 表示“未让自己加冕”。
La bataille de 732 près de Poitiers fut importante, mais son sens a été amplifié par des récits postérieurs.|732 年普瓦捷附近的战役重要，但后世叙事放大了其象征意义。|mais 引出评价的限制。
Les campagnes contre divers adversaires ont donné aux maires du palais des ressources et des soutiens supplémentaires.|对多个对手的军事行动使宫相取得更多资源和支持者。|ont donné...à... 表示给予。
Pépin le Bref a demandé une légitimité politique et religieuse avant de déposer le dernier roi mérovingien.|矮子丕平在废黜末代墨洛温国王前，寻求政治与宗教上的正当性。|avant de 表示先后顺序。
En 751, son accession au trône a transformé une domination de fait en royauté dynastique.|751 年丕平登基，把事实上的优势转化为王朝王权。|transformer A en B 表示转化。
L'alliance avec la papauté a renforcé le nouveau régime, mais elle créait aussi des obligations réciproques.|与教廷结盟巩固新政权，同时也产生双方义务。|mais...aussi 补充代价。
Les campagnes de Pépin en Italie ont contribué à la formation d'un pouvoir territorial pontifical.|丕平在意大利的军事行动帮助教廷形成领土权力。|contribuer à 表示促成。
Le changement de dynastie n'a pas supprimé les négociations permanentes avec les grands du royaume.|王朝更替并未消除国王与大贵族持续协商的需要。|n'a pas supprimé 是复合过去时否定。`),
  5: parseHistoryDeep(`Charlemagne a hérité d'un royaume franc qu'il a encore agrandi par des campagnes militaires.|查理曼继承法兰克王国，又通过军事行动进一步扩张。|qu'il a agrandi 引出关系从句。
La soumission de la Saxe a demandé des décennies et a comporté des massacres et des conversions forcées.|征服萨克森耗时数十年，伴随屠杀与强制皈依。|a demandé 表示“耗费”。
Le royaume lombard d'Italie est passé sous son contrôle après sa campagne de 774.|774 年远征后，意大利伦巴第王国落入他的控制。|après 引出时间。
En 800, le pape l'a couronné empereur à Rome, mais les interprétations de cette cérémonie ont varié.|800 年教皇在罗马为他加冕为皇帝，但对仪式的解释历来不同。|mais 引出解释差异。
Le palais d'Aix-la-Chapelle était un centre de gouvernement, sans être une capitale au sens moderne.|亚琛宫廷是统治中心，但并非现代意义上的固定首都。|sans être 表示“但不是”。
Des savants et des clercs ont participé à la réforme de l'écriture et de l'enseignement.|学者和教士参与了书写方式和教育改革。|ont participé à 表示参与。
Les capitulaires fixaient des objectifs, tandis que les comtes et les évêques en négociaient l'application locale.|敕令确立目标，而伯爵和主教在地方落实时仍会协商。|tandis que 表示同时或对照。
Les envoyés du souverain inspectaient les autorités locales, mais leurs moyens restaient limités.|君主使节巡查地方官员，但其能力仍有限。|leurs 指前面的使节。
Les échanges de manuscrits ont relié des monastères éloignés et favorisé la transmission de textes anciens.|手稿交换联系遥远修道院，促进古代文本流传。|favoriser 表示促进。
La cohésion de cet ensemble dépendait de relations personnelles que ses successeurs eurent du mal à maintenir.|帝国凝聚力依赖私人关系，继承者很难长期维持。|que 引导关系从句，修饰 relations。`),
  6: parseHistoryDeep(`Louis le Pieux a reçu un vaste empire dont l'unité reposait sur des compromis fragiles.|虔诚者路易继承广阔帝国，其统一依赖脆弱妥协。|dont 引出帝国的统一基础。
Ses projets de succession ont été remis en cause par la naissance de nouveaux héritiers et par les ambitions de ses fils.|新继承人的出生及诸子野心打乱了他的继承安排。|ont été remis en cause 是被动结构。
Les guerres civiles ont mobilisé des aristocrates qui changeaient parfois de camp.|内战动员了贵族，他们有时也会改变阵营。|qui 引导关系从句。
En 842, les serments de Strasbourg ont scellé une alliance entre deux frères contre un troisième.|842 年斯特拉斯堡誓言确立两兄弟针对第三人的联盟。|entre...contre... 表示结盟与对抗。
En 843, le traité de Verdun a réparti des territoires entre Charles, Louis et Lothaire.|843 年凡尔登条约在查理、路易和洛泰尔之间划分领地。|répartir...entre... 表示在多人之间分配。
La Francie médiane associait des régions éloignées et difficiles à administrer comme un seul ensemble.|中法兰克包括彼此遥远的地区，难以作为单一整体治理。|difficiles à + 动词原形表示“难以”。
Les royaumes ont continué à se diviser, à se réunir et à changer de frontière après 843.|843 年后诸王国继续分合，边界持续变动。|三个 à 并列动作。
Les langues et les institutions ne sont pas devenues françaises ou allemandes du jour au lendemain.|语言与制度并非一夜之间就变成“法国”或“德国”的。|du jour au lendemain 表示一夜之间。
Les liens de fidélité traversaient souvent les zones définies par les traités.|效忠关系常横跨条约划定的区域。|traversaient 是描述持续情况的未完成过去时。
Faire de Verdun une naissance immédiate de la France et de l'Allemagne projette les nations modernes sur le neuvième siècle.|把凡尔登说成法德两国立即诞生，是将现代民族国家观念投射到 9 世纪。|faire de A B 表示“把 A 当作 B”。`),
  7: parseHistoryDeep(`Les expéditions vikings suivaient les fleuves, où des villes et des monastères étaient vulnérables.|维京远征沿河推进，沿岸城市和修道院容易受到袭击。|où 引导地点关系从句。
Les souverains ont tenté de défendre les vallées, mais dépendaient largement des forces locales.|君主试图防守河谷，却高度依赖地方武装。|mais 引出王权的限制。
L'accord de 911 a reconnu l'autorité de Rollon dans une partie de la basse Seine.|911 年的协议承认罗洛在塞纳河下游部分地区的权力。|dans une partie de 表示局部范围。
La principauté normande s'est ensuite développée grâce à des alliances, des conquêtes et des institutions locales.|诺曼底公国随后依靠联盟、征服和地方制度发展。|grâce à 引出多项因素。
En 1066, le duc Guillaume a conquis l'Angleterre sans cesser d'être un puissant seigneur en Normandie.|1066 年诺曼底公爵威廉征服英格兰，但仍是诺曼底强大领主。|sans cesser de 表示“仍然”。
Les premiers Capétiens ont été choisis dans un monde politique où les grands princes conservaient beaucoup d'autonomie.|早期卡佩国王产生于大诸侯仍高度自治的政治世界。|où 引导背景关系从句。
Élu en 987, Hugues Capet ne gouvernait directement qu'une zone limitée autour de Paris et d'Orléans.|987 年当选的于格·卡佩仅直接统治巴黎与奥尔良附近有限地区。|ne...que 表示“仅”。
Faire sacrer son fils de son vivant aidait à stabiliser une succession qui n'était pas automatiquement acquise.|让儿子在生前加冕，有助于稳定并非天然稳固的继承。|de son vivant 表示“在世时”。
Les châteaux et les fidélités seigneuriales comptaient autant que les ordres royaux dans la vie politique.|在政治生活中，城堡和领主效忠关系与王命同样重要。|autant que 表示同等重要。
La montée des Capétiens fut lente, régionale et dépendante de compromis successifs.|卡佩王权的上升缓慢、地区差异明显，依靠连续妥协。|三个形容词并列描述同一过程。`),
  8: parseHistoryDeep(`Au douzième siècle, les Capétiens ont renforcé leurs liens avec les villes, l'Église et certains vassaux.|12 世纪卡佩王朝加强与城市、教会及部分封臣的联系。|ont renforcé...avec... 表示加强联系。
Philippe Auguste a repris la Normandie au roi d'Angleterre Jean sans Terre au début du treizième siècle.|13 世纪初腓力二世从英王约翰手中夺回诺曼底。|reprendre...à... 表示从某人手中收回。
La victoire de Bouvines en 1214 a consolidé sa position face à une coalition de princes.|1214 年布汶之战巩固了腓力二世面对诸侯联盟的地位。|face à 表示“面对”。
Des baillis et des sénéchaux représentaient le pouvoir royal dans des régions de plus en plus nombreuses.|总管和司法官在越来越多地区代表王权。|de plus en plus 表示逐渐增加。
Les villes ont obtenu des chartes et des privilèges, sans devenir pour autant indépendantes du roi.|城市取得特许状与权利，但并未因此完全独立于王权。|sans...pour autant 表示“但并不因此”。
Sous Louis IX, la justice royale a gagné en prestige, tout en coexistant avec d'autres tribunaux.|路易九世时期王室司法威望上升，同时仍与其他法庭并存。|tout en + 现在分词表示同时。
Les croisades ont renforcé l'image pieuse du roi, mais elles ont aussi entraîné violences et pertes humaines.|十字军东征强化国王的虔敬形象，也造成暴力和生命损失。|mais...aussi 引出另一面。
Les paysans vivaient sous des conditions très différentes selon les terres, les seigneurs et les coutumes.|农民生活条件因土地、领主和习惯法而差异很大。|selon 列出差异因素。
L'essor des foires et des métiers urbains a relié davantage les marchés régionaux.|集市和城市行业的发展使区域市场联系更紧密。|davantage 表示“更多”。
La croissance monarchique n'a pas supprimé les conflits entre le roi, la noblesse et le clergé.|君权增长并未消除国王、贵族与教士之间的冲突。|n'a pas supprimé 是复合过去时否定。`),
  9: parseHistoryDeep(`La crise de succession de 1328 a porté Philippe de Valois au trône, tandis que le roi d'Angleterre contestait ses droits.|1328 年继承危机使瓦卢瓦的腓力登基，英王则争议其继承权。|tandis que 引出对立立场。
La guerre de Cent Ans fut une succession de campagnes, de trêves et de négociations plutôt qu'un combat continu.|百年战争是一系列战役、休战和谈判，而非连续不断的战斗。|plutôt que 表示“而不是”。
Les défaites de Crécy en 1346 et de Poitiers en 1356 ont ébranlé la monarchie française.|1346 年克雷西及 1356 年普瓦捷的失利动摇法国王权。|ont ébranlé 表示“动摇”。
La peste arrivée en 1348 a aggravé les pertes humaines et bouleversé les rapports économiques.|1348 年传入的瘟疫加重人口损失并改变经济关系。|两个动词并列说明影响。
Les impôts de guerre et les révoltes ont montré que les civils supportaient une grande part du conflit.|战争税和叛乱表明平民承担了冲突的大部分代价。|que 引出宾语从句。
Charles V a repris des territoires par une stratégie de sièges et de prudence, sans chercher toujours une grande bataille.|查理五世以围城和审慎战略收复领土，并不总追求大会战。|sans chercher 表示“并不追求”。
La défaite d'Azincourt en 1415 a ouvert une nouvelle crise pour la dynastie des Valois.|1415 年阿金库尔战败使瓦卢瓦王朝再陷危机。|a ouvert 表示“开启”。
Le traité de Troyes de 1420 a contesté les droits du futur Charles VII, mais son application est restée disputée.|1420 年特鲁瓦条约否认未来查理七世的权利，但实施仍充满争议。|mais 引出条约与现实的差别。
Jeanne d'Arc a contribué au siège d'Orléans et au sacre de Charles VII en 1429, sans agir seule.|1429 年贞德助力奥尔良解围与查理七世加冕，但她并非独自行动。|sans agir seule 限定英雄叙事。
La reprise de Bordeaux en 1453 marque habituellement la fin des grandes opérations, tandis que les rivalités franco-anglaises ont continué.|1453 年收复波尔多通常标记大战结束，但法英对抗并未完全停止。|tandis que 引出同时存在的延续。`),
  10: parseHistoryDeep(`Les rois de la fin du quinzième siècle ont cherché à peser en Italie, ce qui a prolongé des guerres coûteuses.|15 世纪末的国王试图在意大利扩张影响，延续了代价高昂的战争。|ce qui 指代前句并引出结果。
La victoire de François Ier à Marignan en 1515 a nourri son prestige, mais ne lui a pas assuré une domination durable en Italie.|弗朗索瓦一世 1515 年马里尼亚诺获胜增加声望，却未确保意大利的持久统治。|mais 引出战果限制。
Le château de Chambord manifeste les ambitions royales et l'influence de formes artistiques nouvelles.|香波堡体现王室雄心与新艺术形式的影响。|manifestER 表示“体现”。
L'imprimerie a accéléré la circulation des livres, des débats religieux et des textes politiques.|印刷术加速书籍、宗教争论与政治文本传播。|三个名词短语并列。
L'ordonnance de Villers-Cotterêts de 1539 a imposé le français dans de nombreux actes de justice et d'administration.|1539 年《维莱-科特雷敕令》要求许多司法与行政文书使用法语。|imposer...dans... 表示规定某领域使用。
Cette mesure n'a pas immédiatement remplacé les langues parlées dans toutes les régions du royaume.|这项规定并未立即取代王国各地的口语。|n'a pas immédiatement 表示“未立即”。
Des humanistes ont relu les auteurs anciens et discuté des méthodes d'éducation.|人文主义者重读古典作者并讨论教育方法。|两个动词并列。
Les échanges avec les mondes atlantiques se sont développés, entraînant aussi des violences coloniales.|与大西洋世界的交流增加，同时也带来殖民暴力。|entraînant 是现在分词，说明后果。
La Réforme protestante a divisé des communautés et suscité des réponses catholiques diverses.|宗教改革分裂了部分社群，也引发多样的天主教回应。|a divisé 与 suscité 并列。
La Renaissance française associe donc innovations artistiques, rivalités militaires et tensions religieuses.|法国文艺复兴因此同时包含艺术创新、军事竞争与宗教紧张。|associer A, B et C 表示将三方面并置。`),
  11: parseHistoryDeep(`À partir de 1562, les guerres de Religion ont opposé des coalitions changeantes plutôt que deux blocs toujours homogènes.|自 1562 年起，宗教战争中的联盟不断变化，并非两个始终整齐对立的集团。|plutôt que 用于纠正简单二分。
La noblesse, les villes et les puissances étrangères ont poursuivi des objectifs parfois distincts.|贵族、城市与外国势力有时各有目标。|parfois 表示并非总是相同。
Le massacre de la Saint-Barthélemy en 1572 a commencé à Paris puis s'est étendu à d'autres villes.|1572 年圣巴托罗缪日屠杀始于巴黎，后波及其他城市。|puis 表示事件先后。
Les violences ont frappé des familles et des communautés bien au-delà des dirigeants politiques.|暴力波及远超政治领袖范围的家庭与社群。|bien au-delà de 表示远超。
La Ligue catholique a contesté l'autorité royale lorsque la succession au trône est devenue incertaine.|王位继承不明朗时，天主教联盟挑战王权。|lorsque 引出时势条件。
Henri de Navarre est devenu roi sous le nom d'Henri IV et s'est converti au catholicisme.|纳瓦拉的亨利继位为亨利四世，并皈依天主教。|sous le nom de 表示“以……之名”。
L'édit de Nantes de 1598 a accordé aux protestants des droits précis, sans établir une égalité religieuse complète.|1598 年《南特敕令》给予新教徒特定权利，却未确立宗教完全平等。|sans établir 表示“但未建立”。
L'application de l'édit a dépendu des lieux, des autorités et des rapports de force locaux.|敕令落实取决于地区、官员及当地力量对比。|dépendre de 表示“取决于”。
L'assassinat d'Henri IV en 1610 a montré que la pacification restait fragile.|1610 年亨利四世遇刺表明和平仍脆弱。|que 引导宾语从句。
La mémoire de ces guerres fut ensuite utilisée pour défendre des projets politiques très différents.|后世借宗教战争记忆支持截然不同的政治主张。|fut utilisée 是被动语态。`),
  12: parseHistoryDeep(`Richelieu a renforcé l'action de la monarchie sous Louis XIII, mais il dépendait toujours des alliances de cour.|黎塞留在路易十三时期强化王权，却仍依赖宫廷联盟。|mais 引出权力的限制。
La Fronde de 1648 à 1653 a révélé des résistances parlementaires, aristocratiques et populaires.|1648 至 1653 年的投石党运动显露司法机构、贵族和平民的多种反抗。|de...à... 表示时间范围。
Après la mort de Mazarin en 1661, Louis XIV a gouverné sans principal ministre.|1661 年马扎然去世后，路易十四不再任用首席大臣。|sans 引出统治方式。
En 1682, la cour s'est installée à Versailles, où cérémonies et accès au roi étaient soigneusement organisés.|1682 年宫廷迁往凡尔赛，仪式和接近国王的机会均受到严密安排。|où 引导地点关系从句。
Les intendants ont relayé des décisions royales, mais la monarchie devait encore négocier avec les pouvoirs locaux.|督办官传达王命，但王室仍须与地方势力协商。|mais 引出中央与地方的张力。
La révocation de l'édit de Nantes en 1685 a accru la persécution des protestants et poussé certains à l'exil.|1685 年撤销《南特敕令》加剧对新教徒迫害，促使一些人流亡。|deux verbes 描述两种后果。
La même année, le Code noir a organisé juridiquement l'esclavage dans les colonies françaises.|同年《黑法典》在法国殖民地以法律形式规范奴隶制。|la même année 指 1685 年。
Les longues guerres ont exigé impôts, emprunts et sacrifices, souvent supportés inégalement.|长期战争需要税款、借贷和牺牲，负担分配并不平等。|souvent supportés 修饰 sacrifices 等负担。
Au dix-huitième siècle, les salons, les académies et les journaux ont élargi certains débats publics.|18 世纪沙龙、学院和报刊扩大了部分公共讨论。|ont élargi 表示“扩大”。
La crise financière de la monarchie a finalement rendu une réforme des impôts de plus en plus urgente.|王室财政危机最终使税制改革愈发迫切。|rendre A + 形容词表示“使 A 变得……”。`),
  13: parseHistoryDeep(`La dette de l'État et les privilèges fiscaux ont rendu difficile une réforme acceptée par tous les groupes.|国家债务和税收特权使各方接受的改革难以实现。|rendre + 形容词表示“使……难”。
En mai 1789, les États généraux se sont réunis à Versailles après une longue interruption.|1789 年 5 月，长期未召开过的三级会议在凡尔赛举行。|après 引出长期中断这一背景。
Le tiers état s'est proclamé Assemblée nationale, affirmant représenter la nation entière.|第三等级宣布成立国民议会，声称代表整个民族。|affirmant 是现在分词，说明其主张。
Le serment du Jeu de paume a engagé des députés à ne pas se séparer avant d'avoir donné une constitution au royaume.|网球厅宣誓使代表承诺，在制定宪法前不解散。|avant d'avoir donné 表示在完成某事之前。
La prise de la Bastille le 14 juillet a symbolisé l'intervention populaire dans la crise politique.|7 月 14 日攻占巴士底狱象征人民介入政治危机。|a symbolisé 表示“象征”。
La nuit du 4 août a lancé l'abolition des privilèges, dont la mise en œuvre fut plus complexe que l'annonce.|8 月 4 日之夜启动废除特权，实际落实比宣告复杂。|dont 引出该改革的实施。
La Déclaration des droits de l'homme et du citoyen a énoncé des principes nouveaux, sans accorder les mêmes droits politiques à tous.|《人权和公民权宣言》提出新原则，却未给予所有人同等政治权利。|sans accorder 表示“但未给予”。
La Constitution de 1791 a établi une monarchie constitutionnelle fondée sur une séparation des pouvoirs.|1791 年宪法确立以权力分立为基础的君主立宪制。|fondée sur 表示“以……为基础”。
La fuite de Varennes en 1791 a gravement érodé la confiance envers Louis XVI.|1791 年瓦雷讷出逃严重损害了民众对路易十六的信任。|envers 表示“对某人”。
La guerre, les insurrections et la journée du 10 août 1792 ont finalement conduit à la chute de la monarchie.|战争、起义和 1792 年 8 月 10 日事件最终导致君主制倒台。|conduire à 表示“导致”。`),
  14: parseHistoryDeep(`La Convention nationale a proclamé la République en septembre 1792 dans un contexte de guerre.|国民公会于 1792 年 9 月在战争背景下宣布共和。|dans un contexte de 表示“在……背景下”。
L'exécution de Louis XVI en janvier 1793 a aggravé les tensions avec les monarchies européennes.|1793 年 1 月处决路易十六加剧了与欧洲君主国的紧张关系。|a aggravé 表示“加剧”。
La levée en masse a mobilisé des citoyens pour la guerre, tout en imposant de lourdes contraintes aux familles.|全民征兵动员公民参战，也使家庭承担沉重负担。|tout en + 现在分词表示同时。
L'insurrection vendéenne et d'autres résistances ont donné lieu à des violences graves des deux côtés.|旺代起义和其他反抗引发双方严重暴力。|donner lieu à 表示“引起”。
Le Comité de salut public a concentré des pouvoirs d'urgence, sans gouverner seul tous les aspects du pays.|救国委员会集中紧急权力，却未独自掌控国家所有事务。|sans gouverner seul 限定其权力范围。
Le Tribunal révolutionnaire et la loi des suspects ont facilité les arrestations et les condamnations.|革命法庭与嫌疑人法令便利了逮捕和定罪。|两个主语共同搭配 ont facilité。
En 1794, la Convention a aboli l'esclavage colonial, dans un contexte marqué aussi par l'insurrection de Saint-Domingue.|1794 年国民公会废除殖民地奴隶制，这也与圣多明各起义密切相关。|dans un contexte marqué par 引出背景。
La chute de Robespierre en thermidor a mis fin à une phase du gouvernement révolutionnaire, mais pas aux conflits.|热月政变推翻罗伯斯庇尔，结束革命政府的一个阶段，但冲突未止。|mais pas 表示“但并未”。
La Constitution de l'an III a mis en place le Directoire et limité le suffrage à certaines catégories.|共和三年宪法建立督政府，并将选举权限制于部分群体。|mettre en place 表示“建立”。
Les crises économiques, les coups de force et la guerre ont fragilisé le régime jusqu'en 1799.|经济危机、政变与战争使督政府到 1799 年愈发脆弱。|jusqu'en 表示时间终点。`),
  15: parseHistoryDeep(`Le coup d'État du 18 Brumaire en 1799 a porté Bonaparte au pouvoir dans le cadre du Consulat.|1799 年雾月十八日政变使波拿巴在执政府体制下掌权。|dans le cadre de 表示“在……制度下”。
Le régime a réorganisé les préfectures et renforcé le contrôle du centre sur les départements.|政权重组省长制度，强化中央对各省的控制。|sur 表示作用对象。
Le Concordat de 1801 a redéfini les relations entre l'État et l'Église catholique.|1801 年政教协定重新界定国家与天主教会关系。|entre A et B 表示两者之间。
Le Code civil de 1804 a unifié de nombreuses règles, tout en maintenant une forte inégalité juridique entre hommes et femmes.|1804 年《民法典》统一许多规则，同时维持明显的男女法律不平等。|tout en + 现在分词表示并存。
En 1802, le pouvoir de Bonaparte a rétabli l'esclavage dans plusieurs colonies où il avait été aboli.|1802 年波拿巴政权在此前已废奴的部分殖民地恢复奴隶制。|où 引导地点关系从句。
L'indépendance d'Haïti en 1804 a montré les limites de la reconquête coloniale française.|1804 年海地独立显示法国重新征服殖民地的企图受挫。|a montré 表示“表明”。
Après le sacre impérial de 1804, les victoires militaires ont étendu l'influence française sans assurer une paix durable.|1804 年帝国加冕后，军事胜利扩大法国影响，却未带来持久和平。|sans assurer 表示“但未确保”。
Le blocus continental a voulu affaiblir le commerce britannique, mais il a aussi perturbé les économies européennes.|大陆封锁意在削弱英国贸易，也扰乱欧洲各地经济。|mais...aussi 引出反作用。
La guerre dans la péninsule Ibérique et la campagne de Russie de 1812 ont épuisé hommes et ressources.|伊比利亚半岛战争与 1812 年俄国战役耗尽兵力和资源。|ont épuisé 表示“耗尽”。
Les défaites de 1813 à 1815 ont conduit à l'abdication, aux Cent-Jours puis à Waterloo, sans effacer les réformes ni leurs contradictions.|1813 至 1815 年败战导致退位、百日复辟与滑铁卢，却未抹去改革及其矛盾。|sans effacer 表示“并未抹去”。`)
};
