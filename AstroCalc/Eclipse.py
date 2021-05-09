from AstroCalc.moon import *

# 精度较低，计算月食误差大
def eclipse(JD, type):
	T = (JD - 2451545) / 36525 # UT时刻，转TD时刻易求得上月日月食
	k = math.floor(1236.85 * T) + type * 0.5
	T = k / 1236.85
	no_eclipse = {0:"朔，未发生日食", 1:"望，未发生月食"}
	magnitude = '' # 食分
	F = ((160.7108 + 390.67050284*k - 0.0016118*pow(T,2) - 0.00000227*pow(T,3) + 0.000000011*pow(T,4))) % 360 # argument of latitude of Moon
	# F ≈ 180°为降交点，F ≈ 360°为升交点
	if abs(sin(F)) > 0.36: # 无日月食情况，返回UT 朔望时刻
		kind = no_eclipse[type]
		JDE = JD # 输入即朔望时间，节约计算
		#JDE = PhaseJDE(JD, type*2)  # 返回朔望时间
	else: # 计算发生时间
		M = (2.5534 + 29.10535670 * k - 0.0000014 * pow(T, 2) - 0.00000011 * pow(T, 3)) % 360  # mean anomaly of Sun
		Mp = (201.5643 + 385.81693528 * k + 0.0107582 * pow(T, 2) + 0.00001238 * pow(T, 3) - 0.000000058 * pow(T,4)) % 360  # mean anomaly of Moon
		Omg = (124.7746 - 1.56375588 * k + 0.0020672 * pow(T, 2) + 0.00000215 * pow(T, 3)) % 360  # Longitude of ascending node of the orbit
		E = 1 - 0.002516 * T - 0.0000074 * pow(T, 2)
		F1 = F - 0.02665 * sin(Omg)
		A1 = 299.77 + 0.107408 * k - 0.009173 * pow(T, 2)
		# 最大食时刻
		JDE = 2451550.09766 + 29.530588861 * k + 0.00015437 * pow(T, 2) - 0.000000150 * pow(T, 3) + 0.00000000073 * pow(T, 4) # 平朔望时间
		arg0 = [-0.4075, 0.1721*E, 0.0161, -0.0097, 0.0073*E, -0.0050*E, -0.0023, 0.0021*E, 0.0012, 0.0006*E, -0.0004, -0.0003*E, 0.0003, -0.0002*E, -0.0002*E, -0.0002]
		arg1 = [-0.4065, 0.1727*E, 0.0161, -0.0097, 0.0073*E, -0.0050*E, -0.0023, 0.0021*E, 0.0012, 0.0006*E, -0.0004, -0.0003*E, 0.0003, -0.0002*E, -0.0002*E, -0.0002]
		arg2 = [Mp, M, 2*Mp, 2*F1, Mp-M, Mp+M, Mp-2*F1, 2*M, Mp+2*F1, 2*Mp+M, 3*Mp, M+2*F1, A1, M-2*F1, 2*Mp-M, Omg] # 角度表示的参数
		if type == 0: # 朔
			for i in range(len(arg2)):
				JDE += arg0[i]*sin(arg2[i])
		elif type == 1: # 望
			for i in range(len(arg2)):
				JDE += arg1[i]*sin(arg2[i])
		# 判断食的类型
		P = 0.2070*E*sin(M) + 0.0024*E*sin(2*M) - 0.0392*sin(Mp) + 0.0116*sin(2*Mp) - 0.0073*E*sin(Mp+M) + 0.0067*E*sin(Mp-M) + 0.0118*sin(2*F1)
		Q = 5.2207 - 0.0045*E*cos(M) + 0.0020*E*cos(2*M) - 0.3299*cos(Mp) - 0.0060*E*cos(Mp+M) + 0.0041*E*cos(Mp-M)
		W = abs(cos(F1))
		r = (P*cos(F1) + Q*sin(F1)) * (1 - 0.0048*W)
		u = 0.0059 + 0.0046*E*cos(M) - 0.0182*cos(Mp) + 0.0004*cos(2*Mp) - 0.0005*cos(M+Mp)
		if type == 0:  # 日食
			if k == -804: r = - 1.5385
			if 0.9972 < abs(r) < 1.5433 + u:
				kind = "日偏食" # 无日食中心
				magnitude = '食分' + str(round((1.5433 + u - abs(r)) / (0.5461 + 2 * u), 2))
			elif 0.9972 < abs(r) < 0.9972+abs(u):
				kind = "全食或环食" # 无日食中心
			elif abs(r) > 1.5433+u:
				kind = "发生日食，地球不可见"
			elif u < 0:
				kind = "日全食"
			elif u > 0.0047:
				kind = "日环食"
			else:
				w = 0.00464 * math.sqrt(1-r*r)
				if u < w:
					kind = "日全环食" # 日月视直径相等
				else:
					kind = "日环食"
		elif type == 1:  # 月食
			magnitude = (1.0128 - u - abs(r)) / 0.5450
			if magnitude < 0: # 本影区无月食，判断半影区
				magnitude = (1.5573 + u - abs(r)) / 0.5450
				if magnitude < 0: # 半影区无月食
					kind = '未发生月食'
					magnitude = ''
					k_list = [-44403.5, -40499.5, -38398.5, -35541.5, -34372.5, -33798.5, -33656.5, -33392.5, -31914.5, -30569.5, -29819.5, -29367.5, -28880.5, -28874.5,
					          -28826.5, -28022.5, -27887.5, -26009.5, -19437.5, -19342.5, -19295.5, -19025.5, -15904.5, -14107.5, -8960.5, -8021.5, -5562.5, -5380.5,-4840.5, -3063.5, 340.5, 1192.5, 5089.5, 6116.5, 9784.5]
					if k in k_list: kind = '月偏食'
			if magnitude != '':
				if magnitude >= 1: kind = '月全食'
				else: kind = '月偏食'
				magnitude = '食分' + str(round(magnitude, 2))
	return JDE, kind, magnitude # UT的date


