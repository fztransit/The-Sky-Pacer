from AstroCalc.SolarTerms import *
from AstroCalc.moon import *
from AncientAstro import *
from Ephem import *
from Data import *
from BasicFunc import *

# 统母
srf = 81  # 朔旦日法
zf = 19  # 章岁（闰法）：朔旦冬至合
zr = 7  # 章闰
tf = 1539  # 统法：朔旦冬至夜半合
yf = 4617  # 元法：日干支再反复
zy = 235
zz = zy - zr  # 章中228
yfa = 2392  # 月法
yue = yfa / srf  # (29+43/81) 朔策
sdy, sxy = divide(yfa, srf)    # 朔旦大小余
zfa = 140530  # 中法
zt = 562120  # 周天
qrf = 4617
zqi = zfa / qrf  # 中气30又2020/4617
qdy, qxy = divide(zfa, qrf)
suiz = 12  # 岁中
yuez = zy + zr  # 月周254
yy = int(zy / zf * yf)  # 元月57105
yz = suiz * yf  # 元中55404
sui = zt / tf  # 365+385/1539 岁实
swzh = 135  # 朔望之会
sf = 23  # 食法
hs = 513  # 会岁
hy = 6345  # 会月 = 章月 * 朔望之会
ty = 19035  # 一统81章*章月235
sy = -143231  # 上元（丁丑，今庚戌）

# 纪母
wxm = ['水', '金', '火', '木', '土']
# 一个行星回合周期（从晨始见到晨始见） = 岁数 / 见中法
ss = {'木':1728, '火':13824, '水':9216, '金':3456, '土':4320}                                    # 岁数：行完整数倍周天的年数
xfs = {'木':1583, '火':6469, '水':29041, '金':2161, '土':4175}                                   # 见中法（大统见复数）= 岁数 - 行率，即一岁数中的见复数（会合周期数）
xzf = {'木':20736, '火':165888, '水':110592, '金':41472, '土':51840}                             # 见中分 = 岁数 * 12，即一岁数的中气数
xrf = {'木':12096, '火':96768, '水':64512, '金':24192, '土':30240}                               # 见闰分 = 岁数 * 7
xyf = {'木':30077, '火':122911, '水':551779, '金':41059, '土':79325}                             # 见月法 = 见中法 * 章岁，即一岁数中的月数
xzrf = {'木':1583*yf, '火':6469*yf, '水':29041*yf, '金':2161*yf, '土':4175*yf}                   # 见中日法 = 见中法 * 元法
xyrf = {'木':30077*srf, '火':122911*srf, '水':551779*srf, '金':41059*srf, '土':79325*srf}   # 见月日法 = 日法 * 见月法
# 一见日数 = (jmjz + jmzy / xfs) * sui / 12
jmjz = {'木':13, '火':25, '水':3, '金':19, '土':12}                                              # 纪母积中 = 见中分 // 见中法（即每一见的中气数）
jmzy = {'木':157, '火':4163, '水':23469, '金':413, '土':1740}                                    # 纪母中余 = 见中分 % 见中法（即每一见的中气余数）
jmjy = {'木':13, '火':26, '水':3, '金':19, '土':12}                                              # 纪母积月 = （章中 * 岁数 + 见闰分） // 见月法
jmyy = {'木':15079, '火':52954, '水':510423, '金':32039, '土':63300}                             # 纪母月余 = （章中 * 岁数 + 见闰分） % 见月法
cxr = {'金':327, '水':65+122029605/134082297}                                                    # 晨见伏日（地外：ss[p]/xfs[p]*sui）

def add2(dy1, xy1, rf, dy2, xy2, n=1, xf1=0, xf2=0, fm=1):  # 被加/减数，日法，加/减数，被加/减数小分，加/减数小分，分母，加/减次数
	zf = ((dy1 * rf + xy1) * fm + xf1) + ((dy2 * rf + xy2) * fm + xf2) * n
	xf = zf % fm
	zy = (zf - xf) // fm
	dy = zy // rf
	xy = zy % rf
	if fm == 1:
		return dy, xy
	else:
		return dy, xy, xf

def xcrxd(dc,rcd):  # 已知星次和入次度求入宿度
	srx = xcxdb[dc][1] # 星次初所对应的星宿
	rxd = math.ceil(xcxdb[dc][2] + rcd)
	i = xingxiu.index(srx)
	while rxd >= xdb[i%28]:
		rxd -= xdb[i%28]
		i += 1
	srx = xingxiu[i%28]
	return srx, rxd

def xcrcd(rcd):  # 古度
	rcd += 15  # 起惊蛰
	i = 3
	while rcd > 0:
		rcd -= xcb[i]
		i += 1


def xdrxd(xd): # 已知自牛宿起的星度求入宿度
	i = 0
	rxd = xd
	while rxd >= xdb[i%28]:
		rxd -= xdb[i%28]
		i += 1
	srx = xingxiu[i%28]
	return srx,int(rxd)+1

# 百刻制
def heshuo(xy,rf):  # 求合朔时刻（小余，日法）
	chen = round((xy / rf) * 12 + 0.5, 14) # 时辰从上一日23时起
	chen_h = int(chen)
	chen_k = round(xy / rf * 100 - int(xy / rf * 12) * 100 / 12, 14)  # 该时辰内的刻数
	if chen_k < 100/24:
		hssj = dizhi[chen_h % 12] + '正' + ke[int(chen_k)] + '刻'
	else:
		chen_k -= 100 / 24
		hssj = dizhi[chen_h % 12] + '初' + ke[int(chen_k)] + '刻'
	return hssj

def glJD(JD, rgz):  # 从古历日期干支中找到其在实历的日期，日干支为干支序
	gzc = rgz - math.floor((JD + 0.5 + 49) % 60)
	if gzc < -30: gzc += 60
	elif gzc > 30: gzc -= 60
	JD += gzc
	return JD

def glDate(year, angle, rgzx, rzd=0):  # 根据古历所推节气干支求日期，适用误差在30日内
	try:
		if angle % 360 == 270: year -= 1
		jd = SolarTermsJD(year, angle % 360)
	except:
		jd = date2JD(angle)  # 此为date
	gzc = (rgzx - gz.index(ganzhiJD(jd))) # 三统历与实历差
	if gzc > 30: gzc -= 60
	elif gzc < -30: gzc += 60
	if jd - int(jd) >= 0.5:  # 第二日
		gzc += 1
	jd0 = int(jd) + gzc + rzd  # 三统历所推日期
	date = JD2date(jd0)[:-9]
	return date, jd0  # 古历日期及儒略日

def TongShu(cxly, month):  # 步中朔
	month -= 1  # 表示月改为计算月
	syjn = -sy + cxly
	if cxly > 0: syjn -= 1
	ryn = syjn % yf  # 入元年
	rtn = ryn % tf  # 入统年
	tzjy, ry = divide(rtn * zy, zf)  # 天正时统内积月
	jy = tzjy + month
	sjr = jy * yfa // srf
	sdy = sjr % 60  # 天正朔大余
	sgz = (sdy + ryn // tf * 40) % 60
	sxy = jy * yfa % srf
	rm = ''
	if ry >= 12:
		run = (235 - ry * 12) // 7  # 年中闰月序，月名='闰'+(i-1)
		zqjr = int(rtn * sui + (run - 1) * zqi)  # 算该月前一月的中气，若前一月无中气，则为该月中气；若为前一月中气，该月无中气
		if 0 <= zqjr - (tzjy + run) * yfa // srf < 2:
			run -= 1
		if month == run: rm = '闰'
		if month >= run: month -= 1
	# 省略节气及五行
	hczf = (sjr * tf + sxy * zf) % zt  # 合辰总分
	hcxd = hczf / tf  # 合辰星度，sjr % sui，（sjr = jy * yfa / srf）
	hcdf = hczf % tf
	tydf = hcdf - zf * sxy  # 太阳本日内行度
	tyxd = hcxd - tydf / tf  # 朔日夜半太阳所在星度
	yldf = sxy * yuez  # 月亮本日内行度：月行速度*月行时间 = 254/19 * xy/81
	ylxd = hcxd - yldf / tf  # 朔日夜半月亮所在星度
	hcsrx, hcrxd = xdrxd(hcxd)
	tysrx, tyrxd = xdrxd(tyxd)
	ylsrx, ylrxd = xdrxd(ylxd)
	hssk = heshuo(sxy,srf)
	return "{}年  三统历 子正 {}{}{} {}合朔\n   合辰在牛宿东{}度，即{}{}度\n   是日夜半太阳在牛宿东{}度，即{}{}度\n\t   月亮在牛宿东{}度，即{}{}度".\
		format(cxly,rm,yuefen[month],gz[sgz],hssk,int(hcxd), hcsrx, hcrxd, int(tyxd % sui), tysrx, tyrxd, int(ylxd % sui), ylsrx, ylrxd)

def JiShu(cxly, p):  # 步五星
	# 推五星见复，置太极上元以来，尽所求年
	syjn = -sy + cxly + 1
	if cxly > 0: syjn -= 1
	# 乘大统见复数，盈岁数得一，则定见复数也。不盈者名曰见复馀。
	dxfs, xfy = divide(syjn * xfs[p], ss[p])  # 定见复数（上元以来见复数），见复余
	# 见复馀盈其见复数，一以上见在往年，倍一以上，又在前往年，不盈者在今年也。
	xfn = cxly
	if xfy > xfs[p]:
		xfn -= 1  # 上年见复
	if p == '火' and xfy > xfs[p]*2:
		xfn -= 1  # 再上年见复
	xfn = cxly - xfy // xfs[p]
	# 推星所见中次，以见中分乘定见复数，盈见中法得一，则积中也。不盈者名曰中馀。以元中除积中，馀则中元馀也。以章中除之，馀则入章中数也。以十二除之，馀则星见中次也。中数从冬至起，次数从星纪起，算外，则星所见中次也。
	jz, zyu = divide(xzf[p] * dxfs, xfs[p])  # 积中及中余：上元以来所积中气及余分
	zyy = jz % yz  # 中元余：元内所积中气
	rzzs = zyy % zz  # 入章中数
	xxzc = rzzs % 12  # 星见中次
	# 推星见月，以闰分乘定见复数，以章岁乘中馀从之，盈见月法得一，并积中，则积月也。不盈者名曰月馀。以元月除积月，名曰月元馀。以章月除月元馀，则入章月数也。以十二除之，至有闰之岁，除十三入章。三岁一闰，六岁二闰，九岁三闰，十一岁四闰，十四岁五闰，十七岁六闰，十九岁七闰。不盈者数起于天正，算外，则星所见月也。
	jr, yyu = divide((xrf[p] * dxfs + zf * zyu), xyf[p])  # 上元以来的积闰及月余（积月余分）
	jy = jr + jz  # 积月：积闰 + 积中
	yyy = jy % yy  # 月元余：一元内所积月
	if (yfa * yyu / xyf[p] + yfa * yyy % srf) / srf > yue:  # 入月日超限
		yyy += 1
		yyu = xyf[p] - yyu
	rzys = yyy % zy  # 入章月数
	rys = rzys * 7 // 235  # 入章月数内所含闰月数（非无中闰）
	yx = (rzys - rys) % 12  # 月序：冬至次月起算
	# 推至日，以中法乘中元馀，盈元法得一，名曰积日，不盈者名曰小馀。小馀盈二千五百九十七以上，中大。数除积日如法，算外，则冬至也。
	zqjr = zfa * zyy / yf  # 元内中气积日（含余分）
	qxy = zfa * zyy % yf  # 积日小余，即中气小余
	zqgz = int(zqjr) % 60  # 中气干支
	dzgz = int(zqjr + zqi * (12-xxzc)) % 60  # 岁终冬至干支
	# 推朔日，以月法乘月元馀，盈日法得一，名曰积日，馀名曰小馀。小馀三十八以上，月大。数除积日如法，算外，则星见月朔日也。
	sjr, sxy = divide(yfa * yyy, srf)  # 一元内朔积日及小余
	sgz = sjr % 60  # 交朔干支
	# 推入中次日度数，以中法乘中馀，以见中法乘其小馀并之，盈见中日法得一，则入中日入次度数也。中次至日数，次以次初数，算外，则星所见及日所在度数也。求夕，在日后十五度。
	rzd = (zfa * zyu + xfs[p] * qxy) / xzrf[p]  # （夜半起算）入中日/次度数及余
	rzdy = (zfa * zyu + xfs[p] * qxy) % xzrf[p]  # 距日度小余
	# 推入月日数，以月，法乘月馀，以见月法乘其小馀并之，盈见月日法得一，则入月日数也。并之大馀，数除如法，则见日也。
	ryrs, ryry = divide(yfa * yyu + xyf[p] * sxy, xyrf[p])  # （夜半起算）入月日数及余 = (yfa / srf) * (yyu / xyf[p]) + sxy / srf
	lrgz = (sgz + ryrs) % 60  # 中气法：(zqgz + int(rzd)) % 60
	zqszyc = rzzs - rzys + rys  # 入中所在月与入月差
	zqsjr = (yfa * (yyy + zqszyc)) // srf
	zqrx = int(zqjr) - zqsjr  # 中气日序
	zqszy = yx + zqszyc
	# 判断实际日期及其他处理
	angle = xxzc * 30 - 90
	ra = (angle * sui / 360 - zqi / 2 + rzd) % sui  # 古度
	srx, rxd = xcrxd(xxzc, rzd)
	date, jd0 = glDate(xfn, angle, zqgz, int(rzd))
	# jd += int(rzd)  # 含具体时刻的日期，用以求该时刻的实际黄经，误差过大可忽略
	dzjr = int(int(zqi * xxzc) + rzd)  # 前冬至（缺冬至小余）至晨始见积日
	# dzjr = int(zqjr - (jz % yz - xxzc) * zqi + int(rzd))
	dzjr = int(zqjr - zyy // 12 * sui + int(rzd))
	''' 推后见可直接调用以上计算获得，以下是完成三统历的完整计算 '''
	if p in ['木', '火', '土']:
		xianming = '晨始见'
		t = 1
	else:
		xianming = '夕始见'
		t = 9 / 16  # 晨见周期，外行星到下次晨见，内行星到夕见。
	# 推晨见加夕，夕见加晨，皆如上法。（如下）
	# 推后见中，加积中于中元馀，加后馀于中馀，盈其法得一，从中元馀，数如法，则见也。
	hjz, hzy = divide((jmjz[p] * xfs[p] + jmzy[p]) * t, xfs[p])
	hjz, hzy = add2(hjz, hzy, xfs[p], zyy, zyu)
	# hjz = (jmjz[p] + jmzy[p] / xfs[p]) * t + jz + zyu / xfs[p]
	# hzy = round((hjz - int(hjz)) * xfs[p])
	# hjz = int(hjz)
	hzyy = hjz % yz  # 后中元余
	hrzzs = hzyy % zz  # 后入章中数
	hxxzc = hrzzs % 12  # 后星见中次
	# 推后见月，加积月于月元馀，加后月馀于月馀，盈其法得一，从月元馀，除数如法，则后见月也。
	hjy, hyy = divide((jmjy[p] * xyf[p] + jmyy[p]) * t, xyf[p])
	hjy, hyy = add2(hjy, hyy, xyf[p], yyy, yyu)
	# hjy = int(yyy + jmjy[p] * t + (jmyy[p] * t + yyu) / xyf[p])
	# hyy = (yyu + (jmjy[p] * xyf[p] + jmyy[p]) * t) % xyf[p]
	hyyy = hjy % yy  # 后月元余
	if (yfa * hyy / xyf[p] + yfa * hyyy % srf) / srf > yue:  # 入月日超限
		hyyy += 1
		hyy = xyf[p] - hyy
	hrzys = hyyy % zy  # 后入章月数
	# 推朔日及入月数，如上法
	hsjr, hsxy = divide(hyyy * yfa, srf)  # 后朔积日即小余
	hsgz = hsjr % 60  # 后朔干支
	hryrs = (yfa * hyy + hsxy * xyf[p]) / xyrf[p]  # 入月日数
	hrys = hrzys * 7 // 235  # 入章月数内所含闰月数
	hyx = hrzys % 12 - hrys  # 后月序：冬至次月起算
	# 推至日及入中次度数，如上法。
	hzqjr = zfa * hzyy / yf  # 中气积日
	hqxy = zfa * hzyy % yf  # 中气积日小余
	hzqgz = int(hzqjr) % 60  # 交中气干支
	hdzgz = int(hzqjr + zqi * (12 - hxxzc)) % 60  # 交冬至干支
	hrzd = (hzy * zfa + hqxy * xfs[p]) / xzrf[p]  # 入中日（入次度）
	# if p in ['水','金']: hrzd += rzdy / xzrf[p]
	# if p in ['水', '金']: hryrs += ryry / xyrf[p]
	hlrgz = (hsgz + int(hryrs)) % 60
	# 日期判断
	if p in ['水', '金']:  # 水金晨见伏日数与行度适差一中气，木火土适差一岁
		hxxzc = (hxxzc + 1) % 12
	angle2 = (hxxzc * 30 - 90) % 360
	ra2 = (angle2 * sui / 360 - zqi / 2 + hrzd) % sui
	hrx, hrxd = xcrxd(hxxzc, hrzd)
	hjd0 = jd0 + int(rzdy/xzrf[p] + ss[p] / xfs[p] * sui * t)
	# 误差修正：水星小约0.5日，金星大约1.5日。原因是三统历纪母与步术误差
	hjd0 = glJD(hjd0, hlrgz)
	hdate = JD2date(hjd0)[:-9]
	csx = "{}年 {}星\n  *晨始见在子正 {}{}{}，即{}\n   是月{}朔，{}中气{}，岁末{}冬至\n   {}星黄经{}度  入{}{}度，即{}{}度\n". \
		format(cxly, p, yuefen[yx % 12], nlrq[ryrs], gz[lrgz], date, gz[sgz], gz[zqgz],
	           jieqi[(rzzs % 12) * 2], gz[dzgz], p, round(ra), xingci[xxzc], round(rzd, 4), srx, rxd)
	hsx = "  *其后{}在{}{}{}，即{}\n   是月{}朔，{}中气{}，岁末{}冬至\n   {}星黄经{}度  入{}{}度，即{}{}度". \
			format(xianming, yuefen[hyx % 12], nlrq[int(hryrs)], gz[hlrgz], hdate, gz[hsgz], gz[hzqgz],
		           jieqi[(hrzzs % 12) * 2], gz[hdzgz], p, round(ra2), xingci[hxxzc], round(hrzd, 4), hrx, hrxd)
	return csx + hsx, jd0, dzjr, xxzc, rzd

# 五星动态：行率 * 行日 = 行度
wxdt = {'木':[['顺',2/11,121],['始留',0,25],['逆',-1/7,84],['复留',0,24+3/7308711],['复顺',2/11,111+1828362/7308711],['伏',983316/10188425,33+3334737/7308711]],
        '火':[['顺',53/92,276],['始留',0,10],['逆',-17/62,62],['复留',0,10],['复顺',53/92,276],['伏',1137699509/1458335386,146+15689700/29867373]],
        '土':[['顺',1/15,87],['始留',0,34],['逆',-5/81,101],['复留',0,33+862455/19275975],['复顺',1/15,85],['伏',9577893/48692083,37+17170170/19275975]],
        '金':[['晨星',['逆',-1/2,6],['始留',0,8],['始顺',33/46,46],['顺',1+15/92,184],['伏',1+(33+611124317/828118971)/92,83]],
                ['昏星',['始顺',1+15/92,181+45/107],['顺',33/46,46],['始留',0,7+62/107],['逆',-1/2,6],['伏逆',-(7+15743480/160896744)/8,16+1295352/9977337]]],
        '水':[['晨星',['逆',-2,1],['始留',0,2],['始顺',6/7,7],['顺',1+1/3,18],['伏',1+(7+1148663412/5083074594)/9,37+122029605/134082297]],
                ['昏星',['始顺',1+1/3,16+1/2],['顺',6/7,7],['始留',0,1+1/2],['逆',-2,1],['伏逆',-(4+37724259/1608987564)/15,24]]]}
qrbc = {'木':15+830643/7308711, '火':16+3735847.5/29867373, '土':15+4216800/19275975, '金':15+2182610/9977337, '水':15+29331410/134082297}

# 仅计算夜半情况
def BuShu(date, p):  # 五步
	jd = math.floor(date2JD(date) + 0.5) # 该日0h
	cxly = GetDate(date)[0]
	while True:
		chenxian, jd0, dzjr, cjzc, rzd = JiShu(cxly+1, p)
		jd2 = jd0 - 0.5  # 晨始见日，去日半次
		if jd < jd2: cxly -= 1
		else: break  # 转到所在晨见周期
	jr = int(jd - jd2)
	jr0 = jr
	xxxd = 0  # 星见宿度
	if p in ['木','火','土']:
		i = -1
		while jr0 > 0:
			i += 1
			jr0 -= wxdt[p][i%6][2]
			xxxd += wxdt[p][i%6][1] * wxdt[p][i%6][2]  # 行星行度
		xxxd += wxdt[p][i%6][1] * jr0
		yxzt = wxdt[p][i % 6][0]
	else:  # 地内行星
		i = 0
		j = 0
		while jr0 >= 0:
			if i == 5:
				i -= 5
				j += 1
			i += 1
			jr0 -= wxdt[p][j%2][i%6][2]
			xxxd += wxdt[p][j%2][i%6][1] * wxdt[p][j%2][i%6][2]  # 行星行度
		xxxd += wxdt[p][j%2][i % 6][1] * jr0
		yxzt = wxdt[p][j%2][0] + wxdt[p][j%2][i % 6][0]
	s_ra = (270 * sui / 360 + dzjr + jr) % sui
	qrd = (-qrbc[p] + xxxd - jr)  # 去日度
	p_ra = round((s_ra + qrd) % sui)
	src = int((rzd + xxxd) // zqi + cjzc) % 12
	rcd = (rzd + xxxd) % 15  # 未根据每次次度精确求解，误差小于0.5度
	srx, rxd = xcrxd(src, rcd)
	if qrd > 0:
		dx = '东'
	else:
		dx = '西'
		qrd = sui - qrd
	return "{}星  运行状态：{}\n   黄经：{}度   入{}{}度，即{}{}度\n   自晨始见以来{}日共行{}度，在日{}{}度"\
		.format(p, yxzt, p_ra, xingci[src], round(rcd,1), srx, rxd, jr, round(xxxd), dx, round(qrd%sui))

# 岁术按平均行率145/1728，则每年为145/1728*562120/1539=30.6489推算
# 步术考虑木星在不同阶段的运行状态和速率不同进行推算，二者存在误差。
def SuiShu(cxly, flag=False):
	syjn = -sy + cxly
	if cxly > 0: syjn -= 1
	dzdy = 8080 * (syjn % tf) // tf % 60
	dzgz = (syjn // tf * 40 + dzdy) % 60
	date = glDate(cxly, 270, dzgz)[0]
	jc, cy = divide((syjn % 1728) * 145, 144)  # 积次，次余
	dc = jc % 12  # 定次，起星纪
	# tsrm = (12 + jc) % 60  # 太岁日名
	jd = cy * 365.25/12 / 144  # 积度（均度）
	srx, rxd = xcrxd(dc,jd)
	ccts = gz[(jc+12) % 60]  # 超辰太岁
	wccts = gz[(cxly-4) % 60]
	# nianming = ganzhiYear(cxly)
	if flag: return xingci[dc], ccts  # ,suiyang[dc%12]
	else: return str(cxly) + '年 三统历所推岁前冬至为：' + date + ' ' + \
				 gz[dzgz] + '\n\t岁星入' + xingci[dc] + str(round(jd,4)) + '度，即入' + srx + '宿' + str(rxd) + '度'
	# 岁名为：'+suiming+'（今'+nianming+'）\n\t


def JiaoShi(cxly):
	syjn = -sy + cxly
	if cxly > 0: syjn -= 1
	jz = 0  # 天正
	ryn = syjn % yf  # 入元年
	rtn = ryn % tf  # 入统年
	tnjy = rtn * zy // zf - jz  # 统内积月，起其正
	sjr = tnjy * yfa / srf
	ry = rtn * 7 % zf
	i = 0
	if ry >= 12: i = (228 - ry * 12) // 7  # 闰月名，从上月
	if (228 - ry * 12) % 7 == 0: i -= 1
	hys = syjn % hs  # 会余岁
	hysjy = zy * hys // zf - jz  # 会余岁积月 tnjy % hy
	shiyu = hysjy * 23 % swzh  # 食余
	if shiyu == 0: shiyue = [0]
	else: shiyue = [(swzh - shiyu) / sf]  # 食所在月
	JDE = PhaseJDE(dzs_find(cxly, 1), 2)  # 冬至月望
	j = 0
	for k in range(int(shiyue[j])): # 天正起计月
		JDE = PhaseJDE(JDE + 29, 2)
	result = '三统历(历元天正)推 ' + str(cxly) + '年 月食发生时间(寅正)：\n'
	while shiyue[j] <= 14:
		sgz = int(sjr + int(shiyue[j]) * yue) % 60
		wgz = int(sjr + int(shiyue[j]) * yue + yue / 2) % 60
		yx = int(shiyue[j])
		if i > 0 and i <= shiyue[j]:
			yx = int(shiyue[j] - 1)  # 闰月后月序
			if shiyue[j] < i + 135 / 23:
				JDE = PhaseJDE(JDE + 29, 2)  # 实历后推一月（仅第一次）
		for k in range(int(shiyue[j])-int(shiyue[j-1])):
			JDE = PhaseJDE(JDE + 29, 2)
		JD = td2jd(JDE)
		JD = glJD(JD, (wgz + ryn // tf * 40) % 60)
		date = JD2date(JD)
		ym = yuefen[yx - 2]
		if int(shiyue[j]) == i and i > 0: ym = '闰' + ym
		if yx < 12: result += '   ' + ym + nlrq[int((wgz-sgz) % 60)] + gz[(wgz + ryn // tf * 40) % 60] + '望，即：' + date[:-9] + '\n'
		shiyue.append(shiyue[j] + 135 / 23)
		j += 1
	return result


