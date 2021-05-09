# 坐标系转换（球面坐标单位为(rad,km)，直角坐标单位为km）
from BasicFunc.mathFunc import *

# Date点日心坐标转地心坐标
def sun2earth(L,B,R, earth): # star(L,B,R), earth(L0,B0,R0） 日心坐标行星与地球位置
	L0,B0,R0 = earth
	x = R*math.cos(B)*math.cos(L) - R0*math.cos(B0)*math.cos(L0)
	y = R*math.cos(B)*math.sin(L) - R0*math.cos(B0)*math.sin(L0)
	z = R*math.sin(B) - R0*math.sin(B0)
	lamda = math.atan2(y,x)  # tanλ = y / x
	beta = math.atan(z / math.sqrt(x**2+y**2)) # tanβ = z / sqrt(x²+y²)
	dt = 0.0057755183 * math.sqrt(x**2+y**2+z**2) # 光行时：距离÷光速（单位：日）
	return lamda*rad%360, beta*rad, dt # 单位：角度

def FK5(L,B,t): # 将地心黄道坐标(L,B)修正到FK5目视系统
	T = t * 10 # JDE儒略世纪数
	Lp = (L - 1.397 * T - 0.00031 * pow(T, 2)) / rad  # 单位弧度
	dL = -0.09033 + 0.03916 * (math.cos(Lp) + math.sin(Lp)) * math.tan(B / rad)  # 单位角秒
	dB = +0.03916 * (math.cos(Lp) - math.sin(Lp))  # 单位角秒
	return dL/3600, dB/3600 # FK5修正值（单位：角度）累加到L,B

# 赤道坐标转黄道坐标
def eq2ec(RA, Dec, e): # 赤经、赤纬、黄赤交角
	L = atan((sin(RA)*cos(e) + tan(Dec)*sin(e)) / cos(RA))
	L = atan2((sin(RA)*cos(e) + tan(Dec)*sin(e)), cos(RA))
	B = asin(sin(Dec)*cos(e) - cos(Dec)*sin(e)*sin(RA))
	return L % 360, B # 黄经、黄纬

# 黄道坐标转赤道坐标
def ec2eq(L, B, e): # 黄经、黄纬、黄赤交角
	RA = atan2((sin(L)*cos(e) - tan(B)*sin(e)), cos(L))
	Dec = asin(sin(B)*cos(e) + cos(B)*sin(e)*sin(L))
	return RA % 360, Dec # 赤经、赤纬

# 本地地平坐标
def eq2ho(H, phi, Dec): # 本地时角、地理纬度φ、赤纬
	A = atan2(sin(H), (cos(H)*sin(phi) - tan(Dec)*cos(phi)))
	h = asin(sin(phi)*sin(Dec) + cos(phi)*cos(Dec)*cos(H))
	return A, h # 方位角、地平纬度

# 地平坐标转赤道坐标
def ho2eq(A, phi, h): # 方位角、地理纬度φ、地平纬度
	H = atan2(sin(A) , (cos(A)*sin(phi) + tan(h)*cos(phi)))
	Dec = asin(sin(phi)*sin(h) - cos(phi)*cos(h)*cos(A))
	return H, Dec # 本地时角、赤纬

# 地平坐标系转时角坐标
def HourAngle(h, Dec, phi): # 地平纬度h，赤纬Dec，地理纬度phi
	cosH = mod((sin(h) - sin(phi) * sin(Dec)) / (cos(phi) * cos(Dec)), 2)
	# 边的余弦公式，sin(h)用于修正大气折射，若h=0，则cosH = -tgφtgδ，值为-1到1
	H = acos(cosH)
	return H