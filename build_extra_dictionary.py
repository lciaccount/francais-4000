from __future__ import annotations
import json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
arr=json.load(open(ROOT/'sentences-4000.json',encoding='utf8'))
h=(ROOT/'index.html').read_text(encoding='utf8')
def grab(a,b):
 st=h.index(a)+len(a); en=h.index(b,st); return json.loads(h[st:en].strip().rstrip(';'))
W=grab('const WORDS=','\n\nconst LEMMA_WORDS=')
L=grab('const LEMMA_WORDS=','\n\nconst BUILTIN_WORD_INDEX=')
D=grab('const DICT_OVERRIDES=','\nconst EXTRA_WORDS_4000=') if '\nconst EXTRA_WORDS_4000=' in h else grab('const DICT_OVERRIDES=','\nconst EXTRA_LEMMA_WORDS=')
E=grab('const EXTRA_LEMMA_WORDS=','\nconst DICT_USAGE_POS=')
pat=re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿŒœÇç]+(?:['’][A-Za-zÀ-ÖØ-öø-ÿŒœÇç]+)?(?:-[A-Za-zÀ-ÖØ-öø-ÿŒœÇç]+)*")
def norm(w):
 x=w.lower().replace('’',"'"); m=re.match(r"^(?:l|d|j|t|c|m|n|s|qu)'(.+)$",x); x=m.group(1) if m else x; return x.strip("-'")
vocab=sorted({norm(m.group(0)) for s in arr for m in pat.finditer(s['fr'])})
missing=[w for w in vocab if w not in (set(W)|set(L)|set(D)|set(E))]

# 为新增语料中旧词典未覆盖的词形补核心释义。变位/倒装形式明确标为“词形”，避免把整句语境冒充词义。
raw='''
a-t-il\t有……吗（avoir 倒装形式）
accessible\t可到达的；可进入的
accessibles\t可到达的；可进入的（复数）
informations\t信息；资料（复数）
trajet\t行程；路线；路程
trouvent\t找到；位于（trouver / se trouver 第三人称复数）
accompagner\t陪同；陪伴
accord\t同意；一致；协议
accueil\t接待；欢迎
accès\t进入；访问；通道
adore\t非常喜欢（adorer 变位）
adresse\t地址
ai-je\t我有……吗（avoir 倒装形式）
aide\t帮助；援助
aidez-moi\t请帮我（aider 的祈使式）
aidez-nous\t请帮助我们（aider 的祈使式）
aidé\t帮助过；得到帮助的（aider 过去分词）
aimable\t友善的；客气的
allez-vous\t您去……吗 / 您好吗中的倒装形式（aller）
allez-y\t请去吧；请继续；您请
amusez-vous\t玩得开心（s’amuser 祈使式）
anglais\t英语；英国的/英语的
année\t年；年份
appartement\t公寓；住房
appelez-moi\t请给我打电话 / 请叫我（appeler 祈使式）
appelle\t打电话；叫作（appeler 变位）
appétit\t食欲；胃口
arrivée\t到达；抵达
articuler\t清楚发音；咬字
asseoir\t使坐下；坐下（s’asseoir）
assez\t相当；足够
assister\t参加；出席；目睹
attendre\t等待
attendu\t等候过的；预期的（attendre 过去分词）
attente\t等待；等候
also\t也
autrement\t以另一种方式；否则
as\t有（avoir 第二人称单数）
vas\t去；状态如何（aller 第二人称单数）
proposer\t提出；提供；建议
université\t大学
études\t学习；学业（复数）
étudie\t学习（étudier 变位）
avais\t有（avoir 未完成过去时）
avance\t提前；前进
avez-vous\t您有……吗（avoir 倒装形式）
bancaires\t银行的（复数）
blessure\t伤口；受伤
blessée\t受伤的（阴性）
bloqué\t被堵住的；被锁住的
bloquée\t被堵住的；被锁住的（阴性）
bâtiment\t建筑物；大楼
cartes\t卡片；银行卡（复数）
cause\t原因；缘故
chance\t运气；机会
chinois\t中文；中国的
commander\t点餐；订购；指挥
commencer\t开始
comprends\t理解；明白（comprendre 变位）
compris\t理解了；包括在内（comprendre 过去分词）
compréhension\t理解；谅解
compte\t账户；计算；打算（compter 变位）
confirme\t确认（confirmer 变位）
connais\t认识；知道（connaître 变位）
connaissance\t认识；知识；相识
connaissez\t认识；知道（connaître 变位）
conseillez\t建议；推荐（conseiller 变位）
consulte\t就诊；咨询（consulter 变位）
conversation\t交谈；对话
conviendrait\t会合适（convenir 条件式）
copie\t副本；复制品
cours\t课程；课；过程中
danger\t危险
dehors\t在外面；外面
demande\t请求；询问；申请
dernière\t最后的；上一个的（阴性）
devons-nous\t我们必须……吗（devoir 倒装形式）
difficile\t困难的
difficulté\t困难
difficultés\t困难（复数）
dirait\t会说；看起来像（dire 条件式）
dis\t说（dire 变位）
disparu\t消失的；不见了
dit-on\t人们怎么说 / 怎么称呼（dire 倒装形式）
documents\t文件；材料（复数）
dois-je\t我必须……吗（devoir 倒装形式）
donner\t给；提供
dormi\t睡过（dormir 过去分词）
doucement\t轻轻地；慢慢地
déclarer\t申报；声明
déclaré\t宣布；申报过（déclarer 过去分词）
décliner\t婉拒；谢绝；下降
dépend\t取决于（dépendre 变位）
dérangement\t打扰；麻烦
déranger\t打扰；妨碍
désolé\t抱歉的；遗憾的
emporter\t带走；外带
encore\t还；再次；仍然
entendu\t听到的；明白了；好的
entrer\t进入
es\t是（être 第二人称单数）
essoufflé\t气喘吁吁的
est-ce\t是否；这是……吗（疑问结构）
est-elle\t她/它是……吗（être 倒装形式）
est-il\t他/它是……吗（être 倒装形式）
et\t和；以及
eu\t有过；得到过（avoir 过去分词）
exacte\t准确的；确切的（阴性）
exactement\t准确地；正是
excusez-moi\t对不起；打扰一下
expliquer\t解释；说明
facilement\t容易地；顺利地
faible\t虚弱的；弱的
faites\t做；使（faire 变位/祈使式）
faut-il\t是否需要；必须……吗（falloir 倒装形式）
feu\t火；火灾
fois\t次；回
formulaire\t表格
forte\t强烈的；严重的（阴性）
france\t法国
fumée\t烟；烟雾
fêtes\t节日；庆典（复数）
gentil\t友好的；好心的
grave\t严重的；重大的
gêne\t不适；妨碍；窘迫
information\t信息；资料
inquiétez\t担心（s’inquiéter 变位/祈使式）
instant\t片刻；瞬间
interprète\t口译员；翻译人员
interprétation\t口译；解释
interrompre\t打断；中断
invitation\t邀请
invite\t邀请（inviter 变位）
itinéraire\t路线；行程
joyeuses\t快乐的；愉快的（阴性复数）
joyeux\t快乐的；愉快的
jusqu'à\t直到；到……为止
laisse\t留下；让（laisser 变位）
laissé\t留下过的（laisser 过去分词）
loin\t远；遥远地
longtemps\t很久；长时间
là\t那里；在那儿
mais\t但是
manque\t缺少；不足；想念
marche\t走路；运转；可行
marcher\t走路；运转
meilleurs\t更好的；最好的（复数）
mieux\t更好地；更好
minute\t分钟
montrer\t展示；指给看
montrez-moi\t请给我看 / 请指给我看
médicale\t医疗的（阴性）
normalement\t正常地；通常
notre\t我们的（单数名词前）
nous\t我们；我们自己
numéro\t号码；编号
obtenir\t获得；取得
opposition\t反对；（银行卡）挂失/止付
opérateur\t运营商；操作员
oui\t是；对
ouvert\t开着的；营业的
ouverte\t开着的；营业的（阴性）
par\t由；通过；每
parce\t因为（常用于 parce que）
parfait\t完美的；很好
parlez\t说话（parler 变位/祈使式）
part\t出发；离开（partir 变位）
passez\t经过；度过（passer 变位/祈使式）
passé\t过去的；发生过的
passée\t过去的；发生过的（阴性）
patience\t耐心
payer\t支付
pensais\t想；认为（penser 未完成过去时）
pense\t想；认为（penser 变位）
penser\t想；认为；记得要
permettez\t允许（permettre 变位）
personne\t人；某人；没有人（否定中）
perte\t丢失；损失
peut-il\t他/它可以……吗（pouvoir 倒装形式）
peut-être\t也许；可能
pied\t脚；步行（à pied）
plaisir\t愉快；乐趣
plein\t满的；全职的（à temps plein）
plutôt\t更；相当；倒不如
position\t位置；地点
possible\t可能的；可行的
pourquoi\t为什么
pourrait\t可以；可能会（pouvoir 条件式）
pouvez-vous\t您能……吗（pouvoir 倒装形式）
première\t第一的；第一次（阴性）
prendrai\t将要拿/点/乘（prendre 简单将来时）
prenez\t拿；乘；请用（prendre 变位/祈使式）
pris\t拿了；乘了；取了（prendre 过去分词）
prix\t价格
problème\t问题；麻烦
produire\t生产；发生（se produire）
profitez\t享受；好好利用（profiter 变位/祈使式）
projets\t计划；项目（复数）
promotion\t促销；折扣；晋升
provisoire\t临时的
présente\t介绍；呈现（présenter 变位）
présenter\t介绍；呈现
prévenir\t通知；提醒；预防
prévenu\t通知过的；提醒过的
prévoit\t预计；计划（prévoir 变位）
prévu\t预计的；安排好的
prêter\t借给
puis-je\t我可以……吗（pouvoir 倒装形式）
quand\t什么时候；当……时
quartier\t街区；地区
quel\t哪个；什么样的（阳性单数）
quelle\t哪个；什么样的（阴性单数）
quelqu'un\t某人；有人
quelques\t几个；一些
quels\t哪些；什么样的（阳性复数）
qui\t谁；……的人/物
quoi\t什么
rapidement\t快速地；尽快
relever\t扶起；站起来（se relever）；记录
remercie\t感谢（remercier 变位）
remplir\t填写；装满
rentrez\t回去；回家（rentrer 变位/祈使式）
reposez-vous\t请休息
respire\t呼吸（respirer 变位）
rester\t停留；留下
restez\t停留；请留下（rester 变位/祈使式）
retard\t迟到；延误
retour\t返回；返程
retourner\t返回；翻转
retrouve\t找到；再次见到（retrouver 变位）
retrouver\t找回；再次见到
revoir\t再次见到；复习
revoit\t再次见到（revoir 变位）
reçu\t收到的；接到的（recevoir 过去分词）
route\t道路；路线
répétez\t请重复（répéter 祈使式）
réseau\t网络；信号
rétablissement\t康复；恢复
réussite\t成功；成就
saigne\t流血（saigner 变位）
sais\t知道；会（savoir 变位）
sans\t没有；不带
santé\t健康；干杯（祝酒）
sera\t将是（être 简单将来时）
serrurier\t锁匠
seulement\t只；仅仅
signaler\t报告；申报
sim\tSIM 卡
sincèrement\t真诚地
situation\t情况；处境
soin\t护理；照料；小心
soins\t护理；医疗处理（复数）
sont\t是（être 第三人称复数）
souhaite\t祝愿；希望（souhaiter 变位）
suite\t接下来；立刻（tout de suite）
sur\t在……上；关于；确定的（sûr）
sécuriser\t确保安全；保护
séjour\t停留；住宿；旅程
sûr\t确定的；安全的
tard\t晚；迟
tenez\t拿着；给您（tenir 祈使式）
toi\t你（重读人称代词）
traduire\t翻译
trop\t太；过于
trousseau\t一串（钥匙）；钥匙串
trouve\t找到；认为（trouver 变位）
trouver\t找到；认为
trouvé\t找到的（trouver 过去分词）
urgence\t紧急情况；急诊
urgences\t急诊科；紧急情况（复数）
venez\t来（venir 变位/祈使式）
venu\t来了；来过（venir 过去分词）
vie\t生活；生命；欲望
viens\t来（venir 变位）
vient\t来；刚刚（venir 变位）
vois\t看见（voir 变位）
vol\t盗窃；飞行
volontaire\t自愿的；故意的
volontiers\t乐意地；很愿意
volée\t被偷的（阴性）
votre\t您的；你们的
voulais\t想要（vouloir 未完成过去时）
voyage\t旅行
vraiment\t真的；非常
vu\t看见过的（voir 过去分词）
vus\t看见过的（阳性复数）
vœux\t祝愿；祝福（复数）
zone\t区域；地带
échanger\t交换；换货
était\t是（être 未完成过去时）
été\t是过；曾经（être 过去分词）；夏天
évacuer\t疏散；撤离
évanouir\t昏厥（s’évanouir）
'''.strip()
gloss={}
for line in raw.splitlines():
    k,v=line.split('\t',1); gloss[k]=v
# typo alias in raw
if 'also' in gloss:
    gloss['aussi']=gloss.pop('also')
left=[w for w in missing if w not in gloss]
extra=[w for w in gloss if w not in missing]
if left:
    print('MISSING GLOSSES',left)
    raise SystemExit(2)
# extra keys harmless but report
print('missing corpus dictionary words:',len(missing),'glossed:',len(gloss),'extra gloss keys:',len(extra))

def ipa(word):
    try:
        p=subprocess.run(['espeak','-q','--ipa=3','-v','fr-fr',word],capture_output=True,text=True,timeout=3)
        return ' '.join(p.stdout.split())
    except Exception: return ''
entries={}
for w in missing:
    entries[w]={'groups':[{'pos':'词汇 / 词形','meanings':[gloss[w]]}],'ipa':ipa(w)}
# UI intentionally splits several inversion / pronominal hyphen forms for clicking.
# Add those split tokens too so every BUILTIN_WORD_INDEX entry has dictionary data.
split_tokens={
 'amusez':'玩；使开心（amuser 变位/祈使式）',
 'devons':'必须；应该（devoir 第一人称复数）',
 'elle':'她；它（阴性）',
 'montrez':'展示；请指出（montrer 变位/祈使式）',
 'reposez':'休息（reposer / se reposer 变位/祈使式）',
 't':'倒装疑问中的连音字母 t，本身无独立词义',
}
for w,m in split_tokens.items():
    entries.setdefault(w,{'groups':[{'pos':'词汇 / 词形','meanings':[m]}],'ipa':ipa(w)})
(ROOT/'extra-words-4000.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('wrote',ROOT/'extra-words-4000.json')
