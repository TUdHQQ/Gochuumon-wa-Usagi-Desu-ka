import json
from PIL import Image, ImageDraw, ImageFont
import os


def save_image(image, output_image_prefix, current_image_id):
    """
    Save the current image with the specified ID.
    """
    if image:
        image.save(f"{output_image_prefix}_{current_image_id}.png")


def generate_char_image(font, char, char_bbox, border_width=2, border_color=(0, 0, 0, 255)):
    """
    Generate the image for a single character with a border.
    """
    char_width = char_bbox[2] - char_bbox[0]
    char_height = char_bbox[3] - char_bbox[1]
    total_width = char_width + 2 * border_width
    total_height = char_height + 2 * border_width

    char_image = Image.new("RGBA", (total_width, total_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(char_image)

    # Draw the border by drawing the character slightly shifted in all directions
    for dx in range(-border_width, border_width + 1):
        for dy in range(-border_width, border_width + 1):
            draw.text(
                (dx - char_bbox[0] + border_width, dy - char_bbox[1] + border_width),
                char,
                font=font,
                fill=border_color
            )

    # Draw the main character in the center
    draw.text(
        (-char_bbox[0] + border_width, -char_bbox[1] + border_width),
        char,
        font=font,
        fill=(255, 255, 255, 255)
    )

    return char_image.crop(char_image.getbbox())


def convert_font(ttf_path, font_size, output_image_prefix="font_bitmap",
                 chars=None, output_json="font_mapping.json",
                 max_image_width=4096, max_image_height=4096):
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmopqrstuvwxyz/:-;!?'.@#%~*&`()°^>+<ﾉ･=″$′_{|}０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ．：；゛゜‘’“”〔〕［］｛｝〈〉《》「」『』【】＜＞〖〗・⋯〜ー♪ぁぃぅぇぉっゃゅょゎァィゥェォッャュョヮヵヶ①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬ⁿ²％–—＿／•βγζημξρστυφχψωÅ√◯⌐¬∣¯Д∥αδεθικλνοπヽヾゝゞ〃仝々〆〇＼＋－±×÷＝≠≦≧∞∴♂♀℃￥＄￠￡＃＆＊＠§☆★○●◎◇◆□■△▲▽▼※〒→←↑↓〓∈∋⊆⊇⊂⊃∪∩∧∨￢⇒⇔∀∃∠⊥⌒∂∇≡≒≪≫∽∝∵∫∬‰♯♭†‡¶あいうえおかがきぎくぐけげこごさざしじすずせぜそぞただちぢつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもやゆよらりるれろわゐゑをんアイウエオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモヤユヨラリルレロワヰヱヲンヴΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ∮∑∟⊿弘蓮喘嬌樹県粥匿燦村里衰蛙且扮栽厭稿胄著殖籠媒腎郵舎筐果律透背徳再分淳哉須離喪失可逆境界追時間跳躍空彷徨蝶翼夢幻形而虚像歪曲自己相似無限連鎖携帯電話仮設確認岐指言右耳通口聞完全音夏強烈曰射受俺顎汗滴落染目女傾見学残顔敵地潜入緊張微塵押向直差添黙誰改切気利倫郎問題場変報合判断雑談危険鉢抜駆考機関動開驚声身深息小振運命石扉選択別葉最後刻懐神志同味表存知者数早速足踏正突愚冒使階段力尽椎名様子膝置額滲拭嬉笑実立込彼幼年齢歳高妹近昔鍵過酷宿負素質普願発成功記念銘打本鳳凰院凶真秘密組織狙狂難覚岡部文字幸取銭湯黄色桶教続半諦始東京秋原駅称館登許持般詮試奥点化含程度男触集妨害嘲唇元識側放棄野逃卷勘弁語興休昼貴重割独脳付事磁波攻撃揺衝屋震違悩胸騒飛禁止視壊渡黒煙虹燐光舞爆鳴方奇妙体鎮座謎器衛星係建頭疑答躊躇何員困惑寄思両歩予待隠対応遠匂陰謀巡避決誘導戻姿探踊祥示横並欲眺茶惜締甲冷期雷翔施供海外火規模卵楕円犬類去流忘保証浮玉厳貸平初甘金挿勢挑戦恨輝児握司書皆盛拍迎現壇仏頂溢諸君史紀論終片信満態聴衆増注解返経怒叫恥輪際乗資格若造眼怖線牧瀬紅莉栖友橋田至誌講演容春級卒業研究術載紹介掲写丸印情周囲走従売浴図悔引悪迫端整欠乱混沌私義捕華麗襲抵抗源慌逸崩製焦筋縄略撤退隙詰距爛曈据惚純粋主悲罠薄汚泣辛冗騙次士颯爽単帰妥番途画審映延垂怪舌構帳倒肢護勝席支隅拉致警戒訴万値皿風拾価性悶劣互軌総毛呑悟消暗腰低慎進角伏服絡鮮血溜死異殺蒼白察皮斉由必遺裏払広焼肉親葬式恐寒抱央苦鈍吸犯救急車萌求伝謹奮静尚結局穢宮腐液膿傷浸章刺丈夫憶測銃状魔軽午徒瞬愕摘説未配替拠末町交蔵左折号檜山古居管房旧扱街需寂店長王寺故市騰道楽材優秀随募属創活詳細闇権項派副産序某煩喋僕嫁氏住極即議砕法厨二病乙昨買威圧与髪治偏屈腕青非頼針涙甜濃幅担役門戸叩申孤壮計仲恩反懸飽愛沈譲寿修蒸暑扇井閉超景牛丼客刹量販響陽炎況奢肩暴澄仕辺暮仰巨墜団狭防儀壁破宇宙圏燃嚙官如代呆吐捨矢封狐継犠牲馬蔽国枢符納庫卓台労働飲料良損臓区室貧乏個雀贅沢促窓提衣羽習慣否脱揶揄棚順調推移務校縁月減令品具偶則栄挙粒砲繫五殻迷彩公洗練每簡隔操温駄健凍課験把縫食検討腹痴専録済秒例誤唸転影守達散敬慮骨誉鼻穴赤箱固弱球積為参環位覧敷陸涼効森羅越激訝観痛草週珍短届隣剣霊祟科伸幽頰柔肌凄惨裾懇丁寧燥老授瞥輩冠誕系刊留鋭猫析頑弾干唱及域娘姑偉渋港沖降億遅伴屁穏鏡銀河領潰拳擬往復机根余矛盾誇絶釈歯第堂齟齬柳林社祓脇川沿釣植木殿巫弊漆憐竹掃除夕刀僧助潮妖雨御武舗清斬邪忍税補酸謝師弟云匠鍛斐照瑕滅賛訪父棒紙幣商頃宝池袋泊鳥借憑雰熟罪劇噴尻眩型晶裕吾障埃淀昭揃枚遊絢将儲採曖昧基板収費磨寝挨拶朝袓久咳阿繁賃暇孃硬熱鈴堵災厄遭妄緒遮勉喉潤技稀繰争勃蔓縦晒訳冊読眠索痕跡喫臭妻恋坂賑査十倍埋祭勧輸版展撮徹底排盗璧削桐郁噂賞複脚詣詞責任奪備句脅編換条閃呪省眉粘遣症耐約束聖兄案尾堅露尖嫉妬塗水承泳窺毒杉黎姉疾迅馴策胆亡召杯曜幹委敗鑑共臨種顕兵軍歴稼監胞沙汰努請政府吹披蘇殊香械寸欧米爪艶康飾俗育鹿漏誓鬼畜暁契憧剰泌塞節歓勇偽凝遂祈塩準苛蛍灯履践疲些適稲漂痺等床肝励尊冥福鼓抑悸宛遡唯綻蹴溶易呂伐布処償錯頻鬱陶充迂闊煮八這曼陀癒弛緩絞架馳州核郊蓄嗅汲酬侵涉倉怠昏撫渴玄佳蟢螂紛唾佐灼獄営看溺札魂繕闘率雇狼狽花弄執覆搭縮岸皇北統晴漁缶描薩摩串列裸賢投姦英翻掛呵掘善揉既督三各停叱咤癇癩裁築永膨述企魅宣捜豪滑維拒沽券獣概飯柄猛忠屑哲穫土垣拗益脆抹畏宗掌評詭範催旺翌吟憩楊枝盲荒賭戮奴隸褒縛歌荘棋盤駒陣競碁預雄凌駕旨厚漢託沸仁餌喝采怯渦卑疼奉諜協塊遇尋穿浅克敢氾濫餅九憎湧辞職膳免漬婚軟候挾梢獵潔四喚津悠遙赦湿侮辱兼便荷麵匹母滞帝族欺瞞淡郷枠蓑財閥戯誠脂乾貼鑠叡麓斜島魚骸徴拷径庭箔捉標群占咎粛粉砂糖埼航唆雲罵肯愁旅却典徐泰軋絵繊愉援紫怨芸釀凹炭箇畑城百騎凱旋虜牢還靴唐稽控招股劫渾揮陥玩獲凡阻署猶挽灰勤柱訂恵嵐鶯谷搔鶏抽坊癖轟諭吉啓嘆紳慰洋謦詐傑苑幾秩顛伊疎巣傍羨煎括暖雁播贄捧軸禍緯刃軒旦医晦叶邂逅革袖胃糸陵剃裔醒肖櫛梳濡殴桜綺曇診菜民狩妊娠垢炸裂拓濁閏濯乳洩噌汁褐盆漠昇栗枕鍋涯甚博芝鳩豆鉄喰礎浚凸忽宅穂層網肘姓酔貫畳盟汝薬虫飄旗貌憂該芻拝悦腺哀賀擦冴遽臀蒙斑庇泉浄培養辿娯倣穹漕牙羊宴逐稚猿餐拘逼矜襟剥禿踵肺腑脈酒仄朱岩檻虎眈峰均筒融拡療漫籍依績芽廃征幕欄芳剤誹謗溝巧顧蓋粗剛贈刮窒泥訓熊帽兆貯偵菓揚絆顰蹙菖蒲邁毅浜鷲闖隊覇硝園墓童傘煽梯痙攣綱蜂膜茨筑藍橙煌柵朦朧嗚咽瀕靖徘徊洪瀉嚥唄嚇俳傭摂駐惧忌辟抉豹閲咄嗟踪胴較釘刑崇貢献班拐紐咆哮頓挫患紋翳碧措萎捗佇搾摺傻濾慨杖兎葛藤暦樽凛繭婦孫筆皺綴吊秤湾謳涎窃蹂躪紡峙摯雪慈牒腋給牌銷季嘔氷姫杞蔑冬零憔悴芯潑剌靄栓脛孔媚撼彗郭牽臆堕濤累醜琴恍睫隈党肥貪埒麦辻棲柑橘腔珠昂澱斎桁襖椅頁赴閑蜃楼矯乖腫罰鐘蚊薔薇錬梁膏豊富砦朴僻猜鉛蝉謐鞘謙遜弍傲呈敏滓批茂賽錠虐靱戚噓購廊咬衡耗懲逮巾貨塚南茅撒漿訊堪沬乞槌窮遵崎湘龍酢亭墟杭燈惹漸緻髄怜悧槍又鱗緑囵憤糊孵朗彿庁貰藻酉僅瓦謂勿此株農沼攪諾塔婆熾轄双凵弦筈淫宜纏殲痩烹捏飢鷹詩剖磯江俊镇从搬咖啡实朋间风丝凉课赶紧哎呀眯酱嘿啦孩兔庵呐你时尝单试怎节热饮难红汤圆或糕嘛遗憾哦唉总该给议问题诶几备选黑垩厉拯游噢广阔强乎们戏查隆宏亲让释规则择项升后进达线优级顺结态变另现详拜托閾歉迟门寞锻炼两摔谢军辈梅哈确钟跑应终坏掉它丢场套误趟处馆虽员并戴吓您长孙读懂气认馁扰继稍扬错视仅险书习无论积头脑许茸尔语术换临烊类边桌责扫调师佣报顾惊讶惯严宠愧拿补减准饭锵炖吃谱趁盘摆嚼猥琐怕顿简份碗爸宵挺挡饱净历圈标记吼战业纪诞摸叔脸闹奋羞预谦娇传驳须聚讨碍碰缘笔呃显举办评价义丽验证效耀夺汇况擅哼增坐络绎劲极夸哪虑找谁闻烤骗沮丧亏离剩咧买坚懈跟哄按侘楚划彻瘾续浪费喂搞沉乐站聊带佩羁绊轻松闲舍烦检享宁蛋堆氛围陪唔捂嘴逛怀谎肚饿嘞暂钱够叠计哭泪毫饰圣眨鸡卖输薪约邀护织统筹执领丰撞诺稳连揭晓谜咕咚伟际轮灭蜡烛仪适饼醇隐藏插龄毕恭玻璃笨亮裙务设爷远假创忆榜恢心爱（内）,呼～，泡了个好澡啊]接下来只要睡觉在那之前…关于智乃的生日\n　发邮件告诉大家！因为想庆祝请多帮忙―对象是理世、千夜纱路还有麻耶和惠这样就一定会哇？已经收到回复她说当然太其他人也么快感动被喜着姐开更加油绝不能辜负意首先礼物吧嗯送什呢手工瓶中船很欢呜但精细东西我做得出吗咦话组装起比较趣制作行新拼图兴所以少都嫌没种特别刚炉面包常算。过用马上决慢听见才今天晚安希望明美[	 构测访阈值盖势删链转观冰兰蕾卡六钮营屏估响伙订蓝铁扎罗职糟恼败伤曾凭冲张愿恒烧赖锐挤满额碎腾函协喷蓬坦杂驯树遐靠讲阵绽杏烘奶寻灵杀偷库仿佛阅轴缺步庄联电挂骂园羹货绕仔运竟翘赛憋团钻导惫闪夹纸莫档块喽挖铲辨针蛇迹袭击滚框键棵塌枯聪附遍胳膊弃咻脏废猎阴灌丛队帅词兽龙伍赞噔赢嘎吱哟绘循环填层盒疏华蒡剑芋尼嘻狡猾岂剧槽鲜筛悉购宫财狱囚翁堡晕吻唤允儿吵狗柜垫谓扭舒审荐喊洒扪陷僵七耍恶罢黔驴穷耽侦咨询衷产乍勺斗识巴颗奖阳旁辅渊攀抢涨谈犀艺银毁窗户雾窥凑眷乘肆挥霍逊叹羡慕练醉搜朵覺奔钢爬扁贴款遁默钥匙晨顶抓枪姆祖页飘载专飞逝养馅诱妒盼桩耻锅衬饶猪颜厌谨缸熬肃噗贵茫喧茄涂懒盯浓软酪噎骚镖缩岁愈药赠范编嗨铃铛莓德柴骤资厅闭叛齐础绵铺焙壳敲倾舀搅拌胡椒盐监胀拖腿竞躁遥雅渐睛压睁滋润霜钝喻瞒拦胜诀窍俩轰劳绪溃荣撑啥肴梦嘘噜彰恰袜悄忧忡递拥碌篝趴倦赔训烂贡淇淋扑纳异毯咯踢冻敌谋阱掐颊沟窝啾洞惕匪钞票驶翠搪丫蹦屉签憬诅咒胁睹杰跃碟蹭·捣潇仓锁闯烟囱乡启址橇纵车李网伦维陌垃圾讯录码频惩罚缓纯谅祷弯搁浦岛噩损沾闷篡醋疗棍熄农叼缠尤罕嗤漱霉菩旷勾韵痊衍簪欣啬纫账颈兑瞎董槟缭泼纠疯蠢揍嗓鉴腌岔饪姜匀戳乔悚碑唬饯抛氓咩绷众酥鲷玛蘸盈辣檬柠砖枉冤贾谛砸砺臂砰盎诸咙烩储帆聘宾杜谊潦芒扔胶橡饵搐荧囔飒艇瞌弗缝蛀竖皱鹤豚喱鲁亚阶哒踩芭桥赚滩迄樱驼晃畅抚缀豫贪搓币墨伪罐潘侣抖膀躬晰销嘀祸扯镜肤勒犹拙蝴瓣瑰玫棉伞荫讪仗泽涓蹲墙桂谐蕉苹侈绿瞧勋鸟呦牵咪哨绒贝绑缎摊膛薰躺慧腻澈舱痒译芹哧蛮剪帕卧俯谍奈谙驭驾宽尺瞄帚淆售篷讽拢咸截坡鞠萝臣蹈栏焉霸尘乌苍嚷僭苺昆囓锈拟韧赏汉晩馕撇垒嚏賓艰捆睦扶涩鼠澜齿賊爹扩蔬捞菇凧撕橱嗒吞咀捷妈笞酵抬厢迭狠苗掴逞渠渗质淌葱匍匐骄仇获哥嚓躲庶皂镊犒啃樣篮胖鶴亜娜舔吝擞拔卸跨螺浑辫箭黏鞭滤逻违凳攒捡鞄灾嘶頬嗜狸瓜汽诚扣卜鸦摄扳顽侧磋斯妇杓诡覗廓顏曳畴詫菊匆凿挣噪仙仆歇幌竿宰钩锥薯淹鱼炫窟歹郑摇渉廉泄巷荡筝裹尬弹瀾啪伺贼坟瞑巻蒂馨悬赌鋼掩繋咔绰挟辑掻尴诗綿豁噛嬢琢贤對毎蜜焚‥壱勲裤薫旬奏敞粮瓷烏袴彙捌颤嘟曹洛訣伎柿祇洁雛瞳韻"

    if not os.path.exists(ttf_path):
        raise FileNotFoundError(f"Font file not found: {ttf_path}")

    font = ImageFont.truetype(ttf_path, font_size)
    char_images = {}
    current_image_id = 0
    current_image = Image.new("RGBA", (max_image_width, max_image_height), (0, 0, 0, 0))
    current_x = 0
    current_y = 0
    max_row_height = 0
    ascend, descend = font.getmetrics()

    for char in chars:
        char_bbox = font.getbbox(char)
        char_image = generate_char_image(font, char, char_bbox)
        char_width, char_height = char_image.size

        # Check if the character fits in the current row
        if current_x + char_width > max_image_width:
            current_x = 0
            current_y += max_row_height + 10
            max_row_height = 0

        # Check if the character fits in the current image
        if current_y + char_height > max_image_height:
            save_image(current_image, output_image_prefix, current_image_id)
            current_image_id += 1
            current_image = Image.new("RGBA", (max_image_width, max_image_height), (0, 0, 0, 0))
            current_x = 0
            current_y = 0
            max_row_height = 0

        char_y = current_y + (ascend + char_bbox[1])
        current_image.paste(char_image, (current_x, char_y), char_image)

        char_images[char] = {
            "a": ascend - char_bbox[1] - font_size,
            "b": char_height,
            "d": descend,
            "h": char_height,
            "height": font_size,
            "id": current_image_id,
            "w": char_width,
            "width": char_width,
            "x": current_x,
            "y": char_y,
        }

        current_x += char_width + 5
        max_row_height = max(max_row_height, char_height)

    save_image(current_image, output_image_prefix, current_image_id)

    with open(output_json, "w", encoding="utf-8") as json_file:
        json.dump(char_images, json_file, ensure_ascii=False, indent=2)

    return char_images


# Example usage
font_mapping = convert_font("方正兰亭圆_GBK_准.ttf", 42)
