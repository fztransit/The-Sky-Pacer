# 求太阳在任意黄经的时间
from BasicFunc import *
from Ephem import *

def ES(year,angle): # 定气（估值用于迭代）
	if angle > 270: year -= 1  # 起冬至（不含，用作年末）
	if year <= 1000:  # -2000 <= year <= 1000:
		Y = year / 1000
		JDE1 = 1721139.29189 + 365242.13740 * Y + 0.06134 * pow(Y, 2) + 0.00111 * pow(Y, 3) - 0.00071 * pow(Y, 4) # 春分
		JDE2 = 1721233.25401 + 365241.72562 * Y - 0.05323 * pow(Y, 2) + 0.00907 * pow(Y, 3) + 0.00025 * pow(Y, 4) # 夏至
		JDE3 = 1721325.70455 + 365242.49558 * Y - 0.11677 * pow(Y, 2) - 0.00297 * pow(Y, 3) + 0.00074 * pow(Y, 4) # 秋分
		JDE4 = 1721414.39987 + 365242.88257 * Y - 0.00769 * pow(Y, 2) - 0.00933 * pow(Y, 3) - 0.00006 * pow(Y, 4) # 冬至
	elif 1000 < year:  # <= 3000:
		Y = (year - 2000) / 1000
		JDE1 = 2451623.80984 + 365242.37404 * Y + 0.05169 * pow(Y, 2) - 0.00411 * pow(Y, 3) - 0.00057 * pow(Y, 4) # 春分
		JDE2 = 2451716.56767 + 365241.62603 * Y + 0.05325 * pow(Y, 2) + 0.00888 * pow(Y, 3) - 0.00030 * pow(Y, 4) # 夏至
		JDE3 = 2451810.21715 + 365242.01767 * Y - 0.11575 * pow(Y, 2) + 0.00337 * pow(Y, 3) + 0.00078 * pow(Y, 4) # 秋分
		JDE4 = 2451900.05952 + 365242.74049 * Y - 0.00623 * pow(Y, 2) - 0.00823 * pow(Y, 3) + 0.00032 * pow(Y, 4) # 冬至
	if 0 <= angle < 90:
		JDE0 = JDE1
	elif 90 <= angle < 180:
		JDE0 = JDE2
	elif 180 <= angle < 270:
		JDE0 = JDE3
	else:
		JDE0 = JDE4
	T = (JDE0 - 2451545) / 36525
	W = 35999.373*T - 2.47
	dr = 1 + 0.0334*cos(W) + 0.0007*cos(2*W)
	series = [ #  A     B                C
				[485,   324.96,     1934.136],
				[203,   337.23,     32964.467],
				[199,   342.08,     20.186],
				[182,   27.85,      445267.112],
				[156,   73.14,      45036.886],
				[136,   171.52,     22518.443],
				[77,    222.54,     65928.934],
				[74,    296.72,     3034.906],
				[70,    243.58,     9037.513],
				[58,    119.81,     33718.147],
				[52,    297.17,     150.678],
				[50,    21.02,      2281.226],
				[45,    247.54,     29929.562],
				[44,    325.15,     31555.956],
				[29,    60.93,      4443.417],
				[18,    155.12,     67555.328],
				[17,    288.79,     4562.452],
				[16,    198.04,     62894.029],
				[14,    199.76,     31436.921],
				[12,    95.39,      14577.848],
				[12,    287.11,     31931.756],
				[12,    320.81,     34777.259],
				[9,     227.73,     1222.114],
				[8,     15.45,      16859.074]]
	S = 0 # S += A * cos(B+C*T)
	for i in range(24):
		S += series[i][0] * cos(series[i][1] + series[i][2]*T)
	JDE = JDE0 + 0.00001 * S / dr
	return JDE

def equinox_solstice(year, angle, ut=8): # 未迭代，只适用分至
	if year <= 0:  year += 1  # 用于天文计算的年份
	JDE = ES(year, angle)  # 初值
	L = sunLBR(JDE)[0]
	JDE += rad * sin(angle - L)
	date = td2date(JDE, ut)  # 默认ut+8
	return date

# 迭代修正精度
def SolarTermsJD(year, angle, ut=8):
	angle %= 360
	if year <= 0:  year += 1  # 用于天文计算的年份
	JDE = ES(year, angle)  # 初值
	JDE1 = JDE
	i = 0
	while True:
		JDE2 = JDE1
		L = sunLBR(JDE2)[0]
		JDE1 += rad * sin(deg2pi(angle - L))
		if abs(JDE1 - JDE2) < 0.000001 or i > 10:
			break
		i += 1
	JD = td2jd(JDE1, ut)  # 默认ut+8
	return JD



def SolarTermsDate(year, angle, ut=8):
	JD = SolarTermsJD(year, angle, ut)
	date = JD2date(JD)
	return date

def SolarTermsJD2(year, angle, month):  # 岁首建寅
	if month > 10 and 270 < angle <= 330:  year += 1  # 岁末冬至后雨水前
	return SolarTermsJD(year, angle)

def EvenTerms(year, angle):  # 十二节
	if 225 <= angle <= 270: year -= 1  # 岁首冬至改为立冬
	JD = SolarTermsJD(year, angle)
	return JD

def selectSTDate(s, year): # 获得选定节气日期
	if s == '前冬至':
		angle = 270
		year -= 1
	else:
		angle = (270 + jieqi.index(s) * 15) % 360
	date = SolarTermsDate(year, angle)
	return date2td(date) # 获得ut+8 date、JDE、T


