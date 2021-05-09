from AstroCalc.StarTable import *
from AstroCalc.SolarTerms import *
from Ephem import *

def PhaseJDE(JD, type): # 输入JD或JDE无差别
	T = (JD - 2451545) / 36525
	k = math.floor(1236.85 * T) + 0.25 * type
	T = k / 1236.85
	JDE = 2451550.09766 + 29.530588861*k + 0.00015437*pow(T,2) - 0.000000150*pow(T,3) + 0.00000000073*pow(T,4)
	if JDE < JD - 1:
		k += 1 # 次月月相（详细比较需迭代）
		T = k / 1236.85
		JDE = 2451550.09766 + 29.530588861 * k + 0.00015437 * pow(T, 2) - 0.000000150 * pow(T, 3) + 0.00000000073 * pow( T, 4)
	M = (2.5534 + 29.10535670*k - 0.0000214*pow(T,2) - 0.00000011*pow(T,3)) % 360 # 太阳平近点角
	Mp = (201.5643 + 385.81693528*k + 0.0107582*pow(T,2) + 0.00001238*pow(T,3) - 0.000000058*pow(T,4)) % 360 # 月亮平近点角
	F = (160.7108 + 390.67050284*k - 0.0016118*pow(T,2) - 0.00000227*pow(T,2) + 0.000000011*pow(T,4)) % 360 # 月亮纬度参数
	O = (124.7746 - 1.56375588*k + 0.0020672*pow(T,2) + 0.00000215*pow(T,3)) % 360 # 白道升交点平经度
	E = 1 - 0.002516*T - 0.0000075*pow(T,2)
	A = [299.77+0.107408*k-0.009173*pow(T,2), 251.88+0.016321*k, 251.83+26.651886*k, 349.42+36.412478*k, 84.66+18.206239*k, 141.74+53.303771*k, 207.14+2.453732*k, 154.84+7.306860*k, 34.52+27.261239*k, 207.19+0.121824*k, 291.34+1.844379*k, 161.72 + 24.198154*k, 239.56+25.513099*k, 331.55+3.592518*k]
	B = [325, 165, 164, 126, 110, 62, 60, 56, 47, 42, 40, 37, 35, 23]
	C_new = [-0.40720, 0.17241*E, 0.01608, 0.01039, 0.00739*E, -0.00514*E, 0.00208*pow(E,2), -0.00111, -0.00057, 0.00056*E, -0.00042, 0.00042*E, 0.00038*E, -0.00024*E, -0.00017, -0.00007, 0.00004, 0.00004, 0.00003, 0.00003, -0.00003, 0.00003, -0.00002, -0.00002, 0.00002]
	C_full = [-0.40614,0.17302*E, 0.01614, 0.01043, 0.00734*E, -0.00515*E, 0.00209*E**2, -0.00111, -0.00057, 0.00056*E, -0.00042, 0.00042*E, 0.00038*E, -0.00024*E, -0.00017, -0.00007, 0.00004, 0.00004, 0.00003, 0.00003, -0.00003, 0.00003, -0.00002, -0.00002, 0.00002 ]
	C_quarter = [-0.62801, 0.17172*E, -0.01183*E, 0.00862, 0.00804, 0.00454*E, 0.00204*E**2, -0.00180, -0.00070, -0.00040, -0.00034*E, 0.00032*E, 0.00032*E, -0.00028*E**2, 0.00027*E, -0.00017, -0.00005, 0.00004, -0.00004, 0.00004, 0.00003, 0.00003, 0.00002, 0.00002, -0.00002]
	C_sin1 = [Mp, M, 2*Mp, 2*F, Mp-M, Mp+M, 2*M, Mp-2*F, Mp+2*F, 2*Mp+M, 3*Mp, M+2*F, M-2*F, 2*Mp-M, O, Mp+M*2, 2*Mp-2*F, 3*M, Mp+M-2*F, 2*Mp+2*F, Mp+M+2*F, Mp-M+2*F, Mp-M-2*F, 3*Mp+M, 4*Mp]
	C_sin2 = [Mp, M, Mp+M, 2*Mp, 2*F, Mp-M, 2*M, Mp-2*F, Mp+2*F, 3*Mp, 2*Mp-M, M+2*F, M-2*F, Mp+2*M, 2*Mp+M, O, Mp-M-2*F, 2*Mp+2*F, Mp+M+2*F, Mp-2*M, Mp+M-2*F, 3*M, 2*Mp-2*F, Mp-M+2*F, 3*Mp+M]
	c1 = 0
	c2 = 0
	correction = [C_new, C_quarter, C_full, C_quarter]
	sin_arg = [C_sin1, C_sin2, C_sin1, C_sin2]
	for i in range(25):
		c1 += correction[type][i] * sin(sin_arg[type][i])
	for i in range(14):
		c2 += B[i] * sin(A[i])
	JDE = JDE + c1 + c2 / 1000000
	W = 0.00306 - 0.00038*E*cos(M) + 0.00026*cos(Mp) - 0.00002*cos(Mp-M) + 0.00002*cos(Mp+M) + 0.00002*cos(2*F)
	if type == 1: JDE += W
	elif type == 3: JDE -= W
	return JDE


# 未根据日月位置计算，误差一分钟内
def PhaseJD(JD, type=0, ut=8):   # 默认ut+8
	JDE = PhaseJDE(JD, type)
	JD = td2jd(JDE, ut)
	return JD

def PhaseDate(date, type, ut=8):
	JD = date2JD(date) - ut / 24
	JDE = PhaseJDE(JD, type)
	return td2date(JDE, ut)


# 未处理超过岁差周期的范围
def dzs_find(year, type=0): # 寻找年前冬至月朔日
	if year == 1: year -= 1 # 公元0改为公元前1
	jd0 = SolarTermsJD(year-1, 270)  # 年前冬至 UT+8
	# 可能的三种朔日（ut+8）。
	jd1 = PhaseJD(jd0 - 0)
	jd2 = PhaseJD(jd0 - 29)
	jd3 = PhaseJD(jd0 - 31)
	# ut+8 0h起算点历日比较
	if DateCompare(jd0, jd1): # 冬至合朔在同一日或下月
		jd = jd1
	elif DateCompare(jd0, jd2) and (not DateCompare(jd0, jd1)): # 冬至在该月
		jd = jd2
	elif DateCompare(jd0, jd3): # 冬至在上月
		jd = jd3
	if type == 1: return jd
	else: return JD2date(jd)


# 现行农历（冬至朔起排）
def currentCalendar(year, type=1):   # type=-1时截止到本年末，=1时截止到次年冬至朔，=0时截止到次年冬至朔次月
	if year == 0: year = 1
	dzs = dzs_find(year, 1)
	shuo = [dzs]  # 存储ut+8 JD
	next_dzs = dzs_find(year + 1, 1)  # 次年冬至朔
	i = -1  # 中气序
	j = -1  # 连续两个冬至月间的合朔次数
	zry = 0
	flag = False
	# 查找所在月及判断置闰
	while not DateCompare(shuo[j + abs(type)], next_dzs):  # 13或14月
		i += 1
		j += 1
		shuo.append(PhaseJD(shuo[j] + 29))  # j+1月朔，ut+8时间
		# 查找本月中气，若无则置闰
		if j == 0: continue  # 冬至月一定含中气，从次月开始查找
		angle = (-90 + 30 * i) % 360  # 本月朔所含中气，起冬至
		qJD = SolarTermsJD(year, angle)  # 本月中气
		# 前气在前朔前且后气在后朔后且未闰下置闰（一般后气在后朔前）
		if DateCompare(qJD, shuo[j + 1]) and flag == False:  # 中气在次月，则本月无中气
			zry = j + 1  # 置闰月
			i -= 1
			flag = True  # 仅第一个无中气月置闰
	# 生成农历月序表
	ym = []
	for k in range(len(shuo)):
		ym.append(yuefen[(k - 2) % 12])  # 默认月序
		if j + abs(type) == 13:  # 仅12次合朔不闰，有闰时修改月名
			if k + 1 == zry:
				ym[k] = '闰' + yuefen[(k-1 - 2) % 12]
			elif k + 1 > zry:
				ym[k] = yuefen[(k-1 - 2) % 12]
	if type == -1:
		ym.pop()
		shuo.pop()
	return ym, shuo   # 月名表，合朔JD日期表


def differRA(p, JDE):
	# moonLBR：70倍截断平均误差小于1s，80倍误差3s
	# PlanetLBR：原截断基础上加5倍误差小于1s，加10倍误差3s
	ra1, dec1 = moonLBR(JDE, 70)[3:]
	if p in ['水','金','火','木','土'] :
		ra2, dec2 = PlanetLBR(p, JDE, 5)[3:]
	else:
		T = (JDE - 2451545) / 36525
		StarPosition(p, T)
		ra2, dec2 = p.ra, p.dec
	return deg2pi(ra1 - ra2), dec1 - dec2

def mcp_ip(p, t2): # 星合月
	t1 = t2 - 10
	t3 = t2 + 10
	L1 = differRA(p, t1)[0]
	L2 = differRA(p, t2)[0]
	L3 = differRA(p, t3)[0]
	if L1 > L2 and L2 < 0 and L1 > 0: L1 -= 360
	if L2 > L3 and L3 < 0 and L2 > 0: L3 += 360
	a = L2 - L1
	b = L3 - L2
	c = L1 + L3 - 2 * L2
	n0 = 0 # 初值
	i = 0
	while True:
		n = -2 * L2 / (a + b + c * n0)
		if abs(n0 - n) < 0.000001: break
		n0 = n
		i += 1
		if i == 100 : break # 插值未得到结果
	JDE = t2 + n * (t2 - t1)
	return JDE

def mcp_it(p, t2): # 行星在angle内的会合（插值估算，用于迭代）
	JDE = mcp_ip(p, t2)
	JD1 = JDE
	i = 0
	while True:
		JD0 = JD1
		L0 = differRA(p, JD0)[0]
		ra1, dec1 = differRA(p, JD0 + 0.000005)
		ra2, dec2 = differRA(p, JD0 - 0.000005)
		L0p = (ra1 - ra2) / 0.00001
		JD1 = JD0 - L0 / L0p
		if abs(L0) <= 0.00001:
			break
		i+=1
	return td2date(JD0), dec1



# 未考虑月相情况
def LunarOccultation(year, p):
	t = date2JD(year) +10  # 会合周期较长，默认date即为JDE
	result = []
	if p in ['水','金','火','木','土']:
		day = 29
	else: # 估算的间隔取值，未优化，可能有漏算或重复计算
		day = 28
	for i in range(13):
		date, dec = mcp_it(p, t+day*i)
		if abs(dec) < 1.2:
			result.append(date)
	return result

