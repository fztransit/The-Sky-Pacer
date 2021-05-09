# 二十八宿距星计算
from BasicFunc import *
from Ephem import *

# 二十八宿距星数据结构
class Star:
	def __init__(self, Chinese_name,Designation, RightAscension, Declination, parallax,pm_ra,pm_dec): # 构造方法
		self.name = Chinese_name
		self.design = Designation
		self.__RA = RightAscension  # J2000.0赤经（单位：时分秒），不可更改
		self.__Dec = Declination    # J2000.0赤纬（单位：度分秒），不可更改
		self.Parallax = parallax    # 周年视差（单位：毫角秒）
		self.propre_ra = pm_ra      # 赤经方向的自行（单位：毫角秒/年）
		self.propre_dec = pm_dec    # 赤纬方向的自行（单位：毫角秒/年）
		self.ra = 0  # 赤经计算值（单位：角度）
		self.dec = 0  # 赤纬计算值（单位：角度）
	def ra2deg(self): # 赤经hms格式转为角度
		h = eval(self.__RA[:self.__RA.index('h')])
		m = eval(self.__RA[self.__RA.index('h')+2:self.__RA.index('m')])
		s = eval(self.__RA[self.__RA.index('m')+2:self.__RA.index('s')])
		deg = (h + m / 60 + s / 3600) / 24 * 360
		return deg
	def dec2deg(self): # 赤纬dms格式转为角度
		d = abs(eval(self.__Dec[:self.__Dec.index('d')]))
		m = eval(self.__Dec[self.__Dec.index('d') + 2:self.__Dec.index("'")])
		s = eval(self.__Dec[self.__Dec.index("'")+2:])
		deg = d + m / 60 + s / 3600
		if '-' in self.__Dec: deg = -deg
		return deg

##########    格式转换工具    ##########
gdzh = 360 / 365.25 # 今度÷该值得古度，古度×该值得今度

def t2date(T): # 儒略世纪数转为ephem使用的时间格式
	JD = T*36525 + 2451545.0
	year, month, day = GetDate(JD2date(JD))[:3]
	d = day - int(day)
	h = int(d*24)
	m = int((d*24-h)*60)
	s = d*86400 - h*3600 - m*60
	return "{}/{}/{} {}:{}:{}".format(year,month,int(day),h,m,int(s))

##########    视位置修正项计算函数   ##########
def Propre(star, T): # 计算自行
	star.ra += star.propre_ra/1000/3600 * T*100
	star.dec += star.propre_dec/1000/3600 * T*100
	return star.ra, star.dec # Date历元的平坐标

def Precession(star, T): # 历元J2000.0至T时刻的岁差
	zeta = (2.650545 + 2306.083227*T + 0.2988499*T**2 + 0.01801828*T**3 - 5.971e-6*T**4 - 3.173e-7*T**5) / 3600
	z = (-2.650545 + 2306.077181*T + 1.0927348*T**2 + 0.01826837*T**3 - 0.000028596*T**4 - 2.904e-7*T**5) / 3600
	theta = (2004.191903*T - 0.4294934*T**2 - 0.04182264*T**3 - 7.089e-6*T**4 -1.274e-7*T**5) / 3600
	# zeta = precessionArgs('zeta', T)
	# z = precessionArgs('z', T)
	# theta = precessionArgs('theta', T)
	A = cos(star.dec) * sin(star.ra+zeta)
	B = cos(theta) * cos(star.dec) * cos(star.ra+zeta) - sin(theta) * sin(star.dec)
	C = sin(theta) * cos(star.dec) * cos(star.ra+zeta) + cos(theta) * sin(star.dec)
	star.ra = math.atan2(A, B) * rad + z
	star.dec = math.asin(C) * rad
	return star.ra, star.dec  # Date历元的平坐标




def Aberration(star, T):
	L2 = 3.1761467 + 1021.3285546 * T
	L3 = 1.7534703 + 628.3075849 * T
	L4 = 6.2034809 + 334.0612431 * T
	L5 = 0.5995465 + 52.9690965 * T
	L6 = 0.8740168 + 21.3299095 * T
	L7 = 5.4812939 + 7.4781599 * T
	L8 = 5.3118863 + 3.8133036 * T
	Lp = 3.8103444 + 8399.6847337 * T  # mean longitude of moon
	D = 5.1984667 + 7771.3771486 * T
	Mp = 2.3555559 + 8328.6914289 * T
	Fp = 1.6279052 + 8433.4661601 * T
	velocity = [  # A,  Xsin, Xcos           Ysin, Ycos                      Zsin, Zcos
		[L3, [-1719914 - 2 * T, -25], [25 - 13 * T, 1578089 + 156 * T], [10 + 32 * T, 684185 - 358 * T]],
		[2 * L3, [6434 + 141 * T, 28007 - 107 * T], [25697 - 95 * T, -5904 - 130 * T], [11141 - 48 * T, -2559 - 55 * T]],
		[L5, [715, 0], [6, -657], [-15, -282]],
		[Lp, [715, 0], [0, -656], [0, -285]],
		[3 * L3, [486 - 5 * T, -236 - 4 * T], [-216 - 4 * T, -446 + 5 * T], [-94, -193]],
		[L6, [159, 0], [2, -147], [-6, -61]],
		[Fp, [0, 0], [0, 26], [0, -59]],
		[Lp + Mp, [39, 0], [0, -36], [0, -16]],
		[2 * L5, [33, -10], [-9, -30], [-5, -13]],
		[2 * L3 - L5, [31, 1], [1, -28], [0, -12]],
		[3 * L3 - 8 * L4 + 3 * L5, [8, -28], [25, 8], [11, 3]],
		[5 * L3 - 8 * L4 + 3 * L5, [8, -28], [-25, -8], [-11, -3]],
		[2 * L2 - L3, [21, 0], [0, -19], [0, -8]],
		[L2, [-19, 0], [0, 17], [0, 8]],
		[L7, [17, 0], [0, -16], [0, -7]],
		[L3 - 2 * L5, [16, 0], [0, 15], [1, 7]],
		[L8, [16, 0], [1, -15], [-3, -6]],
		[L3 + L5, [11, -1], [-1, -10], [-1, -5]],
		[2 * L2 - 2 * L3, [0, -11], [-10, 0], [-4, 0]],
		[L3 - L5, [-11, -2], [-2, 9], [-1, 4]],
		[4 * L3, [-7, -8], [-8, 6], [-3, 3]],
		[3 * L3 - 2 * L5, [-10, 0], [0, 9], [0, 4]],
		[L2 - 2 * L3, [-9, 0], [0, -9], [0, -4]],
		[2 * L2 - 3 * L3, [-9, 0], [0, -8], [0, -4]],
		[2 * L6, [0, -9], [-8, 0], [-3, 0]],
		[2 * L2 - 4 * L3, [0, -9], [8, 0], [3, 0]],
		[3 * L3 - 2 * L4, [8, 0], [0, -8], [0, -3]],
		[Lp + 2 * D - Mp, [8, 0], [0, -7], [0, -3]],
		[8 * L2 - 12 * L3, [-4, -7], [-6, 4], [-3, 2]],
		[8 * L2 - 14 * L3, [-4, -7], [6, -4], [3, -2]],
		[2 * L4, [-6, -5], [-4, 5], [-2, 2]],
		[3 * L2 - 4 * L3, [-1, -1], [-2, -7], [1, -4]],
		[2 * L3 - 2 * L5, [4, -6], [-5, -4], [-2, -2]],
		[3 * L2 - 3 * L3, [0, -7], [-6, 0], [-3, 0]],
		[2 * L3 - 2 * L4, [5, -5], [-4, -5], [-2, -2]],
		[Lp - 2 * D, [5, 0], [0, -5], [0, -2]]]
	XYZ = [0, 0, 0]
	for i in range(36):
		A = velocity[i][0]
		for j in range(3):
			XYZ[j] += velocity[i][j+1][0] * math.sin(A) + velocity[i][j+1][1] * math.cos(A)
	c = 17314463350
	X, Y, Z = XYZ
	abr_ra = (Y * cos(star.ra) - X * sin(star.ra)) / c / cos(star.dec)
	abr_dec = ((X * cos(star.ra) + Y * sin(star.ra)) * sin(star.dec) - Z * cos(star.dec)) / c
	return abr_ra * rad, abr_dec * rad

def Parallax(star, T): # 视差修正（误）
	star.ra += star.Parallax / 1000 * T * 100
	star.dec += star.Parallax / 1000 * T * 100

##########    主函数    ##########
def StarPosition(star, T): # 由J2000.0恒星位置计算任意时刻视位置
	# 获得度数表示的J2000.0恒星位置
	star.ra = star.ra2deg()
	star.dec = star.dec2deg()
	# 获得T时刻平位置
	Propre(star, T)                                         # 计算自行
	Precession(star, T)                                     # 计算岁差
	# 获得T时刻视位置
	nut = nut_eq(star.ra, star.dec, T)                      # 计算章动和黄赤交角
	abr_ra, abr_dec = Aberration(star, T)                   # 计算光行差
	star.ra = (star.ra + nut[0]/3600 + abr_ra) % 360        # 修正章动和光行差
	star.dec = (star.dec + nut[1]/3600 + abr_dec)
	return star.ra, star.dec  # 度数表示的视赤经、视赤纬


def interpolation(star, angle, n0, t2): # 插值计算恒星在赤经为angle时的时间
	t1 = t2 - 5
	t3 = t2 + 5
	StarPosition(star, t1)
	ra1 = star.ra % 360 * 3600 # 赤经变化量小，改为角秒计算
	StarPosition(star, t2)
	ra2 = star.ra % 360 * 3600
	StarPosition(star, t3)
	ra3 = star.ra % 360 * 3600
	a = ra2 - ra1
	b = ra3 - ra2
	c = ra1 + ra3 - 2*ra2
	n = -2*(ra2-angle) / (a + b + c*n0)
	return n,t1

def iteration(star, angle, t2): # 迭代修正精度
	if angle == 0: angle = 360
	n0 = 0 # 初值
	i = 0
	while True:
		n, t1 = interpolation(star, angle * 3600, n0, t2)
		#n = -2 * (ra2 - angle*3600) / (a + b + c * n0)
		if abs(n0 - n) < 0.000000000001: break
		n0 = n
		i += 1
		if i == 20: break # 超出计算机精度处理范围
	return t2date(t2+n*(t2-t1))

def YearItera(hx, angle, t2): # 按年份修正
	angle %= 360
	StarPosition(hx, t2)
	ra = round(hx.ra % 360, 1)
	if abs(ra - angle) > 180: ra += 360
	t2 += (angle - ra) * 257.72 / 360  # 根据岁差周期重新估算初值
	j = 0
	while True:
		date = iteration(hx, angle, t2)
		year = date.split('/')[0]
		t = int(year) / 100 - 20
		StarPosition(hx, t)
		ra = round(hx.ra % 360, 1)
		if abs(ra - angle) < 0.1: break
		t2 = t
		j += 1
		if j > 10:
			year = year + '\n异常结果，请重新估值（该年实际赤经为' + str(ra) + '）'
			break  # 超出计算机精度处理范围
			#YearItera(hx, angle, t2)
	return year
