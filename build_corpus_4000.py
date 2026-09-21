from __future__ import annotations
import json,re,subprocess,unicodedata
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT=Path(__file__).resolve().parent
INDEX=ROOT/'index.html'
old=INDEX.read_text(encoding='utf-8')
m=re.search(r'const SENTENCES=(\[.*?\]);\nconst CATEGORIES=',old,re.S)
OLD=json.loads(m.group(1))
CATS=json.loads(re.search(r'const CATEGORIES=(\[.*?\]);',old,re.S).group(1))
bycat={i:[x for x in OLD if x['category']==i][::4] for i in range(20)}

ALL=[]
def add(c,fr,zh):
    # Apply the compulsory elisions/contractions that templating can otherwise miss.
    fr=fr.strip()
    fr=re.sub(r'\bque ([aeiouyàâäéèêëîïôöùûühœ])',r'qu’\1',fr,flags=re.I)
    fr=re.sub(r'\bde le\b','du',fr,flags=re.I)
    fr=re.sub(r'\bde les\b','des',fr,flags=re.I)
    fr=re.sub(r'\bà le\b','au',fr,flags=re.I)
    fr=re.sub(r'\bà les\b','aux',fr,flags=re.I)
    fr=re.sub(r'\bde ([aeiouyàâäéèêëîïôöùûühœ])',r'd’\1',fr,flags=re.I)
    fr=re.sub(r'\s+([,.;!?])',r'\1',fr)
    fr=re.sub(r'\s{2,}',' ',fr)
    if fr[-1] not in '.!?': fr+='.'
    ALL.append({'category':c,'fr':fr,'zh':zh.strip()})

def take(c, items):
    seen=set(); out=[]
    for fr,zh in items:
        k=fr.lower().replace('’',"'").strip()
        if k in seen: continue
        seen.add(k); out.append((fr,zh))
    if len(out)<200: raise RuntimeError(f'cat {c}: only {len(out)}')
    for fr,zh in out[:200]: add(c,fr,zh)

# 0 问候与礼貌：按真实交际功能分组，不再机械拼接互相冲突的寒暄。
def cat0():
    out=[]
    greet=[('Bonjour','你好/日安'),('Bonsoir','晚上好'),('Salut','嗨'),('Bonjour à tous','大家好'),('Bonsoir à tous','大家晚上好')]
    ctx=[('Comment allez-vous ?','您好吗？'),('Comment ça va ?','你好吗？'),('J’espère que vous allez bien.','希望您一切都好。'),('Ça me fait plaisir de vous voir.','很高兴见到您。'),('Ravi de vous revoir.','很高兴再次见到您。'),('Bienvenue !','欢迎！'),('Vous avez passé une bonne journée ?','您今天过得好吗？'),('Tout va bien ?','一切都好吗？'),('Ça fait longtemps !','好久不见！'),('Quel plaisir de vous voir !','见到您真高兴！')]
    informal_ctx=[('Comment ça va ?','你好吗？'),('J’espère que tu vas bien.','希望你一切都好。'),('Ça me fait plaisir de te voir.','很高兴见到你。'),('Content de te revoir.','很高兴再次见到你。'),('Bienvenue !','欢迎！'),('Tu as passé une bonne journée ?','你今天过得好吗？'),('Tout va bien ?','一切都好吗？'),('Ça fait longtemps !','好久不见！'),('Quel plaisir de te voir !','见到你真高兴！'),('Quoi de neuf ?','最近怎么样？')]
    for g,gz in greet:
        use_ctx=informal_ctx if g=='Salut' else ctx
        for t,tz in use_ctx: out.append((f'{g} ! {t}',f'{gz}！{tz}'))
    thanks=[('Merci.','谢谢。'),('Merci beaucoup.','非常感谢。'),('Merci pour votre aide.','谢谢您的帮助。'),('Merci pour votre patience.','谢谢您的耐心。'),('Merci pour votre temps.','谢谢您抽时间。'),('Merci pour l’information.','谢谢您提供的信息。'),('Merci pour votre message.','谢谢您的消息。'),('Merci pour l’invitation.','谢谢您的邀请。'),('Merci d’être venu.','谢谢您过来。'),('C’est très gentil, merci.','您太好了，谢谢。')]
    resp=[('Je vous en prie.','不客气。'),('De rien.','不客气。'),('Avec plaisir.','很乐意。'),('Il n’y a pas de quoi.','不用客气。')]
    out += thanks
    out += resp
    apologies=[('Excusez-moi.','打扰一下/对不起。'),('Pardon.','抱歉。'),('Je suis désolé.','对不起。'),('Désolé pour le retard.','抱歉我迟到了。'),('Désolé de vous déranger.','抱歉打扰您。'),('Excusez-moi de vous interrompre.','抱歉打断您。'),('Je vous demande pardon.','请您原谅。'),('Ce n’était pas volontaire.','我不是故意的。'),('J’ai fait une erreur, désolé.','我弄错了，对不起。'),('Merci de votre compréhension.','谢谢您的理解。')]
    out += apologies
    polite=[('S’il vous plaît.','请。'),('S’il te plaît.','请（对熟人）。'),('Après vous.','您先请。'),('Allez-y.','您请/请继续。'),('Prenez votre temps.','您慢慢来。'),('Pas de problème.','没问题。'),('Bien sûr.','当然。'),('Avec plaisir.','乐意效劳。'),('Un instant, s’il vous plaît.','请稍等。'),('Merci d’avance.','先谢谢您。')]
    out += polite
    fare=[('À bientôt !','回头见！'),('À demain !','明天见！'),('À tout à l’heure !','待会儿见！'),('À plus tard !','晚点见！'),('Au revoir !','再见！'),('Bonne journée !','祝您今天愉快！'),('Bonne soirée !','祝您晚上愉快！'),('Bonne nuit !','晚安！'),('Bon week-end !','周末愉快！'),('Bon voyage !','旅途愉快！'),('Bonne route !','一路平安！'),('À la prochaine !','下次见！'),('On se revoit bientôt.','我们很快再见。'),('Prenez soin de vous.','请保重。'),('Rentrez bien.','回去路上注意安全。')]
    out += fare
    wishes=[('Bon courage !','加油/祝顺利！'),('Bonne chance !','祝你好运！'),('Félicitations !','恭喜！'),('Joyeux anniversaire !','生日快乐！'),('Bonne année !','新年快乐！'),('Joyeuses fêtes !','节日快乐！'),('Bon appétit !','祝你好胃口！'),('Santé !','干杯/祝健康！'),('Profitez bien !','好好享受！'),('Amusez-vous bien !','玩得开心！'),('Reposez-vous bien.','好好休息。'),('Bon rétablissement !','祝早日康复！'),('Mes meilleurs vœux.','致以最美好的祝愿。'),('Je vous souhaite une bonne journée.','祝您今天愉快。'),('Je vous souhaite un bon séjour.','祝您旅途/停留愉快。')]
    out += wishes
    small=[('Vous êtes d’ici ?','您是本地人吗？'),('C’est votre première fois ici ?','这是您第一次来这里吗？'),('Vous connaissez bien le quartier ?','您熟悉这个街区吗？'),('Vous avez passé un bon week-end ?','您周末过得好吗？'),('Vous avez des projets pour ce soir ?','您今晚有什么安排吗？'),('Il fait beau aujourd’hui, n’est-ce pas ?','今天天气不错，是吧？'),('Vous avez trouvé facilement ?','您顺利找到这里了吗？'),('Ça fait plaisir de vous revoir.','很高兴又见到您。'),('Comment s’est passée votre journée ?','您今天过得怎么样？'),('Quoi de neuf ?','最近怎么样？'),('Ça va mieux aujourd’hui ?','今天好些了吗？'),('Vous avez bien dormi ?','您睡得好吗？'),('Tout se passe bien ?','一切进展顺利吗？'),('Je suis content de vous voir.','很高兴见到您。'),('Enchanté de faire votre connaissance.','很高兴认识您。')]
    out += small
    # 补充 40 条简短、可直接使用的礼貌表达
    extra=[
      ('Puis-je vous aider ?','我可以帮您吗？'),('Vous avez besoin d’aide ?','您需要帮助吗？'),('Merci, c’est parfait.','谢谢，这样很好。'),('Ça me va, merci.','这样可以，谢谢。'),('Pas maintenant, merci.','现在不用，谢谢。'),('Non merci, c’est gentil.','不用了，谢谢您的好意。'),('Oui, volontiers.','好啊，很乐意。'),('Pourquoi pas ?','为什么不呢？'),('D’accord, merci.','好的，谢谢。'),('Très bien, à bientôt.','好的，回头见。'),('À demain, bonne soirée.','明天见，祝您晚上愉快。'),('Merci encore.','再次感谢。'),('Excusez-moi, je n’ai pas compris.','对不起，我没听懂。'),('Pardon, vous pouvez répéter ?','抱歉，您能重复一遍吗？'),('Vous pouvez parler un peu plus lentement ?','您能再说慢一点吗？'),('Comment dit-on ça en français ?','这个用法语怎么说？'),('Je vous laisse passer.','您先过。'),('Tenez, je vous en prie.','给您，请。'),('C’est pour vous.','这是给您的。'),('Ne vous inquiétez pas.','您别担心。'),('Ce n’est pas grave.','没关系。'),('Ça arrive.','这种事难免。'),('Merci de m’avoir prévenu.','谢谢您提前告诉我。'),('Merci de me l’avoir dit.','谢谢您告诉我。'),('Je comprends.','我明白。'),('Je vois.','我懂了。'),('Exactement.','正是。'),('Tout à fait.','完全正确。'),('Pas tout à fait.','不完全是。'),('Ça dépend.','这要看情况。'),('Je suis d’accord.','我同意。'),('Je ne suis pas sûr.','我不太确定。'),('Ça marche.','可以/成交。'),('Entendu.','好的，明白。'),('À votre service.','愿意为您效劳。'),('Bienvenue chez nous.','欢迎来我们这里。'),('Faites comme chez vous.','请像在自己家一样随意。'),('Merci pour l’accueil.','谢谢您的招待。'),('C’était un plaisir.','很愉快。'),('Au plaisir de vous revoir.','期待再次见到您。')]
    out+=extra
    courtesy=[
      ('Excusez-moi, puis-je vous poser une question ?','打扰一下，我可以问您一个问题吗？'),('Excusez-moi, avez-vous une minute ?','打扰一下，您有一分钟吗？'),('Puis-je entrer ?','我可以进来吗？'),('Puis-je m’asseoir ici ?','我可以坐这里吗？'),('Puis-je ouvrir la fenêtre ?','我可以开窗吗？'),('Puis-je fermer la porte ?','我可以关门吗？'),('Vous permettez ?','可以吗？'),('Je vous remercie sincèrement.','我真诚地感谢您。'),('Merci, vous m’avez beaucoup aidé.','谢谢，您帮了我大忙。'),('C’est très aimable à vous.','您真是太客气了。'),('Je suis ravi de vous rencontrer.','很高兴认识您。'),('Je suis heureux de faire votre connaissance.','很高兴认识您。'),('Ça fait longtemps qu’on ne s’est pas vus.','我们好久没见了。'),('Heureux de vous revoir.','很高兴再次见到您。'),('Passez une bonne journée.','祝您今天愉快。'),('Passez une bonne soirée.','祝您晚上愉快。'),('Passez un bon week-end.','祝您周末愉快。'),('Bon retour !','祝您返程顺利！'),('À très bientôt !','很快再见！'),('À la semaine prochaine !','下周见！'),('Merci d’être là.','谢谢您能来。'),('Merci de m’avoir attendu.','谢谢您等我。'),('Pardon pour l’attente.','抱歉让您久等了。'),('Désolé pour le dérangement.','抱歉给您添麻烦。'),('Je vous prie de m’excuser.','请您原谅。'),('Ce sera avec plaisir.','我很乐意。'),('Volontiers, merci.','好啊，谢谢。'),('Je préfère décliner, merci.','我还是婉拒了，谢谢。'),('Merci, mais ce ne sera pas possible.','谢谢，不过这次不行。'),('Je vous souhaite bon courage.','祝您顺利。'),('Je vous souhaite bonne chance.','祝您好运。'),('Félicitations pour votre réussite !','祝贺您取得成功！'),('Tous mes vœux de bonheur.','祝您幸福。'),('Profitez bien de votre séjour.','祝您旅途/停留愉快。'),('Bon voyage et à bientôt.','旅途愉快，回头见。'),('Merci pour cette agréable soirée.','谢谢这个愉快的夜晚。'),('J’ai été ravi de vous rencontrer.','很高兴认识您。'),('Au revoir et bonne journée.','再见，祝您今天愉快。'),('Bonne continuation !','祝接下来一切顺利！'),('À bientôt, prenez soin de vous.','回头见，请保重。')]
    out+=courtesy
    take(0,out)
cat0()

# 通用：原始25个概念 + 7个完全适配该类概念的自然变体。
def cat1():
    jobs=[('étudiant','学生'),('professeur','老师'),('ingénieur','工程师'),('médecin','医生'),('infirmier','护士'),('designer','设计师'),('développeur','开发人员'),('comptable','会计'),('cuisinier','厨师'),('serveur','服务员'),('vendeur','销售员'),('photographe','摄影师'),('musicien','音乐人'),('architecte','建筑师'),('journaliste','记者'),('avocat','律师'),('chauffeur','司机'),('chercheur','研究人员'),('traducteur','翻译'),('entrepreneur','创业者'),('stagiaire','实习生'),('manager','经理'),('technicien','技术员'),('artiste','艺术家'),('consultant','顾问')]
    out=[]
    for j,z in jobs:
      if j=='étudiant':
        out += [('Je suis étudiant.','我是学生。'),('J’étudie à l’université.','我在大学学习。'),('Je suis étudiant depuis trois ans.','我读大学已经三年了。'),('En ce moment, je suis étudiant à temps plein.','我目前是全日制学生。'),('Je viens de commencer mes études.','我刚开始我的学业。'),('Je suis en cours aujourd’hui.','我今天有课。'),('Dans la vie, je suis étudiant.','我的身份是学生。'),('Quand je me présente, je dis que je suis étudiant.','自我介绍时，我会说我是学生。')]
      else:
        out += [
         (f'Je suis {j}.',f'我是{z}。'),(f'Je travaille comme {j}.',f'我的工作是{z}。'),(f'Je travaille comme {j} depuis trois ans.',f'我做{z}已经三年了。'),(f'En ce moment, je travaille comme {j}.',f'我目前从事{z}工作。'),(f'Je viens de commencer comme {j}.',f'我刚开始做{z}。'),(f'Je suis {j} à temps plein.',f'我是全职{z}。'),(f'Dans la vie, je suis {j}.',f'我的职业/身份是{z}。'),(f'Quand je me présente, je dis que je suis {j}.',f'自我介绍时，我会说我是{z}。')]
    take(1,out)
cat1()

def cat2():
    rel=[('mon père','我爸爸'),('ma mère','我妈妈'),('mon frère','我哥哥/弟弟'),('ma sœur','我姐姐/妹妹'),('mon mari','我丈夫'),('ma femme','我妻子'),('mon fils','我儿子'),('ma fille','我女儿'),('mon grand-père','我爷爷/外公'),('ma grand-mère','我奶奶/外婆'),('mon oncle','我叔叔/舅舅'),('ma tante','我姑姑/姨妈'),('mon cousin','我的男性堂/表亲'),('ma cousine','我的女性堂/表亲'),('mon neveu','我侄子/外甥'),('ma nièce','我侄女/外甥女'),('mes parents','我父母'),('mes enfants','我孩子们'),('mes grands-parents','我祖父母/外祖父母'),('mon beau-père','我岳父/公公/继父'),('ma belle-mère','我岳母/婆婆/继母'),('mon beau-frère','我的男性姻亲'),('ma belle-sœur','我的女性姻亲'),('mon petit-fils','我孙子/外孙'),('ma petite-fille','我孙女/外孙女')]
    out=[]
    for r,z in rel:
      out += [(f'Voici {r}.',f'这是{z}。'),(f'Je vais vous présenter {r}.',f'我给您介绍一下{z}。'),(f'Je parle souvent avec {r}.',f'我经常和{z}聊天。'),(f'Je vais voir {r} ce week-end.',f'这个周末我要去见{z}。'),(f'J’ai reçu un message de {r}.',f'我收到了{z}的消息。'),(f'Je dois appeler {r} ce soir.',f'我今晚得给{z}打电话。'),(f'Je passe beaucoup de temps avec {r}.',f'我和{z}经常待在一起。'),(f'{r.capitalize()} habite en France.',f'{z}住在法国。')]
    take(2,out)
cat2()

def cat3():
    rooms=[('la cuisine','厨房'),('le salon','客厅'),('la chambre','卧室'),('la salle de bains','浴室'),('le balcon','阳台'),('le jardin','花园'),('la porte','门'),('la fenêtre','窗户'),('la table','桌子'),('la chaise','椅子'),('le canapé','沙发'),('le lit','床'),('le réfrigérateur','冰箱'),('le four','烤箱'),('le micro-ondes','微波炉'),('la machine à laver','洗衣机'),('la lampe','灯'),('la télévision','电视'),('le placard','橱柜'),('le miroir','镜子'),('le bureau','书桌/办公室'),('le garage','车库'),('la douche','淋浴间'),('les toilettes','卫生间'),('l’entrée','入口/玄关')]
    out=[]
    for n,z in rooms:
      est='sont' if n.startswith('les ') else 'est'
      verb='sont' if n.startswith('les ') else 'est'
      trouve='se trouvent' if n.startswith('les ') else 'se trouve'
      out += [(f'Où {verb} {n} ?',f'{z}在哪里？'),(f'Vous pouvez me montrer {n} ?',f'您能给我指一下{z}吗？'),(f'Je cherche {n}.',f'我在找{z}。'),(f'{n.capitalize()} {verb} où, exactement ?',f'{z}具体在哪里？'),(f'Je voudrais voir {n}.',f'我想看看{z}。'),(f'Est-ce que je peux utiliser {n} ?',f'我可以使用{z}吗？'),(f'Pouvez-vous me dire où {trouve} {n} ?',f'您能告诉我{z}在哪里吗？'),(f'Je voudrais savoir où {trouve} {n}.',f'我想知道{z}在哪里。')]
    take(3,out)
cat3()

def action_cat(c, actions, timeword='aujourd’hui'):
    out=[]
    for inf,z in actions:
      out += [(f'Je vais {inf}.',f'我要{z}。'),(f'Je dois {inf} {timeword}.',f'我{timeword=="aujourd’hui" and "今天" or ""}得{z}。'),(f'Je voudrais {inf} maintenant.',f'我现在想{z}。'),(f'Je peux {inf} tout de suite.',f'我现在就可以{z}。'),(f'Je viens de {inf}.',f'我刚刚{z}。'),(f'Je dois penser à {inf}.',f'我得记得{z}。'),(f'Je n’ai pas encore eu le temps de {inf}.',f'我还没来得及{z}。'),(f'J’ai prévu de {inf}.',f'我计划{z}。')]
    take(c,out)

actions4=[('me lever tôt','早起'),('prendre une douche','洗澡'),('me brosser les dents','刷牙'),('préparer le petit-déjeuner','准备早餐'),('boire un café','喝咖啡'),('aller au travail','去上班'),('prendre le métro pour aller au travail','坐地铁去上班'),('lire mes messages','看消息'),('faire une pause','休息一下'),('déjeuner','吃午饭'),('faire une promenade','散步'),('faire les courses','买东西'),('rentrer à la maison','回家'),('préparer le dîner','准备晚饭'),('faire la vaisselle','洗碗'),('prendre un bain','泡澡'),('regarder la télévision','看电视'),('lire un livre','看书'),('écouter de la musique','听音乐'),('faire du sport','运动'),('appeler mes parents','给父母打电话'),('préparer mes affaires','收拾东西'),('mettre le réveil','设置闹钟'),('me coucher tôt','早睡'),('dormir huit heures','睡八小时')]
action_cat(4,actions4)

def cat5():
    times=[('ce matin','今天早上'),('cet après-midi','今天下午'),('ce soir','今晚'),('demain matin','明天早上'),('demain après-midi','明天下午'),('demain soir','明晚'),('lundi','星期一'),('mardi','星期二'),('mercredi','星期三'),('jeudi','星期四'),('vendredi','星期五'),('samedi','星期六'),('dimanche','星期日'),('à huit heures','八点'),('à neuf heures','九点'),('à dix heures','十点'),('à midi','中午十二点'),('à quatorze heures','十四点'),('à dix-huit heures','十八点'),('à vingt heures','二十点'),('la semaine prochaine','下周'),('le mois prochain','下个月'),('ce week-end','这个周末'),('dans une heure','一小时后'),('dans dix minutes','十分钟后')]
    out=[]
    for t,z in times:
      out += [(f'On se voit {t}.',f'我们{z}见。'),(f'Est-ce que vous êtes libre {t} ?',f'您{z}有空吗？'),(f'Je suis disponible {t}.',f'我{z}有空。'),(f'Ça vous va, {t} ?',f'{z}可以吗？'),(f'Je peux passer {t}.',f'我可以{z}过去。'),(f'Le rendez-vous est prévu {t}.',f'约会/预约安排在{z}。'),(f'Je vous appelle {t}.',f'我{z}给您打电话。'),(f'Je vous confirme ça {t}.',f'我{z}给您确认这件事。')]
    take(5,out)
cat5()

def cat6():
    cond=[('Il fait beau','天气很好'),('Il fait chaud','天气很热'),('Il fait froid','天气很冷'),('Il fait frais','天气凉爽'),('Il y a du soleil','有太阳'),('Il y a du vent','有风'),('Il pleut','下雨'),('Il neige','下雪'),('Il y a du brouillard','有雾'),('Le ciel est couvert','天空阴沉'),('Le ciel est clair','天空晴朗'),('Il fait humide','天气潮湿'),('Il fait sec','天气干燥'),('Il y a un orage','有雷雨'),('Il y a des nuages','有云'),('La température monte','气温在升高'),('La température baisse','气温在下降'),('Le temps change vite','天气变化很快'),('La pluie s’arrête','雨停了'),('Le vent se lève','起风了'),('Le soleil se couche','太阳要落山了'),('La nuit est douce','夜晚很温和'),('L’air est agréable','空气很舒适'),('Il fait trente degrés','气温三十度'),('Il fait dix degrés','气温十度')]
    out=[]
    for f,z in cond:
      fl=f[0].lower()+f[1:]
      out += [(f'{f} aujourd’hui.',f'今天{z}。'),(f'Ce matin, {fl}.',f'今天早上{z}。'),(f'Cet après-midi, {fl}.',f'今天下午{z}。'),(f'Demain, on prévoit que {fl}.',f'预计明天{z}。'),(f'On dirait que {fl}.',f'看起来{z}。'),(f'J’ai vu que {fl}.',f'我看到{z}。'),(f'Pour l’instant, {fl}.',f'目前{z}。'),(f'D’après la météo, {fl}.',f'根据天气预报，{z}。')]
    take(6,out)
cat6()

def cat7():
    items=[('ce pantalon','这条裤子'),('cette chemise','这件衬衫'),('cette robe','这条连衣裙'),('ce manteau','这件外套'),('cette veste','这件夹克'),('ces chaussures','这双鞋'),('ce sac','这个包'),('ce chapeau','这顶帽子'),('cette écharpe','这条围巾'),('cette montre','这块手表'),('ce téléphone','这部手机'),('cet ordinateur','这台电脑'),('ce chargeur','这个充电器'),('ce livre','这本书'),('ce cahier','这个笔记本'),('ce stylo','这支笔'),('cette bouteille','这个瓶子'),('ce cadeau','这件礼物'),('ce parfum','这瓶香水'),('ce savon','这块肥皂'),('cette serviette','这条毛巾'),('ce fromage','这块奶酪'),('ce pain','这个面包'),('ces fruits','这些水果'),('ces légumes','这些蔬菜')]
    out=[]
    for n,z in items:
      out += [(f'Je cherche {n}.',f'我在找{z}。'),(f'Combien coûte {n} ?',f'{z}多少钱？'),(f'Je voudrais voir {n}, s’il vous plaît.',f'我想看看{z}，谢谢。'),(f'Est-ce que {n} est en promotion ?',f'{z}在打折吗？'),(f'Vous avez {n} en stock ?',f'{z}有现货吗？'),(f'Je vais prendre {n}.',f'我要买{z}。'),(f'Je peux payer {n} par carte ?',f'我可以刷卡支付{z}吗？'),(f'Je voudrais échanger {n}.',f'我想换{z}。')]
    take(7,out)
cat7()

def cat8():
    foods=[('un café','一杯咖啡'),('un thé','一杯茶'),('un chocolat chaud','一杯热巧克力'),('un jus d’orange','一杯橙汁'),('une bouteille d’eau','一瓶水'),('une baguette','一根法棍'),('un croissant','一个可颂'),('une omelette','一份煎蛋卷'),('une salade','一份沙拉'),('une soupe','一份汤'),('un sandwich','一个三明治'),('un steak','一份牛排'),('du poulet','鸡肉'),('du poisson','鱼'),('des pâtes','意大利面'),('du riz','米饭'),('des frites','薯条'),('une pizza','一个披萨'),('un dessert','一份甜点'),('une glace','一份冰淇淋'),('un gâteau','一块蛋糕'),('du fromage','奶酪'),('des fruits','水果'),('un petit-déjeuner','一份早餐'),('un menu du jour','一份今日套餐')]
    out=[]
    for n,z in foods:
      out += [(f'Je voudrais {n}, s’il vous plaît.',f'我想要{z}，谢谢。'),(f'Je vais prendre {n}.',f'我要{z}。'),(f'Est-ce que vous avez {n} ?',f'你们有{z}吗？'),(f'Je peux avoir {n} ?',f'我可以要{z}吗？'),(f'Je voudrais commander {n}.',f'我想点{z}。'),(f'Sans trop attendre, je prendrai {n}.',f'如果不用等太久，我要{z}。'),(f'Vous me conseillez {n} ?',f'您推荐{z}吗？'),(f'Je peux emporter {n} ?',f'{z}可以打包带走吗？')]
    take(8,out)
cat8()

def cat9():
    modes=[('le métro','地铁'),('le bus','公交车'),('le train','火车'),('le tramway','有轨电车'),('le taxi','出租车'),('le vélo','自行车'),('la voiture','汽车'),('le RER','法兰西岛区域快铁'),('le TGV','法国高速列车'),('l’avion','飞机'),('le bateau','船'),('le ferry','渡轮'),('la navette','接驳车'),('le car','长途大巴'),('la moto','摩托车'),('la trottinette','滑板车'),('le covoiturage','拼车'),('le train de nuit','夜行列车'),('le train régional','区域列车'),('la ligne un','一号线'),('la ligne deux','二号线'),('la ligne trois','三号线'),('le bus de nuit','夜班公交'),('la navette aéroport','机场接驳车'),('le funiculaire','缆索铁路')]
    out=[]
    for n,z in modes:
      out += [(f'Je prends {n}.',f'我乘{z}。'),(f'Je vais prendre {n}.',f'我要乘{z}。'),(f'Où est-ce que je peux prendre {n} ?',f'我在哪里可以乘{z}？'),(f'Je préfère prendre {n}.',f'我更愿意乘{z}。'),(f'Je voudrais des informations sur {n}.',f'我想了解{z}的信息。'),(f'Pouvez-vous m’aider à prendre {n} ?',f'您能帮我乘坐/使用{z}吗？'),(f'Je voudrais savoir où trouver {n}.',f'我想知道在哪里能找到{z}。'),(f'Est-ce que je peux utiliser {n} pour ce trajet ?',f'这段路我可以乘坐/使用{z}吗？')]
    take(9,out)
cat9()

def cat10():
    needs=[('une chambre simple','一间单人房'),('une chambre double','一间双人房'),('une chambre calme','一间安静的房间'),('une chambre avec vue','一间带景观的房间'),('une chambre non-fumeur','一间无烟房'),('un lit double','一张双人床'),('deux lits simples','两张单人床'),('le petit-déjeuner','早餐'),('une place de parking','一个停车位'),('le Wi-Fi gratuit','免费 Wi-Fi'),('une serviette propre','一条干净毛巾'),('un oreiller supplémentaire','一个额外枕头'),('une couverture','一条毯子'),('un sèche-cheveux','一个吹风机'),('un adaptateur','一个转换插头'),('un coffre-fort','一个保险箱'),('la climatisation','空调'),('un service de réveil','叫醒服务'),('une consigne à bagages','行李寄存'),('un plan de la ville','一张城市地图'),('un taxi pour l’aéroport','一辆去机场的出租车'),('une nuit supplémentaire','多住一晚'),('un départ tardif','延迟退房'),('une facture','一张发票'),('la clé de la chambre','房间钥匙')]
    out=[]
    def de_form(n):
      if n.startswith('un '): return 'd’un '+n[3:]
      if n.startswith('une '): return 'd’une '+n[4:]
      if n.startswith('le '): return 'du '+n[3:]
      if n.startswith('la '): return 'de la '+n[3:]
      if n.startswith('l’'): return 'de '+n
      return 'de '+n
    for n,z in needs:
      out += [(f'Je voudrais {n}.',f'我想要{z}。'),(f'Est-ce que vous avez {n} ?',f'您这里有{z}吗？'),(f'Je peux avoir {n}, s’il vous plaît ?',f'我可以要{z}吗？'),(f'Je voudrais savoir si vous pouvez me proposer {n}.',f'我想知道您能否提供{z}。'),(f'Comment puis-je obtenir {n} ?',f'我怎样才能获得{z}？'),(f'Pouvez-vous m’aider à obtenir {n} ?',f'您能帮我获得{z}吗？'),(f'J’ai besoin {de_form(n)}.',f'我需要{z}。'),(f'À qui dois-je demander pour obtenir {n} ?',f'我应该向谁询问才能获得{z}？')]
    take(10,out)
cat10()

def cat11():
    places=[('la gare','火车站'),('la station de métro','地铁站'),('l’arrêt de bus','公交站'),('l’aéroport','机场'),('l’hôtel','酒店'),('le restaurant','餐厅'),('le café','咖啡馆'),('la pharmacie','药店'),('l’hôpital','医院'),('la banque','银行'),('le distributeur','自动取款机'),('la poste','邮局'),('le supermarché','超市'),('le marché','市场'),('le musée','博物馆'),('le parc','公园'),('la mairie','市政厅'),('l’office de tourisme','游客中心'),('les toilettes publiques','公共卫生间'),('le commissariat','警察局'),('la boulangerie','面包店'),('la bibliothèque','图书馆'),('le centre-ville','市中心'),('la place principale','主广场'),('la rue de la Paix','和平街')]
    out=[]
    for n,z in places:
      est='sont' if n.startswith('les ') else 'est'
      accessible='accessibles' if n.startswith('les ') else 'accessible'
      out += [(f'Où {est} {n} ?',f'{z}在哪里？'),(f'Comment aller à {n} ?',f'怎么去{z}？'),(f'Je cherche {n}.',f'我在找{z}。'),(f'{n.capitalize()} {est} loin d’ici ?',f'{z}离这里远吗？'),(f'Est-ce que {n} {est} {accessible} à pied ?',f'可以步行去{z}吗？'),(f'Quel est le chemin le plus rapide pour {n} ?',f'去{z}最快怎么走？'),(f'Vous pouvez me montrer {n} sur la carte ?',f'您能在地图上给我指出{z}吗？'),(f'Je suis près de {n}, c’est bien ça ?',f'我现在在{z}附近，对吗？')]
    take(11,out)
cat11()

actions12=[('répondre aux e-mails','回复邮件'),('préparer la réunion','准备会议'),('appeler un client','给客户打电话'),('finir ce rapport','完成这份报告'),('vérifier les chiffres','核对数字'),('mettre à jour le document','更新文档'),('envoyer le fichier','发送文件'),('organiser mon agenda','整理日程'),('faire une présentation','做演示'),('prendre des notes','做笔记'),('discuter du projet','讨论项目'),('corriger une erreur','纠正错误'),('demander un délai','申请延期'),('confirmer le rendez-vous','确认预约'),('réserver une salle','预订会议室'),('imprimer le contrat','打印合同'),('signer le document','签署文件'),('relire le message','重新检查消息'),('partager mon écran','共享屏幕'),('rejoindre la visioconférence','加入视频会议'),('terminer cette tâche','完成这个任务'),('planifier la semaine','规划这一周'),('parler avec mon collègue','和同事交谈'),('faire une pause café','喝咖啡休息一下'),('ranger mon bureau','整理办公桌')]
action_cat(12,actions12)

actions13=[('apprendre du vocabulaire','学词汇'),('réviser la grammaire','复习语法'),('écouter un dialogue','听对话'),('lire un article','读一篇文章'),('écrire un paragraphe','写一段文字'),('faire un exercice','做一道练习'),('corriger mes erreurs','改正错误'),('mémoriser cette phrase','记住这个句子'),('pratiquer la prononciation','练习发音'),('poser une question','提一个问题'),('répondre à la question','回答问题'),('prendre des notes en cours','上课做笔记'),('chercher un mot','查一个单词'),('utiliser le dictionnaire','使用词典'),('regarder une vidéo','看视频'),('faire mes devoirs','做作业'),('préparer l’examen','准备考试'),('réviser la leçon','复习课文'),('parler en français','说法语'),('écouter du français','听法语'),('lire à voix haute','大声朗读'),('répéter la phrase','重复句子'),('travailler avec un partenaire','和搭档练习'),('faire une dictée','做听写'),('étudier pendant trente minutes','学习三十分钟')]
action_cat(13,actions13)

def cat14():
    symptoms=[('mal à la tête','头疼'),('mal à la gorge','嗓子疼'),('mal au dos','背疼'),('mal au ventre','肚子疼'),('de la fièvre','发烧'),('un rhume','感冒'),('une toux','咳嗽'),('le nez bouché','鼻塞'),('des vertiges','头晕'),('des nausées','恶心'),('une allergie','过敏'),('une douleur au genou','膝盖疼'),('une douleur à l’épaule','肩膀疼'),('une douleur à la dent','牙疼'),('une douleur à l’oreille','耳朵疼'),('les yeux fatigués','眼睛疲劳'),('du mal à dormir','睡不好'),('des difficultés à respirer','呼吸困难'),('une petite coupure','有个小伤口'),('une brûlure légère','有轻微烫伤'),('une douleur musculaire','肌肉疼'),('une migraine','偏头痛'),('l’estomac sensible','胃不舒服'),('une irritation de la peau','皮肤刺激/不适'),('beaucoup de fatigue','很疲惫')]
    out=[]
    for n,z in symptoms:
      out += [(f'J’ai {n}.',f'我{z}。'),(f'Depuis ce matin, j’ai {n}.',f'从今天早上开始，我{z}。'),(f'J’ai encore {n}.',f'我还是{z}。'),(f'Je consulte parce que j’ai {n}.',f'我来看医生，因为我{z}。'),(f'Qu’est-ce que je peux prendre si j’ai {n} ?',f'如果我{z}，可以吃什么药？'),(f'Est-ce grave si j’ai {n} ?',f'我{z}严重吗？'),(f'J’ai {n} depuis deux jours.',f'我{z}已经两天了。'),(f'Je voudrais expliquer au médecin que j’ai {n}.',f'我想告诉医生我{z}。')]
    take(14,out)
cat14()

actions15=[('charger mon téléphone','给手机充电'),('connecter le Wi-Fi','连接 Wi-Fi'),('envoyer un message','发消息'),('passer un appel','打电话'),('répondre à l’appel','接电话'),('laisser un message vocal','留语音留言'),('ouvrir l’application','打开应用'),('fermer l’application','关闭应用'),('redémarrer le téléphone','重启手机'),('mettre le téléphone en silencieux','把手机调成静音'),('augmenter le volume','调高音量'),('baisser le volume','调低音量'),('activer le Bluetooth','打开蓝牙'),('désactiver le Bluetooth','关闭蓝牙'),('partager la connexion','共享网络'),('envoyer une photo','发送照片'),('télécharger le fichier','下载文件'),('ouvrir le lien','打开链接'),('scanner le code QR','扫描二维码'),('changer le mot de passe','修改密码'),('vérifier la connexion','检查网络连接'),('allumer l’ordinateur','打开电脑'),('éteindre l’ordinateur','关闭电脑'),('faire une visioconférence','进行视频会议'),('sauvegarder mes données','备份数据')]
action_cat(15,actions15)

def cat16():
    acts=[('lire un roman','读小说'),('regarder un film','看电影'),('regarder une série','看电视剧'),('écouter de la musique','听音乐'),('jouer au football','踢足球'),('jouer au basket','打篮球'),('jouer au tennis','打网球'),('faire du vélo','骑自行车'),('faire de la randonnée','徒步'),('nager','游泳'),('courir','跑步'),('faire du yoga','做瑜伽'),('prendre des photos','拍照'),('dessiner','画画'),('cuisiner','做饭'),('faire du jardinage','做园艺'),('visiter un musée','参观博物馆'),('aller au cinéma','去电影院'),('aller au concert','去听音乐会'),('jouer aux jeux vidéo','玩电子游戏'),('faire un pique-nique','野餐'),('voyager','旅行'),('danser','跳舞'),('chanter','唱歌'),('me reposer','休息')]
    out=[]
    for a,z in acts:
      out += [(f'J’aime {a}.',f'我喜欢{z}。'),(f'J’aime bien {a} le week-end.',f'我周末喜欢{z}。'),(f'J’adore {a}.',f'我非常喜欢{z}。'),(f'J’aimerais {a} plus souvent.',f'我想更经常{z}。'),(f'Quand j’ai du temps, j’aime {a}.',f'有空的时候我喜欢{z}。'),(f'Ça me détend de {a}.',f'{z}让我放松。'),(f'On peut {a} ensemble un jour.',f'哪天我们可以一起{z}。'),(f'Je préfère {a} avec des amis.',f'我更喜欢和朋友一起{z}。')]
    take(16,out)
cat16()

def cat17():
    acts=[('prendre un café','喝咖啡'),('déjeuner','吃午饭'),('dîner','吃晚饭'),('aller au cinéma','去看电影'),('faire une promenade','散步'),('aller au parc','去公园'),('visiter le musée','参观博物馆'),('faire du shopping','逛街'),('jouer au tennis','打网球'),('faire du vélo','骑自行车'),('prendre un verre','喝一杯'),('aller au concert','去听音乐会'),('venir chez moi','来我家'),('faire un pique-nique','野餐'),('cuisiner','做饭'),('étudier','学习'),('pratiquer le français','练习法语'),('regarder un film','看电影'),('faire une randonnée','徒步'),('aller à la plage','去海滩'),('visiter le centre-ville','逛市中心'),('prendre des photos','拍照'),('jouer à un jeu','玩游戏'),('fêter ton anniversaire','庆祝你的生日'),('passer la soirée','度过晚上')]
    out=[]
    for a,z in acts:
      out += [(f'Tu veux {a} avec moi ?',f'你想和我一起{z}吗？'),(f'Ça te dit de {a} ?',f'你想{z}吗？'),(f'On pourrait {a} ce week-end.',f'这个周末我们可以{z}。'),(f'Est-ce que tu es libre pour {a} ?',f'你有空一起{z}吗？'),(f'J’aimerais bien {a} avec toi.',f'我很想和你一起{z}。'),(f'On se retrouve pour {a} ?',f'我们碰面一起{z}好吗？'),(f'Je t’invite à {a}.',f'我邀请你一起{z}。'),(f'Quel jour te conviendrait pour {a} ?',f'哪天适合一起{z}？')]
    take(17,out)
cat17()

def cat18():
    states=[('content','开心'),('heureux','幸福/高兴'),('calme','平静'),('détendu','放松'),('motivé','有动力'),('fatigué','疲惫'),('stressé','有压力'),('inquiet','担心'),('surpris','惊讶'),('déçu','失望'),('triste','难过'),('en colère','生气'),('nerveux','紧张'),('confiant','有信心'),('curieux','好奇'),('impatient','迫不及待'),('satisfait','满意'),('fier','自豪'),('perdu','迷茫'),('occupé','忙'),('libre','有空'),('prêt','准备好了'),('malade','不舒服/生病'),('affamé','很饿'),('assoiffé','很渴')]
    out=[]
    for a,z in states:
      out += [(f'Je suis {a}.',f'我{z}。'),(f'Aujourd’hui, je me sens {a}.',f'今天我感觉{z}。'),(f'En ce moment, je suis plutôt {a}.',f'我现在比较{z}。'),(f'Je me sens un peu {a}.',f'我感觉有点{z}。'),(f'Je suis vraiment {a} aujourd’hui.',f'我今天真的很{z}。'),(f'Je ne pensais pas être aussi {a}.',f'我没想到自己会这么{z}。'),(f'Après ça, je me sens {a}.',f'那之后我感觉{z}。'),(f'Je voulais vous dire que je suis {a}.',f'我想告诉您，我现在{z}。')]
    take(18,out)
cat18()

def cat19():
    # 25 核心求助意图，每个意图配 8 种真实可用表达；避免“紧急：+任意句”式机械凑数。
    intents=[
      [('Appelez la police !','请报警！'),('Pouvez-vous appeler la police ?','您能报警吗？'),('J’ai besoin de la police.','我需要警察帮助。'),('C’est urgent, appelez la police.','情况紧急，请报警。'),('Où est le commissariat le plus proche ?','最近的警察局在哪里？'),('Je voudrais parler à la police.','我想和警察说明情况。'),('Aidez-moi à contacter la police.','请帮我联系警察。'),('Quel est le numéro de la police ?','报警电话是多少？')],
      [('Appelez une ambulance !','请叫救护车！'),('Pouvez-vous appeler une ambulance ?','您能叫救护车吗？'),('J’ai besoin d’une ambulance.','我需要救护车。'),('C’est urgent, appelez une ambulance.','情况紧急，请叫救护车。'),('Une personne est blessée.','有人受伤了。'),('Il faut une ambulance tout de suite.','需要立刻叫救护车。'),('Aidez-moi à appeler les secours.','请帮我呼叫急救。'),('Où est l’hôpital le plus proche ?','最近的医院在哪里？')],
      [('Appelez les pompiers !','请叫消防员！'),('Il y a un incendie.','这里发生了火灾。'),('Je vois de la fumée.','我看到有烟。'),('Le feu s’est déclaré ici.','这里起火了。'),('Il faut évacuer le bâtiment.','需要疏散这栋楼。'),('Où est la sortie de secours ?','紧急出口在哪里？'),('Aidez-moi à sortir.','请帮我出去。'),('Quel est le numéro des pompiers ?','消防电话是多少？')],
    ]
    # 其余22个用每项8句的精选模板
    cores=[
      ('un médecin','医生'),('de l’aide','帮助'),('mon chemin','路'),('mon portefeuille','钱包'),('mon téléphone','手机'),('mon passeport','护照'),('mes clés','钥匙'),('un accident','事故'),('me sentir mal','身体不舒服'),('respirer','呼吸'),('une blessure','受伤'),('mon ami blessé','朋友受伤'),('la sortie de secours','紧急出口'),('le commissariat','警察局'),('l’hôpital le plus proche','最近的医院'),('un taxi','出租车'),('mon ambassade','我的大使馆'),('ma carte bancaire','我的银行卡'),('une déclaration','报案/声明'),('parler plus lentement','说慢一点'),('répéter','重复一遍'),('un interprète','翻译人员')]
    out=[]
    for block in intents: out+=block
    # 手工按语义类型生成，确保每句话都自然
    specific=[
      [('J’ai besoin d’un médecin.','我需要医生。'),('Y a-t-il un médecin ici ?','这里有医生吗？'),('Pouvez-vous appeler un médecin ?','您能叫医生吗？'),('Où puis-je trouver un médecin ?','我在哪里能找到医生？'),('Je dois voir un médecin rapidement.','我需要尽快看医生。'),('C’est une urgence médicale.','这是医疗急症。'),('Aidez-moi à trouver un médecin.','请帮我找医生。'),('Je ne me sens pas bien, j’ai besoin d’un médecin.','我不舒服，需要医生。')],
      [('Aidez-moi, s’il vous plaît.','请帮帮我。'),('J’ai besoin d’aide.','我需要帮助。'),('Pouvez-vous m’aider ?','您能帮我吗？'),('Je suis en difficulté.','我遇到困难了。'),('Je ne sais pas quoi faire.','我不知道该怎么办。'),('S’il vous plaît, restez avec moi.','请陪我一下。'),('Pouvez-vous prévenir quelqu’un ?','您能通知别人吗？'),('Merci de m’aider, c’est urgent.','请帮帮我，情况紧急。')],
      [('Je me suis perdu.','我迷路了。'),('Je ne trouve plus mon chemin.','我找不到路了。'),('Pouvez-vous m’indiquer où je suis ?','您能告诉我我现在在哪里吗？'),('Je dois retrouver le centre-ville.','我得找到回市中心的路。'),('Pouvez-vous me montrer le chemin ?','您能给我指路吗？'),('Je n’ai plus de réseau et je suis perdu.','我没信号了，而且迷路了。'),('Je voudrais retourner à mon hôtel.','我想回酒店。'),('Aidez-moi à retrouver mon chemin.','请帮我找到路。')],
      [('On m’a volé mon portefeuille.','我的钱包被偷了。'),('Mon portefeuille a disparu.','我的钱包不见了。'),('Je veux signaler le vol de mon portefeuille.','我想报案说钱包被偷。'),('Je dois bloquer mes cartes bancaires.','我得冻结银行卡。'),('Où puis-je faire une déclaration de vol ?','我在哪里可以报失窃？'),('J’avais mon portefeuille il y a quelques minutes.','几分钟前我的钱包还在。'),('Pouvez-vous m’aider à appeler ma banque ?','您能帮我给银行打电话吗？'),('Je pense qu’on m’a volé mon portefeuille.','我觉得钱包被偷了。')],
      [('On m’a volé mon téléphone.','我的手机被偷了。'),('Mon téléphone a disparu.','我的手机不见了。'),('Je veux signaler le vol de mon téléphone.','我想报案说手机被偷。'),('Je dois bloquer ma carte SIM.','我得停用 SIM 卡。'),('Pouvez-vous me prêter un téléphone ?','您能借我一部电话吗？'),('Je n’ai plus accès à mon téléphone.','我现在无法使用手机。'),('Je pense qu’on m’a pris mon téléphone.','我觉得有人拿走了我的手机。'),('Aidez-moi à contacter mon opérateur.','请帮我联系运营商。')],
      [('J’ai perdu mon passeport.','我的护照丢了。'),('Je ne trouve plus mon passeport.','我找不到护照了。'),('Je dois déclarer la perte de mon passeport.','我得申报护照遗失。'),('Où est mon ambassade ?','我的大使馆在哪里？'),('Je dois demander un document provisoire.','我需要申请临时证件。'),('Pouvez-vous m’aider à contacter mon ambassade ?','您能帮我联系大使馆吗？'),('Mon passeport a disparu aujourd’hui.','我的护照今天不见了。'),('Que dois-je faire si j’ai perdu mon passeport ?','护照丢了我该怎么办？')],
      [('J’ai perdu mes clés.','我的钥匙丢了。'),('Je ne trouve plus mes clés.','我找不到钥匙了。'),('Je suis bloqué dehors sans mes clés.','我没带钥匙，被锁在门外。'),('Pouvez-vous appeler un serrurier ?','您能叫锁匠吗？'),('J’ai peut-être laissé mes clés ici.','我可能把钥匙落在这里了。'),('Avez-vous trouvé des clés ?','您捡到钥匙了吗？'),('Je cherche un trousseau de clés.','我在找一串钥匙。'),('Qui puis-je appeler pour ouvrir la porte ?','我该找谁来开门？')],
      [('Il y a eu un accident.','这里发生了事故。'),('Je viens d’assister à un accident.','我刚目睹了一起事故。'),('Quelqu’un est blessé après un accident.','事故后有人受伤。'),('Il faut sécuriser la zone.','需要确保现场安全。'),('Pouvez-vous appeler les secours ?','您能呼叫救援吗？'),('L’accident vient de se produire.','事故刚刚发生。'),('La route est bloquée à cause d’un accident.','道路因事故堵塞。'),('Je voudrais signaler un accident.','我想报告一起事故。')],
      [('Je ne me sens pas bien.','我感觉不舒服。'),('Je me sens très faible.','我感觉非常虚弱。'),('J’ai besoin de m’asseoir.','我需要坐一下。'),('Je crois que je vais m’évanouir.','我觉得我要晕倒了。'),('Pouvez-vous rester avec moi ?','您能陪我一下吗？'),('Je voudrais un peu d’eau.','我想喝点水。'),('Je me sens mal depuis quelques minutes.','我几分钟前开始不舒服。'),('Appelez un médecin si ça ne va pas mieux.','如果我没有好转，请叫医生。')],
      [('Je ne peux pas respirer.','我无法呼吸。'),('J’ai du mal à respirer.','我呼吸困难。'),('Je manque d’air.','我喘不上气。'),('Appelez une ambulance, je respire mal.','请叫救护车，我呼吸困难。'),('Aidez-moi à m’asseoir.','请帮我坐下。'),('Je suis essoufflé et ça ne passe pas.','我气喘得厉害，而且没有缓解。'),('J’ai une forte gêne pour respirer.','我呼吸非常不畅。'),('C’est difficile de respirer normalement.','我很难正常呼吸。')],
      [('Je suis blessé.','我受伤了。'),('Je me suis fait mal.','我受伤了。'),('J’ai une blessure qui saigne.','我有伤口在流血。'),('J’ai besoin de soins.','我需要处理伤口。'),('Pouvez-vous m’aider à nettoyer la blessure ?','您能帮我清理伤口吗？'),('Je ne peux pas marcher normalement.','我无法正常走路。'),('La douleur est assez forte.','疼得比较厉害。'),('Je voudrais voir un médecin pour cette blessure.','我想让医生看看这个伤。')],
      [('Mon ami est blessé.','我的朋友受伤了。'),('Mon ami a besoin d’aide.','我的朋友需要帮助。'),('Mon ami saigne.','我的朋友在流血。'),('Pouvez-vous appeler une ambulance pour mon ami ?','您能给我的朋友叫救护车吗？'),('Mon ami ne peut pas se relever.','我的朋友站不起来。'),('Restez avec mon ami, s’il vous plaît.','请陪着我的朋友。'),('Je vais chercher de l’aide pour mon ami.','我要去给朋友找人帮忙。'),('Mon ami a besoin de soins rapidement.','我的朋友需要尽快治疗。')],
      [('Où est la sortie de secours ?','紧急出口在哪里？'),('Montrez-moi la sortie de secours, s’il vous plaît.','请给我指出紧急出口。'),('La sortie de secours est-elle ouverte ?','紧急出口开着吗？'),('Je dois trouver la sortie de secours.','我得找到紧急出口。'),('Quelle sortie devons-nous prendre ?','我们该走哪个出口？'),('Est-ce le chemin vers la sortie de secours ?','这是去紧急出口的路吗？'),('La sortie est-elle par ici ?','出口是在这边吗？'),('Aidez-nous à évacuer par la sortie de secours.','请帮我们从紧急出口疏散。')],
      [('Je cherche le commissariat le plus proche.','我在找最近的警察局。'),('Quel est le commissariat le plus proche ?','最近的警察局在哪里？'),('Je dois aller au commissariat.','我得去警察局。'),('Pouvez-vous m’indiquer le chemin du commissariat ?','您能告诉我去警察局怎么走吗？'),('Le commissariat est-il ouvert ?','警察局开门吗？'),('Je voudrais faire une déclaration au commissariat.','我想去警察局报案。'),('Pouvez-vous m’accompagner au commissariat ?','您能陪我去警察局吗？'),('Je cherche le commissariat de ce quartier.','我在找这个街区的警察局。')],
      [('Où est l’hôpital le plus proche ?','最近的医院在哪里？'),('Quel est l’itinéraire le plus rapide pour l’hôpital ?','去医院最快怎么走？'),('J’ai besoin d’aller à l’hôpital.','我需要去医院。'),('Pouvez-vous appeler un taxi pour l’hôpital ?','您能叫辆出租车去医院吗？'),('Quel hôpital est ouvert maintenant ?','现在哪家医院开着？'),('Il faut aller aux urgences.','需要去急诊。'),('Combien de temps faut-il pour aller à l’hôpital ?','去医院要多久？'),('Montrez-moi l’hôpital sur la carte.','请在地图上给我指出医院。')],
      [('Pouvez-vous appeler un taxi ?','您能叫一辆出租车吗？'),('J’ai besoin d’un taxi tout de suite.','我现在就需要出租车。'),('Où puis-je trouver un taxi ?','我在哪里能找到出租车？'),('Appelez-moi un taxi pour l’hôtel, s’il vous plaît.','请给我叫辆去酒店的出租车。'),('Le taxi peut-il venir ici ?','出租车能来这里吗？'),('Combien de temps faut-il attendre un taxi ?','等出租车要多久？'),('Je voudrais réserver un taxi.','我想预订出租车。'),('Pouvez-vous m’aider à donner l’adresse au chauffeur ?','您能帮我把地址告诉司机吗？')],
      [('Je dois contacter mon ambassade.','我得联系我的大使馆。'),('Où est mon ambassade ?','我的大使馆在哪里？'),('Pouvez-vous m’aider à appeler mon ambassade ?','您能帮我给大使馆打电话吗？'),('J’ai besoin du numéro de mon ambassade.','我需要大使馆的电话号码。'),('Je voudrais prendre rendez-vous à l’ambassade.','我想预约去大使馆。'),('C’est urgent, je dois parler à mon ambassade.','情况紧急，我需要联系大使馆。'),('Comment aller à mon ambassade ?','怎么去我的大使馆？'),('Je dois expliquer ma situation à l’ambassade.','我得向大使馆说明我的情况。')],
      [('Je dois bloquer ma carte bancaire.','我得冻结银行卡。'),('Ma carte bancaire a été volée.','我的银行卡被偷了。'),('J’ai perdu ma carte bancaire.','我的银行卡丢了。'),('Pouvez-vous m’aider à appeler ma banque ?','您能帮我联系银行吗？'),('Je veux faire opposition sur ma carte.','我想挂失/停用银行卡。'),('Je dois sécuriser mon compte bancaire.','我得保护我的银行账户。'),('Je ne peux plus utiliser ma carte.','我的卡现在不能用了。'),('Où puis-je contacter ma banque ?','我在哪里可以联系银行？')],
      [('Je voudrais faire une déclaration.','我想做一份报案/声明。'),('Je voudrais signaler un vol.','我想报失窃。'),('Je voudrais signaler une perte.','我想报遗失。'),('Où puis-je faire une déclaration ?','我在哪里可以报案/登记？'),('De quels documents ai-je besoin ?','我需要哪些材料？'),('Pouvez-vous m’aider à remplir le formulaire ?','您能帮我填表吗？'),('Je voudrais obtenir une copie de la déclaration.','我想拿一份报案记录副本。'),('Je dois expliquer exactement ce qui s’est passé.','我得准确说明发生了什么。')],
      [('Pouvez-vous parler plus lentement ?','您能说慢一点吗？'),('Parlez plus lentement, s’il vous plaît.','请说慢一点。'),('Je ne comprends pas quand vous parlez trop vite.','您说得太快时我听不懂。'),('Pouvez-vous articuler un peu plus ?','您能说得更清楚一点吗？'),('Un peu plus lentement, s’il vous plaît.','请再慢一点。'),('Je comprends mieux si vous parlez lentement.','您说慢一点我更容易听懂。'),('Pouvez-vous dire ça plus doucement ?','您能慢一点说这句话吗？'),('Merci de parler lentement.','谢谢您说慢一点。')],
      [('Pouvez-vous répéter ?','您能重复一遍吗？'),('Répétez, s’il vous plaît.','请再说一遍。'),('Je n’ai pas entendu, pouvez-vous répéter ?','我没听清，您能重复吗？'),('Pouvez-vous répéter la dernière phrase ?','您能重复最后一句吗？'),('Encore une fois, s’il vous plaît.','请再说一遍。'),('Je n’ai pas compris ce mot.','我没听懂这个词。'),('Pouvez-vous le dire autrement ?','您能换一种说法吗？'),('Pouvez-vous écrire ce que vous venez de dire ?','您能把刚才的话写下来吗？')],
      [('J’ai besoin d’un interprète.','我需要翻译人员。'),('Y a-t-il quelqu’un qui parle chinois ?','有人会说中文吗？'),('Pouvez-vous trouver un interprète ?','您能找一位口译员吗？'),('Je parle seulement un peu français.','我只会一点法语。'),('J’ai besoin d’aide pour traduire.','我需要翻译帮助。'),('Pouvez-vous appeler quelqu’un qui parle anglais ?','您能找会说英语的人吗？'),('Je voudrais un interprète pour cette conversation.','这次谈话我需要口译员。'),('Est-ce qu’un service d’interprétation est disponible ?','这里有口译服务吗？')]
    ]
    for block in specific: out+=block
    out += [
      ('Je suis en danger, aidez-moi.','我有危险，请帮我。'),
      ('Pouvez-vous rester avec moi jusqu’à l’arrivée des secours ?','在救援人员到来前，您能陪着我吗？'),
      ('Je ne connais pas l’adresse exacte.','我不知道确切地址。'),
      ('Pouvez-vous indiquer notre position aux secours ?','您能把我们的位置告诉救援人员吗？'),
      ('Je dois contacter un proche.','我需要联系亲友。'),
      ('Pouvez-vous me prêter votre téléphone pour un appel urgent ?','我能借您的电话打一个紧急电话吗？')]
    take(19,out)
cat19()

if len(ALL)!=4000:
    raise SystemExit(f'expected 4000 got {len(ALL)}')
# ids and IPA. eSpeak is called once per sentence because punctuation can produce
# extra output lines in --stdin batch mode. Parallel calls keep this fast offline.
for i,s in enumerate(ALL,1): s["id"]=i
def make_ipa(text):
    try:
        proc=subprocess.run(["espeak","-q","--ipa=3","-v","fr-fr",text], capture_output=True, text=True, timeout=5)
        return " ".join(proc.stdout.split())
    except Exception:
        return ""
with ThreadPoolExecutor(max_workers=32) as pool:
    ipa_lines=list(pool.map(make_ipa,(x["fr"] for x in ALL)))
for s,ipa in zip(ALL,ipa_lines): s["ipa"]=ipa

# QA
frs=[s['fr'].lower().replace('’',"'") for s in ALL]

assert len(set(frs))==4000, f'duplicates {4000-len(set(frs))}'
for s in ALL:
    if re.search(r'À bientôt[,，].*(ravi|comment allez)',s['fr'],re.I): raise AssertionError(s)
    if 'ensemble avec moi' in s['fr']: raise AssertionError(s)
    if s['fr'].startswith('Où ') and s['fr'].endswith('.'): raise AssertionError(s)

out=ROOT/'sentences-4000.json'
out.write_text(json.dumps(ALL,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'wrote {out} : {len(ALL)} sentences')
for c in range(20): print(c, sum(1 for s in ALL if s['category']==c))
