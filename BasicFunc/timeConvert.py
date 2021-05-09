# 时间系统转换
from Ephem import *
from Data import *
import math

####################     日期转换     ####################
def day2hms(JD, format=0): # 0h起算的日数转时分秒
	d = JD - math.floor(JD) # 取出一日的小数部分（<0.0000001非输出位数）
	h = int(d * 24)
	m = int(round((d * 24 - h) * 60, 4))
	if m == 60:
		m = 0
		h += 1
	s = d * 86400 - h * 3600 - m * 60
	if abs(s) < 0.001: s = 0
	if format == 0:
		return "{:02d}:{:02d}:{:05.2f}".format(h, m, s)
	else:  # 用于时分秒转换
		return h % 24, m, round(s, 2)

def hms2day(hour, minute, second):
	day = (hour * 3600 + minute * 60 + second) / 86400
	return day

def GetDate(date): # 日期格式 "year/month/day hh:mm:ss" 或 "year-month-day hh:mm:ss"
	date = str(date).strip().split(" ")
	# 提供两种日期格式
	try:  # yy/mm/dd
		ymd = date[0].split("/")
		year = int(ymd[0])
	except:  # yy-mm-dd
		ymd = date[0].split("-")
		try:
			year = int(ymd[0])  # 第一个为负号，则第一项非数字
		except:  # 公元前
			year = -int(ymd[1])
			ymd = ymd[1:]
	try:
		month = int(ymd[1])
	except:
		month = 1
	try:
		day = int(ymd[2])
	except:
		day = 1
	try:
		date[1]  # 存在hms
		try:
			hms = date[1].split(":")
			hour = int(hms[0])
			try:
				minute = int(hms[1])
			except:
				minute = 0
			try:
				second = float(hms[2])
			except:
				second = 0
		except:
			minute, second = 0, 0
	except:
		hour, minute, second = 0, 0, 0
	return year, month, day, hour, minute, second

def date2JD(date):
	Year, Month, Day, hour, minute, second = GetDate(date)
	if Year < 0: Year += 1
	D = Day + hms2day(hour, minute, second)
	if Month in [1,2]:
		M = Month + 12
		Y = Year - 1
	else:
		Y = Year
		M = Month
	B = 0
	if Y > 1582 or (Y==1582 and M>10) or (Y==1582 and M==10 and D>=15):
		B = 2 - math.floor(Y/100) + math.floor(Y/400)  # 公元1582年10月15日以后每400年减少3闰
	JD = math.floor(365.25*(Y+4716)) + math.floor(30.6*(M+1)) + D + B - 1524.5
	return JD

def JD2date(JD):
	JD += 0.5  # 以BC4713年1月1日0时为历元
	Z = math.floor(JD)  # 年月日
	F = JD - Z  # 时分秒
	if Z < 2299161:  # 儒略历
		A = Z
	else:  # 格里历
		a = math.floor((Z - 1867216.25) / 36524.25)
		A = Z + 1 + a - math.floor(a / 4)
	k = 0
	while True:  # 在上一月
		B = A + 1524   # 以BC4717年3月1日0时为历元
		C = math.floor((B - 122.1) / 365.25)  # 积年
		D = math.floor(365.25 * C)  # 积年的日数
		E = math.floor((B - D) / 30.6)  # B-D为年内积日，E即月数
		day = B - D - math.floor(30.6 * E) + F
		hms = day2hms(F)
		if int(hms[:2]) == 24: # 当夜24点，实为第二日0点
			A += 1
			F = 0
			continue
		if day >= 1: break
		A -= 1
		k += 1
	month = E - 1 if E < 14 else E - 13
	year = C - 4716 if month > 2 else C - 4715
	day += k
	if int(day) == 0: day += 1
	if year <= 0: year -= 1  # 天文计算年转为公元纪年
	return "{}/{:02d}/{:02d} {}".format(year, month, int(day), hms[:-3])  # 秒的小数部分舍去，不进位




def JDN(JD):
	return math.floor(JD + 0.5)

def getWeekday(year, month, day):
	jdn = JDN(date2JD(str(year) + '/' + month + '/' + str(day)))
	weekday = weeks[math.floor(jdn % 7)]
	return jdn, weekday

def dateDiffer(JD1, JD2):
	return JDN(JD1) - JDN(JD2)

def DateCompare(JD1, JD2):  # ut+8 0h起算点历日比较
	if JDN(JD1) >= JDN(JD2): return True
	else: return False  # JD1 < JD2

def UTdate(date, ut=8): # ut为返回时间，ut=8返回ut，ut=0，返回ut+8，ut=-1 用于格式化
	JD = date2JD(date)
	if ut == 0: JD -= 8 /24
	elif ut == 8: JD += 8/24
	elif ut == -1: JD = JD
	date = JD2date(JD)
	return date

####################     年份转换     ####################
def ganzhiYear(year):
	if year == 0:
		# ngz = "不存在公元0年\n公元元年干支为辛酉"
		ngz = ''
	elif year < 0:
		ngz = gz[(year - 3) % 60]
	else:
		ngz = gz[(year - 4) % 60]
	return ngz

def ganzhiJD(JD, ut=0):  # ut+0结果为同ut
	rgz = gz[math.floor(JD + 0.5 + 49 + ut/24) % 60]
	return rgz

def ganzhiDate(date):  # ut+8 date
	JD = date2JD(date)
	rgz = ganzhiJD(JD)
	return rgz

def gzYear(year):
	if year == 0: year += 1
	year = str(year) + '年(' + ganzhiYear(year) + ')'
	return year

def gyjn(year): # 给定年份年转公元纪年
	if year == 0:
		return "无公元0年"
	if year < 0:
		return "公元前" + str(-year) + "年"
	elif year == 1:
		return "公元元年"
	elif year > 0:
		return "公元" + str(year) + "年"

def gyjnFormat(year): # 对齐输出
	if year < 0:
		return "公元前{:>3}年（{}）\t".format(-year, ganzhiYear(year))
	elif year == 1:
		return "公元   元年（" + ganzhiYear(year) + "）\t"
	elif year > 0:
		return "公元{:>5}年（{}）\t".format(year, ganzhiYear(year))

def gyjnBC(year):  # 公元前以BC表示，年代表专用
	if year == 0: year += 1
	year = str(year).replace("-", "BC")
	return year

####################     时间转换     ####################


def EquationTime(JDE):  # 真太阳时与平太阳时之差
	t = (JDE - 2451545) / 365250
	L0 = (280.4664567 + 360007.6982779 * t + 0.03032028 * t**2 + t**3 / 49931 - t**4 / 15300 - t**5 / 2000000) % 360  # 平黄经
	dp, de, e = nutation(t * 10)
	ra = sunLBR(JDE)[3]  # 视赤经
	E = L0 - 0.005718 - ra + dp/3600 * cos(e)
	return E  # 角度

def deltaT(JD):
	date = JD2date(JD)
	Y, M = GetDate(date)[:2]
	y = Y + (M - 0.5) / 12
	# NASA DeltaT 计算法
	if Y < -500:
		u = (y - 1820) / 100
		dt = -20 + 32 * pow(u,2)
	elif -500 <= Y < 500:
		u = y / 100
		dt = 10583.6 - 1014.41 * u + 33.78311 * pow(u,2) - 5.952053 * pow(u,3)- 0.1798452 * pow(u,4) + 0.022174192 * pow(u,5) + 0.0090316521 * pow(u,6)
	elif 500 <= Y < 1600:
		u = (y - 1000) / 100
		dt = 1574.2 - 556.01 * u + 71.23472 * pow(u,2) + 0.319781 * pow(u,3) - 0.8503463 * pow(u,4) - 0.005050998 * pow(u,5) + 0.0083572073 * pow(u,6)
	elif Y >= 1600:
		if (Y >= 1600 and Y < 1700):
			u = y - 1600
			dt = 120 - 0.9808 * u - 0.01532 * pow(u,2) + pow(u,3) / 7129
		elif (Y >= 1700 and Y < 1800):
			u = y - 1700
			dt = 8.83 + 0.1603 * u- 0.0059285 * pow(u,2)+ 0.00013336 * pow(u,3)- pow(u,4) / 1174000
		elif (Y >= 1800 and Y < 1860):
			u = y - 1800
			dt = 13.72 - 0.332447 * u+ 0.0068612 * pow(u,2)+ 0.0041116 * pow(u,3)- 0.00037436 * pow(u,4)+ 0.0000121272 * pow(u,5)- 0.0000001699 * pow(u,6)+ 0.000000000875 * pow(u,7)
		elif (Y >= 1860 and Y < 1900):
			u = y -1860
			dt = 7.62 + 0.5737 * u - 0.251754 * pow(u,2)+ 0.01680668 * pow(u,3)- 0.0004473624 * pow(u,4)+ pow(u,5) / 233174
		elif (Y >= 1900 and Y < 1920):
			u = y - 1900
			dt = 1.494119 * u - 2.79- 0.0598939 * pow(u,2)+ 0.0061966 * pow(u,3)- 0.000197 * pow(u,4)
		elif (Y >= 1920 and Y < 1941):
			u = y - 1920
			dt = 21.20 + 0.84493 * u - 0.076100 * pow(u,2) + 0.0020936 * pow(u,3)
		elif (Y >= 1941 and Y < 1961):
			u = y - 1950
			dt = 29.07 + 0.407 * u - pow(u,2) / 233 + pow(u,3) / 2547
		elif (Y >= 1961 and Y < 1986):
			u = y - 1975
			dt = 45.45 + 1.067 * u - pow(u,2) / 260 - pow(u,3) / 718
		elif (Y >= 1986 and Y < 2005):
			u = y - 2000
			dt = 63.86 + 0.3345 * u- 0.060374 * pow(u,2)+ 0.0017275 * pow(u,3)+ 0.000651814 * pow(u,4)+ 0.00002373599 * pow(u,5)
		elif (Y >= 2005 and Y < 2050):
			u = y - 2000
			dt = 62.92 + 0.32217 * u + 0.005589 * pow(u,2)
		elif (Y >= 2050 and Y <= 2150):
			u = (y - 1820) / 100
			dt = 32 * pow(u,2) - 0.5628 * (2150 - y) - 20
		elif Y > 2150: # and Y <= 3000:
			u = (y - 1820) / 100
			dt = 32 * pow(u,2) - 20
	return dt # 单位：时秒

# 恒星时指从春分点距子午圈的时角
def jd2st(JD): # IAU2000格林尼治恒星时，JD为任意时刻的格林尼治时间
	dt = deltaT(JD)
	T = (JD - 2451545 + dt/86400) / 36525 # TD
	GST0 = math.pi*2 * (0.7790572732640 + 1.00273781191135448 * (JD - 2451545)) * rad + (0.014506 + 4612.15739966 * T + 1.39667721 * T**2 - 0.00009344 * T**3 + 0.00001882 * T**4) / 3600  # 单位：角度
	dp, de, e = nutation(T)
	GST = GST0 + (dp * cos(e)) / 3600   # 真恒星时 = 平恒星时 + 赤经章动，单位：角度
	return GST % 360 # 格林尼治恒星时（本地恒星时=格林尼治恒星时+地理经度（向东为正））

def td2jd(JDE, ut=8): #力学时转世界时 （+8h），day含小数
	dt = deltaT(JDE)
	# △T = TD - UT # 单位时秒
	JD = JDE - dt / 86400  # 转为0h UT的儒略日
	JD += ut / 24 # 转为8h UT的儒略日
	return JD

def td2date(JDE, ut=8): # 输入时间作为历书时进行计算
	JD = td2jd(JDE, ut) # 已转为ut+8时间
	date = JD2date(JD)
	date = GetDate(date) # y,m,d,h,mi,s
	return "{:02d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(date[0], date[1], date[2], date[3], date[4], round(date[5]))

def ut2td(date): # 任意时区ut时转历书时
	JD = date2JD(date)
	dt = deltaT(JD)
	JDE = JD + dt / 86400
	return JDE

def jd2td(JD, gL):
	JD -= gL / 360
	dt = deltaT(JD)
	JDE = JD + dt / 86400
	if gL < 0: JDE -= 1
	return JDE

def date2td(date): # 从输入日期（UT+8h）中获得JDE和T
	JD = date2JD(date) - 8 / 24  # ut JD
	date = JD2date(JD + 8/24)  # UT +8
	dt = deltaT(JD)
	JDE = JD + dt / 86400
	T = (JDE - 2451545) / 36525  # 儒略世纪数
	return date, JDE, T

def getInput(time):
	try:
		year = int(time)
		flag = True
		date, JDE, T = 0, 0, 0
	except:
		flag = False # 指定日期计算
		date, JDE, T = date2td(time)
		year = date.split('/')[0]
	return year, flag, date, JDE, T


