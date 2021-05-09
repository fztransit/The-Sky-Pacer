# VSOP87D的周期项计算，结果为Date点地心坐标的视黄经、视黄纬、距离
# 计算表达式：S += A * cos(B + Cτ)
# A为振幅，B为相位，C为频率，τ为儒略千年数
from Ephem import *
from BasicFunc.mathFunc import *


##########    VSOP87D（Date历元行星日心位置）    ##########
def computeVSOP(list, T, n=1): # n用于截取计算周期项，只能为正整数，默认1为不截取
   LBR = [0, 0, 0]
   for i in range(3): # L、B、R
     for j in range(len(list[i])): # number of series
         value = 0
         series = list[i][j]
         if j < 3: terms = len(series) // n
         else: terms = len(series)
         for k in range(terms):
             value += series[k][0] * math.cos(series[k][1] + series[k][2] * T)
         LBR[i] += value * T**j
   return LBR # L、B单位弧度，R单位AU

##########    太阳位置（地心坐标）    ##########
def sunLBR(JDE): # Date点地心太阳地球位置
   t = (JDE - 2451545) / 365250
   L, B, R = computeVSOP(earthVSOP87, t, 2)
   # 日心坐标系地球位置转为地心坐标系太阳位置
   L = (L * rad + 180) % 360   # 太阳地心几何黄经L，单位角度
   B = -(B * rad)  # 太阳地心几何黄纬B，单位角度
   dL, dB = FK5(L,B,t)  # FK5坐标修正值（单位：角度）
   dp, de, e = nutation(t*10)  # 获得黄经章动（单位：角秒）
   # 修正坐标、黄经章动、光行差
   L = (L + dL + (dp + (-20.4898 / R)) / 3600)  # 视黄经，单位角度
   B = (B + dB / 3600)  # 视黄纬，单位角度
   ra, dec = ec2eq(L, B, e)
   return L, B, R, ra, dec       # L,B单位角度，R单位AU

##########    行星视位置    ##########
def appCorrect(L,B,R, LBRearth, t): # 视位置修正（地球日心坐标和已计算光行时后的行星地心坐标）
   L, B, dt = sun2earth(L, B, R, LBRearth)  # 木星的地心坐标位置
   dL_abr, dB_abr = aberration(L, B, LBRearth[0], t)  # 光行差修正值
   L += dL_abr
   B += dB_abr
   dL_FK5, dB_FK5 = FK5(L, B, t)  # FK5坐标修正值（单位：角秒）
   L += dL_FK5
   B += dB_FK5
   dp, de, e = nutation(t*10)  # 获得黄经章动（单位：角秒）
   L += dp / 3600
   return L, B, R, e

def PlanetLBR(p, JDE, n=1):
   t = (JDE - 2451545) / 365250
   # 日心坐标行星位置（L, B单位弧度，R单位AU）
   L, B, R = computeVSOP(planetVSOP87[p], t, 20*n)
   # 转为地心坐标系行星位置
   LBRearth = computeVSOP(earthVSOP87, t, 3*n) # 获得地球日心坐标
   L, B, dt = sun2earth(L, B, R, LBRearth) # 获得光行时dt
   t -= dt/365250 # 计算t-dt时刻的行星位置
   n2 = {'水': 5, '金': 3, '火': 2, '木': 2, '土': 2}
   L, B, R = computeVSOP(planetVSOP87[p], t, n2[p]*n)
   L, B, R, e = appCorrect(L, B, R, LBRearth, t) # 视位置
   RA, Dec = ec2eq(L, B, e)
   return L, B, R, RA, Dec    # L, B单位角度，R单位AU

