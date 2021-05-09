import math
from Data import *

def divide(dividend, divisor, f=0, r=False):  # divmod()
	quotient = dividend // divisor
	remainder = dividend % divisor
	if f: quotient %= f
	if r:   # 四舍五入
		if remainder >= round(quotient / 2): quotient += 1
		return quotient
	return int(quotient), int(remainder)

def qyfs(yfa, rf, n):  # 大余转为整数，n朔为1，1/2为望，1/4为上弦
	yfa *= n
	if yfa != int(yfa):  # 非整数
		dy = int(yfa // rf)
		xy = yfa % rf
	else: dy, xy = divide(yfa, rf)  # 小余是整数
	return dy, xy

def qy(dy1, xy1, rf, dy2, xy2, xf1=0, xf2=0, fm=1, n=1):  # 被加/减数，日法，加/减数，被加/减数小分，加/减数小分，分母，加/减次数
	zf = ((dy1 * rf + xy1) * fm + xf1) + ((dy2 * rf + xy2) * fm + xf2) * n
	xf = zf % fm
	zy = (zf - xf) // fm
	dy = int(zy // rf)
	xy = zy % rf
	if fm == 1: return dy % 60, xy + xf, xf
	else: return dy % 60, int(xy), xf

def dxyMul(dy1, xy1, rf1, dy2, xy2=0, rf2=1):   # 大小余相乘
	zf1 = dy1 * rf1 + xy1
	zf2 = dy2 * rf2 + xy2
	zf = zf1 * zf2
	rf = rf1 * rf2
	dy, xy = divide(zf, rf)
	return zf  # dy, xy, rf



def fsAdd(dy1, xy1, rf1, dy2, xy2, rf2, rf):
	tf = dy1 * rf1 * rf2 + xy1 * rf2 + dy2 * rf1 * rf2 + xy2 * rf1
	dy = tf // (rf1 * rf2)
	xy = tf % (rf1 * rf2) // (rf1*rf2//rf)
	return dy, xy


def dxyMod(zf1, rf1, zf2, rf2, ts=False):
	if rf1 == rf2:
		if ts is False: ts = 1
		rf2 *= ts
	dy, xy = divide((zf1 * rf2) % (zf2 * rf1), rf1 * rf2)
	xy, xf = divide(xy, rf1)
	if ts is not False:
		if rf2 == rf1 * ts:  # 倍数
			xy, xf = divide(xy, ts)
		else:  # 约数
			xf /= (rf1 / ts)
		return dy, xy, xf
	else: return dy, xy

def scrl(jy, sxdf, sxxf, ts, tongzhou, zhoufa):  # 朔差入历
	sxzf = (sxdf * ts + sxxf) * jy
	rlrf, rlrxf = divide(sxzf, ts)
	rlf = rlrf % tongzhou
	rlrs, rlry = divide(rlf, zhoufa)
	return rlrs, rlry, rlrxf

def jryf(jr, rf):  # 积日余分
	dy = int(jr % 60)  # 大余：整数部分
	xy = round(jr * rf) % rf  # 小余：小数部分 * 日法
	return dy % 60, xy

def epoch2tz(li, ydy, yxy, qdy, qxy, qxf):  # 月，气
	ydy, yxy = qy(ydy, yxy, li.srf, li.backYue * li.sdy, li.backYue * li.sxy)[:2]
	qdy, qxy, qxf = qy(qdy, qxy, li.qrf, li.qdy, li.qxy, qxf, li.qxf, li.qfm, li.backQi*2)
	li.yrs(yxy)
	if (qdy - ydy) % 60 >= li.yueri:  # 正月前有闰（未必该月即闰月），需加推一月
		x = li.backYue // abs(li.backYue)
		ydy, yxy = qy(ydy, yxy, li.srf, x * li.sdy, x * li.sxy)[:2]
	return ydy, yxy, qdy, qxy, qxf



