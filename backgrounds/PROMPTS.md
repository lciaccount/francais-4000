# 背景选择插画提示词

本目录的 17 张 WebP 插画由内置 imagegen 工具生成，随后机械转码压缩；其中 16 张可选作背景，`histoire-france.webp` 仅供独立的“法国历史”和“历史人物”栏目使用，不是人物肖像。所有插画都不是景点照片或历史文物复刻。统一提示词：16:9 法语学习网站背景，手绘 gouache 旅行海报风格、细线建筑／风景描绘、轻微纸张肌理、暖白与低饱和法国蓝、少量酒红点缀；为半透明文字卡留白；无文字、商标、旗帜和水印。

各图主体：

| 文件 | 主体 |
| --- | --- |
| `eiffel.webp` | 巴黎埃菲尔铁塔与塞纳河 |
| `soleil.webp` | 路易十四与凡尔赛宫花园意象 |
| `fleur.webp` | 鸢尾花纹章的织物与纸张图案 |
| `louvre.webp` | 卢浮宫庭院及玻璃金字塔 |
| `versailles.webp` | 凡尔赛宫正面与花园喷泉 |
| `cote-azur.webp` | 蔚蓝海岸、地中海、滨海城镇 |
| `bourgogne.webp` | 勃艮第葡萄园与石砌村庄 |
| `normandie.webp` | 诺曼底海崖、草地与半木构村庄 |
| `pantheon.webp` | 巴黎先贤祠的柱廊与穹顶 |
| `champs-elysees.webp` | 香榭丽舍大街与凯旋门方向 |
| `mont-saint-michel.webp` | 潮汐海湾中的圣米歇尔山及修道院 |
| `provence.webp` | 普罗旺斯薰衣草田、石砌山村与柏树 |
| `chambord.webp` | 卢瓦尔河谷香波堡的文艺复兴式屋顶 |
| `strasbourg.webp` | 斯特拉斯堡“小法兰西”的木筋屋与运河 |
| `bretagne.webp` | 布列塔尼玫瑰花岗岩海岸、海面与灯塔 |
| `lyon.webp` | 索恩河畔里昂老城与富维耶山 |
| `histoire-france.webp` | 罗马石拱、中世纪建筑与古典巴黎元素的艺术化历史长卷；并非同一时空的真实场景 |

生成时各图还分别指定对应主体、横向构图、真实可辨的地标／地域特征；`soleil.webp` 使用 historical-scene 用例，其他图使用 illustration-story 用例。背景是艺术化示意，不应作为实景或建筑考证材料。

新增六图的最终提示词采用内置 imagegen 模式。公共部分为：`16:9 wide illustrated background for an elegant French language learning website. Hand-painted gouache travel poster, delicate architectural and landscape linework, subtle paper grain, warm ivory, muted French blue, restrained burgundy accents. Clear focal point in center with calm peripheral areas for translucent interface cards. No text, logos, flags, watermarks, borders. Distinct recognizable real French landscape, artistic illustration not an exact documentary photo.` 各图分别追加下列主体描述：

| 文件 | 追加提示词 |
| --- | --- |
| `mont-saint-michel.webp` | Mont Saint-Michel rising from its tidal bay in Normandy, medieval abbey on the granite island, shallow reflective water and broad sky, view from across the bay. |
| `provence.webp` | Provence lavender fields in bloom near a pale stone hill village, rows of lavender, cypress trees, warm southern sunlight, subtle farmhouse. |
| `chambord.webp` | Château de Chambord in the Loire Valley, accurate silhouette with many Renaissance roof towers and chimneys, formal lawns and soft morning light. |
| `strasbourg.webp` | Strasbourg Petite France district, half-timbered Alsatian houses and narrow canals with a stone bridge, warm muted daylight. |
| `bretagne.webp` | Brittany's Côte de Granit Rose, rose-copper granite boulders, small coastal path and turquoise sea, a distant modest lighthouse, breezy Atlantic sky. |
| `lyon.webp` | Old Lyon on the banks of the Saône, Renaissance facades, Fourvière hill and basilica in the distance, stone bridges, gentle late-afternoon light. |

`histoire-france.webp` 使用内置 imagegen 模式生成。最终提示词：

> Use case: historical-scene. Asset type: wide illustrated background for an educational French-history chapter in an existing French travel notebook website. Primary request: a painterly visual evocation of the long history of France, from Roman Gaul and medieval dynasties through the Renaissance and French Revolution to the First Empire. Scene/backdrop: a warm parchment-toned panorama arranged as subtle visual layers, with a Roman stone arch at far left, medieval abbey/castle silhouettes toward the center, and a classical Paris riverside cityscape toward the right; a small distant Napoleonic-era architectural silhouette, without identifiable people or battle scenes. Style/medium: refined hand-painted watercolor and gouache with textured paper, matching a tasteful illustrated French heritage travel poster. Composition/framing: wide 16:9 landscape, cohesive single scene rather than labeled timeline panels, gentle details around edges and an open, calm center suitable for responsive cropping and overlay text. Lighting/mood: luminous late-afternoon sky, scholarly and evocative. Color palette: muted limestone, parchment, dusty blue, sage, restrained warm gold. Constraints: no text, dates, logos, flags, maps with labels, watermarks, modern vehicles or modern architecture. Historically plausible architectural styles; do not portray different eras as literally coexisting in a documentary photograph.
