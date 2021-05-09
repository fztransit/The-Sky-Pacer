from AncientAstro.liFunc import *
from BasicFunc.mathFunc import *
from BasicFunc.globalVariable import *

LYSSstate = [True]

def tzs(li, year, rank=-1):
	li.jsb = [[0 for i in range(4)] for j in range(16)]
	if li.type <= 4 and li.type != 3:
		return tzs1(li, year, rank)
	else:
		return tzs2(li, year, -1)

def tzs1(li, year, rank=-1):  # 颛顼历亥月起，其他历子月起
	li.array(rank)
	# 基本推步算法
	li.syjn = li.getSyjn(year)
	li.syjy = (li.syjn * li.zy) // li.zs
	qxf = 0
	if li.type == 4:
		li.sjf = li.syjy * li.yfa
		ydy, yxy = divide(li.sjf, li.srf, 60)
		qdy, qxy = divide(li.syjn * li.sz, li.qrf, 60)
		li.rbn = li.syjn % li.bf  # +1入蔀年
		li.rbs = li.syjn % li.yf // li.bf  # +1入蔀/纪数
		if (qdy - ydy) % 60 >= li.yrs(yxy):  # 首月为闰月
			ydy, yxy = qy(ydy, yxy, li.srf, li.sdy, li.sxy)[:2]
			li.syjy += 1
	else:
		li.rbn = li.syjn % li.bf  # +1入蔀年
		if li.type == 1: li.rbs = li.syjn % li.jf // li.bf  # +1入蔀数
		else: li.rbs = li.syjn % li.yf // li.bf  # +1入蔀/纪数
		jy = (li.rbn * li.zy) // li.zs  # 蔀内积月，每年235/19月
		li.ry = li.rbn * li.zy % li.zs  # 闰余 rbn * zy - jy * zs
		if li.bsry > 0:  # 首月中气非朔
			if li.lyry: jy -= li.bsry / li.zs  # 历元有闰余，转到无闰余日
			if li.ry + li.bsry >= li.zs: jy += 1  # 上一年有闰，需加回
		li.ry = (li.bsry + li.zy * li.rbn) % li.zs
		li.sjf = jy * li.yfa
		ydy, yxy = divide(li.sjf, li.srf, 60)  # 天正朔蔀内积日 = 积月 * 朔策(yfa / by)
		qdy, qxy = divide(li.rbn * li.sz, li.qrf, 60)  # 中气积日 = 积年 * 岁长
		if (qdy - ydy) % 60 >= li.yrs(yxy):  # 首月为闰月
			ydy, yxy = qy(ydy, yxy, li.srf, li.sdy, li.sxy)[:2]
			li.syjy += 1
		# 根据历元和建正修改至天正冬至或岁首月
		if li.backYue != 0 and li.backQi != 0:  # 非天正冬至需回推
			ydy, yxy, qdy, qxy, qxf = epoch2tz(li, ydy, yxy, qdy, qxy, qxf)
		else: li.yrs(yxy)
		if li.rbn == 0 and li.ssy < li.qly/2:  # 回推时跨到上一蔀（岁首＜历元）
			ydy = (ydy + li.bsgzc) % 60
			qdy = (qdy + li.bsgzc) % 60
	return ydy, yxy, qdy, qxy, qxf

def tzs2(li, year, rank):
	li.array(rank)
	# 基本推步算法
	li.syjn = li.getSyjn(year)
	szf = li.syjn * li.sz  # 岁积分
	qdy, qxy = divide(szf, li.qrf, 60)
	li.ry = szf % li.yfa  # 距冬至月朔日积分
	li.sjf = szf - li.ry  # 总实
	yldy, ylxy = divide(li.ry, li.qrf, 60)  # 冬至月龄
	ydy, yxy = qy(qdy, qxy, li.srf, -yldy, -ylxy)[:2]
	ydy, yxy = divide(li.sjf, li.srf, 60)
	qxf = 0
	return ydy, yxy, qdy, qxy, qxf


def getRlr(li, sjf):  # 上元以来积年、朔积分，入纪以来积月
	# 入历日＝（朔望月－交点月）×上元积月mod交点月＝上元积月×朔望月mod交点月＝上元积年×岁实mod交点月 li.syjn*li.sui%li.jdy
	rlrs, rlry, rlrxf = dxyMod(sjf, li.srf, li.tongzhou, li.zhoufa, li.ts)   # 一般式（部分历法不适用）
	# 各历具体算法
	if li.lm == '乾象历':
		sxdf, sxxf = divide((li.zy + li.zs) // 2 * li.yfa - li.ts * li.tongzhou, li.ts)  # 朔行分＝（朔望月－交点月）×周日法
		rlrs, rlry, rlrxf = scrl(sjf//li.yfa, sxdf, sxxf, li.ts, li.tongzhou, li.zhoufa)  # （合朔时）入历日、余、小分
	elif li.lm in ['景初历', '元嘉历', '正光历', '兴和历']:  # 纪差、日法＝周法
		# if li.lm == '景初历':
		# 	cjjc = li.tongzhou - int(li.jf * li.sui * li.srf) % li.tongzhou  # 迟疾纪差
		# 	cjcl = (103947 - li.syjn // li.jf * cjjc) % li.tongzhou  # 迟疾差率
		# elif li.lm == '元嘉历':
		# 	cjjc = int(li.jf * li.sui * li.srf) % li.tongzhou  # 纪月 * 通数（纪日） = 纪法 * 岁实 / 朔策 * 通数 = 纪法 * 岁实 / 纪日 * 日法 * 纪日 = 纪法 * 岁实 * 日法
		# 	cjcl = (17663 + li.syjn // li.jf * cjjc) % li.tongzhou
		# elif li.lm == '正光历':
		# 	cjjc = li.tongzhou - int(li.jf * li.sui * li.srf) % li.tongzhou
		# 	cjcl = (63568 - li.syjn // li.jf * cjjc) % li.tongzhou
		# elif li.lm == '兴和历':
		# 	cjjc = int(li.jf * li.sui * li.srf) % li.tongzhou
		# 	cjcl = (0 + li.syjn // li.jf * cjjc) % li.tongzhou
		if 'j' in ylb[li.lm][1]: j = ylb[li.lm][1]['j']
		jnjy = (li.rbn * li.zy) // li.zs
		cjjc = int(li.jf * li.sui * li.srf) % li.tongzhou
		if li.lm in ['景初历', '正光历']:
			cjjc = li.tongzhou - cjjc
			n = -1
		else: n = 0
		cjcl = (j + n * (li.syjn // li.jf * cjjc)) % li.tongzhou
		rlrs, rlry = divide((jnjy * li.yfa + cjcl) % li.tongzhou, li.zhoufa)  # 合朔时
		rlrs, rlry, rlrxf = dxyMod(jnjy * li.yfa + cjcl, li.srf, li.tongzhou, li.zhoufa)
	elif li.lm in ['大明历', '大业历', '戊寅历']:
		sjr, yxy = divide(sjf, li.srf)
		rlrs, rlry = divide(sjr * li.zhoufa % li.tongzhou, li.zhoufa)  # 夜半
		if li.lm == '大明历':
			jsry, rlrxf = divide(yxy * 2029 * 2, li.ts)  # 将“小余/日法”化为“（小余+小分/分母）/历法”形式，以与入历日余相加减
		elif li.lm == '大业历':
			jsry, rlrxf = divide(yxy * (li.zhoufa * li.ts // li.srf), li.ts)  # jsry, rlrxf = divide(yxy * li.zhoufa, li.srf)化为通数为分母
		elif li.lm == '戊寅历':
			jsry, rlrxf = divide(yxy * 14484, li.ts)
		rlrs, rlry = qy(rlrs, rlry, li.zhoufa, 0, jsry)[:2]  # 加时
		rlrs, rlry = dxyMod(rlrs*li.zhoufa+rlry, li.zhoufa, li.tongzhou, li.zhoufa)[:2]  # 加时满则去之
	elif li.lm == '皇极历':
		rlrs, rlry = divide(sjf / li.srf * li.zhoufa % li.tongzhou, li.zhoufa)
		rlrxf = 0
	elif li.lm == '麟德历':
		# zs = li.syjn * li.sz + m * li.yfa - li.ry  # 加时（夜半-=月小余）
		zs = sjf
		bianfen, rlrxf = divide(zs * 12 % li.tongzhou, 12)
		rlrs, rlry = divide(bianfen, li.srf)
	elif li.lm in ['大衍历', '宣明历']:
		rlrs = 0
		rlrf = sjf * li.ts % li.tongzhou
		if li.lm == '宣明历' and rlrf > li.tongzhou / 2:
			rlrf -= li.tongzhou / 2
			rlrs += 14
		rlry = rlrf // li.ts % li.zhoufa
		rlrs += rlrf // li.ts // li.zhoufa
		rlrxf = rlrf % li.ts
	return int(rlrs), int(rlry), rlrxf


def rxys(li, sjf, m=0):
	# 入气日＝朔积日mod气长＝朔望月×上元积月mod气长＝li.syjy*li.yue%(li.zqi/2)
	l = rcb[li.lm][1]['l'] if 'l' in rcb[li.lm][1] else 1
	# 线性插值
	srqx = int((sjf / li.srf) // (li.qice / li.qrf) % 24)
	rqr = (sjf / li.srf) % (li.qice / li.qrf)  # 入平气（含日余）
	if li.type > 4:
		rqr += li.xhs[srqx] * l / li.qrf  # 定气（原朔积分－定气积分＝原朔积分－（原气积分－先后数）（先减后加））
	if li.lm in ['大业历', '戊寅历']:
		qc = 15 if rqr < 15 else 16
	elif li.lm in ['麟德历']:
		qc = li.sz / 24 / li.qrf
	else: qc = (li.sz / 24 - li.ysf[srqx] * l) / li.qrf
	if rqr > qc:
		rqr %= qc  # 入定气
		srqx = (srqx + 1) % 24
	elif rqr < 0:
		srqx = (srqx - 1) % 24
		qc = (li.sz / 24 - li.ysf[srqx] * l) / li.qrf
		rqr %= qc  # 入上一定气
	syl = li.r_syl[srqx]
	ysjf = li.r_ysjf[srqx]  # 所入气序
	dys = ysjf + syl * rqr / qc
	return round(dys), srqx, rqr, qc  # 入气定盈缩


def yxcj(li, sjf, m=0):
	rlrs, rlry, rlrxf = getRlr(li, sjf)
	ysjf = li.y_ysjf[rlrs]
	syl = li.y_syl[rlrs]
	if li.lm in ['乾象历', '景初历', '元嘉历', '大明历', '大业历', '戊寅历']:
		cf = li.cf[rlrs]
		if li.lm == '元嘉历':
			cf += rlry * li.xc[rlrs] // li.zhoufa  # 定差法
		tz = ylb[li.lm][1]['tz'] if 'tz' in ylb[li.lm][1] else 1
		if li.lm == '乾象历':  # 小分表示（差法已通分）
			djf = ysjf * tz + dxyMul(rlry, rlrxf, li.ts, syl)
			if rlrs == 27:
				djf = ysjf * tz + dxyMul(rlry, rlrxf, li.ts, syl, li.zrxf, li.zryu)
		elif li.lm in ['景初历', '元嘉历', '大明历', '戊寅历']:
			rlry = rlry + rlrxf / li.ts
			djf = ysjf + rlry * syl  # 入历加时盈缩/定积分 ysjf + (rlry + rlrxf / li.ts) * syl
			if rlrs == 27:
				djf = ysjf + dxyMul(rlry, 0, 1, syl, li.zrxf, li.zryu) / li.zryu
				cf += li.zryu
		jsxy, jsxf = divide(djf, cf)  # 加时小余及分
	elif li.lm in ['正光历', '兴和历']:
		rlry = rlry + rlrxf / li.ts
		jsxy = ysjf + (rlry * syl) / li.ypxf  # 盈缩积分已除差法，cf = li.ypxf
	elif li.type > 4:  # 等间距二次插值
		if rlrs in [6, 13, 20, 27]:
			if li.lm == '宣明历':
				n = ((rlrs % 14) + 1) // 7
				x = li.tongzhou / li.zhoufa / li.ts * n / 4
				ljz = (x - int(x)) * li.zhoufa
			else:
				n = (rlrs + 1) // 7
				ljz = li.zhoufa * (9 - n) / 9
			if rlry < ljz:
				jsys = (rlry / ljz) * syl[0]
			else:
				jsys = syl[0] + ((rlry - ljz) / (li.zhoufa - ljz)) * syl[1]
		else: jsys = (rlry / li.zhoufa) * syl
		jsxy = ysjf + jsys  # 损益率及盈缩积分已除差法，cf = li.ypxf
	return round(jsxy)


def txw(li, yxy, m):  # 平朔历退弦望
	if li.lm in lkb0 and yxy < li.srf / 4:
		sjf = li.sjf + li.yfa * m
		srqx, rqr = divide(sjf / li.srf, li.sz / 24 / li.qrf, 24)
		idx = [0, 0.25, 0.5, 0.75].index(m - int(m))
		n = 1
		if rqr < 4 or rqr > 11:   # 所近节气（估算）
			srqx = (srqx + 1) % 24
			n = 0
		if li.lm in ['景初历', '元嘉历']:
			lkxy = lkb0[li.lm][srqx][n]
			if yxy < lkxy: li.jsb[int(m)][idx] = -1
		else:
			xwlk = yxy * 100 / li.srf
			if srqx >= len(lkb0[li.lm]): srqx = 24 - srqx
			jqblk = lkb0[li.lm][srqx] / 2
			if xwlk < jqblk: li.jsb[int(m)][idx] = -1

jsxyb = GolVar([])

def jinshuo(li, srqx, rqr, qc, ydy, yxy, m):
	idx = [0, 0.25, 0.5, 0.75].index(m - int(m))
	if li.lm in ['崇玄历']:  # 公式法
		ddz = (li.syjn * li.sz + li.xhs[0]) / li.qrf
		dxz = ((li.syjn + 0.5) * li.sz + li.xhs[12]) / li.qrf
		sqr = (li.sjf + m * li.yfa) / li.srf
		A = (sqr - ddz) % li.sui
		if A > li.sui / 2:
			A = (sqr - dxz) % li.sui
		if A > li.zt / li.qrf / 4: A = li.sui / 2 - A
		B = A ** 2 * 100 / 1667.5  # 单位：分
		xxs = abs(500 - B) * B / 1800 + B  # 消息数
		dcf = ((li.syjn + 0.25) * li.sz + li.xhs[6]) / li.qrf
		dqf = ((li.syjn + 0.25) * li.sz + li.xhs[18]) / li.qrf
		if dcf < sqr < dqf: glm = xxs + 1752
		else: glm = 2748 - xxs
		ccys = glm * 135 / 100  # 晨初余数
		if int(m) == m:  # 进朔
			if yxy > li.srf / 40 * 29:
				yxy2 = li.srf - yxy
				if yxy2 < ccys: li.jsb[int(m)][idx] = 1
			if jsxyb.flag: jsxyb.setValue([ydy, yxy, int(li.srf - ccys)])
		return 0
	if li.lm in lkb or li.lm in ['五纪历', '正元历']:
		if li.lm in lkb:
			liname = li.lm
			lisrf = li.srf
		else:
			liname = '大衍历'
			lisrf = 3040
		kf = lkb[liname]['kf']
		qcybdl = str(lkb[liname]['yl'][srqx]).split('.')  # 气初晨前刻/夜半定刻
		qchmxy = (int(qcybdl[0]) + int(qcybdl[1]) / kf) / 100 * lisrf  # 单位：日法
		if li.lm == '戊寅历': return 0
		qs = lkb[liname]['qs'][srqx]
	if int(m) == m:  # 进朔
		if 6 <= srqx < 18 and li.lm in ['宣明历']:
			zjl = qs / qc  # 陟降率
			lc = 5 / 24 * zjl * rqr  # 漏差
			hmxy = qchmxy - lc
			cfybdl = str(lkb[li.lm]['yl'][6]).split('.')
			cfhmxy = int(cfybdl[0]) * kf + int(cfybdl[1])
			if hmxy < cfhmxy: jsz = abs(0.75 * li.srf - abs(cfhmxy - hmxy) / 5)
			else: jsz = 0.75 * li.srf
		elif li.lm in ['五纪历', '正元历']:
			zjl = lkb[liname]['fl'][srqx]
			if srqx in [4, 7, 16, 19]:
				for i in range(rqr):
					zjl += lkb[liname]['xc'][srqx][int(i // 3)]
			xxds = dcjs(rqr, qs, zjl / 100)
			ccys = qchmxy + xxds / kf / 100 * lisrf
			yxy2 = li.srf - yxy
			jsz = (ccys / lisrf - 0.1) * li.srf
			if yxy2 < jsz:
				li.jsb[int(m)][idx] = 1
			if jsxyb.flag: jsxyb.setValue([ydy, yxy, int(li.srf - jsz)])
			return 0
		else:  jsz = 0.75 * li.srf
		if yxy >= jsz:
			li.jsb[int(m)][idx] = 1
		if jsxyb.flag: jsxyb.setValue([ydy, yxy, int(jsz)])
	else:  # 退弦望
		if li.lm == '戊寅历':
			txwz = qchmxy
		elif li.lm == '麟德历':
			fl = lkb[li.lm]['fl'][srqx] / 100
			gj = 17 if 6 < srqx < 18 else 16  # 春分后秋分前
			qsl2 = rqr * (qs + (rqr - 1) / 2 * fl)  # 单位：刻分
			qsl = dcjs(rqr, qs, fl)
			kc = (qsl * 180 / (11 * gj)) / kf  # 单位：刻
			txwz = qchmxy - (kc / 2) / 100 * li.srf  # 定刻（单位：日法）
		elif li.lm == '大衍历':
			zjl = lkb[li.lm]['fl'][srqx]
			if srqx in [4, 7, 16, 19]:
				for i in range(rqr):
					zjl += lkb[li.lm]['xc'][srqx][int(i // 3)]
			xxds = dcjs(rqr, qs, zjl / 100)
			txwz = qchmxy + xxds / kf / 100 * li.srf
		elif li.lm == '宣明历':
			zjl = qs / qc  # 陟降率
			lc = 5 / 24 * zjl * rqr  # 漏差（单位：日法）
			txwz = qchmxy - lc  # 昏明小余
		if li.lm in lkb and yxy < txwz:  # 日出前退日
			li.jsb[int(m)][idx] = -1

def setBJS(li):  # 各历不进朔年份
	year = li.syjn + li.sy + 1
	if li.lm == '麟德历' and not(708 <= year <= 716 or 721 <= year <= 728):
		return True
	elif li.lm == '大衍历' and 729 <= year <= 734:
		return True
	return False


def ps2ds(li, m, flag=False):  # 从平朔求定朔，flag：部分历法在特定年限内不进朔的标记，只用于与文献相联系的历表
	sjf = li.sjf + m * li.yfa
	ydy, yxy = divide(sjf, li.srf, 60)
	if li.type > 4 or li.lm in ['戊寅历']:
		dys, srqx, rqr, qc = rxys(li, sjf, m)  # 盈加缩减
	if li.lm == '麟德历': sjf += round(dys)
	jsxy = yxcj(li, sjf, m)
	ydy, yxy = qy(ydy, yxy, li.srf, 0, -jsxy + dys)[:2]  # 定大小余
	if (li.type > 4 or li.lm in ['戊寅历']) and not (flag and setBJS(li)):
		jinshuo(li, srqx, int(rqr), qc, ydy, yxy, m)
		if m == int(m): ydy = (ydy + li.jsb[int(m)][0]) % 60
	return ydy, round(yxy)


def findFirstQi(li, ydy, qdy, qxy, qxf, yueri):
	jqx = 0  # 每年出现的第一个节气，设为小寒
	wjq = False
	jdy1, jxy1, jxf1 = qy(qdy, qxy, li.qrf, -li.qdy, -li.qxy, qxf, -li.qxf, li.qfm)  # 大雪
	jdy2, jxy2, jxf2 = qy(qdy, qxy, li.qrf, li.qdy, li.qxy, qxf, li.qxf, li.qfm)  # 小寒
	if (jdy1 - ydy) % 60 >= yueri:  # 小雪不在冬至月，考虑大寒
		if (jdy2 - ydy) % 60 >= yueri:  # 小寒也不在，正月无节气
			wjq = True
			fisrtQi = [None, None, jqx]
			jdy, jxy, jxf = jdy1, jxy1, jxf1  # 回推上月节气必得大雪
		else:
			jdy, jxy, jxf = jdy2, jxy2, jxf2  # 正月小寒
	else:
		jqx = -1
		jdy, jxy, jxf = jdy1, jxy1, jxf1  # 正月大雪
	if wjq == False:
		fisrtQi = [jdy, jxy, jqx]
	return jdy, jxy, jxf, fisrtQi


def calendar(li, year, ss, jq=False, flag=False, rank=-1):
	n = 2 if ss else 0  # 岁首起排（返回从历元到次年岁首）
	if li.type < 4 or (645 <= year <= 665 and li.lm == '戊寅历'):
		return psCalendar(li, year, n, jq, rank)
	elif li.type >= 4:
		return dsCalendar(li, year, n, jq, flag, rank)

def psCalendar(li, year, n, jq=False, rank=-1):  # 平朔历表
	ydy, yxy, qdy, qxy, qxf = tzs(li, year, rank)
	liList = [['', 0, ydx[li.yrs(yxy)], ydy, yxy, qdy, qxy]]
	if jq:  # 判断冬至月节气，或为大雪，或为小寒，或即无，其他月同理
		jdy, jxy, jxf, firstQi = findFirstQi(li, ydy, qdy, qxy, qxf, li.yueri)
		liList[0].append(firstQi)
	j = 1  # i合朔次数（历表序），j月序
	for i in range(1, 13+n):  # 共计算13+n月，无闰（或无气）时剔除最后一月
		run, ydy, yxy, qdy, qxy, qxf = li.wzqy(ydy, yxy, qdy, qxy, qxf)
		if li.ssy < li.qly / 2 and li.rbn == 0 and j == li.qly // 2 and not run:  # 跨蔀
			ydy = (ydy - li.bsgzc) % 60
			qdy = (qdy - li.bsgzc) % 60
			if jq: jdy = (jdy - li.bsgzc) % 60  # 跨蔀
		if run:
			j -= 1
			liList.append([run, j % 12, ydx[li.yueri], ydy, yxy, None, None])
		else:
			liList.append([run, j % 12, ydx[li.yueri], ydy, yxy, qdy, qxy])
		if jq:
			wjq, ydy, yxy, jdy, jxy, jxf = li.wzqy(ydy, yxy, jdy, jxy, jxf, False)
			if wjq:
				liList[i].append([None, None])
			else:
				liList[i].append([jdy, jxy])
		j += 1
	if j == 13+n:  # 闰月或有无节气月输出13个月，否则输出12个月
		liList.pop()  # k为0有无节气月（值必为FALSE），为1或11则无
		if jq: jxf = (jxf - li.qxf) % li.qfm
	if li.type != 3 and li.rbn == li.bf - 1 and li.ssy > li.qly / 2:  # 跨蔀首
		for m in range(11, len(liList)):
			for n in [3, 5, 7]:
				liList[m][n] = (liList[m][n] - li.bsgzc) % 60
			if jq: liList[m][9][0] = (liList[m][9][0] - li.bsgzc) % 60
	return liList


def dsCalendar(li, year, n, jq=False, flag=False, rank=-1):
	liList = []
	ydy, yxy, qdy, qxy, qxf = tzs(li, year, rank)  # 本月平朔平气
	ydy0, yxy0 = ps2ds(li, 0, flag)  # 本月定朔
	tzdxy = [ydy0, qdy, qxy, qxf]
	j = 0  # i合朔次数，j月序
	for i in range(13+n):  # 共计算14月，无闰（或无气）时剔除最后一月
		ydy, yxy = qy(ydy, yxy, li.srf, li.sdy, li.sxy)[:2]  # 次月平朔
		ydy1, yxy1 = ps2ds(li, i+1, flag)  # 次月定朔
		yueri = (ydy1 - ydy0) % 60  # 本月日数
		if (qdy - ydy0) % 60 >= yueri:
			run = '闰'
			j -= 1
			liList.append([run, j % 12, ydx[yueri], ydy0, yxy0, None, None])
		else:
			run = ''
			liList.append([run, j % 12, ydx[yueri], ydy0, yxy0, qdy, qxy])
			qdy, qxy, qxf = qy(qdy, qxy, li.qrf, li.qdy, li.qxy, qxf, li.qxf, li.qfm, 2)  # 次月气
		j += 1
		ydy0, yxy0 = ydy1, yxy1
	if jq:  # 判断冬至月节气，或为大雪，或为小寒，或即无，其他月同理
		jdy, jxy, jxf, firstQi = findFirstQi(li, tzdxy[0], tzdxy[1], tzdxy[2], tzdxy[3], (liList[1][3] - liList[0][3]) % 60)
		liList[0].append(firstQi)
		for k in range(13+n):
			if (jdy - liList[k][3]) % 60 >= dxy[liList[k][2]] and k != 0:
				liList[k].append([None, None])
			else:
				if k != 0: liList[k].append([jdy, jxy])
				jdy, jxy, jxf = qy(jdy, jxy, li.qrf, li.qdy, li.qxy, jxf, li.qxf, li.qfm, 2)  # 本月节气
	if j == 13+n:  # 闰月或有无节气月输出13个月，否则输出12个月
		liList.pop()  # k为0有无节气月（值必为FALSE），为1或11则无
	li.jsb = li.jsb[:len(liList)]  #
	return liList



def addMonth(li, yqdxy, yx, n, m=0): # 年首回推（未处理跨蔀首），或年末后推（未处理含小分）
	if yqdxy[2] == None:  # 无中气前月中气必在本月节气前-1，后月中气必在本月节气后+1
		qdy, qxy = qy(yqdxy[4][0], yqdxy[4][1], li.qrf, li.qdy, li.qxy, 0, li.qxf, li.qfm, n)[:2]
	else: qdy, qxy = qy(yqdxy[2], yqdxy[3], li.qrf, li.qdy, li.qxy, 0, li.qxf, li.qfm, n * 2)[:2]
	if yqdxy[4][0] == None:  # 无节气前月节气必在本月中气前-1，后月节气必在本月中气后+1
		jdy, jxy = qy(yqdxy[2], yqdxy[3], li.qrf, li.qdy, li.qxy, 0, li.qxf, li.qfm, n)[:2]
	else: jdy, jxy = qy(yqdxy[4][0], yqdxy[4][1], li.qrf, li.qdy, li.qxy, 0, li.qxf, li.qfm, n * 2)[:2]
	li.jsb.append([0] * 4)
	if li.type > 4 or (li.lm == '戊寅历' and not 164367 <= li.syjn <= 164387):  # 645-665平朔
		if n == -1:
			ydy, yxy = ps2ds(li, n, True)
			li.jsb = [li.jsb[-1]] + li.jsb[:-1]
			if len(jsxyb.gvar) != 0 and jsxyb.flag: jsxyb.setValue(-1, 1)
			yueri = (yqdxy[0] - ydy) % 60
		else:
			ydy, yxy = ps2ds(li, m-1+n, True)
			li.jsb.append([0] * 4)
			ydy1, yxy1 = ps2ds(li, m+n, True)
			yueri = (ydy1 - ydy) % 60
			li.jsb.pop()
	else:
		ydy, yxy = qy(yqdxy[0], yqdxy[1], li.srf, n * li.sdy, n * li.sxy)[:2]
		yueri = li.yrs(yxy)
	run = ''
	if (qdy - ydy) % 60 >= yueri:
		run = '闰'
		qdy, qxy = None, None
	if (jdy - ydy) % 60 >= yueri:
		jdy, jxy = None, None
	return [run, yx+n, ydx[yueri], ydy, yxy, qdy, qxy, [jdy, jxy]]


