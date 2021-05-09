# 升降中天
from Data import *
from AstroCalc import *


def rst_estimate(st0, ra, dec, gL, phi, h): # 估算rst时间，date为ut 0h
	Ht = (ra - gL - st0) % 360 # 格林尼治0h天体在gL地区的本地时角（负为未上中天，正为已上中天）
	H0 = HourAngle(h, dec, phi) # 地平纬度h到天顶的时角
	transit = Ht # 上中天时角
	rise = (Ht - H0) % 360 # 升起时角：从地平纬度h到达上中天的时间
	set = (Ht + H0) % 360 # 降下时角：从上中天到达地平纬度h的时间
	return rise/360, set/360, transit/360 # 转为日数表示的时间

def rst_correct(m, n, JD, dt, time, gL, phi, h): # 时角修正
	if m == 0: # 太阳
		ra, dec = sunLBR(JD + time + dt)[3:]
	elif m == 1: # 月亮
		ra, dec = moonLBR(JD + time + dt)[3:]
	st = jd2st(JD + time) # UT time时刻的格林尼治恒星时
	if n == 0: # 中天
		Ht = (st + gL) % 360 - ra # UT time时刻的本地时角（限定在当日）
		time -= Ht / 360
	else: # 升降
		Hs = (st + gL) % 360 - ra
		hs = eq2ho(Hs, phi, dec)[1]
		time += (hs - h) / (cos(dec)*cos(phi)*sin(Hs)) / 360
	return time

def SunRS(JD, dt, st0, gL, phi, h): # 太阳升降时间（date为ut8时间，日期与ut相同）
	ra, dec = sunLBR(JD + dt)[3:]
	if h == -7: h = -50 / 60
	rise, set, transit = rst_estimate(st0, ra, dec, gL, phi, h) # UT 0h的估算结果，日出为第二天的结果
	# 对估算结果进行修正（太阳运行较慢，无需迭代）
	# dt应为JD+time的dt，误差小于精度，故忽略
	upper_transit = rst_correct(0, 0, JD, dt, transit, gL, phi, h)
	lower_transit= rst_correct(0, 0, JD, dt, transit+0.5, gL, phi, h)
	rise = rst_correct(0, 1, JD-1, dt, rise, gL, phi, h)
	set = rst_correct(0, 2, JD, dt, set, gL, phi, h)
	return rise, set, upper_transit, lower_transit

# 月亮每日延时出入约48分钟，计算结果可能在下一天
def MoonRS(JD, dt, st0, gL, phi): # 月亮升降时角
	R, ra, dec = moonLBR(JD + dt)[2:] # TD = UT + △T
	pi = 1.3156 * pow(10, 9) / R # 地平视差
	h = 0.7275 * pi/3600 - 34/60 # 视地平纬度
	rise, set, transit = rst_estimate(st0, ra, dec, gL, phi, h)
	upper_transit = rst_correct(1, 0, JD, dt, transit, gL, phi, h)
	upper_transit = rst_correct(1, 0, JD, dt, upper_transit, gL, phi, h)
	#lower_transit= rst_correct(1, 0, JD, dt, transit+0.5, gL, phi, h)
	lower_transit = rst_correct(1, 0, JD, dt, upper_transit+0.5, gL, phi, h) # 由上中天时间修正
	rise = rst_correct(1, 1, JD, dt, rise, gL, phi, h)
	rise = rst_correct(1, 1, JD, dt, rise, gL, phi, h) # 再次修正（未迭代）
	set = rst_correct(1, 2, JD, dt, set, gL, phi, h)
	set = rst_correct(1, 2, JD, dt, set, gL, phi, h) # 再次修正
	return rise, set, upper_transit, lower_transit

def rst(date, gL, phi, h):
	JD = int(date2JD(date) + 0.5) - 0.5 # ut 0时，用于估算
	dt = deltaT(JD) / 86400
	st0 = jd2st(JD)  # UT 0h的格林尼治恒星时
	if h != 0.125:
		rise, set, ut, lt = SunRS(JD, dt, st0, gL, phi, h)
		rise -= 1
		lt -= 0.5
	else:
		rise, set, ut, lt = MoonRS(JD, dt, st0, gL, phi)
		lt += 0.5
	JD = JD + gL / 360 # 地方平时 = UT + 地理经度
	if h == -7: # 36分钟
		rise -= 2.5 / 100
		set += 2.5 / 100
	RiseTime = JD2date(JD + rise)
	SetTime = JD2date(JD + set)
	UtTime = JD2date(JD + ut)
	LtTime = JD2date(JD + lt)
	return RiseTime, SetTime, UtTime, LtTime


