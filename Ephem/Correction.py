# 岁差、章动、视差、光行差等修正
from BasicFunc import *

def nutation(T):  # 儒略世纪数
	# 平距角（单位：弧度）
	D = ((1072260.70369 + 1602961601.2090 * T - 6.3706 * pow(T,2) + 0.006593 * pow(T,3) - 0.00003169 * pow(T,4)) / 3600.0) / rad
	# 月亮平近点角（单位：弧度）
	L = ((485868.249036 + 1717915923.2178 * T + 31.8792 * pow(T,2) + 0.051635 * pow(T,3) - 0.00024470 * pow(T,4)) / 3600.0) / rad
	# 太阳平近点角（单位：弧度）
	Lp = ((1287104.79305 + 129596581.0481 * T - 0.5532 * pow(T,2) + 0.000136 * pow(T,3) - 0.00001149 * pow(T,4)) / 3600.0) / rad
	# 月亮纬度参数（单位：弧度）
	F = ((335779.526232 + 1739527262.8478 * T - 12.7512 * pow(T,2) - 0.001037 * pow(T,3) + 0.00000417 * pow(T,4)) / 3600.0) / rad
	# 白道升交点平经度（单位：弧度）
	Om = ((450160.398036 - 6962890.5431 * T + 7.4722 * pow(T,2) + 0.007702 * pow(T,3) - 0.00005939 * pow(T,4)) / 3600.0) / rad
	terms = [   # 表达式：arg = m1*L  +  m2*Lp  +  m3*F  +  m4*D  +  m5*Om   单位：弧度
				# DeltaPsiTerm += (AA + BB * T) * sin(arg) + CC * cos(arg)
				# DeltaEpsTerm += (DD + EE * T) * cos(arg) + FF * sin(arg)
				# m1  m2  m3  m4  m5   AA    BB       CC      DD      EE   FF   (单位：10000000角秒）
				0, 0, 0, 0, 1, -172064161, -174666, 33386, 92052331, 9086, 15377,
				0, 0, 2, -2, 2, -13170906, -1675, -13696, 5730336, -3015, -4587,
				0, 0, 2, 0, 2, -2276413, -234, 2796, 978459, -485, 1374,
				0, 0, 0, 0, 2, 2074554, 207, -698, -897492, 470, -291,
				0, 1, 0, 0, 0, 1475877, -3633, 11817, 73871, -184, -1924,
				0, 1, 2, -2, 2, -516821, 1226, -524, 224386, -677, -174,
				1, 0, 0, 0, 0, 711159, 73, -872, -6750, 0, 358,
				0, 0, 2, 0, 1, -387298, -367, 380, 200728, 18, 318,
				1, 0, 2, 0, 2, -301461, -36, 816, 129025, -63, 367,
				0, -1, 2, -2, 2, 215829, -494, 111, -95929, 299, 132,

				0, 0, 2, -2, 1, 128227, 137, 181, -68982, -9, 39,
				-1, 0, 2, 0, 2, 123457, 11, 19, -53311, 32, -4,
				-1, 0, 0, 2, 0, 156994, 10, -168, -1235, 0, 82,
				1, 0, 0, 0, 1, 63110, 63, 27, -33228, 0, -9,
				-1, 0, 0, 0, 1, -57976, -63, -189, 31429, 0, -75,
				-1, 0, 2, 2, 2, -59641, -11, 149, 25543, -11, 66,
				1, 0, 2, 0, 1, -51613, -42, 129, 26366, 0, 78,
				-2, 0, 2, 0, 1, 45893, 50, 31, -24236, -10, 20,
				0, 0, 0, 2, 0, 63384, 11, -150, -1220, 0, 29,
				0, 0, 2, 2, 2, -38571, -1, 158, 16452, -11, 68,

				0, -2, 2, -2, 2, 32481, 0, 0, -13870, 0, 0,
				-2, 0, 0, 2, 0, -47722, 0, -18, 477, 0, -25,
				2, 0, 2, 0, 2, -31046, -1, 131, 13238, -11, 59,
				1, 0, 2, -2, 2, 28593, 0, -1, -12338, 10, -3,
				-1, 0, 2, 0, 1, 20441, 21, 10, -10758, 0, -3,
				2, 0, 0, 0, 0, 29243, 0, -74, -609, 0, 13,
				0, 0, 2, 0, 0, 25887, 0, -66, -550, 0, 11,
				0, 1, 0, 0, 1, -14053, -25, 79, 8551, -2, -45,
				-1, 0, 0, 2, 1, 15164, 10, 11, -8001, 0, -1,
				0, 2, 2, -2, 2, -15794, 72, -16, 6850, -42, -5,

				0, 0, -2, 2, 0, 21783, 0, 13, -167, 0, 13,
				1, 0, 0, -2, 1, -12873, -10, -37, 6953, 0, -14,
				0, -1, 0, 0, 1, -12654, 11, 63, 6415, 0, 26,
				-1, 0, 2, 2, 1, -10204, 0, 25, 5222, 0, 15,
				0, 2, 0, 0, 0, 16707, -85, -10, 168, -1, 10,
				1, 0, 2, 2, 2, -7691, 0, 44, 3268, 0, 19,
				-2, 0, 2, 0, 0, -11024, 0, -14, 104, 0, 2,
				0, 1, 2, 0, 2, 7566, -21, -11, -3250, 0, -5,
				0, 0, 2, 2, 1, -6637, -11, 25, 3353, 0, 14,
				0, -1, 2, 0, 2, -7141, 21, 8, 3070, 0, 4,

				0, 0, 0, 2, 1, -6302, -11, 2, 3272, 0, 4,
				1, 0, 2, -2, 1, 5800, 10, 2, -3045, 0, -1,
				2, 0, 2, -2, 2, 6443, 0, -7, -2768, 0, -4,
				-2, 0, 0, 2, 1, -5774, -11, -15, 3041, 0, -5,
				2, 0, 2, 0, 1, -5350, 0, 21, 2695, 0, 12,
				0, -1, 2, -2, 1, -4752, -11, -3, 2719, 0, -3,
				0, 0, 0, -2, 1, -4940, -11, -21, 2720, 0, -9,
				-1, -1, 0, 2, 0, 7350, 0, -8, -51, 0, 4,
				2, 0, 0, -2, 1, 4065, 0, 6, -2206, 0, 1,
				1, 0, 0, 2, 0, 6579, 0, -24, -199, 0, 2,

				0, 1, 2, -2, 1, 3579, 0, 5, -1900, 0, 1,
				1, -1, 0, 0, 0, 4725, 0, -6, -41, 0, 3,
				-2, 0, 2, 0, 2, -3075, 0, -2, 1313, 0, -1,
				3, 0, 2, 0, 2, -2904, 0, 15, 1233, 0, 7,
				0, -1, 0, 2, 0, 4348, 0, -10, -81, 0, 2,
				1, -1, 2, 0, 2, -2878, 0, 8, 1232, 0, 4,
				0, 0, 0, 1, 0, -4230, 0, 5, -20, 0, -2,
				-1, -1, 2, 2, 2, -2819, 0, 7, 1207, 0, 3,
				-1, 0, 2, 0, 0, -4056, 0, 5, 40, 0, -2,
				0, -1, 2, 2, 2, -2647, 0, 11, 1129, 0, 5,

				-2, 0, 0, 0, 1, -2294, 0, -10, 1266, 0, -4,
				1, 1, 2, 0, 2, 2481, 0, -7, -1062, 0, -3,
				2, 0, 0, 0, 1, 2179, 0, -2, -1129, 0, -2,
				-1, 1, 0, 1, 0, 3276, 0, 1, -9, 0, 0,
				1, 1, 0, 0, 0, -3389, 0, 5, 35, 0, -2,
				1, 0, 2, 0, 0, 3339, 0, -13, -107, 0, 1,
				-1, 0, 2, -2, 1, -1987, 0, -6, 1073, 0, -2,
				1, 0, 0, 0, 2, -1981, 0, 0, 854, 0, 0,
				-1, 0, 0, 1, 0, 4026, 0, -353, -553, 0, -139,
				0, 0, 2, 1, 2, 1660, 0, -5, -710, 0, -2,

				-1, 0, 2, 4, 2, -1521, 0, 9, 647, 0, 4,
				-1, 1, 0, 1, 1, 1314, 0, 0, -700, 0, 0,
				0, -2, 2, -2, 1, -1283, 0, 0, 672, 0, 0,
				1, 0, 2, 2, 1, -1331, 0, 8, 663, 0, 4,
				-2, 0, 2, 2, 2, 1383, 0, -2, -594, 0, -2,
				-1, 0, 0, 0, 2, 1405, 0, 4, -610, 0, 2,
				1, 1, 2, -2, 2, 1290, 0, 0, -556, 0, 0	]
	i = 0
	dp = 0
	de = 0
	while i < 77 * 11:
		arg = terms[i]*L + terms[i+1]*Lp + terms[i+2]*F + terms[i+3]*D + terms[i+4]*Om
		dp += (terms[i+5] + terms[i+6]*T) * math.sin(arg) + terms[i+7] * math.cos(arg)   # 黄经章动
		de += (terms[i+8] + terms[i+9]*T) * math.cos(arg) + terms[i+10] * math.sin(arg)  # 交角章动
		i += 11
	dp /= 10000000 # Delta PSi 单位：角秒
	de /= 10000000 # Delta Epsilon 单位：角秒
	# 黄赤交角修正
	U = T / 100
	e0 = 23 * 3600 + 26 * 60 + 21.448 - 4680.93 * U - 1.55 * pow(U, 2) + 1999.25 * pow(U, 3) - 51.38 * pow(U, 4) - 249.67 * pow(U, 5) - 39.05 * pow(U, 6) + 7.12 * pow(U, 7) + 27.87 * pow(U, 8) + 5.79 * pow(U, 9) + 2.45 * pow(U, 10)
	e = e0 + de # 黄赤交角，单位角秒
	return dp, de, e / 3600  # 黄经章动、交角章动（单位角秒），e单位度数


def nut_eq(ra, dec, T): # 赤经赤纬（角度）
	dp, de, e = nutation(T)
	nut_ra = (cos(e) + sin(e)*sin(ra)*tan(dec)) * dp - cos(ra)*tan(dec)*de
	nut_dec = sin(e)*cos(ra)*dp + sin(ra)*de
	return nut_ra, nut_dec, e # 赤经赤纬方向的章动


# PO3模型岁差
PO3 = { 'phi': [0, 5038.481507, -1.0790069, -0.00114045, +0.000132851, -9.51e-8],
		'w': [84381.406000, -0.025754, +0.0512623, -0.00772503, -4.67e-7, +3.337e-7],
		'P': [0, 4.199094, +0.1939873, -0.00022466, -9.12e-7, +1.20e-8],
		'Q': [0, -46.811015, +0.0510283, +0.00052413, -6.46e-7, -1.72e-8],
		'E': [84381.406000, -46.836769, -0.0001831, +0.00200340, -5.76e-7, -4.34e-8],
		'x': [0, 10.556403, -2.3814292, -0.00121197, +0.000170663, -5.60e-8],
		'pi': [0, 46.998973, -0.0334926, -0.00012559, +1.13e-7, -2.2e-9],
		'II': [629546.7936, -867.95758, +0.157992, -0.0005371, -0.00004797, +7.2e-8],
		'p': [0, 5028.796195, +1.1054348, +0.00007964, -0.000023857, +3.83e-8],
		'theta': [0, 2004.191903, -0.4294934, -0.04182264, -7.089e-6, -1.274e-7],
		'zeta': [2.650545, 2306.083227, +0.2988499, +0.01801828, -5.971e-6, -3.173e-7],
		'z': [-2.650545, 2306.077181, +1.0927348, +0.01826837, -0.000028596, -2.904e-7], }

def precessionArgs(name, T):
	arg = 0
	for i in range(len(PO3[name])):
		arg += PO3[name][i] * pow(T, i)
	return arg / 3600


# 行星光行差
def aberration(L,B,L0,T): # 行星地心坐标几何黄经黄纬、地球日心坐标几何黄经、儒略千年数
	T = T * 10 # 儒略世纪数
	L0 = L0 + 180/rad # 太阳地心坐标几何黄经（单位：角度转弧度）
	L /= rad
	B /= rad
	e = 0.016708617 - 0.000042037 * T - 0.0000001236 * pow(T, 2)  # 地球轨道离心率
	pi = (102.93735 + 1.71953*T + 0.00046*T**2) / rad  # 轨道近日点经度（单位：角度转弧度）
	k = 20.49552
	dL = (-k*math.cos(L0-L) + e*k*math.cos(pi-L)) / math.cos(B) # 黄经光行差（单位：角秒）
	dB = -k * math.sin(B) * (math.sin(L0-L) - e*math.sin(pi-L)) # 黄纬光行差（单位：角秒）
	return dL/3600, dB/3600 # 光行差修正值（单位：角度）累加到L,B

# 恒星光行差
def Aberration2(eps, star, T): # 赤经赤纬的光行差（黄赤交角ε、恒星数据项、儒略世纪数）
	L = (computeVSOP(earthVSOP87, T/10, 100)[0] * rad + 180) % 360 # Date点的太阳地心坐标几何黄经（单位：角度）
	e = 0.016708617 - 0.000042037 * T - 0.0000001236 * pow(T, 2)  # 地球轨道离心率
	pi = 102.93735 + 1.71953*T + 0.00046*T**2  # 轨道近日点经度（单位：角度）
	k = 20.49552 # 光行差常数
	abr_ra = -k * (cos(star.ra)*cos(L)*cos(eps) + sin(star.ra)*sin(L)) / cos(star.dec) + e*k * (cos(star.ra)*cos(pi)*cos(eps) + sin(star.ra)*sin(pi)) / cos(star.dec)
	abr_dec = -k * (cos(L)*cos(eps) * (tan(eps)*cos(star.dec)-sin(star.ra)*sin(star.dec)) + cos(star.ra)*sin(star.dec)*sin(L)) + e*k * (cos(pi)*cos(eps) * (tan(eps)*cos(star.dec)-sin(star.ra)*sin(star.dec)) + cos(star.ra)*sin(star.dec)*sin(pi))
	return abr_ra/3600, abr_dec/3600 # 光行差修正值（单位：角度）