import json
from PIL import Image, ImageDraw, ImageFont
import os


def save_image(image, output_image_prefix, current_image_id):
    """
    Save the current image with the specified ID.
    """
    if image:
        image.save(f"{output_image_prefix}_{current_image_id}.png")


def generate_char_image(font, char, char_bbox):
    """
    Generate the image for a single character.
    """
    char_width = char_bbox[2] - char_bbox[0]
    char_height = char_bbox[3] - char_bbox[1]
    char_image = Image.new("RGBA", (char_width, char_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(char_image)
    draw.text((-char_bbox[0], -char_bbox[1]), char, font=font, fill=(255, 255, 255, 255))
    return char_image.crop(char_image.getbbox())


def convert_font(ttf_path, font_size, output_image_prefix="font_bitmap",
                 chars=None, output_json="font_mapping.json",
                 max_image_width=2048, max_image_height=1024):
    """
    Convert a font to character images and generate a JSON mapping.
    """
    if chars is None:
        chars = " 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz　/:-;!?'.@#%~*&`()°^>+<ﾉ･=″$′,[\]_{|}…０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ、。，．：；？！゛゜‘’“”（）〔〕［］｛｝〈〉《》「」『』【】＜＞〖〗・⋯〜ー♪―ぁぃぅぇぉっゃゅょゎァィゥェォッャュョヮヵヶ①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬ⁿ²％–—＿／•βγζημξρστυφχψωÅ√◯⌐¬∣¯Д∥αδεθικλνοπヽヾゝゞ〃仝々〆〇＼＋－±×÷＝≠＜＞≦≧∞∴♂♀℃￥＄￠￡％＃＆＊＠§☆★○●◎◇◆□■△▲▽▼※〒→←↑↓〓∈∋⊆⊇⊂⊃∪∩∧∨￢⇒⇔∀∃∠⊥⌒∂∇≡≒≪≫∽∝∵∫∬‰♯♭♪†‡¶あいうえおかがきぎくぐけげこごさざしじすずせぜそぞただちぢつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもやゆよらりるれろわゐゑをんアイウエオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモヤユヨラリルレロヮワヰヱヲンヴΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ∮∑∟⊿弘蓮喘嬌樹県粥匿燦村里衰蛙且扮瓶栽厭稿胄著殖籠媒腎郵舎筐因果律透明背徳再生分淳哉須離喪失不可逆境界面上追加時間跳躍空理彷徨蝶翼夢幻形而虚像歪曲自己相似無限連鎖携帯電話呼出仮設定確認岐先指言右耳当通口聞完全音夏強烈曰射受俺顎汗一滴落染作目前少女首傾見中学残顔今敵地潜入緊張感微塵手押向直人差添黙誰改切会気利倫太郎問題場変報告合的判断雑談危険鉢抜駆考機関動開驚声身深息小振運命石扉選択別葉最後刻懐神意志同味表存在知者世数早速足踏正突愚冒使階段来力尽椎名様子膝置額滲拭嬉笑実物立込彼幼年齢下歳高妹近家所昔鍵過酷宿負素質以普願安発成功記念銘打本鳳凰院凶真秘密組織狙狂難覚岡部文字幸好取嫌銭湯黄色桶教続半諦始東京秋原駅称館登有特許持般詮試奥点化含程度男触集妨害嘲唇元識側放棄野逃卷勘弁語興休昼貴重割独脳天付事件起磁波攻撃揺衝屋震違悩多胸騒飛禁止視壊渡黒煙虹燐光舞爆鳴方奇妙体鎮座謎器大工衛星用係建頭疑然答躊躇何員困惑寄思両歩予待隠対応遠匂陰謀巡避決誘導戻姿探踊祥示横並欲眺心茶惜締甲冷期想雷翔施供海外火規模卵楕円犬類去流行忘保証浮玉厳貸平初甘金挿勢回挑戦恨輝児握司書皆盛拍迎現壇仏頂溢諸君史紀論終片信満態聴衆増注解返望経怒叫恥輪際乗資格若造眼怖線牧瀬紅莉栖友橋田至誌才講演内容春級卒業研究術載紹介掲写丸印象情周囲走従売浴図悔引悪迫端整欠比美乱混沌私義捕華麗襲抵抗源慌逸精崩製焦筋縄略撤退隙詰距爛曈据惚純粋主悲罠薄汚泣辛冗得騙次士颯爽送単帰妥番油途着画審映延垂怪舌構帳倒肢護勝席支隅拉致都警戒訴万値皿風拾価能性悶劣互常軌総毛呑悟路消暗腰低慎進角伏服装絡鮮血溜死異殺他蒼白察皮斉由必遺裏払広焼肉親葬式恐寒抱央苦鈍吸犯救急車萌求伝謹奮静尚結局穢宮腐液膿傷浸章刺丈夫憶測銃状魔軽午徒瞬千愕摘説未配替我拠末町交蔵左折号檜山古居管房旧扱街需要寂店長王寺故市騰道楽材優秀随募属創趣活詳細闇権項派副産序某煩喋僕嫁氏住極即議砕法厨二病乙昨買威圧与髪治偏屈腕青非頼針涙甜濃幅担役門戸叩申孤壮計仲恩反懸飽愛沈譲寿修蒸暑扇井閉超景牛丼客刹那量販快響陽炎況奢肩暴澄仕辺暮仰巨墜団狭防儀壁破宇宙圏燃嚙官如代制呆吐捨矢封狐継犠牲馬蔽国枢符納庫卓台労働飲料良損臓区室貧乏個雀贅沢促窓提衣羽習慣否脱揶揄棚順調推移務校縁月減令品具偶則栄挙粒砲繫五殻迷彩公洗練更每簡隔操到温了駄健凍課験把縫食検討腹痴接専録済秒例誤唸転影守達散敬礼慮骨誉鼻穴赤箱固弱球積為参環位覧敷陸涼効森羅越激訝観痛草週珍短届隣剣霊祟科伸幽頰柔肌凄惨裾懇丁寧燥老授瞥輩冠誕系刊留鋭猫析頑弾干唱及域娘姑偉渋港沖降億遅伴屁穏夜鏡銀河領船潰拳擬往復机根余矛盾誇絶釈歯第堂齟齬柳林社祓脇川沿釣植木殿巫弊漆憐竹掃除夕刀僧助潮妖雨御武舗清斬邪忍税補酸謝師弟云匠鍛斐照瑕滅喜賛訪父棒紙幣商頃宝池袋泊鳥借憑雰熟罪劇噴尻眩型晶新裕吾障埃淀曰昭和揃枚遊絢将儲採算曖昧基板収費磨寝包挨拶朝袓久咳阿繁希賃暇孃硬熱鈴堵災厄遭妄緒遮勉喉潤技稀繰争勃蔓縦晒訳冊読眠索痕跡喫臭妻恋坂賑査十倍埋祭勧輸版展撮徹底排盗璧削桐郁噂賞複脚詣詞責任奪備句脅編換条閃呪省眉粘遣症耐約束聖兄案尾堅露尖嫉妬塗水承泳窺毒杉黎姉疾迅馴策胆亡召杯曜幹委敗鑑共臨種顕兵軍歴稼監胞沙汰努請政府吹披蘇殊香械寸欧米爪艶康飾俗育鹿漏誓鬼畜暁契憧剰泌塞節歓勇偽凝遂祈塩準苛蛍灯履践疲些適稲漂麻痺等床肝励尊冥福鼓抑悸宛遡唯綻蹴溶易呂忙伐布処償錯頻鬱陶充迂闊煮八這曼陀癒弛緩絞架馳州核郊蓄嗅汲酬侵涉倉怠昏撫渴玄佳蟢螂紛唾佐灼獄営看溺札魂繕闘率雇狼狽花弄執覆搭縮岸皇北統晴漁缶描薩摩串列裸睡賢投姦英翻掛呵被掘善揉既督三各停叱咤癇癩裁築永膨述企魅宣捜豪滑維拒沽券獣概飯柄猛忠屑哲穫土垣拗益脆抹畏宗掌評詭範催旺翌吟憩楊枝盲荒賭戮奴隸褒縛歌荘棋盤駒陣競碁預雄凌駕旨厚漢託沸仁餌喝采怯渦卑疼奉諜協塊遇尋穿浅克敢氾濫餅九憎湧辞職膳免漬婚軟候挾梢獵潔四喚津悠遙赦湿侮辱兼便荷麵匹母滞帝族欺瞞淡郷枠蓑財閥戯誠脂乾貼鑠叡麓斜島魚骸徴拷径庭箔捉標群占咎粛粉砂糖埼航唆雲罵肯愁旅却典徐泰軋絵繊愉援紫怨芸釀凹炭箇畑城百騎凱旋虜牢還靴慢唐稽控招股劫渾揮陥玩獲凡阻署猶挽灰勤柱訂恵没嵐鶯谷搔鶏抽坊癖轟諭吉啓嘆紳慰洋謦詐傑苑幾秩顛伊疎巣傍羨煎括西暖雁播贄捧軸禍緯刃軒旦医晦叶邂逅革袖胃糸陵剃裔醒肖櫛梳濡殴桜綺曇診菜民狩妊娠垢炸裂拓濁閏濯乳洩噌汁褐盆漠昇栗枕鍋涯甚博芝鳩豆鉄喰礎浚凸忽宅穂層網肘姓酔貫畳盟汝薬捉虫飄旗貌憂該祝芻拝悦腺哀賀擦冴遽臀蒙斑庇泉浄培養辿娯倣穹漕牙羊宴逐稚猿晚餐拘逼矜襟剥禿踵肺腑脈酒仄朱岩檻虎眈峰均筒融拡療漫籍依績芽廃征幕欄芳剤誹謗溝巧顧蓋粗剛贈刮窒泥訓熊帽兆貯偵菓揚絆顰蹙菖蒲邁毅浜鷲闖隊覇硝園墓童傘煽梯痙攣綱蜂膜茨筑藍橙煌柵朦朧嗚咽瀕靖徘徊洪瀉嚥唄嚇俳傭摂駐惧忌辟抉豹閲咄嗟踪胴較釘刑崇貢献班拐紐咆哮頓挫患紋翳碧措萎捗佇搾摺傻濾慨杖兎葛藤暦樽凛繭婦孫筆皺綴吊秤湾謳涎窃蹂躪紡峙摯雪慈牒腋給牌銷季嘔氷姫杞蔑冬零憔悴芯潑剌靄栓脛孔媚撼彗郭牽臆堕濤累醜琴恍睫隈党肥貪埒麦辻棲柑橘腔珠昂澱斎桁襖椅棲頁赴閑蜃楼矯乖腫罰鐘蚊薔薇錬梁膏豊富砦朴僻猜鉛蝉謐鞘謙遜弍傲呈敏滓批茂賽錠虐靱戚噓購廊咬衡耗懲逮巾貨塚南茅撒漿訊堪沬乞槌泡窮遵崎湘龍酢亭墟杭燈惹漸緻髄怜悧槍又鱗緑囵憤糊風孵朗彿庁貰藻酉僅瓦謂勿此株農沼攪諾塔婆熾轄双凵弦筈淫宜纏殲痩烹捏飢鷹詩剖磯江俊"

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
        current_image.paste(char_image, (current_x, char_y))

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


font_mapping = convert_font("方正兰亭圆_GBK_准.ttf", 24)
