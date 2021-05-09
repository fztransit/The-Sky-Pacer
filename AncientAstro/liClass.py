from Data import *
from AncientAstro.liCalc import *


class Li:
	def __init__(self, name, liyuan, yfa, srf, sz, qrf):  # 所有历法的共有属性（历名，历元，朔策(yfa/srf)，气策(sz/bf)）
		self.lm = name
		self.ly = liyuan
		if yfa < srf: self.yfa = yfa + 29 * srf  # 只给出余分
		else: self.yfa = yfa
		self.srf = srf  # 朔旦日法
		self.yue = self.yfa / self.srf
		self.sdy, self.sxy = divide(self.yfa, self.srf)
		if sz < qrf: self.sz = sz + 365 * qrf
		else: self.sz = sz
		self.qrf = qrf
		self.sui = self.sz / self.qrf
		self.qdy, self.qxy = divide(self.sz / 24, self.qrf)


	def bjsgz(self, bf):
		self.bsgzc = round(self.sui * bf % 60)  # 蔀/纪首干支差
		bs = 60 // math.gcd(self.bsgzc, 60)  # int(self.bsgzc * 60 / math.gcd(self.bsgzc, 60) / self.bsgzc)
		jf = bs * bf  # 甲子夜半朔旦冬至，四分历为纪法，非四分历即元法
		self.bsgz = [0] * bs  # 蔀/纪首干支序
		for i in range(bs):
			self.bsgz[i] = (i * self.bsgzc + self.lyrgz) % 60
		return jf

	def yrs(self, yxy):  # 判断大小月
		if yxy < self.srf - self.sxy:
			self.yueri = 29
			return 29
		else:
			self.yueri = 30
			return 30

	def wzqy(self, ydy_0, yxy_0, qdy_0, qxy_0, qxf_0, thisYue=True):  # 判断本月是否为无中气月（本月气大小余、朔大小余），无节气月亦适用
		if thisYue: ydy, yxy = qy(ydy_0, yxy_0, self.srf, self.sdy, self.sxy)[:2]
		else: ydy, yxy = ydy_0, yxy_0  # 输入即次月大小余
		qdy, qxy, qxf = qy(qdy_0, qxy_0, self.qrf, self.qdy, self.qxy, qxf_0, self.qxf, self.qfm, 2)
		self.yrs(yxy)
		if (qdy - ydy) % 60 >= self.yueri:  # 本月应有之中气在次月
			return '闰', ydy, yxy, qdy_0, qxy_0, qxf_0  # 有闰返回下月朔及本月中气
		else:
			return '', ydy, yxy, qdy, qxy, qxf  # 无闰返回下月朔及下月中气


class Sfl(Li):
	type = 1  # 第一类：四分历
	yfa = 27759
	srf = 940
	bf = 76
	sz = 1461
	qrf = 4
	df = 32
	zs = 19
	zr = 7
	jys = 605
	qfm = 1
	qxf = 0

	def __init__(self, name, liyuan, **kwargs):
		self.sz *= (self.df / self.qrf)
		self.qrf = self.df
		Li.__init__(self, name, liyuan, self.yfa, self.srf, self.sz, self.qrf)
		try: self.lyjzss = kwargs['lyjzss']
		except: self.lyjzss = ['冬至','子','子']
		self.basicData(kwargs)
		self.zhangqi()
		self.jf = self.bjsgz(self.bf)
		self.yf = self.jf * 60 // math.gcd(self.jf, 60)  # 元法（岁复甲子）

	def zhangqi(self):
		self.zqi = self.sui / 12
		self.zq = self.zs * 12 	    # 章气=章岁*12
		self.zy = self.zq + self.zr  # 章月=章气+章闰=章岁*12+章闰

	def basicData(self, kwargs):
		# 可能存在的参数，不存在赋默认值
		self.qly = jieqi.index(self.lyjzss[0])
		self.jian = dizhi.index(self.lyjzss[1])
		self.suis = dizhi.index(self.lyjzss[2])
		if 6 < self.suis < 12: self.suis -= 12
		try: self.lyrgz = gz.index(kwargs['lyrgz'])
		except: self.lyrgz = 0
		try:
			self.bsry = kwargs['bsry']
			self.lyry = True  # 有闰余，历元不正
		except:
			self.bsry = 0
			self.lyry = False
		try: self.bm = kwargs['bm']
		except: self.bm = ['蔀']  # 无蔀/纪名

	def array(self, rank):  # 根据历元岁首建正判定默认排表序
		# 建表用数据（修改岁首月确定排表用的每年第一个月）
		if rank == -1: self.ssy = self.suis if self.suis < 0 else 0     # 冬至和岁首的最小值
		elif rank == 0: self.ssy = 0                                    # 冬至起排
		elif rank == 1: self.ssy = self.suis                            # 从岁首起排
		elif rank == 2: self.ssy = self.suis if self.suis > 0 else 0    # 冬至和岁首的最大值
		if self.qly % 2 == 1:  # 节气为历元，而岁首为中气，需转换
			self.bsry = (((self.zqi/2) / self.yue * 228) - self.zr * ((self.qly+1) / 2 - self.ssy)) / 12
			# 省为self.bsry = (121 - self.zr * (self.qly / 2 - self.ssy)) / 12，单位：月
		self.backYue = self.ssy - (self.qly + 1) // 2
		self.backQi = self.ssy - self.qly / 2
		self.jzy = self.jian - self.ssy  # 建正所在的月

	def dygz(self, dy):  # 由蔀首开始求的大余转为干支需加上蔀首干支序
		if dy is None: return ' 无 '
		if self.type > 2: gzdy = dy
		else: gzdy = dy + self.bsgz[self.rbs]
		return gz[gzdy % 60]

	def getSyjn(self, year):  # 算外
		self.sy = self.ly - self.jys * self.yf  # 上元
		jn = year - self.sy
		if year > 0: jn -= 1  # 实际为jn-=1; if year<0,jn+=1
		return jn


class Psl(Sfl, Li):
	type = 2  # 第二类：使用平朔平气法的历

	def __init__(self, name, liyuan, yfa, srf, sz, qrf, zhang, **kwargs):
		Li.__init__(self, name, liyuan, yfa, srf, sz, qrf)  # 指定父类的构造函数
		try:
			self.qrf = kwargs['df']  # 度法，纪法约/倍数
			self.sz = int(self.sz * self.qrf / qrf)
		except: pass
		if self.sz / 24 != self.sz // 24:
			self.qfm = 24
			self.qxf = int(self.sz - self.sz//24*24)
		else:
			self.qfm, self.qxf = 1, 0
		self.qdy, self.qxy = divide(self.sz / 24, self.qrf)
		self.zs, self.zr = zhang
		self.zhangqi()
		try: self.lyjzss = kwargs['lyjzss']
		except: self.lyjzss = ['冬至','寅','寅']
		try: self.jf = kwargs['jf']  # 纪法（夜半朔旦冬至）
		except: self.jf = qrf
		self.bf = qrf  # 非计算日法
		self.basicData(kwargs)
		self.yf = self.bjsgz(self.bf)  # 元法（甲子夜半朔旦冬至）
		try: self.jys = kwargs['jys']
		except: self.jys = 0  # 无上元


class Psl2(Psl, Li):  # 丢失定朔数据的定朔历（破章法）
	type = 3

	def __init__(self, name, liyuan, yfa, zongfa, sz, **kwargs):
		Li.__init__(self, name, liyuan, yfa, zongfa, sz, zongfa)  # 指定父类的构造函数
		self.sy = liyuan
		self.sui = self.sz / self.qrf
		self.qice = self.sz / 24
		if self.sz / 24 != self.sz // 24:
			self.qfm = 24
			self.qxf = int(self.sz - self.sz//24*24)
		else:
			self.qfm, self.qxf = 1, 0
		try: self.lyjzss = kwargs['lyjzss']
		except: self.lyjzss = ['冬至','寅','子']
		self.basicData(kwargs)
		self.yf = 0  # 无元法
		try: self.jys = kwargs['jys']
		except: self.jys = 0  # 无上元


import xlwt
wb = xlwt.Workbook(encoding = 'utf-8')
ws = wb.add_sheet('Sheet1', cell_overwrite_ok=True)
wb1 = xlwt.Workbook(encoding = 'utf-8')
wd = wb1.add_sheet('Sheet2', cell_overwrite_ok=True)


class Dsl(Psl):
	type = 4  # 第三类：使用定朔平气法的历

	def __init__(self, name, liyuan, yfa, srf, sz, bufa, zhang, zhoufa, zryu, **kwargs):
		super(Dsl, self).__init__(name, liyuan, yfa, srf, sz, bufa, zhang, **kwargs)  # 无需指定父类，当有多重继承关系时也只初始化一次
		self.qice = self.sz / 24
		self.zhoufa = zhoufa
		self.zryu = zryu
		try: self.zt = kwargs['zt']
		except: self.zt = self.sz
		self.tongzhou = zhoufa * 27 + zryu
		self.jdy = 27 + zryu / zhoufa
		self.zhangqi()
		self.ypxf = self.zy + self.zs  # 月平行分
		if self.lm in rcb: self.rcb_args()  # 生成日躔表其他参数
		if self.lm in ylb: self.ylb_args()  # 生成月离表其他参数

	def rcb_args(self):
		self.r_syl = rcb[self.lm][0]  # 盈缩分（损益率）
		self.r_ysjf = [0]
		for j in range(1, 24):
			self.r_ysjf.append(self.r_ysjf[j-1] + rcb[self.lm][0][j-1])

	def ylb_args(self):  # 月行迟疾历相关数据，计算用值，非表值
		ysxf = []
		self.y_syl = []  # 损益率
		self.y_ysjf = [0]  # 月盈缩积分
		self.xc = []   # 行差：相邻两日月实行差
		self.cf = []  # 差法：月日相对速度
		self.ts = ylb[self.lm][1]['ts'] if 'ts' in ylb[self.lm][1] else 1  # 小分分母
		a = ylb[self.lm][1]['a'] if 'a' in ylb[self.lm][1] else 1
		b = ylb[self.lm][1]['b'] if 'b' in ylb[self.lm][1] else 1
		c = ylb[self.lm][1]['c'] if 'c' in ylb[self.lm][1] else 1
		l = ylb[self.lm][1]['l'] if 'l' in ylb[self.lm][1] else 1
		d0 = 0

		for i in range(28):
			ysxf.append(a * ylb[self.lm][0][i])
			self.y_syl.append(round((ysxf[i] - self.ypxf) * l))
			if i != 0:
				if self.lm == '大明历':
					ypxf = (self.zt / self.bf / self.yfa * self.srf + 1) * self.zs
					d = round((ypxf - self.ypxf) * self.srf * i) - d0
					d0 += d
					self.y_ysjf.append(self.y_ysjf[i-1] + (ysxf[i-1] - self.ypxf) * self.srf - d)
				else:
					self.y_ysjf.append(self.y_ysjf[i - 1] + round((ysxf[i-1] - self.ypxf) * b))
					if 'd' in ylb[self.lm][1]:
						self.y_ysjf[i] += ylb[self.lm][1]['d'][i-1]
					if i == 27:  # 周日损益率及月实行小分
						self.zrxf = round((round(abs(self.y_ysjf[i]) / b) * l * self.zhoufa - round(abs(self.y_syl[i]) * self.zryu)))
			self.xc.append(ylb[self.lm][0][(i+1)%28] - ylb[self.lm][0][i])
			self.cf.append(c * (ysxf[i] - self.zs))


class Dsl2(Psl2):
	type = 5  # 破章法、总法、进朔法

	def __init__(self, name, liyuan, yfa, zongfa, sz, tongzhou, qifa, zhuanfa, **kwargs):
		Psl2.__init__(self, name, liyuan, yfa, zongfa, sz)  # 指定父类的构造函数

		self.tongzhou = tongzhou
		zhoufa = qifa * zongfa
		self.zryu = tongzhou % zhoufa
		self.jdy = tongzhou / zhoufa
		self.zhoufa = self.srf = self.qrf = zongfa
		# self.qdy, self.qxy = divide((self.sz - self.qxf//2) / 12, self.qrf)
		self.zhuanfa = zhuanfa
		try:
			sc = kwargs['sc']
			self.zt = self.sz + sc
			self.ypxd = self.zt / self.yfa + 1
		except:
			self.ypxd = self.sz / self.yfa + 1
			self.zt = self.sz
		self.ypxf = self.ypxd * zhuanfa
		self.ts = qifa
		self.rcb_args()
		self.ylb_args()

	def rcb_args(self):
		self.ysf = rcb[self.lm][0]  # 盈缩分（日实行分－日平行分）
		self.xhs = [0]
		self.r_syl = []  # 陟降率
		self.r_ysjf = [0]

		d = rcb[self.lm][1]['d'] if 'd' in rcb[self.lm][1] else 1
		l = rcb[self.lm][1]['l'] if 'l' in rcb[self.lm][1] else 1
		if 'p' in rcb[self.lm][1]: self.ypxd = rcb[self.lm][1]['p']

		for j in range(24):
			self.r_syl.append(round(self.ysf[j] / self.ypxd * l))
			if j != 0:
				self.xhs.append(self.xhs[j-1] + rcb[self.lm][0][j-1])
				self.r_ysjf.append(self.r_ysjf[j-1] + self.r_syl[j-1])


	def ylb_args(self):  # 月行迟疾历相关数据，计算用值，非表值
		ysxf = []
		self.y_syl = []  # 损益率（6、13、20、27皆为无效值）
		self.y_ysjf = [0]  # 月盈缩积分
		self.xc = []  # 行差：相邻两日月实行差
		self.zjd = ['0']

		a = ylb[self.lm][1]['a'] if 'a' in ylb[self.lm][1] else 1
		b = ylb[self.lm][1]['b'] if 'b' in ylb[self.lm][1] else 1
		l = ylb[self.lm][1]['l'] if 'l' in ylb[self.lm][1] else 1
		cm = ylb[self.lm][1]['cm'] if 'cm' in ylb[self.lm][1] else {}
		if 'p' in ylb[self.lm][1]: self.ypxf = ylb[self.lm][1]['p']

		if self.lm in ['大衍历', '崇玄历']: ysxf = ylb[self.lm][0]
		if self.lm in ['大衍历', '宣明历']: zjf = 0

		for i in range(28):
			if self.lm not in ['大衍历', '崇玄历']: ysxf.append(a * ylb[self.lm][0][i])
			if self.lm == '皇极历':
				self.y_syl.append(int((ysxf[i] - self.ypxf) * l) + ylb[self.lm][1]['dl'][i])
			elif self.lm in ['大衍历', '崇玄历'] and (6 <= i <= 13 or 20 <= i <= 27):
				if 6 <= i < 13: x = i+1
				if 20 <= i < 27: x = i+1
				if i in [6, 20]:
					if self.lm in ['崇玄历']:
						self.y_syl.append(ylb[self.lm][1]['cm'][i])
					else:
						syl1 = round((ysxf[i] - self.ypxf) / self.ypxf * self.srf)
						syl2 = round((ysxf[x] - self.ypxf) / self.ypxf * self.srf)
						self.y_syl.append([syl1, syl2])
				elif i in [13, 27]: self.y_syl.append(ylb[self.lm][1]['cm'][i])
				else:
					self.y_syl.append(round((ysxf[x] - self.ypxf) / self.ypxf * self.srf))
			else:
				syl = round((ysxf[i] - self.ypxf) / self.ypxf * self.srf)
				if i in [6, 13, 20, 27]:
					if len(cm) > 0:
						syl = cm[i+1]
					else:  # 线性插值
						if self.lm == '宣明历': n = ((i % 14) + 1) // 7
						else: n = (i + 1) // 7
						m = -1 if i in [6, 20] else 1
						syl = [round(syl * (9-n) / 9), round(syl * n / 9) * m]
				self.y_syl.append(syl)
			if 'd0' in ylb[self.lm][1] and i not in [6, 13, 20, 27]:
				self.y_syl[i] += ylb[self.lm][1]['d0'][i]
			if i != 0:
				if i in [7, 14, 21]:
					if self.lm == '宣明历' and i == 14: syl1 = self.y_syl[i - 1][0]
					else: syl1 = self.y_syl[i - 1][0] + self.y_syl[i - 1][1]
				else: syl1 = self.y_syl[i - 1]
				self.y_ysjf.append(self.y_ysjf[i - 1] + int(syl1 * b))
				if 'd' in ylb[self.lm][1]:
					self.y_ysjf[i] += ylb[self.lm][1]['d'][i - 1]
				if self.lm in ['大衍历', '宣明历']:
					zjf += ysxf[i-1]
					zjd, zf = divide(zjf, self.zhuanfa)
					self.zjd.append(str(zjd)+'°'+str(zf))
			self.xc.append(ylb[self.lm][0][(i + 1) % 28] - ylb[self.lm][0][(i) % 28])


