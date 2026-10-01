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
  const more = {
    eiffel:[
      ["Elle se dresse près de la Seine, au cœur de la capitale.",'它矗立在首都市中心、塞纳河附近。','地点描述','se dresser 表示“矗立”；près de 表示“在……附近”。',{dresse:'矗立',près:'靠近',seine:'塞纳河',capitale:'首都'}],
      ["On peut admirer Paris depuis ses différents étages.",'人们可以从它的不同楼层眺望巴黎。','on + pouvoir + 动词原形','depuis 引出观看的位置；ses 指铁塔的。',{admirer:'欣赏',depuis:'从',différents:'不同的',étages:'楼层'}]],
    soleil:[
      ["Son règne a profondément marqué l'histoire de France.",'他的统治深刻影响了法国历史。','主语 + 复合过去时 + 宾语','a marqué 表示已发生的影响；profondément 修饰动词。',{règne:'统治时期',profondément:'深刻地',marqué:'影响'}],
      ["À Versailles, les arts occupaient une place importante à la cour.",'在凡尔赛，艺术在宫廷生活中占有重要地位。','地点 + 主语 + 未完成过去时','occupaient 描述过去持续的状态；à la cour 指宫廷中。',{arts:'艺术',occupaient:'占据',place:'地位',cour:'宫廷'}]],
    fleur:[
      ["Ce motif apparaît souvent dans les décors de Versailles.",'这一纹样常出现在凡尔赛的装饰中。','主语 + 频率副词 + 地点','souvent 表示“经常”；dans 引出出现的场所。',{motif:'图案',apparaît:'出现',décors:'装饰'}],
      ["Il ne faut pas la confondre avec une simple fleur de jardin.",'不要把它与普通的园艺花卉混为一谈。','il ne faut pas + 动词原形','confondre A avec B 表示“把 A 与 B 混淆”；这里强调纹章意义。',{confondre:'混淆',simple:'普通的',jardin:'花园'}]],
    louvre:[
      ["La pyramide de verre se trouve au centre de sa cour.",'玻璃金字塔位于卢浮宫庭院中央。','主语 + se trouver + 地点','se trouve 表示“位于”；de verre 修饰 pyramide。',{pyramide:'金字塔',verre:'玻璃',centre:'中央',cour:'庭院'}],
      ["Les visiteurs y découvrent des œuvres de différentes époques.",'游客在那里可以欣赏不同时代的艺术作品。','主语 + y + 动词 + 宾语','y 代替前文的地点；des œuvres 指艺术作品。',{visiteurs:'游客',découvrent:'发现；欣赏',œuvres:'作品',époques:'时代'}]],
    versailles:[
      ["La galerie des Glaces est l'une de ses salles les plus célèbres.",'镜厅是宫内最著名的厅室之一。','l’un de + 复数名词','l’une de ses salles les plus célèbres 表示“最著名的厅室之一”。',{galerie:'长廊',glaces:'镜子',salles:'厅室',célèbres:'著名的'}],
      ["Le domaine raconte la vie de la cour et l'histoire du pouvoir royal.",'这处宫苑展现宫廷生活与王权历史。','主语 + 动词 + 两个并列宾语','raconte 在这里引申为“讲述、呈现”；de la cour 修饰 vie。',{domaine:'宫苑',raconte:'讲述',pouvoir:'权力',royal:'王室的'}]],
    'cote-azur':[
      ["Le climat méditerranéen favorise les promenades en bord de mer.",'地中海气候适合沿海漫步。','主语 + 动词 + 宾语','favorise 表示“有利于”；en bord de mer 表示“在海边”。',{climat:'气候',méditerranéen:'地中海的',favorise:'有利于',promenades:'散步'}],
      ["Nice et ses environs mêlent paysages marins et vie urbaine.",'尼斯及周边地区融合了海滨景色与城市生活。','并列主语 + 动词 + 并列宾语','mêlent 表示“混合”；ses 指 Nice 的。',{environs:'周边',mêlent:'融合',marins:'海洋的',urbaine:'城市的'}]],
    bourgogne:[
      ["Ses paysages viticoles racontent une longue histoire du vin.",'当地的葡萄种植景观讲述着悠久的葡萄酒历史。','主语 + 动词 + 宾语','viticoles 表示“与葡萄种植有关的”；du vin 是 de le vin 的缩合。',{paysages:'风景',viticoles:'葡萄种植的',longue:'漫长的',vin:'葡萄酒'}],
      ["Les villages et les marchés permettent de découvrir les produits locaux.",'村庄和集市让人们发现当地物产。','主语 + permettre de + 动词原形','permettent de 表示“使……成为可能”；locaux 与复数 produits 一致。',{marchés:'集市',permettent:'使能够',produits:'产品',locaux:'当地的'}]],
    normandie:[
      ["Les falaises d'Étretat offrent des vues spectaculaires sur la Manche.",'埃特勒塔的海崖提供俯瞰英吉利海峡的壮丽景色。','主语 + 动词 + 宾语 + 地点','sur la Manche 表示“朝向英吉利海峡”；offrent 意为“提供”。',{falaises:'海崖',offrent:'提供',vues:'景色',Manche:'英吉利海峡'}],
      ["La région est aussi connue pour ses pommes et ses fromages.",'这一地区也以苹果和奶酪闻名。','être connu pour + 名词','aussi 表示“也”；connue 与阴性 région 一致。',{région:'地区',connue:'闻名的',pommes:'苹果',fromages:'奶酪'}]],
    pantheon:[
      ["Sa grande coupole domine le paysage du quartier.",'它的大圆顶耸立在街区的景观之上。','主语 + 动词 + 宾语','domine 表示“高耸于……之上”；du 是 de le 的缩合。',{coupole:'穹顶',domine:'高于',paysage:'景观',quartier:'街区'}],
      ["On y découvre des pages importantes de l'histoire française.",'人们在那里可以了解法国历史的重要篇章。','on + y + 动词 + 宾语','y 代替先贤祠；des pages 在这里比喻历史篇章。',{découvre:'了解',pages:'篇章',importantes:'重要的',histoire:'历史'}]],
    'champs-elysees':[
      ["Elle relie la place de la Concorde à la place Charles-de-Gaulle.",'它连接协和广场与戴高乐广场。','relier A à B','relie 表示“连接”；à 引出连接的另一端。',{relie:'连接',place:'广场',Concorde:'协和'}],
      ["L'Arc de Triomphe marque l'extrémité ouest de cette perspective.",'凯旋门标志着这条景观轴线的西端。','主语 + 动词 + 宾语','marque 表示“标志”；ouest 表示“西边”。',{marque:'标志',extrémité:'尽头',ouest:'西部',perspective:'景观轴线'}]]
  };
  for (const scene of scenes) scene.lines.push(...more[scene.id].map(([fr,zh,structure,grammar,gloss]) => ({fr,zh,structure,grammar,gloss})));
  const added = [
    {id:'mont-saint-michel',name:'圣米歇尔山',fr:'Le Mont-Saint-Michel',place:'Normandie · 诺曼底',source:'https://www.abbaye-mont-saint-michel.fr/decouvrir/histoire-du-monument',lines:[
      ["Le Mont-Saint-Michel s'élève au milieu d'une vaste baie.",'圣米歇尔山矗立在一片广阔海湾中央。','主语 + 代词式动词 + 地点','s’élève 表示“耸立”；au milieu de 表示“在……中央”。',{élève:'耸立',milieu:'中央',vaste:'广阔的',baie:'海湾'}],
      ["Une abbaye domine ce rocher depuis le Moyen Âge.",'一座修道院自中世纪起便矗立在这块岩石上。','主语 + 动词 + 宾语 + 时间','depuis 引出延续至今的起点；domine 表示“高于”。',{abbaye:'修道院',domine:'高于',rocher:'岩石',moyen:'中间的',âge:'时代'}],
      ["Les marées transforment régulièrement le paysage autour du mont.",'潮汐不断改变山周围的景观。','主语 + 动词 + 宾语','régulièrement 修饰 transforment，表示“定期地”。',{marées:'潮汐',transforment:'改变',régulièrement:'定期地',paysage:'景观'}],
      ["Ses ruelles conduisent les visiteurs vers l'abbaye.",'狭窄街巷引领游客走向修道院。','主语 + 动词 + 宾语 + 方向','vers 表示“朝向”；ses 指圣米歇尔山的。',{ruelles:'小巷',conduisent:'引领',visiteurs:'游客',abbaye:'修道院'}]]},
    {id:'provence',name:'普罗旺斯',fr:'La Provence',place:'Sud de la France · 法国南部',source:'https://www.france.fr/fr/article/routes-lavande-provence/',lines:[
      ["En Provence, les champs de lavande colorent certains paysages d'été.",'在普罗旺斯，薰衣草田为部分夏日景色染上色彩。','地点 + 主语 + 动词 + 宾语','en Provence 表示“在普罗旺斯”；certains 表示“某些”。',{champs:'田野',lavande:'薰衣草',colorent:'着色',été:'夏天'}],
      ["Les villages de pierre se dressent souvent sur les collines.",'石砌村庄常坐落于山丘之上。','主语 + 代词式动词 + 地点','se dressent 表示“矗立”；souvent 表示“经常”。',{villages:'村庄',pierre:'石头',dressent:'矗立',collines:'山丘'}],
      ["Les marchés présentent des produits et des saveurs de la région.",'市集展示当地物产与风味。','主语 + 动词 + 并列宾语','des produits et des saveurs 是两个并列宾语。',{marchés:'集市',présentent:'展示',produits:'产品',saveurs:'风味'}],
      ["La lavande participe aussi à la vie des habitants et de la nature.",'薰衣草也与当地居民生活和自然环境息息相关。','主语 + participer à + 名词','participe à 表示“参与、作用于”；des 是 de les 的缩合。',{lavande:'薰衣草',participe:'参与',habitants:'居民',nature:'自然'}]]},
    {id:'chambord',name:'香波堡',fr:'Le château de Chambord',place:'Val de Loire · 卢瓦尔河谷',source:'https://www.chambord.org/fr/presentation-le-chateau-de-chambord/',lines:[
      ["François Ier a lancé la construction du château de Chambord en 1519.",'弗朗索瓦一世于 1519 年启动了香波堡的建造。','主语 + 复合过去时 + 宾语 + 时间','a lancé 是 lancer 的复合过去时；en 引出年份。',{lancé:'启动',construction:'建造',château:'城堡'}],
      ["Le château est un grand témoignage de la Renaissance française.",'这座城堡是法国文艺复兴的重要见证。','主语 + être + 表语','témoignage 在这里表示历史见证；de la 修饰 Renaissance。',{témoignage:'见证',renaissance:'文艺复兴',française:'法国的'}],
      ["Son célèbre escalier possède deux rampes qui tournent autour d'un même centre.",'著名的楼梯有两条绕同一中心旋转的梯道。','主句 + qui 引导的关系从句','qui 指代 rampes；autour de 表示“围绕”。',{escalier:'楼梯',possède:'拥有',rampes:'梯道',tournent:'旋转'}],
      ["Depuis les terrasses, on découvre les toits et le vaste domaine.",'从露台上，人们可以欣赏屋顶与广阔园区。','地点前置 + on + 动词 + 宾语','depuis 表示观看起点；vaste 表示“广阔的”。',{terrasses:'露台',découvre:'欣赏',toits:'屋顶',domaine:'园区'}]]},
    {id:'strasbourg',name:'斯特拉斯堡',fr:'Strasbourg',place:'Alsace · 阿尔萨斯',source:'https://www.france.fr/fr/destination/strasbourg/',lines:[
      ["Strasbourg est une ville d'Alsace traversée par l'Ill.",'斯特拉斯堡是一座有伊尔河流经的阿尔萨斯城市。','主语 + être + 表语','traversée 是过去分词作后置定语，与 ville 保持阴性一致。',{ville:'城市',traversée:'穿过',ill:'伊尔河'}],
      ["Dans la Petite France, des maisons à colombages bordent les canaux.",'在“小法兰西”街区，木筋屋沿运河排列。','地点 + 主语 + 动词 + 宾语','à colombages 修饰 maisons；bordent 意为“沿着……排列”。',{maisons:'房屋',colombages:'木筋',bordent:'沿岸排列',canaux:'运河'}],
      ["La cathédrale rappelle le riche patrimoine de la ville.",'大教堂让人想起这座城市丰富的文化遗产。','主语 + 动词 + 宾语','rappelle 表示“使想起”；de la ville 修饰 patrimoine。',{cathédrale:'大教堂',rappelle:'使想起',patrimoine:'遗产',riche:'丰富的'}],
      ["On peut parcourir son centre historique à pied ou en bateau.",'人们可以步行或乘船游览历史城区。','on + pouvoir + 动词原形','à pied 与 en bateau 表示两种出行方式。',{parcourir:'游览',centre:'中心',historique:'历史的',bateau:'船'}]]},
    {id:'bretagne',name:'布列塔尼',fr:'La Bretagne',place:'Atlantique · 大西洋',source:'https://www.france.fr/fr/destination/bretagne/',lines:[
      ["La Bretagne possède un littoral varié et de nombreux phares.",'布列塔尼拥有多样的海岸线和许多灯塔。','主语 + 动词 + 并列宾语','varié 修饰 littoral；de nombreux 修饰复数 phares。',{possède:'拥有',littoral:'海岸线',varié:'多样的',phares:'灯塔'}],
      ["Sur la Côte de Granit Rose, les rochers prennent des teintes cuivrées.",'在玫瑰花岗岩海岸，岩石呈现铜粉色调。','地点 + 主语 + 动词 + 宾语','prennent des teintes 表示“呈现某种色调”。',{granit:'花岗岩',rochers:'岩石',teintes:'色调',cuivrées:'铜色的'}],
      ["Le sentier côtier permet d'explorer des paysages marins.",'海岸步道让人得以探索海滨景色。','主语 + permettre de + 动词原形','permet de 表示“使……能够”；côtier 修饰 sentier。',{sentier:'小路',côtier:'沿海的',explorer:'探索',marins:'海洋的'}],
      ["La mer et les marées rythment la vie de cette région.",'大海与潮汐塑造着这一地区的生活节奏。','并列主语 + 动词 + 宾语','rythment 意为“赋予节奏”；复数主语对应复数动词。',{mer:'大海',marées:'潮汐',rythment:'赋予节奏',région:'地区'}]]},
    {id:'lyon',name:'里昂',fr:'Lyon',place:'Rhône et Saône · 罗讷河与索恩河',source:'https://www.france.fr/fr/destination/lyon/',lines:[
      ["Lyon se situe au confluent du Rhône et de la Saône.",'里昂位于罗讷河与索恩河的汇合处。','主语 + se situer + 地点','au confluent de 表示“在……汇合处”。',{situe:'位于',confluent:'汇合处',rhône:'罗讷河',saône:'索恩河'}],
      ["Le Vieux Lyon conserve des rues qui rappellent la Renaissance.",'里昂老城保留着让人想起文艺复兴时期的街巷。','主句 + qui 引导的关系从句','qui 指代 rues；rappellent 意为“使想起”。',{vieux:'古老的',conserve:'保留',rues:'街道',renaissance:'文艺复兴'}],
      ["Les traboules sont des passages qui traversent des immeubles.",'“穿楼巷”是穿过建筑的通道。','主句 + qui 引导的关系从句','qui 指代 passages；traversent 表示“穿过”。',{traboules:'穿楼巷',passages:'通道',traversent:'穿过',immeubles:'楼房'}],
      ["La ville est également réputée pour sa cuisine et ses marchés.",'这座城市也以美食与市集闻名。','être réputé pour + 名词','réputée 与阴性 ville 一致；également 表示“也”。',{réputée:'闻名的',cuisine:'烹饪；美食',marchés:'市集'}]]}
  ];
  for (const scene of added) {
    scene.lines = scene.lines.map(([fr,zh,structure,grammar,gloss]) => ({fr,zh,structure,grammar,gloss}));
    scenes.push(scene);
  }
  const deeper = {
    eiffel:[
      ["Sa structure de fer était une prouesse technique à la fin du dix-neuvième siècle.",'它的铁结构在十九世纪末是一项技术壮举。','主语 + 未完成过去时 + 表语','était 描述过去的评价；à la fin de 表示“在……末期”。',{structure:'结构',fer:'铁',prouesse:'壮举',siècle:'世纪'}],
      ["Aujourd'hui, les visiteurs peuvent observer la ville sous plusieurs angles.",'如今，游客可以从多个角度俯瞰这座城市。','主语 + pouvoir + 动词原形','peuvent 后接动词原形 observer；sous plusieurs angles 表示“从多个角度”。',{visiteurs:'游客',observer:'观察',plusieurs:'多个',angles:'角度'}]],
    soleil:[
      ["Le roi utilisait les arts pour mettre en scène son pouvoir.",'国王借助艺术展示自己的权力。','主语 + 未完成过去时 + 目的状语','utilisait 描述过去的惯常做法；pour 后接动词原形表目的。',{utilisait:'使用',arts:'艺术',scène:'舞台',pouvoir:'权力'}],
      ["À la cour, les nobles devaient respecter des règles précises.",'在宫廷里，贵族必须遵守明确的礼仪规则。','地点 + 主语 + devoir + 动词原形','devaient 表示过去的义务；respecter 意为“遵守”。',{nobles:'贵族',devaient:'必须',respecter:'遵守',règles:'规则'}]],
    fleur:[
      ["On retrouve ce signe sur des portraits et des objets royaux.",'在王室肖像和器物上都能找到这一标志。','on + 动词 + 宾语 + 地点','retrouve 表示“再次看到、找到”；sur 引出图案所在位置。',{retrouve:'找到',signe:'标志',portraits:'肖像',objets:'器物'}],
      ["Dans ce contexte, la fleur de lys représente surtout la royauté.",'在这一语境里，百合花纹章主要代表王权。','地点状语 + 主语 + 动词 + 宾语','dans ce contexte 限定含义；surtout 表示“主要”。',{contexte:'语境',représente:'代表',surtout:'主要',royauté:'王权'}]],
    louvre:[
      ["Le palais est devenu un musée ouvert au public après la Révolution française.",'法国大革命后，这座宫殿成为向公众开放的博物馆。','主语 + devenir 的复合过去时 + 表语','est devenu 表示“成为”；ouvert au public 修饰 musée。',{devenu:'成为',ouvert:'开放的',public:'公众',révolution:'革命'}],
      ["La pyramide associe le verre moderne aux façades anciennes du palais.",'玻璃金字塔把现代材料与宫殿古老的立面连接在一起。','主语 + associer A à B','associe A à B 表示“将 A 与 B 结合”；anciennes 修饰 façades。',{pyramide:'金字塔',associe:'结合',verre:'玻璃',façades:'建筑立面'}]],
    versailles:[
      ["Les jardins ont été dessinés avec de longues perspectives et des bassins.",'花园以绵长的景观轴线和水池布局。','主语 + 复合过去时被动语态','ont été dessinés 表示“被设计”；avec 引出设计元素。',{jardins:'花园',dessinés:'设计',perspectives:'景观轴线',bassins:'水池'}],
      ["La galerie des Glaces relie le salon de la Guerre au salon de la Paix.",'镜厅连接战争厅与和平厅。','relier A à B','relie 表示“连接”；au 是 à le 的缩合。',{galerie:'长廊',glaces:'镜子',relie:'连接',guerre:'战争',paix:'和平'}]],
    'cote-azur':[
      ["À Nice, la promenade des Anglais longe la baie et ses plages.",'在尼斯，英国人散步大道沿着海湾与海滩延伸。','地点 + 主语 + 动词 + 宾语','longe 表示“沿着……延伸”；ses 指海湾的。',{promenade:'步道',anglais:'英国人',longe:'沿着',baie:'海湾'}],
      ["Dans l'arrière-pays, des villages perchés dominent la Méditerranée.",'在内陆腹地，山顶村庄俯瞰地中海。','地点 + 主语 + 动词 + 宾语','perchés 表示“高踞的”；dominent 表示“俯瞰”。',{arrière:'后方',villages:'村庄',perchés:'高踞的',dominent:'俯瞰'}]],
    bourgogne:[
      ["Dijon fut autrefois la capitale des ducs de Bourgogne.",'第戎从前曾是勃艮第公爵的都城。','主语 + 简单过去时 + 表语','fut 是 être 的简单过去时，常用于历史叙述；des 是 de les 的缩合。',{autrefois:'从前',capitale:'都城',ducs:'公爵'}],
      ["Dans les vignobles, chaque parcelle peut posséder un sol différent.",'在葡萄园中，每块地可以拥有不同的土壤。','地点 + 主语 + pouvoir + 动词原形','peut 后接 posséder；chaque 后用单数名词。',{vignobles:'葡萄园',parcelle:'地块',posséder:'拥有',sol:'土壤'}]],
    normandie:[
      ["Les plages du Débarquement rappellent les événements de 1944.",'登陆海滩令人想起 1944 年的历史事件。','主语 + 动词 + 宾语','rappellent 表示“使想起”；du 是 de le 的缩合。',{plages:'海滩',débarquement:'登陆',rappellent:'使想起',événements:'事件'}],
      ["Le lait des vaches normandes sert à fabriquer plusieurs fromages célèbres.",'诺曼底奶牛的乳汁被用于制作多种著名奶酪。','主语 + servir à + 动词原形','sert à fabriquer 表示“用于制作”；des 引出所属关系。',{lait:'牛奶',vaches:'奶牛',fabriquer:'制作',fromages:'奶酪'}]],
    pantheon:[
      ["Dans la crypte reposent des personnalités honorées par la nation.",'地下墓室安葬着受到国家敬重的人物。','地点状语前置 + 倒装主谓','地点置于句首后，动词 reposent 位于复数主语之前。',{crypte:'地下墓室',reposent:'安息',personnalités:'人物',honorées:'受表彰的'}],
      ["Le pendule de Foucault y illustre la rotation de la Terre.",'傅科摆在那里展示地球的自转。','主语 + y + 动词 + 宾语','y 代替先贤祠；illustre 意为“形象地展示”。',{pendule:'摆',illustre:'展示',rotation:'旋转',terre:'地球'}]],
    'champs-elysees':[
      ["Cette perspective fait partie d'un grand axe historique de Paris.",'这条景观大道属于巴黎宏大的历史轴线。','faire partie de + 名词','fait partie de 表示“属于……的一部分”；d’un 是 de un 的省音。',{perspective:'景观大道',partie:'部分',axe:'轴线',historique:'历史的'}],
      ["L'avenue accueille aussi des célébrations et de grands rassemblements.",'这条大街也承载庆典与大型集会。','主语 + 动词 + 并列宾语','accueille 表示“迎接、举办”；des 引出复数宾语。',{avenue:'大街',accueille:'举办',célébrations:'庆典',rassemblements:'集会'}]],
    'mont-saint-michel':[
      ["Au Moyen Âge, l'abbaye attirait des pèlerins venus de loin.",'中世纪时，修道院吸引远道而来的朝圣者。','时间 + 主语 + 未完成过去时','attirait 描述过去持续的现象；venus de loin 修饰 pèlerins。',{abbaye:'修道院',attirait:'吸引',pèlerins:'朝圣者',loin:'远方'}],
      ["Les moines y conservaient et étudiaient des manuscrits.",'修士们在那里保存并研究手稿。','主语 + y + 两个并列动词','y 代替修道院；conservaient 与 étudiaient 均为未完成过去时。',{moines:'修士',conservaient:'保存',étudiaient:'研究',manuscrits:'手稿'}]],
    provence:[
      ["La floraison de la lavande attire des visiteurs pendant l'été.",'夏季薰衣草开花吸引游客前来。','主语 + 动词 + 宾语 + 时间','pendant 表示“在……期间”；de la lavande 修饰 floraison。',{floraison:'开花',lavande:'薰衣草',attire:'吸引',visiteurs:'游客'}],
      ["Près de Gordes, l'abbaye de Sénanque se trouve au milieu des champs.",'在戈尔德附近，塞南克修道院坐落在田野之间。','地点 + 主语 + se trouver + 地点','près de 表示“靠近”；au milieu de 表示“在……中间”。',{près:'附近',abbaye:'修道院',milieu:'中间',champs:'田野'}]],
    chambord:[
      ["Sur son escalier à double révolution, deux personnes peuvent monter sans se croiser.",'在双螺旋楼梯上，两个人可以同时上行而不相遇。','地点 + 主语 + pouvoir + 动词原形','sans 后接动词原形；se croiser 表示“相遇、交错”。',{escalier:'楼梯',double:'双重的',monter:'上楼',croiser:'相遇'}],
      ["Le château est entouré d'un vaste domaine de forêts et de jardins.",'城堡周围是一片广阔的森林与花园园区。','être entouré de + 名词','entouré 与阳性 château 一致；de 引出环绕之物。',{entouré:'被环绕',vaste:'广阔的',domaine:'园区',forêts:'森林'}]],
    strasbourg:[
      ["Le centre historique de Strasbourg figure au patrimoine mondial.",'斯特拉斯堡历史城区列入世界遗产。','主语 + figurer à + 名词','figure au 表示“列于”；au 是 à le 的缩合。',{centre:'中心',historique:'历史的',figure:'列入',patrimoine:'遗产'}],
      ["La ville accueille aussi plusieurs institutions européennes.",'这座城市也设有多个欧洲机构。','主语 + 动词 + 宾语','accueille 在这里表示“容纳、设有”；plusieurs 修饰复数。',{accueille:'设有',plusieurs:'多个',institutions:'机构',européennes:'欧洲的'}]],
    bretagne:[
      ["Le sentier des Douaniers suit une grande partie du littoral breton.",'海关小径沿着布列塔尼海岸线的很大一部分延伸。','主语 + 动词 + 宾语','suit 表示“沿着”；du 是 de le 的缩合。',{sentier:'小径',douaniers:'海关人员',suit:'沿着',littoral:'海岸线'}],
      ["Ses ports et ses îles rappellent l'importance de la mer dans la région.",'港口与岛屿体现了海洋在当地的重要性。','主语 + 动词 + 宾语','rappellent 在这里表示“使人意识到”；de la mer 修饰 importance。',{ports:'港口',îles:'岛屿',rappellent:'提醒',importance:'重要性'}]],
    lyon:[
      ["Dans les bouchons lyonnais, on découvre une cuisine locale généreuse.",'在里昂小餐馆里，人们可以品尝丰盛的本地菜。','地点 + on + 动词 + 宾语','on 泛指“人们”；généreuse 在这里形容菜肴丰盛。',{bouchons:'里昂传统小餐馆',découvre:'发现；品尝',cuisine:'菜肴',généreuse:'丰盛的'}],
      ["Depuis la colline de Fourvière, on voit la ville et ses deux fleuves.",'从富维耶山上可以看到城市与两条河流。','地点 + on + 动词 + 宾语','depuis 表示视线起点；ses 指里昂的。',{colline:'山丘',voit:'看见',ville:'城市',fleuves:'河流'}]]
  };
  for (const scene of scenes) scene.lines.push(...deeper[scene.id].map(([fr,zh,structure,grammar,gloss]) => ({fr,zh,structure,grammar,gloss})));
  const lastDetails = {
    eiffel:[
      ["Des expériences scientifiques et des transmissions radio ont prolongé sa vie.",'科学实验和无线电传输延续了铁塔的生命。','并列主语 + 复合过去时 + 宾语','ont prolongé 是复合过去时；sa 指铁塔的。',{expériences:'实验',scientifiques:'科学的',transmissions:'传输',prolongé:'延长'}],
      ["Le soir, son éclairage donne un autre visage au paysage parisien.",'夜晚，灯光让巴黎的景致呈现另一番面貌。','时间 + 主语 + 动词 + 宾语','donne un autre visage à 表示“赋予另一种面貌”；au 是 à le 的缩合。',{soir:'夜晚',éclairage:'灯光',visage:'面貌',parisien:'巴黎的'}]],
    soleil:[
      ["Dans les décors de Versailles, le soleil évoquait la puissance du roi.",'在凡尔赛的装饰中，太阳象征国王的权力。','地点 + 主语 + 未完成过去时 + 宾语','évoquait 描述过去持续的象征意义；du 是 de le 的缩合。',{décors:'装饰',évoquait:'使人想到',puissance:'权力',roi:'国王'}],
      ["Les fêtes de la cour mêlaient musique, théâtre et danse.",'宫廷庆典融合了音乐、戏剧与舞蹈。','主语 + 动词 + 并列宾语','mêlaient 是未完成过去时，表示惯常的宫廷活动。',{fêtes:'庆典',cour:'宫廷',mêlaient:'融合',théâtre:'戏剧'}]],
    fleur:[
      ["Le dessin stylisé apparaît sur des tissus, des armes et des armoiries.",'这种风格化纹样出现在织物、武器与纹章上。','主语 + 动词 + 并列地点','stylisé 表示“风格化的”；三个 des 引出并列名词。',{dessin:'图案',stylisé:'风格化的',tissus:'织物',armoiries:'纹章'}],
      ["Sa répétition sur un manteau rendait le pouvoir royal immédiatement visible.",'披风上反复出现的图案让王权一眼可辨。','主语 + 动词 + 宾语 + 补语','rendait A B 表示“使 A 变得 B”；immédiatement 修饰 visible。',{répétition:'重复',manteau:'披风',rendait:'使变得',visible:'可见的'}]],
    louvre:[
      ["L'histoire du Louvre commence avec une forteresse médiévale.",'卢浮宫的历史始于一座中世纪堡垒。','主语 + 动词 + avec + 名词','commence avec 表示“始于”；médiévale 修饰阴性 forteresse。',{commence:'开始',forteresse:'堡垒',médiévale:'中世纪的'}],
      ["En parcourant ses salles, on traverse aussi plusieurs siècles d'architecture.",'穿行于各个展厅时，人们也能看到跨越多个世纪的建筑变迁。','现在分词短语 + 主句','en parcourant 表示“在游览时”；plusieurs 修饰复数 siècles。',{parcourant:'游览',salles:'展厅',traverse:'穿越',siècles:'世纪'}]],
    versailles:[
      ["André Le Nôtre a organisé les jardins autour de grandes allées symétriques.",'安德烈·勒诺特尔围绕对称大道规划了花园。','主语 + 复合过去时 + 宾语','a organisé 是复合过去时；autour de 表示“围绕”。',{organisé:'规划',jardins:'花园',allées:'林荫道',symétriques:'对称的'}],
      ["Les bosquets formaient de petits espaces pour la promenade et les fêtes.",'林苑形成供散步与举行庆典的小型空间。','主语 + 未完成过去时 + 宾语','formaient 描述过去园林布局；pour 引出用途。',{bosquets:'林苑',formaient:'形成',espaces:'空间',promenade:'散步'}]],
    'cote-azur':[
      ["Le village d'Èze offre un panorama sur la mer depuis les hauteurs.",'埃兹村从高处提供眺望大海的全景。','主语 + 动词 + 宾语 + 地点','depuis 表示观看起点；les hauteurs 指高处。',{village:'村庄',offre:'提供',panorama:'全景',hauteurs:'高处'}],
      ["À Grasse, la tradition des parfums relie les fleurs aux savoir-faire locaux.",'在格拉斯，香水传统把花卉与当地工艺联系起来。','地点 + 主语 + relier A à B','relie A à B 表示“连接 A 和 B”；locaux 与复数 savoir-faire 一致。',{parfums:'香水',relie:'连接',fleurs:'花卉',savoir:'技艺'}]],
    bourgogne:[
      ["Les climats du vignoble désignent des parcelles aux caractères particuliers.",'勃艮第葡萄园的“风土区”指各有特色的地块。','主语 + 动词 + 宾语','désignent 表示“指称”；aux 是 à les 的缩合。',{climats:'风土区',vignoble:'葡萄园',désignent:'指称',parcelles:'地块'}],
      ["À Beaune, les anciens hospices témoignent aussi de l'histoire locale.",'在博讷，古老的慈善医院也见证了当地历史。','地点 + 主语 + 动词 + 补语','témoignent de 表示“见证”；anciens 修饰 hospices。',{anciens:'古老的',hospices:'慈善医院',témoignent:'见证',locale:'当地的'}]],
    normandie:[
      ["Les ports et les stations balnéaires montrent d'autres visages de la côte.",'港口与海滨度假地展现了海岸的不同面貌。','并列主语 + 动词 + 宾语','montrent 表示“展示”；d’autres 表示“其他的”。',{ports:'港口',stations:'度假地',balnéaires:'海滨的',côte:'海岸'}],
      ["Entre mémoire et nature, la région réunit plusieurs histoires de France.",'在历史记忆与自然风景之间，这片地区汇聚了法国的多种故事。','状语 + 主语 + 动词 + 宾语','entre A et B 表示“在 A 与 B 之间”；réunit 意为“汇集”。',{mémoire:'记忆',nature:'自然',région:'地区',réunit:'汇集'}]],
    pantheon:[
      ["Le bâtiment était d'abord destiné à devenir une église dédiée à sainte Geneviève.",'这座建筑最初计划成为献给圣热纳维耶芙的教堂。','主语 + 过去被动结构 + 不定式','était destiné à 表示“原本计划”；dédiée 与阴性 église 一致。',{bâtiment:'建筑',destiné:'计划用于',église:'教堂',dédiée:'献给'}],
      ["Son histoire reflète les changements politiques de la France.",'它的历史折射出法国的政治变迁。','主语 + 动词 + 宾语','reflète 表示“反映”；politiques 修饰复数 changements。',{histoire:'历史',reflète:'反映',changements:'变化',politiques:'政治的'}]],
    'champs-elysees':[
      ["En marchant vers l'ouest, on voit l'Arc de Triomphe grandir peu à peu.",'向西行走时，凯旋门会逐渐映入眼帘并显得越来越近。','现在分词短语 + 主句','en marchant 表示“在行走时”；peu à peu 表示“逐渐”。',{marchant:'行走',ouest:'西方',grandir:'变大',peu:'一点'}],
      ["La largeur de l'avenue laisse de la place aux promeneurs et aux événements.",'大道的宽度为行人和活动留出了空间。','主语 + laisser + 宾语 + 补语','laisse de la place à 表示“给……留出空间”。',{largeur:'宽度',laisse:'留下',promeneurs:'散步者',événements:'活动'}]],
    'mont-saint-michel':[
      ["La baie change d'aspect selon la lumière, le temps et le niveau de l'eau.",'海湾会随着光线、天气与水位呈现不同面貌。','主语 + 动词 + selon + 并列名词','selon 表示“根据、随着”；d’aspect 表示“外观”。',{baie:'海湾',aspect:'面貌',lumière:'光线',niveau:'水位'}],
      ["Du village jusqu'au sommet, les bâtiments racontent plusieurs siècles d'histoire.",'从村庄到山顶，建筑诉说着数个世纪的历史。','范围状语 + 主语 + 动词 + 宾语','du...jusqu’au... 表示“从……直到……”；racontent 为比喻用法。',{village:'村庄',sommet:'山顶',bâtiments:'建筑',racontent:'讲述'}]],
    provence:[
      ["La couleur des champs varie avec les saisons et la lumière du jour.",'田野的颜色随季节与日光变化。','主语 + 动词 + avec + 并列名词','varie 表示“变化”；avec 引出变化所依的条件。',{couleur:'颜色',champs:'田野',varie:'变化',saisons:'季节'}],
      ["Entre villages, marchés et abbayes, la région possède un patrimoine varié.",'从村庄、集市到修道院，这一地区拥有多样的文化遗产。','列举状语 + 主语 + 动词 + 宾语','entre 在这里引出范围；varié 修饰 patrimoine。',{villages:'村庄',marchés:'集市',abbayes:'修道院',patrimoine:'遗产'}]],
    chambord:[
      ["Les nombreuses cheminées donnent au toit une silhouette reconnaissable.",'众多烟囱让屋顶形成容易辨认的轮廓。','主语 + donner A à B','donnent A à B 表示“赋予 B 一种 A”；reconnaissable 修饰 silhouette。',{cheminées:'烟囱',toit:'屋顶',silhouette:'轮廓',reconnaissable:'可辨认的'}],
      ["Ce domaine rappelle les ambitions du roi François Ier à la Renaissance.",'这片园区令人想起文艺复兴时期弗朗索瓦一世的雄心。','主语 + 动词 + 宾语 + 时间','rappelle 表示“使人想起”；à la Renaissance 限定时代。',{domaine:'园区',rappelle:'使人想起',ambitions:'雄心',renaissance:'文艺复兴'}]],
    strasbourg:[
      ["La cathédrale gothique domine les toits du vieux centre.",'哥特式大教堂高耸于老城区屋顶之上。','主语 + 动词 + 宾语','domine 表示“高耸于……之上”；du 是 de le 的缩合。',{cathédrale:'大教堂',gothique:'哥特式的',domine:'高耸',toits:'屋顶'}],
      ["La ville associe aujourd'hui son héritage alsacien à une vie européenne.",'如今，这座城市融合了阿尔萨斯传统与欧洲城市生活。','主语 + associer A à B','associe A à B 表示“将 A 与 B 结合”；aujourd’hui 表示“如今”。',{associe:'结合',héritage:'遗产',alsacien:'阿尔萨斯的',européenne:'欧洲的'}]],
    bretagne:[
      ["La lumière changeante révèle des couleurs différentes sur les rochers.",'变幻的光线让岩石呈现不同色彩。','主语 + 动词 + 宾语 + 地点','changeante 修饰 lumière；sur 引出颜色显现的位置。',{lumière:'光线',changeante:'变化的',révèle:'显现',rochers:'岩石'}],
      ["Sur cette côte, les phares rappellent les liens anciens entre les habitants et la mer.",'在这片海岸，灯塔提醒人们居民与大海长久的联系。','地点 + 主语 + 动词 + 宾语','rappellent 表示“使想起”；entre A et B 表示“两者之间”。',{phares:'灯塔',liens:'联系',anciens:'久远的',habitants:'居民'}]],
    lyon:[
      ["Sur les pentes de la Croix-Rousse, l'histoire des ouvriers de la soie reste présente.",'在红十字山坡上，丝绸工人的历史仍随处可见。','地点 + 主语 + rester + 表语','reste présente 表示“仍然存在”；des 是 de les 的缩合。',{pentes:'山坡',ouvriers:'工人',soie:'丝绸',présente:'存在的'}],
      ["Entre les deux fleuves, les quartiers racontent des époques différentes.",'两条河流之间的街区讲述着不同时代的故事。','地点 + 主语 + 动词 + 宾语','entre 引出位置；racontent 在这里是比喻用法。',{fleuves:'河流',quartiers:'街区',racontent:'讲述',époques:'时代'}]]
  };
  for (const scene of scenes) scene.lines.push(...lastDetails[scene.id].map(([fr,zh,structure,grammar,gloss]) => ({fr,zh,structure,grammar,gloss})));
  const extraSources = {
    eiffel:'https://www.toureiffel.paris/fr/le-monument/tour-eiffel-et-sciences',
    soleil:'https://www.chateauversailles.fr/decouvrir/les-ressources/versailles-cour',
    fleur:'https://www.chateauversailles.fr/resources/pdf/fr/presse/dp_louisxiv.pdf',
    louvre:'https://musee.louvre.fr/decouvrir/le-palais',
    versailles:'https://www.chateauversailles.fr/decouvrir/domaine/jardins/bosquets',
    pantheon:'https://www.paris-pantheon.fr/decouvrir/le-pendule-de-foucault',
    'champs-elysees':'https://www.france.fr/fr/article/grands-evenements-france/'
  };
  const dialog = document.querySelector('#sceneDialog');
  const choices = document.querySelector('#sceneChoices');
  const content = document.querySelector('#sceneContent');
  const safeIds = new Set(scenes.map(s => s.id));
  let selected = localStorage.getItem('fr4000-scene') || 'none';
  if (!safeIds.has(selected)) selected = 'none';
  let active = scenes.find(s => s.id === selected) || scenes[0];
  let lookup = null;
  let returnFocus = null;
  let playingKey = null;
  function syncPlayback() {
    content.querySelectorAll('[data-play-key]').forEach(button => {
      const playing = state.mode === 'scene' && button.dataset.playKey === playingKey;
      button.textContent = playing ? '■ 停止' : button.dataset.label;
      button.setAttribute('aria-pressed', String(playing));
    });
    const stop = content.querySelector('[data-action="stop"]');
    if (stop) stop.hidden = state.mode !== 'scene';
  }
  window.addEventListener('playbackstop', () => {playingKey = null; syncPlayback();});

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
    const sourceLinks = [s.source, extraSources[s.id]].filter(Boolean).map((url,i) => `<a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">资料 ${i+1} ↗</a>`).join(' · ');
    document.querySelector('#sceneTitle').textContent = s.name;
    content.innerHTML = `<div class="sceneArtwork"><div class="sceneHero" style="background-image:url('./backgrounds/${s.id}.webp')"><div><small>${escapeHtml(s.place)}</small><h3>${escapeHtml(s.fr)}</h3><p>${escapeHtml(s.name)}</p></div></div><p class="sceneSource">内容参考：${sourceLinks} · 插画为 AI 创作，非实景照片。</p></div><div class="sceneReading"><p class="sceneAudioNote">介绍句使用设备的法语／中文语音朗读，不属于三种内置音色；点播放后默认无限循环，再点停止。音标由 eSpeak NG 自动生成，仅供参考。</p><div class="sceneFooter"><button class="scenePlayAll" type="button" data-action="play-all" data-play-key="all" data-label="▶ 连读介绍 · 循环" aria-pressed="false">▶ 连读介绍 · 循环</button><button class="sceneStop" type="button" data-action="stop" hidden>■ 停止播放</button><span>点击法语单词查词并循环听发音</span></div><div class="sceneLines">${s.lines.map((line,i) => `<article class="sceneLine" data-line="${i}"><div class="sceneFrench" lang="fr">${wordButtons(line.fr)}</div><div class="sceneIpa" lang="fr" aria-label="法语参考音标">/${escapeHtml(window.FRANCE_SCENE_IPA?.[line.fr] || '')}/</div><div class="sceneChinese" lang="zh-CN">${escapeHtml(line.zh)}</div><div class="sceneLineActions"><button type="button" data-action="play-fr" data-play-key="fr-${i}" data-label="▶ 法语" aria-pressed="false">▶ 法语</button><button type="button" data-action="play-zh" data-play-key="zh-${i}" data-label="▶ 中文" aria-pressed="false">▶ 中文</button><button type="button" data-action="explain" aria-expanded="false">句子讲解</button></div><div class="sceneExplanation" hidden><div><strong>句型：</strong>${escapeHtml(line.structure)}</div><div><strong>解析：</strong>${escapeHtml(line.grammar)}</div></div></article>`).join('')}</div></div></div>`;
    syncPlayback();
  }
  function play(text,lang,key,all=false) {
    if (state.mode === 'scene' && playingKey === key) {stopAll(); return;}
    stopAll(true);
    hideDictionaryVisual();
    state.mode = 'scene';
    const token = ++state.token;
    const lines = all ? active.lines.map(x => x.fr) : [text];
    let i = 0;
    playingKey = key;
    syncPlayback();
    setStatus(`背景选择 · ${active.name} · 循环朗读中`);
    const next = () => {
      if (state.mode !== 'scene' || state.token !== token) return;
      speakOnce(lines[i++ % lines.length],lang,() => {
        if (state.mode === 'scene' && state.token === token) setTimeout(next, 350);
      },{onerror:() => {state.mode = null; playingKey = null; syncPlayback(); setStatus('设备语音未能播放；请检查系统语音与静音设置。');}});
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
    if (state.mode === 'scene' || state.mode === 'word' || state.mode === 'word-preview') stopAll(true);
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
    if (action === 'stop') {stopAll(); return;}
    if (action === 'play-all') {play('', 'fr-FR', 'all', true); return;}
    const article = button.closest('.sceneLine');
    const line = active.lines[Number(article.dataset.line)];
    if (action === 'play-fr') play(line.fr,'fr-FR',`fr-${article.dataset.line}`);
    if (action === 'play-zh') play(line.zh,'zh-CN',`zh-${article.dataset.line}`);
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
