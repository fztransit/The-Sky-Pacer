from BasicFunc import *
from AstroCalc import *
from AncientAstro import *
import re
import time

def era2year(ui):
	eraname = ui.txtLyear.text()
	for i in range(len(eranames)):  # len(dynasties)
		if eraname in eranames[i]:
			ui.txtLyear.setText(str(-841+i))
			break

def YearConvert(ui):  # 纪年转换
	if ui.txtEditYear.text() == '':  # 无输入或不在范围内
		ui.edit.append("输入“年限/年份/朝代/帝王/年号”获得年号表\n或输入“朝代*”获取在位时间表\n输入“朝代/帝王/年号”自动跳出相关年号可选择查找\n")
		return 0
	try:  # 判断输入值是否为整数
		if '*' in ui.txtEditYear.text():
			s = ui.txtEditYear.text().split('*')
			lower = int(s[0])
			upper = int(s[1])
			year = lower  # 查找的首年
			if lower > upper: ui.edit.append('输入错误，*号左侧应为年代下限，右侧为上限')
		else:
			year = eval(ui.txtEditYear.text())  # 获得输入
			upper = year
		if year == upper == 0: ui.edit.append("不存在公元0年，请重新输入")
		while year <= upper:
			eraname = eranameSearch(ui, year)
			eraname = eraname.split('、')
			for i in range(len(eraname)):
				if year == 0: continue
				if i == 0: ui.edit.append(gyjnFormat(year) + eraname[i])
				else: ui.edit.append('\t\t' + eraname[i])
			year += 1
	except: # 王公纪年转公元纪年
		for i in range(len(dynasties)):  # 朝代
			if ui.txtEditYear.text()[:-1] in dynasties[i][0] and ui.txtEditYear.text()[-1] == '*':  # 只输入朝代，给出朝代信息
				if dynasties[i][0] in ['周', '鲁']:
					ui.edit.append('\t{}：? - {}'.format(dynasties[i][0], gyjnBC(dynasties[i][2])))
				elif dynasties[i][0] == '秦':
					ui.edit.append('\t秦：BC221 - BC206，凡15年')
				elif dynasties[i][0] == '汉':  # 跨不存在的公元0年
					ui.edit.append('\t{}：{} - {}，凡{}年'.format(dynasties[i][0], gyjnBC(dynasties[i][1]), dynasties[i][2], dynasties[i][2]-(dynasties[i][1])))
				#elif dynasties[i][0] == '清':  # 从入关算起
				#	ui.edit.append('{}：1644 - {}，凡268年\n'.format(dynasties[i][0], dynasties[i][-1]))
				else:
					ui.edit.append('\t{}：{} - {}，凡{}年'.format(dynasties[i][0], gyjnBC(dynasties[i][1]+snb[i]), gyjnBC(dynasties[i][2]), dynasties[i][2]-(dynasties[i][1]+snb[i])+1))
				firstYear = dynasties[i][1]
				for j in range(len(dynasties[i][3])):  # 王号
					mark = dynasties[i][5][j][0]
					if j != 0:
						firstYear = firstYear + duration
						if isinstance(mark, str) and int(mark) > 0: firstYear -= 1
					duration = 0
					if i > 2 and j == 0:
						firstYear += snb[i]
						duration = -snb[i]
					idx = 0  # 年号年数索引
					for k in range(len(dynasties[i][4][j])):  # 年号
						if isinstance(dynasties[i][5][j][k+idx], str):  # 有字符串标记
							idx += 1
							mark = int(dynasties[i][5][j][k+idx-1])
							if mark == 0:  # 继用年号，已用年数从前王末年中取
								duration += dynasties[i][5][j][k+idx] - dynasties[i][5][j-1][-1]
							elif mark < 0:  # 次年改元且指定已用年数
								duration += dynasties[i][5][j][k+idx] + mark - 1
							else:  # 同年改元
								if k == 0:
									duration = dynasties[i][5][j][k+idx] - mark + 1
								else:
									duration += dynasties[i][5][j][k+idx] - mark
						else:
							duration += dynasties[i][5][j][k+idx]
					if firstYear == 0: firstYear += 1
					lastYear = firstYear + duration-1
					ui.edit.append('{0:{4}<8}{1:>5} - {2:<5}\t凡{3:2}年'.format(
						dynasties[i][0]+dynasties[i][3][j], gyjnBC(firstYear), gyjnBC(lastYear), duration, chr(12288)))
				try: ui.edit.append('    用历【' + lclf[dynasties[i][0]] + '】')  # getLCLF(2, dynasties[i][0])
				except: ui.edit.insertPlainText('')  # 无数据
		for i in range(len(eranames)): # 遍历查找
			if ui.txtEditYear.text() in eranames[i]:
				eraname = eranames[i].split('、')
				for j in range(len(eraname)):
					if j == 0: ui.edit.append(gyjnFormat(-841+i) + eraname[j])
					else:
						ui.edit.append('\t\t' + eraname[j])
	ui.edit.append('')

def YearGZ(ui):  # 年份干支转换
	try:
		if '*' not in ui.txtEditYear.text():  # 求年干支
			nian = int(ui.txtEditYear.text())
			if nian == 0:
				ui.edit.append("不存在公元0年\n公元元年为辛酉年\n")
			else:
				if nian < 0:
					ui.edit.append(gyjn(nian) + ' 干支为：' + gz[(nian - 3) % 60] + '\n')
				else:
					ui.edit.append(gyjn(nian) + ' 干支为：' + gz[(nian - 4) % 60] + '\n')
		else:  # 输出干支表
			s = ui.txtEditYear.text().split('*')
			lower = int(s[0])
			upper = int(s[1])
			Y = []
			year = lower  # 查找的首年
			ui.edit.append(gyjn(lower) + ' 到 ' + gyjn(upper) + ' 的干支表：')
			while year <= upper:
				if year == 0: year += 1
				Y.append('{:>4}'.format(year) + ' ' + ganzhiYear(year))
				year += 1
			for i in range(len(Y)//4+1): # 行数
				ui.edit.append('')
				for j in range(4): # 列数
					if i * 4 + j >= len(Y): break
					ui.edit.insertPlainText(" " + Y[i * 4 + j] + "  ")
	except:
		ui.edit.append('输入年份或年限，生成干支表')
	ui.edit.append('')

def JDconvert(ui): # 日期转换
	try:
		JD = float(ui.txtEditDate.text())
		date = JD2date(JD)
		ui.edit.append('儒略日' + ui.txtEditDate.text() + '为公历：\n    UT+0:00：' + date)
		date = JD2date(JD + 8/24)
		ui.edit.append('    UT+8:00：' + date + '  干支' + ganzhiJD(JD, 8) + '\n')
	except: # 公历转儒略日
		try:
			JD = date2JD(ui.txtEditDate.text())
			MJD = ''
			if JD > 2400000.5:
				MJD = '\t简化儒略日：' + str(int(JD-2400000.5))
			ui.edit.append(ui.txtEditDate.text() + '\n    为儒略日：' + str(JD)+ '\t干支' + ganzhiJD(JD, 8)
			               + '\n    JDN：' + str(JDN(JD)) + MJD + '\n')
		except: # 不支持非日期格式的输入
			ui.edit.append('输入儒略日转公历或输入公历转儒略日。\n')

def DateCalc(ui):
	try:
		try:
			date1, date2 = ui.txtEditDate.text().split('+')
			flag = 0
		except:
			date1, date2 = ui.txtEditDate.text().split('*')
			flag = 1
		try:  # 日期 ± 某值
			try: date1 = JD2date(int(date1))
			except: pass
			if flag == 0: difference = date2JD(date1) + float(date2)
			else: difference = date2JD(date1) - float(date2)
			date = JD2date(difference)
			rgz1 = ganzhiDate(date1)
			rgz2 = ganzhiJD(difference)
			qh = ['后', '前']
			ui.edit.append(date1 + rgz1 + '（不含）的' + date2 + '日' + qh[flag] + '为：' + date[:-9] + ' ' + rgz2 + '\n')
		except:  # 日期差
			if flag == 1:
				difference = dateDiffer(date2JD(date1), date2JD(date2))
				qh = '(含) 后第 ' if difference >= 0 else '(含) 前第 '
				ui.edit.append(date1 + '(不含) 在' + date2 + qh + str(abs(difference)) + ' 日\n')
			else:
				ui.edit.append('只计算日期差，没有日期和\n')
	except:
		ui.edit.append('本项计算日期与日期或日期与某数值相加减\n以*代替减号，以区别日期格式或表示公元前的负号\n'
		               '计算两个日期相减，如：date1*date2\n计算某日期前后某日，如：date+某数，或date*某数\n')

def dayConvert(ui):
	if '*' in ui.txtEditDate.text() or '+' in ui.txtEditDate.text(): DateCalc(ui)
	else:
		try:
			float(ui.txtEditDate.text())
			JDconvert(ui)
		except:
			try:
				date2JD(ui.txtEditDate.text())
				JDconvert(ui)
			except:
				ui.edit.append('输入错误，请重新输入。\n')

def SiderealTime(ui):
	try:
		diqu, long, lat = GetGeoCoord(ui)
		JD = date2JD(ui.txtEditTime.text()) - long / 360
		st = jd2st(JD)
		hms = day2hms((st + long) / 360)
		if long < 0:
			ui.edit.append('西经' + str(round(-long, 1)) + '度 平太阳时：' + JD2date(JD) + '\n\t地方真恒星时为：' + hms + '\n')
		else:
			ui.edit.append('东经' + str(round(long, 1)) + '度 平太阳时：' + JD2date(JD) + '\n\t地方真恒星时为：' + hms + '\n')
	except:
		ui.edit.append("请确认时间或地点输入正确\n")

def SolarTime(ui, flag):
	try:
		JD = date2JD(ui.txtEditTime.text())
		dt = deltaT(JD)
		E = EquationTime(JD + dt/86400) / 360
		ui.edit.append(JD2date(JD))
		if flag:  # 平转真
			JD += E
			ui.edit.append('\t真太阳时为：' + JD2date(JD) + '\n')
		else:  # 真转平
			JD -= E
			ui.edit.append('\t平太阳时为：' + JD2date(JD) + '\n')
	except:
		ui.edit.append("单击平太阳神转真太阳时，右击真太阳时转平太阳时\n")

def findDate(ui):  # 查找指定干支的年或月相
	try:
		s = ui.txtEditGZScope.text().split('*')
		upper = int(s[0])
		lower = int(s[1])
		if upper > lower:
			ui.edit.append(ErrorHint + '\n')
			return 0
		if ui.cblFindDate.currentText() == '年':
			Y = []
			num = gz.index(ui.txtEditGZ.text()) + 4
			x = (num - upper) % 60  # 下限与干支首年的差
			year = upper + x  # 查找的首年
			if upper < 0: upper += 1  # 转为计算用年
			if lower < 0: lower += 1
			while year <= lower:
				if upper <= year <= lower:
					if year < 0: Y.append(year - 1)
					else: Y.append(year)
				year += 60
			ui.edit.append("{}至{}内".format(gyjn(upper), gyjn(lower)))
			if len(Y) != 0:
				ui.edit.insertPlainText('  ' + ui.txtEditGZ.text() + "年为")
				for i in range(len(Y)):
					if i % 6 == 0: ui.edit.append('')
					ui.edit.insertPlainText('{:>7}'.format(Y[i]))
			else:
				ui.edit.insertPlainText("  没有" + ui.txtEditGZ.text() + "年")
		else:
			dayIdx = ["前三日", "前二日", "前一日", "", "后一日", "后二日", "后三日"]
			ui.edit.append(gyjn(upper) + '至' + gyjn(lower) + '间' + ui.cblFindDate.currentText() + dayIdx[ui.cblDateTolerance.currentIndex()] + '为' + ui.txtEditGZ.text() +  '的日期为：')
			phaseIdx = [-1, 0, 2, 1, 3]
			JDE = date2JD(upper) - 29
			JD0 = date2JD(lower + 1) + 1
			n = 1
			while JDE < JD0:
				JDE = PhaseJDE(JDE + 27, phaseIdx[ui.cblFindDate.currentIndex()])
				JD = td2jd(JDE)
				if ganzhiJD(JD++int(ui.cblDateTolerance.currentText())) == ui.txtEditGZ.text():
					ui.edit.append("{:>3}\t{:>11}".format(n, JD2date(JD+int(ui.cblDateTolerance.currentText()))[:-9]))
					n += 1
	except:  # 不支持非日期格式的输入
		ui.edit.append(ErrorHint)
		ui.edit.append('')


'''  干支月历 '''
def YNRQ(ui): # 月内日期
	try:
		day1 = gz.index(ui.txtEditSRGZ.text())
		day2 = gz.index(ui.txtEditLRGZ.text())
		d = (day2 - day1) % 60
		if d < 30:
			ui.edit.append(ui.txtEditLRGZ.text() + '在' + ui.txtEditSRGZ.text() + '朔月的' + nlrq[(day2 - day1) % 60] + '日\n')
		else:
			ui.edit.append(ui.txtEditLRGZ.text() + '日(含)  在' + ui.txtEditSRGZ.text() + '朔(不含)前' + str(60-d) + '日\n\t或在其后' + str(d) + '日（即第' + str(d+1) + '日(含朔)）\n')
	except:
		ui.edit.append('求日期需输入朔日干支和历日干支\n')

def YueLi(ui):
	try:
		day1 = gz.index(ui.txtEditSRGZ.text())
		for i in range(10):
			ui.edit.append(nlrq[i] +  ' ' + gz[(day1+i)%60] + '      ' +
			                nlrq[10+i] +  ' ' + gz[(10 + day1+i)%60] + '      ' +
			                nlrq[20+i] +  ' ' + gz[(20 + day1+i)%60])
		try:
			day2 = gz.index(ui.txtEditLRGZ.text())
			d = (day2 - day1) % 60
			if d < 30:
				ui.edit.append(ui.txtEditLRGZ.text() + '在' + ui.txtEditSRGZ.text() + '朔月的' + nlrq[(day2 - day1) % 60] + '日\n')
			else:
				ui.edit.append(ui.txtEditLRGZ.text() + '日(含)距' + ui.txtEditSRGZ.text() + '朔(含)' + str(d+1) + '日\n')
		except:
			ui.edit.append("")
	except:
		ui.edit.append('请输入朔日干支\n')

def NTS(ui):
	try:
		day = ui.txtEditLRGZ.text()[:2]
		rq = int(ui.txtEditLRGZ.text()[2:])
		day_gzx = gz.index(day)
		ui.edit.append('某月'+nlrq[rq-1]+'日为'+day+'，则该月朔日为'+ gz[(1-rq+day_gzx)%60] + '\n')
	except:
		ui.edit.append('此项为已知某日干支和日期，求所在月的朔日干支\n请在历日干支中输入干支和日期，如：甲子1\n')



'''   岁星纪年  '''
def TSJN(ui):
	year = int(ui.txtEditSxjn.text())
	if year == 0:
		ui.edit.append(ErrorHint + '\n')
	elif year < 0:
		n = -year  # 年的个位数
		niangan = (8 - n % 10 - 1) % 10
		nianzhi = (10 - n % 12 - 1) % 12
		ui.edit.append("{}\t太岁在{}\t岁名 {}({})\n".format(gyjn(year),dizhi[nianzhi],suiyang[niangan] + suiyin[nianzhi], tiangan[niangan] + dizhi[nianzhi]))
	else:
		niangan = (year % 10 - 3 - 1) % 10
		nianzhi = (year % 12 - 3 - 1) % 12
		ui.edit.append("{}\t太岁在{}\t岁名 {}({})\n".format(gyjn(year),dizhi[nianzhi],suiyang[niangan] + suiyin[nianzhi], tiangan[niangan] + dizhi[nianzhi]))

def WCC(ui):
	year = int(ui.txtEditSxjn.text())
	if year == 0:
		ui.edit.append(ErrorHint + '\n')
	elif year < 0 :
		ui.edit.append(gyjn(year)+ '（' + ganzhiYear(year) + '）\t岁在' + xingci[(year - 7 + i) % 12] + '（无超辰）\n')  # 无超辰法岁星位置
	elif year > 0 :
		ui.edit.append(gyjn(year)+ '（' + ganzhiYear(year) + '）\t岁在' + xingci[(year - 8 + i) % 12] + '（无超辰）\n')

def stlss(year):
	src, ccts = SuiShu(year, True)
	ccfly = 50
	if year < 0: year += 1  # 计算用
	if abs(ccfly - year) % 144 == 0:
		src = '超' + xingci[xingci.index(src)-1] + ' ' + src
	return '\t三统历超辰法：' + src# + '（' + ccts + '）'  # + '  岁名'+ suiming + '（今' + nianming+'）'

def STSCC(ui):
	year = int(ui.txtEditSxjn.text())
	if year == 0:
		ui.edit.append(ErrorHint + '\n')
		return 0
	ccf = stlss(year)
	ui.edit.append(gyjn(year) + '（' + ganzhiYear(year) + '）' + ccf + '\n')

def MXWZ(ui):
	year = int(ui.txtEditSxjn.text())
	if year == 0:
		ui.edit.append(ErrorHint + '\n')
		return 0
	date = equinox_solstice(year - 1, 270, 0)
	JDE = ut2td(date)
	jL1 = PlanetLBR('木', JDE)[0]
	jL2 = PlanetLBR('木', JDE+365)[0]
	if abs(jL1 - jL2) > 60: jL2 += 360
	src1, rcd = rcd_calc(jL1, 1)
	src2, rcd = rcd_calc((jL1+jL2)/2, 1)
	ui.edit.append(gyjn(year) + '\t 木星木星真实（岁首冬至）位置为：' + src1[1:] + '\n（' + ganzhiYear(year) + '）\t\t（首尾平均）位置为：' + src2[1:] + '\n')

def SXJN(ui):
	year = int(ui.txtEditSxjn.text())
	if year == 0:
		ui.edit.append(ErrorHint + '\n')
	n = -year
	if year < 0: n -= 1
	niangan = (7 - n % 10 - 1) % 10
	nianzhi = (9 - n % 12 - 1) % 12
	ui.edit.append("{}\t太岁在{}\t岁名 {}\n".format(gyjn(year),dizhi[nianzhi],suiyang[niangan] + suiyin[nianzhi]))
	ui.edit.insertPlainText('（' + ganzhiYear(year) + '）\t无超辰法：岁在' + xingci[(year - 8 + i) % 12])  # 无超辰法岁星位置 + '（' + dizhi[(5 - nianzhi - i) % 12] + '）'
	ccf = stlss(year)
	ui.edit.append(ccf)
	date = SolarTermsDate(year - 1, 270, 0)
	JDE = ut2td(date)
	jL1 = PlanetLBR('木', JDE)[0]
	jL2 = PlanetLBR('木', JDE+365)[0]
	if abs(jL1 - jL2) > 60: jL2 += 360
	src1, rcd = rcd_calc(jL1, 1)
	src2, rcd = rcd_calc((jL1+jL2)/2, 1)
	ui.edit.append('\t是年木星真实（岁首冬至）位置为：' + src1[1:] + '\n\t\t（首尾平均）位置为：' + src2[1:] + '\n')


''' 农历与公历转换 '''


def Solar2LunarCalendar(ui, JD):
		date = JD2date(JD)
		year, month, day = GetDate(date)[:3]
		# 判断所在年
		nian = year  # 农历年，起冬至朔
		dzs = date2JD(dzs_find(year))
		next_dzs = date2JD(dzs_find(year + 1))  # 次年冬至朔
		if DateCompare(JD, next_dzs):  # 属次年
			nian += 1
		elif not DateCompare(JD, dzs):  # 属上年（BC1100前的情况）
			nian -= 1
		# 判断所在月
		ym, shuo = currentCalendar(nian)
		szy = -1
		for i in range(len(shuo)):
			if DateCompare(JD, shuo[i]):
				szy += 1  # date所在的阴历月序，起冬至朔
		# 判断该日在月内日期
		rgz = gz.index(ganzhiJD(JD))  # 所求日干支
		ssgz = gz.index(ganzhiJD(shuo[szy]))  # 实朔干支
		rq = (rgz - ssgz) % 60  # math.floor(JD + 0.5) - math.floor(shuo[szy] + 0.5)
		sc2lcDay = '\t公历    ' + date[:-9].replace('/', '.').replace('-', 'BC') + '（星期' + weeks[math.floor(JD% 7)] + '）\t\tJDN：' + str(JD)
		# 判断节气月
		jqy, jqr = SolarTermsDate(year, month * 30 + 255)[:-9].split('/')[1:]
		if int(jqy) != month: month -= (int(jqy) - month)
		if year < 0: year += 1
		if day >= int(jqr): ygz = gz[(year * 12 + 12 + month) % 60]
		else: ygz = gz[(year * 12 + 11 + month) % 60]
		if szy < 2: nian -= 1  # 子正改为寅正
		if nian < 0: nian += 1
		sc2lcDay += '\n\t对应实历（寅正）：' + gz[(nian - 4) % 60] + '年 ' + ygz + '月 ' + gz[rgz] + '日 ' + ym[szy] + nlrq[rq] + '\n'
		return sc2lcDay
