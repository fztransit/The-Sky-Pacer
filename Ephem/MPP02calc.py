from Ephem import *

##########    VSOP87D（Date历元行星日心位置）    ##########
def computeMain(list, t, args):
	D, F, l, lp = args[:4]
	triFunc = [math.sin, math.sin, math.cos]
	LBR = [0, 0, 0]
	for i in range(3):  # L、B、R
		series = list[i]
		for k in range(len(series)):
			LBR[i] += series[k][4] * triFunc[i]((series[k][0] * D + series[k][1] * F + series[k][2] * l + series[k][3] * lp) / 3600 / rad)
	return LBR  # L、B单位弧度，R单位AU

def computePer(list, t, args1, args2, n=1): # n用于截取计算周期项，只能为正整数，默认1为不截取
	Me, V, Ma, J, S, U, N = args1
	D, F, l, lp, T, Z = args2
	LBR = [0, 0, 0]
	for i in range(2):  # L、B、R（跳过对R的修正，平均误差小于20km）
		for j in range(len(list[i])):  # number of series
			value = 0
			series = list[i][j]
			if j < 2:
				terms = len(series) // n
			else:
				terms = len(series)
			for k in range(terms):
				phi = (series[k][2] * D + series[k][3] * F + series[k][4] * l + series[k][5] * lp + series[k][6] * Me + series[k][7] * V + series[k][8] * T\
				      + series[k][9] * Ma + series[k][10] * J + series[k][11] * S + series[k][12] * U + series[k][13] * N + series[k][14] * Z) / 3600 / rad
				value += (series[k][0] * math.sin(phi) + series[k][1] * math.cos(phi))
			LBR[i] += value * t ** j
	return LBR  # L、B单位弧度，R单位AU

def computeMPP(JDE, n=1):
	t = (JDE - 2451545) / 36525

	# Planetary Arguments
	Me = 252 * 3600 + 15 * 60 +  3.216919 + 538101628.68888 * t
	V  = 181 * 3600 + 58 * 60 + 44.758419 + 210664136.45777 * t
	Ma = 355 * 3600 + 25 * 60 +  3.642778 +  68905077.65936 * t
	J  =  34 * 3600 + 21 * 60 +  5.379392 +  10925660.57335 * t
	S  =  50 * 3600 +  4 * 60 + 38.902495 +   4399609.33632 * t
	U  = 314 * 3600 +  3 * 60 +  4.354234 +   1542482.57845 * t
	N  = 304 * 3600 + 20 * 60 + 56.808371 +    786547.89700 * t
	plans = [Me, V, Ma, J, S, U, N]

	# Fundamental Arguments

	dG = 0.00085
	dE = -0.00006
	dep = 0.00224
	v = 1732559343.73604 / 3600 / rad  # W1/cy
	dW11 = -0.07008  # ΔW1/cy
	dT1 = 0.00732  # ΔT/cy
	W23 = [14643420.3171 / 3600 / rad, -6967919.5383 / 3600 / rad]  # W2/cy, W3/cy
	Bp = [[0.311079095, -0.004482398, -0.001102485,  0.001056062,  0.000050928],
	      [0.103837907,  0.000668287, -0.001298072, -0.000178028, -0.000037342]]
	m = 0.074801329
	a = 0.002571881
	ddW = [0, 0]
	for i in range(2):
		x = Bp[i][0] + 2*a*Bp[i][4] / (3*m)
		y = Bp[i][1] * dG + Bp[i][2] * dE + Bp[i][3] * dep
		ddW[i] = (W23[i] / v - m * x) * dW11 + x * dT1 + v * y

	dW1 = -0.07008 - 0.35106 * t - 0.03743 * t**2 - 0.00018865 * t**3 - 0.00001024 * t**4
	dW2 = 0.20794 + 0.08017 * t + 0.00470602 * t**2 - 0.00025213 * t**3
	dW3 = -0.07215 - 0.04317 * t - 0.00261070 * t**2 - 0.00010712 * t**3
	dT = -0.00033 + 0.00732 * t
	dw = -0.00749

	W1 = 218 * 3600 + 18 * 60 + 59.95571 + 1732559343.73604 * t -   6.8084 * t**2 +   0.006604 * t**3 - 0.00003169 * t**4 + dW1
	W2 =  83 * 3600 + 21 * 60 + 11.67475 +   14643420.3171  * t -  38.2631 * t**2 -   0.045047 * t**3 + 0.00021301 * t**4 + dW2 + ddW[0]
	W3 = 125 * 3600 +  2 * 60 + 40.39816 -    6967919.5383  * t +   6.3590 * t**2 +   0.007625 * t**3 - 0.00003586 * t**4 + dW3 + ddW[1]
	T  = 100 * 3600 + 27 * 60 + 59.13885 +   129597742.2930 * t -   0.0202 * t**2 +   0.000009 * t**3 + 0.00000015 * t**4 + dT
	w  = 102 * 3600 + 56 * 60 + 14.45766 +       1161.24342 * t + 0.529265 * t**2 - 0.00011814 * t**3 + 0.000011379 * t**4 + dw

	D  = W1 - T + 180 * 3600
	F  = W1 - W3
	l  = W1 - W2
	lp = T  - w
	Z = W1 + (5029.0966 - 0.29965) * t
	funds = [D, F, l, lp, T, Z]

	LBR = [0, 0, 0]
	LBR1 = computeMain(main, t, funds)
	LBR2 = computePer(perturbations, t, plans, funds, n)
	p = (5029.0966 * t + 1.1120 * t**2 + 0.000077 * t**3 - 0.00002353 * t**4) - 0.29965 * t
	LBR[0] = W1 + LBR1[0] + LBR2[0] + p
	LBR[1] = LBR1[1] + LBR2[1]
	LBR[2] = (LBR1[2] + LBR2[2]) * 384747.961370173/384747.980674318
	return LBR

def moonLBR(JDE, n=30): # 默认截断，平均误差小于0.0001°
	L, B, R = computeMPP(JDE, n)
	T = (JDE - 2451545) / 36525
	dp, de, e = nutation(T)
	L = (L + dp) / 3600 % 360
	B /= 3600
	ra, dec = ec2eq(L, B, e)
	return L, B, R, ra, dec

def moonXYZ(JDE):
	T = (JDE - 2451545) / 36525
	P = 0.10180391e-4 * T + 0.47020439e-6 * T**2 - 0.5417367e-9 * T**3 - 0.2507948e-11 * T**4 + 0.463486e-14 * T**5
	Q = -0.113469002e-3 * T + 0.12372674e-6 * T**2 + 0.12654170e-8 * T**3 - 0.1371808e-11 * T**4 - 0.320334e-14 * T**5
	sq = math.sqrt(1 - P * P - Q * Q)
	p11 = 1 - 2 * P * P
	p12 = 2 * P * Q
	p13 = 2 * P * sq
	p21 = 2 * P * Q
	p22 = 1 - 2 * Q * Q
	p23 = -2 * Q * sq
	p31 = -2 * P * sq
	p32 = 2 * Q * sq
	p33 = 1 - 2 * P * P - 2 * Q * Q
	L, B, R = computeMPP(JDE, 1)
	L = L / 3600 / rad
	B = B / 3600 / rad
	x0 = R * math.cos(L) * math.cos(B)
	y0 = R * math.sin(L) * math.cos(B)
	z0 = R * math.cos(B)
	X = p11 * x0 + p12 * y0 + p13 * z0
	Y = p21 * x0 + p22 * y0 + p23 * z0
	Z = p31 * x0 + p32 * y0 + p33 * z0
	return X, Y, Z

