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
    document.querySelector('#sceneTitle').textContent = s.name;
    content.innerHTML = `<div class="sceneHero" style="background-image:url('./backgrounds/${s.id}.webp')"><div><small>${escapeHtml(s.place)}</small><h3>${escapeHtml(s.fr)}</h3><p>${escapeHtml(s.name)}</p></div></div><p class="sceneSource">内容参考：<a href="${s.source}" target="_blank" rel="noopener noreferrer">查看原始资料 ↗</a> · 插画为 AI 创作，非实景照片。</p><p class="sceneAudioNote">介绍句使用设备的法语／中文语音朗读，不属于三种内置音色；点播放后默认无限循环，再点停止。音标由 eSpeak NG 自动生成，仅供参考。</p><div class="sceneLines">${s.lines.map((line,i) => `<article class="sceneLine" data-line="${i}"><div class="sceneFrench" lang="fr">${wordButtons(line.fr)}</div><div class="sceneIpa" lang="fr" aria-label="法语参考音标">/${escapeHtml(window.FRANCE_SCENE_IPA?.[line.fr] || '')}/</div><div class="sceneChinese" lang="zh-CN">${escapeHtml(line.zh)}</div><div class="sceneLineActions"><button type="button" data-action="play-fr" data-play-key="fr-${i}" data-label="▶ 法语" aria-pressed="false">▶ 法语</button><button type="button" data-action="play-zh" data-play-key="zh-${i}" data-label="▶ 中文" aria-pressed="false">▶ 中文</button><button type="button" data-action="explain" aria-expanded="false">句子讲解</button></div><div class="sceneExplanation" hidden><div><strong>句型：</strong>${escapeHtml(line.structure)}</div><div><strong>解析：</strong>${escapeHtml(line.grammar)}</div></div></article>`).join('')}</div><div class="sceneFooter"><button class="scenePlayAll" type="button" data-action="play-all" data-play-key="all" data-label="▶ 连读介绍 · 循环" aria-pressed="false">▶ 连读介绍 · 循环</button><button class="sceneStop" type="button" data-action="stop" hidden>■ 停止播放</button><span>点击法语单词查词并循环听发音</span></div>`;
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
    if (state.mode === 'scene') stopAll(true);
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
