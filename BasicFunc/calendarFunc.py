# 历法转换相关处理函数
from BasicFunc.timeConvert import *

def eranameSearch(ui, year):
	if year == 0:
		return eranames[841 + year + 1]
	elif year < -841 or year > 1911:
		ui.edit.append('超出年号查找范围（BC841-1911）')
		return ""
	else:
		return eranames[841 + year]


def glDzsJD(gldzs, sldzs, slcys, flag=False):  # 古历冬至朔干支、实历冬至及次月朔JD
	gldzsGZX = gz.index(gldzs)
	sldzsGZX = math.floor((sldzs + 0.5 + 49) % 60)
	gzc = gldzsGZX - sldzsGZX  # 正为先天，负为后天
	#if sldzsGZX == 0 and gzc < 0: gzc -= 60
	realGldzs = sldzs # 古历冬至朔对应的实历月朔
	yxc = 0  # 古历与实历冬至月序差
	if 55 > abs(gzc) > 25:  # 冬至朔误差过大（不适用距历元较远引起的误差）
		realGldzs = slcys  # 古历冬至朔在实历次月
		yxc = 1
	gzc = gldzsGZX - math.floor((realGldzs + 0.5 + 49) % 60)  # shuo[yxc]为古历冬至月对应的实历月
	if gzc > 20: gzc -= 60  # 超过一甲子周期
	if gzc < -20: gzc += 60
	gldzsJD = int(realGldzs + 0.5) + gzc
	if flag: return gldzsJD, yxc
	else: return gldzsJD

def glSJD(JD, sgz):  # 实历朔JD与古历朔干支，确定为同一月序
	gzc = math.floor((JD + 0.5 + 49) % 60) - sgz
	if gzc > 55: gzc -= 60
	if gzc < -55: gzc += 60
	JD -= gzc
	return JD


def getMonth(gls, gldzsJD, JD):  # 求某日所在古历月（古历朔干支表，实历朔JD表、所求日）
	jr = int(JD + 0.5) - gldzsJD  # 古历自冬至朔以来的积日
	n = 2  # 古历月序，2为从冬至月开始
	if jr >= dxy[gls[n][-3]]:
		while jr >= 0:
			jr -= dxy[gls[n][-3]]
			n += 1
		n -= 1  # 不含次月
	elif jr < 0: n -= 1  # 不在起始月
	return n


def findYX(ymb, n, month, date1):  # 查找date在历法中的月序（起冬至月）
	szy = 0
	leap = False
	x = -1 if ymb[0][-1] == "月" else -4
	for i in range(n):
		if "闰" in ymb[i][:x]: leap = True  # 截止到查找月有闰
		if ymb[i][:x] == date1[:-3]:  # 按月序查找
			if ymb[i + 1][:x] == month[:-1] or '闰' in month:
				szy += 1  # 可能为闰月（不闰则计算次月）
			break
		szy += 1  # 输入月份对应的实历月序
	return szy, leap

def findYX(ymb, date):  # 表起冬至朔（date闰与月表闰可能不同）
	month = date[:-2].replace('闰', '')
	yf = yuefen.index(month) + 2  # 寅正
	x = -1 if ymb[0][-1] == "月" else -4
	szy = yf if ymb[yf][:x] == month[:-1] else 1 + yf  # 该月序
	if date[0] == '闰': szy += 1
	return szy

def rq2date(nm, ymb, date):  # 农历日期转公历日期，nm为前月、本月、次月朔JD
	rq_name = date[-2:]
	x = -1 if ymb[1][-1] == "月" else -4
	try:  # 直接给出日期
		rq = nlrq.index(rq_name)
		date2 = str(JD2date(nm[1] + rq))[:-9]
		wr = ' 无' + date[:-2] if ymb[1][0] != date[0] else ''
		return date2 + ' ' + ganzhiJD(nm[1]) + '（' + ymb[1][:x] + '月）' + wr
	except:  # 已知日干支
		rgzx = gz.index(rq_name)
		re1, re2 = "", ""
		for i in [1, 0, 2]:  # 不在本月则判断前后月
			sgzx = gz.index(ganzhiJD(nm[i]))
			rq = (rgzx - sgzx) % 60
			if not DateCompare(nm[i] + rq, nm[i+1]):  # 干支在该月
				date2 = str(JD2date(nm[i] + rq))[:-9]
				wr = ' 无' + date[:-2] if ymb[1][0] != date[0] else ''
				if i == 1:
					re2 = rq_name + '为' + ymb[i][:x] + '月' + nlrq[rq] + '' + '，即：' + date2 + wr
					break
				if i == 0: re1 = '或在上月' + nlrq[rq] + '，即' + date2 + wr + '\n'
				elif i == 2:
					re2 = '（月内无' + rq_name + '）      或在次月' + nlrq[rq] + '，即' + date2
		return re1 + re2


