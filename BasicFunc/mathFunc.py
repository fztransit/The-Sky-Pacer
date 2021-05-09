import math
rad = 180 / math.pi
# 度数转弧度“度数 / rad”，弧度转度数“弧度 * rad”

def sin(degree):
	degree = (degree % 360) / rad
	sin = math.sin(degree)
	return round(sin,15)

def cos(degree):
	degree = (degree % 360) / rad
	cos = math.cos(degree)
	return round(cos,15)

def tan(degree):
	degree = (degree % 360) / rad
	tan = math.tan(degree)
	return round(tan,15)

def asin(x):
	asin = math.asin(x) * rad
	return  round(asin,14)

def acos(x):
	acos = math.acos(x) * rad
	return  round(acos,13)

def atan(x):
	atan = math.atan(x) * rad
	return  round(atan,16)

def atan2(y,x):
	atan2 = math.atan2(y,x) * rad
	return round(atan2,16)

def deg2dms(deg): # 度数转度分秒，仅用于输出表示
	a = deg - int(deg) # 获取度数的小数部分
	b = abs(a * 3600) # 小数部分全部转为角秒表示
	m = int(b / 60) # 整数部分为分
	s = b % 60 # 余数部分为秒
	if -1 < deg < 0:
		return " -{:1d}º{:02d}'{:05.2f}\"".format(int(deg),m,round(s,4))
	else:
		return "{:3d}º{:02d}'{:05.2f}\"".format(int(deg),m,round(s,4))


def deg2hms(deg): # 度数转时分秒，仅用于赤经输出表示
	deg = round(deg % 360, 4)
	a = deg/15 - int(deg/15) # 获取度数的小数部分
	b = a * 3600
	m = int(b / 60)
	s = b % 60
	return "{:02d}h{:02d}m{:05.2f}s".format(int(deg/15), m, round(s,2))

def ra2deg(h,m,s): # 赤经转度数表示
	deg = (h + m/60 + s/3600) / 24 * 360
	return deg

def dms2deg(degree): # 度:分:秒 格式转为度数表示
	degree = str(degree)
	dms = degree.split(':')
	deg = int(dms[0]) + int(dms[1])/60 + float(dms[2])/3600
	return deg # 时分秒转度数即*15

def deg2ra(deg):
	h = deg / 360 * 24
	m = (h - int(h)) * 60
	s = (m - int(m))*60
	return "{:2d}h{:02d}m{:05.2f}s".format(int(h), int(m), round(s,2))

def mod(x, y):
	return x - y * math.floor(x / y + 0.5)

def deg2pi(deg): # 角度转为-180°至180°
	deg = mod(deg, 360)
	return deg

def rad2pi(rad): # 角度转为-π至π
	rad = mod(rad, math.pi*2)
	return rad

def lenDigit(number):  # 整数
	if number == 0:
		return 1
	length = int(math.log10(abs(number))) + 1
	if number < 0:
		length += 1
	return length

def lenXY(yfa, n):
	xy = yfa / n
	if xy == int(xy): xy = int(xy)
	length = len(str(xy))
	return length

def dcjs(n, a, d):
	s = n * a + n * (n - 1) * d / 2
	return round(s, 12)

def dyqys(a, m):  # ax ≡ 1 (mod m)
	k0 = 0
	k1 = 1
	m0 = m
	while a != 1:
		q = m // a
		r = m % a
		m = a
		a = r
		k = k0 - q * k1
		k0 = k1
		k1 = k
	return m0 + k



def lce(a, m, b=1):   # ax ≡ b (mod m)
	hcf = math.gcd(a, m)
	if b % hcf != 0: return []  # 无解
	a0 = a // hcf
	m0 = m // hcf
	b0 = b // hcf
	x0 = dyqys(a0, m0)   # a0 * x ≡ 1 (mod m0)
	n = (b0 * x0) % m0
	x = []
	for i in range(hcf):
		x.append((n + i * m0) % m)
	return x



def Calculator(ui):
	try:
		if ui.txtEditExpression.text() == "":
			ui.edit.append("可输入计算表达式。按回车计算。\n "
						"支持加减乘除取余、幂运算、角度弧度转换。\n "
						"如幂运算：为“10**2”，三次方为“10**3”，或调用函数pow(10,4)。\n"
						"角度转弧度/rad，弧度转角度*rad。如“180/rad”，“3.14*rad”.\n ")
			return 0
		if 'rad' in ui.txtEditExpression.text():
			c1 = (ui.txtEditExpression.text().split('rad')[0])
			c = eval(c1 + str(rad))
		else:
			c = eval(ui.txtEditExpression.text())
		ui.edit.append(ui.txtEditExpression.text() + ' = ' + str(c) + '\n')
	except:
		ui.edit.append("输入错误，请重新输入\n")
		

def Deg2DMS(ui): # 互转
	try:
		deg = eval(ui.txtEditExpression.text())
		dms = deg2dms(deg)
		ui.edit.append(ui.txtEditExpression.text() + '度的角度表示：' + dms + '\n')
	except:
		if '°' in ui.txtEditExpression.text(): dmsChar = ['°', '′', '″']
		elif 'º' in ui.txtEditExpression.text(): dmsChar = ['º', "'", '"']
		try:
			dms = ui.txtEditExpression.text()
			d = float(dms.split(dmsChar[0])[0])
			try: # 有'm'情况
				m = float(dms.split(dmsChar[0])[1].split(dmsChar[1])[0])
				try: # 有's'情况
					s = float(dms.split(dmsChar[0])[1].split(dmsChar[1])[1].split(dmsChar[2])[0])
				except: # 无's'情况
					try: # 实际有值
						s = float(dms.split(dmsChar[0])[1].split(dmsChar[2])[1])
					except: # 无值
						s = 0
			except:
				m = 0
				s = 0
			deg = d + m / 60 + s / 3600
			ui.edit.append(ui.txtEditExpression.text() + '的度数表示：' + str(deg) + '°\n')
		except:
			ui.edit.append("输入度分秒（°′″）转为度数或输入度数转为度分秒\n")

def Deg2HMS(ui): # 互转
	try:
		deg = eval(ui.txtEditExpression.text())
		hms = deg2hms(deg % 360)
		ui.edit.append(ui.txtEditExpression.text() + '度的时角表示：' + hms + '\n')
	except:
		try:
			hms = ui.txtEditExpression.text()
			h = float(hms.split('h')[0])
			try: # 有'm'情况
				m = float(hms.split('h')[1].split('m')[0])
				try: # 有's'情况
					s = float(hms.split('h')[1].split('m')[1].split('s')[0])
				except: # 无's'情况
					try: # 实际有值
						s = float(hms.split('h')[1].split('m')[1])
					except: # 无值
						s = 0
			except:
				m = 0
				s = 0
			deg = (h + m / 60 + s / 3600) / 24 * 360
			ui.edit.append(ui.txtEditExpression.text() + '的度数表示：' + str(deg) + '°\n')
		except:
			ui.edit.append("输入时分秒（hms）转为度数或输入度数转为时分秒\n")