tiangan = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
dizhi = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
gz = [''] * 60  # 六十甲子表
for i in range(60):
	gz[i] = tiangan[i % 10] + dizhi[i % 12]
zodiac = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪', ]
jieqi = ["冬至","小寒","大寒","立春","雨水","惊蛰","春分","清明","谷雨","立夏","小满","芒种","夏至","小暑","大暑","立秋","处暑","白露","秋分","寒露","霜降","立冬","小雪","大雪"]
yuefen = ["正月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"]
yuefen2 = ["正月","腊月","一月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"]
yuefen3 = ["建子月","建丑月","建寅月","建卯月","建辰月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"]
nlrq = ["初一","初二","初三","初四","初五","初六","初七","初八","初九","初十","十一","十二","十三","十四","十五","十六","十七","十八","十九","二十","廿一","廿二","廿三","廿四","廿五","廿六","廿七","廿八","廿九","三十"]
weeks = ['一', '二', '三', '四', '五', '六', '日']
days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
ydx = {30: '大', 29: '小'}
dxy = {'大': 30, '小': 29}
ke = ['初', '一', '二', '三', '四']
hzjs = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
xingci = ['星纪','玄枵','诹訾','降娄','大梁','实沈','鹑首','鹑火','鹑尾','寿星','大火','析木']
suiyang = ["焉逢","端蒙","游兆","彊梧","徒維","祝犁","商橫","昭阳","橫艾","尚章"]
suiyin = ["困敦","赤奋若","攝提格","单阏","执徐","大荒落","敦牂","协洽","涒滩","作鄂","淹茂","大渊献"]
xingxiu = ['牛', '女', '虚', '危', '室', '壁', '奎', '娄', '胃', '昴', '毕', '觜', '参', '井', '鬼', '柳', '星', '张', '翼', '轸', '角', '亢', '氐', '房', '心', '尾', '箕', '斗']
xdb = [8, 12, 10, 17, 16, 9, 16, 12, 14, 11, 16, 2, 9, 33, 4, 15, 7, 18, 18, 17, 12, 9, 15, 5, 5, 18, 11, 26.25]  # 岁起牵牛
xcxdb = [['星纪','斗',12], ['玄枵','女',8], ['诹訾','危',16], ['降娄','奎',5], ['大梁','胃',7], ['实沈','毕',12],
         ['鹑首','井',16], ['鹑火','柳',9], ['鹑尾','张',18], ['寿星','轸',12], ['大火','氐',5], ['析木','尾',10]]
xcb = [30, 30, 31, 30, 30, 31, 30, 31, 30, 31, 30, 31] # 古度星次黄经表
gdb = ['初','一','二','三','四','五','六','七','八','九','十','十一','十二','十三','十四','十五','十六','十七','十八','十九','二十','二十一','二十二','二十三','二十四','二十五','二十六','二十七','二十八','二十九','三十','三十一','三十二','三十三']
# 添加节日：节日表[[月，日, 节日] * n]，sc公历节日，lc农历节日
scfestivals = [[1, 1, "元旦"], [5, 1, "劳动节"], [10, 1, "国庆"]]
lcfestivals = [['十二月', '三十', '除夕'], ['正月', '初一', "春节"], ['正月', '十五', "元宵"], ['五月', '初五', "端午"],
               ["七月", "初七", "七夕"], ['七月', '十五', "中元"], ['八月', '十五', "中秋"], ['九月', '初九', '重阳'],]
''' ComboBox用数据'''
stTable = ["前冬至", "全年", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至"]
phases = ['朔', '望', '上弦', '下弦', '全部月相', '指定节气']
fivePlanets = ["木星", "火星", "水星", "金星", "土星", "全部"]
sandhya = ["太阳-50′", "民用-6°", "古历-2.5刻", "航海-12°", "天文-18°", "地平0°"]
sandhyaLat = {"太阳-50′":-50/60, '民用-6°':-6, '古历-2.5刻':-7, '航海-12°':-12,'天文-18°':-18,'地平0°':0} # 约-7°
lsGLB = ['汉-三统历','东汉-四分历', '唐-大衍历', '唐-开元占经', '元-授时历', '实际计算',]

ErrorHint = "输入错误，请重新输入"
