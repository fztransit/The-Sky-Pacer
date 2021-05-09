from Data.EraName import *
from BasicFunc import *
from AncientAstro import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QComboBox
from UI.timeTools import *
import copy

Year = 0
Month = 0
EmperorIdx = -1
Nian = []
RX = 0  # 选中行列
Selected = None
glyb, glqb, glxw = [], [], []
glMonthInfo = []
sc2glb = []

def font2(text, size=18, bold="normal", color="black"):
	text = "<font style='font-size:" + str(size) + "px; text-align:center; color:" + color + ";font-weight:" + str(bold) + ";'>" + str(text) + "</font>"
	return text

def formatDate(JD):
	date = JD2date(JD)[-14:-9]
	month, day = date.split('/')
	date = month.lstrip('0') + '.' + day.lstrip('0')
	return date

def calcChar(string):
	count = 0
	for char in string:
		if 65 <= ord(char) <= 90 or char == ' ':
			count += 1
		elif char.isdigit() or char == '.':
			count += 1
		elif char.isalpha() or char in ['：', '（', '）']:
			count += 2
		elif char == '\t':
			num = count % 8
			count += 8 - num
	return count

def getReign(reginText):  # 提取年号
	regin = reginText[:-4]
	if regin[-1] == '元': return regin[:-1]
	for i in range(len(regin) - 1):
		for j in range(len(hzjs)):
			if hzjs[j] == regin[-1]:
				regin = regin[:-1]
				continue
			if j == len(hzjs) - 1:
				return regin
	else:
		return ''

def getQM(rqx, qb):
	qm = ''
	for q in range(len(qb)):
		if rqx == qb[q][0]: qm += '   ' + qb[q][1]
	return qm

def getDynasties(dynasty):
	cd, cdnhb = [], [[], [], [], []]
	for d in dynasties[3:]:
		if d[1] <= Year <= d[2] and d[0] != dynasty:  # 待处理首年接续
			cd.append(d[0])
	eras = eratable[841 + Year]
	if len(cd) != 0:
		for d in cd:
			for era in eras:
				if d == era[0]:
					for i in range(4):
						cdnhb[i].append(era[i])
	return cdnhb


def getFirstMonth(dynasty, emperor, reign, yb):
	m = 0 if yb[yb[1]+3][:-3] in ['正月', '建子月'] else 1
	if dynasty in nhsmb:
		for j in range(len(nhsmb[dynasty])):
			nyb = nhsmb[dynasty][j][-1]
			if nyb[0] <= Year <= nyb[2]:
				if len(nhsmb[dynasty][j]) > 1 and isinstance(nhsmb[dynasty][j][0], str):
					if nhsmb[dynasty][j][0] != reign: continue
					if len(nhsmb[dynasty][j]) == 3:
						if nhsmb[dynasty][j][1] != emperor: continue
				if Year == nyb[0]:
					m = nyb[1] - 1   # 该年首月
					if len(nyb) == 5:
						if nyb[-1] == '*': m += 1  # 起闰月
	return m + yb[1]  # yb[m+3+yb[1] :]  # m起的历表


#################### 界面更新 #########################

def displayEraname(ui):
	jn = gyjn(Year) + '（' + ganzhiYear(Year) + '）：'
	count = calcChar(jn)
	if count + len(eranames[841 + Year])*2 > 100:
		num = count//2
		if count % 2 == 1: num += 1
		era = eranames[841 + Year][:(100-count)//2] + '<br/>' + '&nbsp;'*num + eranames[841 + Year][(100-count)//2:]
	else: era = eranames[841 + Year]
	text = font2(gyjn(Year),12,800) + '（' + ganzhiYear(Year) + '）：' + era
	ui.labEraName.setText(text)

def Solar2Guli(JD):
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
	ym, shuo = currentCalendar(nian)
	# 判断该日在古代历法中的日期
	sc2glzb = []
	if 690 <= nian <= 700: yfb = yuefen2
	elif nian == 762: yfb = yuefen3
	else: yfb = yuefen
	glsTables2 = findBxlf(nian)  # 古历朔列表，0为历名，1为上年末月，-1为次年首月
	glsTables = []
	for i in range(len(glsTables2)):  # 并立朝代展开
		cdb = glsTables2[i][0][1:-4].split('、')
		for j in range(len(cdb)):
			glsTables.append(['(' + cdb[j] + glsTables2[i][0][-4:]])
			length = len(glsTables) - 1
			glsTables[length] = glsTables[length] + glsTables2[i][1:]
	for glsTable in glsTables:
		cdm = glsTable[0][1:-4]
		if cdm == '唐':
			gailib = ['闰十月大甲午', '正月小甲子', '腊月小癸巳']
			if nian == 698:
				for i in range(2, 5): glsTable[i] = gailib[i - 2]
		gldzsJD = glDzsJD(glsTable[2][-2:], shuo[0], shuo[1])
		n = getMonth(glsTable, gldzsJD, JD)
		m = 0
		if cdm == '新' and nian == 9:  # 丑正改为寅正
			for i in range(1, 3):
				glsTable[i] = yfb[yfb.index(glsTable[i][:-3]) - 1] + glsTable[i][-3:]
			if n > 2: m -= 1
		if cdm == '更始' and nian == 23:  # 丑正改为寅正
			for i in range(1, len(glsTable)):
				glsTable[i] = yfb[yfb.index(glsTable[i][:-3]) - 1] + glsTable[i][-3:]
		if cdm == '魏':  # 寅正改为丑正
			if nian == 237:
				for i in range(6, len(glsTable)):
					glsTable[i] = yfb[(yfb.index(glsTable[i][:-3])+1)%12] + glsTable[i][-3:]
				if n > 5: m -= 1
			elif 238 <= nian <= 239:
				for i in range(1, len(glsTable)):
					if glsTable[i][0] == '闰':
						glsTable[i] = '闰' + yfb[(yfb.index(glsTable[i][1:-3]) + 1) % 12] + glsTable[i][-3:]
					else: glsTable[i] = yfb[(yfb.index(glsTable[i][:-3])+1)%12] + glsTable[i][-3:]
				m -= 1
			elif nian == 240:  # 跨年后建正变化
				for i in range(1, 3):
					glsTable[i] = yfb[yfb.index(glsTable[i][:-3])+1] + glsTable[i][-3:]
				glsTable[3] = '后' + glsTable[3]
		if cdm == '新' and 10 <= nian <= 23: m -= 1
		if cdm == '魏' and 238 <= nian <= 239: m -= 1
		if cdm == '唐' and (690 <= nian <= 700 or nian == 762): m -= 2  # 年首起子月
		zyx = 4+m if glsTable[4+m][:-3] == yfb[0] else 5+m  # 闰在冬至月与正月间
		nian2 = nian - 1 if n < zyx else nian
		if nian2 != nian and nian2 == 8: cdm = '汉'
		glyx = glsTable[n]
		yx = yfb.index(glyx[:-3].replace('闰', '').replace('后', ''))
		for era in eratable[841+nian2]:  # 按年号展开
			if cdm == era[0]:
				sc2glzb.append([glsTable[0][1:-4], nian2, era, glyx[:-3], JDN(JD)])  # glrq, gz[rgz],
				if cdm in nhsmb:  # 非全年年号截取，及一年多年号拼接
					for nhnyb in nhsmb[cdm]:
						if len(nhnyb) == 3 and nhnyb[1] != era[1]:
							continue
						nyb = nhnyb[-1]
						if ((len(nhnyb) > 1 and nhnyb[0] == era[2]) or len(nhnyb) == 1) and ((nyb[0] == nian2 and nyb[1] > yx+1) or (nyb[2] == nian2 and nyb[3] < yx+1)):
							sc2glzb.pop()  # 该年不存在该月（在首月前或末月后）
	return sc2glzb

def searchEraname(ui):
	global EmperorIdx, Nian, sc2glb
	sc2glb = []
	try:
		int(ui.editSearch.text())
	except:
		flag0 = False
	try:
		if not flag0:
			JD = JDN(date2JD(ui.editSearch.text().replace('.', '-')))
			if not 1683489 < JD <= 2071727:
				sc2lcDay = Solar2LunarCalendar(ui, JD)
				return ui.labDateInfo.setText('日期超出本历表更新范围（BC104.2.22 - 960.1.30），无法跳转，以下提供实历月日参考。\n' + sc2lcDay)
			sc2glzb = Solar2Guli(JD)
			sc2glb = sc2glzb[0]
			for i in range(len(sc2glzb)):
				if ui.cblDynasty.currentText() == sc2glzb[i][0]:  # 本朝优先
					sc2glb = sc2glzb[i]
			Nian = sc2glb[2]
			EmperorIdx = Nian[-1][1]
			if Nian[-1][0] == 3: EmperorIdx -= 5
			ui.cblDynasty.setCurrentIndex(Nian[-1][0] - 3)
			ui.rbAll.setChecked(True)
	except:
		try:
			year = int(ui.editSearch.text())
			if not (-104 <= year <= 960 and year != 0):
				return ui.labDateInfo.setText('不在古代历法纪年范围内（BC104-1911）或超出程序完成年份（暂更至959），可前往万年历查看。')
			flag = False
			eraInfo = eratable[841 + year]
			for k in range(len(eraInfo)):
				if eraInfo[k][0] == ui.cblDynasty.currentText():
					eraname = eranames[841 + year].split('、')[k]
					flag = True   # 当前朝代内存在该年
					break
			if not flag:  # 不存在默认第一个
				k = -1
				eraname = eranames[841 + year].split('、')[0]
			flag = False
		except:
			flag, flag2 = True, False
			eraname = ui.editSearch.text()
			dynastyTable = [dynasties[3+ui.cblDynasty.currentIndex()]] + dynasties[3:3+ui.cblDynasty.currentIndex()] + dynasties[3+ui.cblDynasty.currentIndex()+1:28]  # 本朝优先
			for dynasty in dynastyTable:
				if flag2: break
				for i in range(len(dynasty[4])):
					if flag2: break
					for j in range(len(dynasty[4][i])):
						if ui.editSearch.text() == dynasty[4][i][j]:
							eraname = dynasty[0] + dynasty[3][i] + dynasty[4][i][j] + '元年'
							flag2 = True
							break
			try: idx = single_eranames.index(eraname)
			except:
				return ui.labDateInfo.setText('输入错误，不存在此年号或存在于更新范围外（暂更至后周）。')
			year = year_eranames[idx]
			if not -104 <= year <= 959 or eraname[0] == '辽':
				return ui.labDateInfo.setText('不在古代历法纪年范围内（BC104-1911，暂更至959，不含辽），可前往万年历查看。')
			eraInfo = eratable[841 + year]
		if flag or k == -1:
			for k in range(len(eraInfo)):
				if eraInfo[k][0] in eraname and eraInfo[k][1] in eraname and eraInfo[k][2] in eraname:
					break  # 指定年号一一对应
		i, j = eraInfo[k][-1]
		EmperorIdx = j - 5 if i == 3 else j
		Nian = eraInfo[k]
		ui.cblDynasty.setCurrentIndex(i-3)
	ui.updateERYY()  # addEmperor(setIdx)→addReign(setIdx)→addYue(displayEraname)→updateYue

def addEmperorItems(ui, flag=True):
	global EmperorIdx
	ui.cblEmperor.blockSignals(True)
	ui.cblEmperor.clear()
	idx = ui.cblDynasty.currentIndex() + 3
	for j in range(len(dynasties[idx][3])):
		if idx > 3 or (idx == 3 and j > 4):
			ui.cblEmperor.addItem(dynasties[idx][3][j])
	if EmperorIdx != -1:
		ui.cblEmperor.setCurrentIndex(EmperorIdx)
		EmperorIdx = -1
	ui.cblEmperor.blockSignals(False)

def addReignItems(ui):
	global Nian
	ui.cblReign.blockSignals(True)
	ui.cblReign.clear()
	idx1 = ui.cblDynasty.currentIndex() + 3
	idx2 = ui.cblEmperor.currentIndex()
	if idx1 == 3: idx2 += 5
	# 该帝号起始年
	if idx1 == 3 and idx2 == 5:
		startYear = -104
	else:
		startYear = dynasties[idx1][1]
		for m in range(idx2):
			for n in range(len(dynasties[idx1][5][m])):
				if isinstance(dynasties[idx1][5][m][n], str):
					if int(dynasties[idx1][5][m][n]) < 0:
						startYear += int(dynasties[idx1][5][m][n])
					else:
						startYear -= int(dynasties[idx1][5][m][n])
				else:
					startYear += dynasties[idx1][5][m][n]
				if startYear == 0: startYear += 1
	# 生成年号
	start = 0
	s = 0
	x = 0
	z = 0
	for k in range(len(dynasties[idx1][5][idx2])):
		if idx1 == 3 and idx2 == 5 and k < 6:
			continue
		years = dynasties[idx1][5][idx2][k]
		if isinstance(years, str):
			if int(years) == 0:
				start = dynasties[idx1][5][idx2-1][-1]
			elif int(years) > 0:
				start = abs(int(years)) - 1
				x -= 1
			else:
				start = abs(int(years))
			s += 1
			continue
		if idx2 == 0 and k == 0: start = snb[idx1]
		if start == years:  # 不足一年
			start -= 1
		for y in range(start, years):
			item = dynasties[idx1][4][idx2][k-s] + sz2hz(y) + '年-' + ganzhiYear(startYear+x)
			ui.cblReign.addItem(item)
			if Nian != [] and Nian[2] == dynasties[idx1][4][idx2][k-s] and Nian[3] == y:
				idx = z
				ui.cblReign.setCurrentIndex(idx)
				Nian = []
			x += 1
			z += 1
		start = 0
	ui.cblReign.blockSignals(False)

def addYueItems(ui):
	global glyb, glqb, glxw, Year
	ui.cblYue.blockSignals(True)
	ui.cblYue.clear()
	dynasty = ui.cblDynasty.currentText()
	emperor = ui.cblEmperor.currentText()
	reign = ui.cblReign.currentText()
	for i in range(len(eranames)):  # 遍历查找
		if dynasty + emperor + reign[:-3] in eranames[i]:
			Year = -841 + i
			break
	displayEraname(ui)
	reign = getReign(reign)
	if dynasty == '晋' and reign == '永安':
		emperor = ui.cblReign.currentIndex()
	jsxyb.reset([])  # 初始化及进朔小余表可设值
	glyb, glqb, glxw, m1, m2 = autoBxlf(Year, dynasty, emperor, reign)   # 入口（该年在指定年号中的历表）
	jsxyb.setFlag()  # 进朔小余表不可设值
	jsxyb.gvar = jsxyb.gvar[1:]
	if sc2glb != []: sc2glb.insert(4, m1-glyb[1])
	yb = glyb[m1+3:m2]  # m起的历表
	for i in range(len(yb)):
		sign = ' '
		if len(jsxyb.gvar) != 0:
			if gz[jsxyb.gvar[m1+i][0]] != yb[i][-2:]: sign = '*'
		ui.cblYue.addItem(yb[i][:-3] + yb[i][-2:] + sign)
	getNianLi(ui)
	ui.cblYue.blockSignals(False)

def getNianLi(ui):  # 每更新年号或年序即计算
	global Ymb, Shuo, Yxc, Cdnhb
	Ymb, Shuo = currentCalendar(Year, 0)
	if Year in [698, 725] and ui.cblReign.currentText()[:2] in ['圣历', '开元']: Yxc = 1
	else: gldzsJD, Yxc = glDzsJD(glyb[3][-2:], Shuo[0], Shuo[1], True)
	Cdnhb = getDynasties(ui.cblDynasty.currentText())

def updateYue(ui):
	ui.cblYue.lineEdit().setCursorPosition(0)
	getYueLi(ui)
	displayYue(ui)
	displayDateInfo(ui)

def getYueLi(ui):
	global glMonthInfo, Month, Ymb, Shuo
	jz = glyb[1]
	yb = glyb[3:]  # 起冬至朔
	Month = jz if yb[jz][:-3] in ['正月', '建子月'] else jz+1  # 指定建正正月
	my = Month + 12 if yb[jz+12][:-3] in ['正月', '建子月'] else Month + 13  # 指定建正正月
	run = '<br/>闰十月' if Year == 697 else '<br/>无闰'
	for i in range(Month, my):
		if '闰' in yb[i]: run = '<br/>' + yb[i][:-3]
	if ui.sender() == ui.editSearch and sc2glb != []:
		idx = 0
		while sc2glb[3] != yb[Month][:-3]:
			Month += 1
			idx += 1
		ui.cblYue.setCurrentIndex(idx-sc2glb[4])
		ui.cblYue.lineEdit().setCursorPosition(0)
	else:
		while ui.cblYue.currentText()[:-3] != yb[Month][:-3]:
			Month += 1
	gly = yb[Month]
	glyr = dxy[gly[-3]]
	if len(Shuo) <= Month + Yxc + 1:
		ymb1, shuo1 = currentCalendar(Year + 1)
		Ymb = Ymb[:-2] + ymb1[:4]
		Shuo = Shuo[:-2] + shuo1[:4]
	slsJD = Shuo[Month + Yxc]
	glsJD = glJD(slsJD, gz.index(gly[-2:]))
	slyr = dateDiffer(Shuo[Month + Yxc + 1], slsJD)
	sly = Ymb[Month + Yxc]
	qb = glxw[Month] + glqb[Month]    # 0-2古历弦望，3-4古历中节，5-7实历弦望，8-实历中节
	if 690 <= Year <= 700: yfb = yuefen2
	elif Year == 762: yfb = yuefen3
	else: yfb = yuefen
	ymx = yfb.index(gly[:-3].replace('闰','').replace('后',''))
	year = Year + 1 if Year < 0 else Year
	ygz = gz[(year*12+ymx+14) % 60]
	ui.labYearInfo.setText(font2(gyjnBC(Year) + '<br/>' + ganzhiYear(Year) + '年<br/>' + ygz + '月<br/>' + dizhi[jz] + '正' + run, 14))

	glMonthInfo = [glsJD, glyr, slsJD, slyr, sly, qb]


def getQSXW(slsJD, arg):
	ymb, shuo, yxc = Ymb, Shuo, Yxc
	if arg[-1] in [0, 1]:
		global compareInfo, mCdnhb
		qb, selectedCD, currentCD = arg[:-1]
		mCdnhb = copy.deepcopy(Cdnhb)  # 按月处理的年号表
		cd, dh, nh = copy.deepcopy(mCdnhb[:-1])
		glm, glsJD2, glyr2, gly2, ry, qb2 = [], [], [], [], [], []
		k = 0
		for i in range(len(cd)):
			flag = False
			try: glyb2, glqb2, glxw2, m1, m2 = autoBxlf(Year, cd[i], dh[i], nh[i])
			except: flag = True  # 有年无历
			if flag:
				for j in range(4):
					mCdnhb[j].pop(i+k)
				k -= 1
				continue
			yb2 = glyb2[3:]
			gldzsJD2, yxc2 = glDzsJD(yb2[0][-2:], shuo[0], shuo[1], True)
			yx = Month + yxc - yxc2
			jz = glyb2[1]
			if (yx < m1 and m1 == jz) or (yx == m2 - 3 and yb2[yx][:-3] in ['正月', '建子月']):  # 未出现子正对比需要
				if yx < m1 and m1 == jz: year = Year - 1
				else: year = Year + 1
				eraInfo = eratable[841+year]
				flag = False
				for x, era in enumerate(eraInfo):
					if era[0] == currentCD: continue
					if cd[i] == era[0]:  # 该朝有上年
						flag2 = True  # 默认全年
						if era[0] in nhsmb:
							for j in range(len(nhsmb[era[0]])):
								nyb = nhsmb[era[0]][j][-1]
								if nyb[0] <= year <= nyb[2]:
									flag2 = False
									if len(nhsmb[era[0]][j]) > 1 and isinstance(nhsmb[era[0]][j][0], str):
										if nhsmb[era[0]][j][0] != era[2]: continue
										if len(nhsmb[era[0]][j]) == 3:
											if nhsmb[era[0]][j][1] != era[1]: continue
									if year == Year + 1:
										fisrtM = nyb[1] if year == nyb[1] else 1
										if yx - (m2 - 3) + 1 >= fisrtM:  # 存在于次年首月后
											flag = True
											continue
									elif year == Year - 1:
										lastM = nyb[3] if year == nyb[2] else 12
										if 12 + yx - 1 <= lastM:
											flag = True  # 存在于上年末月前
											continue
						if flag or flag2:
							for n in range(1, 4):  mCdnhb[n][i+k] = era[n]
						elif mCdnhb[2][i+k] == era[2]:  # 上年年号不同时仅删除本年年号
							for n in range(4): mCdnhb[n].pop(i+k)
							k -= 1
							continue
			elif yx >= m2 - 3 or yx < m1 and m1 != jz:  # yx < m and m == jz：在上年
				for n in range(4): mCdnhb[n].pop(i+k)
				k -= 1
				continue
			glm.append(glyb2[:2])
			gly2.append(yb2[yx])
			glsJD2.append(glJD(slsJD, gz.index(yb2[yx][-2:])))
			glyr2.append(dxy[yb2[yx][-3]])
			fm = jz if yb2[jz][:-3] in ['正月', '建子月'] else jz + 1
			flag3 = True
			if len(yb2[fm:]) == 14:
				for r in range(1, len(yb2[fm:])):
					if yb2[fm+r][0] in ['闰', '后']:
						ry.append(yb2[fm+r][:-3])
						flag3 = False
			if flag3:
				ry.append('无闰')
			qb2.append(glxw2[yx] + glqb2[yx])
			if selectedCD == cd[i] and arg[-1] == 1:
				qb += glxw2[yx] + glqb2[yx]
		compareInfo = [glm, gly2, glsJD2, glyr2, ry, qb2]
	if arg[-1] in [0, 2]:  # 实历气朔弦望
		slyr = arg[-2]
		qb2 = []
		for i in range(3):
			xwJD = PhaseJD(slsJD, 1 + i)
			xwrq = dateDiffer(xwJD, slsJD)
			qb2.append([xwrq, ['上弦', '望', '下弦'][i]])
		zqc = 0
		for i in range(Month + yxc):  # 本月（不含）前有闰
			if '闰' in ymb[i]: zqc = -1
		if ymb[Month + yxc][0] == '闰':
			qb2.append([''])
		else:
			angle = (Month + yxc + zqc - 3) % 12 * 30
			slzq = SolarTermsJD2(Year, angle, Month)
			slzqrx = dateDiffer(slzq, slsJD)
			qb2.append([slzqrx, jieqi[(Month + yxc + zqc) * 2 % 24]])
		sljq1 = SolarTermsJD2(Year, (Month - 3.5) % 12 * 30, Month)
		sljq2 = SolarTermsJD2(Year, (Month - 2.5) % 12 * 30, Month)
		if DateCompare(sljq1, slsJD) and not DateCompare(sljq1, slsJD + slyr):  # glsJD ≤ sljq ＜ glsJD+slyr
			qb2.append([dateDiffer(sljq1, slsJD), jieqi[(Month * 2 - 1) % 24]])
		elif DateCompare(sljq2, slsJD) and not DateCompare(sljq2, slsJD + slyr):
			qb2.append([dateDiffer(sljq2, slsJD), jieqi[(Month * 2 + 1) % 24]])
		else:
			qb2.append(['', ''])
	if arg[-1] == 2:  # 只计算实历
		return qb2
	elif arg[-1] == 0:  # 计算实历和古历
		return qb + qb2, mCdnhb[0]
	else:  # 只计算古历
		return qb, mCdnhb[0], glsJD2, glyr2, gly2


def displayYue(ui):
	global glDateInfo
	glsJD, glyr, slsJD, slyr, sly, qb = glMonthInfo
	selectedCD = ui.cblCompare.currentText()
	qb2 = copy.deepcopy(qb)
	if ui.cblCompare.currentText() == '实历':
		qb, cd = getQSXW(slsJD, [qb2, selectedCD, slyr, 0])
	else:
		qb, cd, glsJD2, glyr2, gly2 = getQSXW(slsJD, [qb2, selectedCD, ui.cblDynasty.currentText(), 1])
		if ui.cblCompare.currentText() in cd:
			idx = cd.index(ui.cblCompare.currentText())
			slsJD, slyr, sly = glsJD2[idx], glyr2[idx], gly2[idx][:-3]  # 对比月
	ui.cblCompare.clear()
	ui.cblCompare.addItems(['无'] + cd + ['实历'])
	ui.cblCompare.setCurrentText(selectedCD)
	# 显示月历
	glDateInfo = [[]] * 32  # [[''] * 3] * 32
	glsgzx = gz.index(ganzhiJD(glsJD))
	slsgzx = gz.index(ganzhiJD(slsJD))
	glrc, slrc, num = 0, 0, glyr
	mingzx, minday = glsgzx, glsJD
	if ui.cblCompare.currentText() != '无':
		rc = dateDiffer(slsJD, glsJD)
		if rc > 0: slrc = rc
		else:
			mingzx = slsgzx
			minday = slsJD
			glrc = -rc
		if DateCompare(slsJD+slyr, glsJD+glyr):
			num = dateDiffer(slsJD+slyr, minday)
		else: num = dateDiffer(glsJD+glyr, minday)
	for m in range(2):
		ui.labs[m*2+4][10-m*9].setText('')
		ui.labs[m*2+5][10-m*9].setText('')
	texts = [['']*num, ['']*num, ['']*num, ['']*num]
	for i in range(num):
		texts[0][i] = font2(gz[(mingzx + i) % 60], 18, 400, '#008B8B')  # 干支行 FF8247
		ui.labs[i // 10 * 2][i % 10 + 1].setText(texts[0][i])
		if i-glrc < glyr:
			texts[1][i] = font2(formatDate(glsJD - glrc + i), 16, 600)  # 公历行
			if i < glrc:
				texts[2][i] = ''
				glDateInfo[i] = ['', JDN(glsJD - glrc + i)]
			else:
				for j in range(5):  # 优先显示节气
					if qb[j][0] == i-glrc:
						texts[2][i] = font2(qb[j][1], 16, 200, 'red')
				if texts[2][i] == '': texts[2][i] = font2(nlrq[i-glrc], 16, 600)  # 古历行
				# texts[2][i] = font2(nlrq[i-glrc], 16, 600)
				glDateInfo[i] = [nlrq[i-glrc], JDN(glsJD - glrc + i)]
			ui.labs[i // 10 * 2 + 1][i % 10 + 1].setText(texts[1][i] + '<br/>' + texts[2][i])
		else:
			texts[1][i] = font2(formatDate(glsJD - glrc + i), 16, 600)
			glDateInfo[i] = ['', JDN(glsJD - glrc + i)]  # 合历末日
		if ui.cblCompare.currentText() != '无':
			if i-slrc < slyr:
				if i < slrc:
					texts[3][i] = ''
					glDateInfo[i].append('')
				else:
					for j in range(5, len(qb)):
						if qb[j][0] == i - slrc:
							texts[3][i] = font2(qb[j][1], 16, 200, 'DeepPink')
					if texts[3][i] == '': texts[3][i] = font2(nlrq[i - slrc], 16, 400)  # 实历行
					# texts[3][i] = font2(nlrq[i - slrc], 16, 600)
					glDateInfo[i].append(nlrq[i - slrc])
				ui.labs[i // 10 * 2 + 1][i % 10 + 1].setText(texts[1][i] + '<br/>' + texts[2][i] + '<br/>' + texts[3][i])
			else: glDateInfo[i].append('')  # 合历末日
	lm = glyb[0][0:3]
	yfb = yuefen2 if 690 <= Year <= 700 else yuefen
	if ui.cblDynasty.currentText() in lbxd:
		for newMonth in lbxd[ui.cblDynasty.currentText()]:
			if newMonth[2] == 1 and newMonth[1] == Year and newMonth[0] in ui.cblReign.currentText():
				yx = yfb.index(newMonth[3][0][:-3].replace('闰', '').replace('后', ''))
				if yx+glyb[1] == Month: lm = newMonth[-1]  # 修改历名
	for j in range(3):
		if ui.cblCompare.currentText() != '无': ui.labs[j*2+1][0].setText('公  历<br/>' + font2(lm + '<br/>', 18) + font2('-'*30+'<br/>', 4) + font2(sly, 14))
		else: ui.labs[j * 2 + 1][0].setText('公  历<br/>' + font2(lm + '<br/>' + '<br/>', 18))
	glDateInfo[-1] = qb


def displayDateInfo(ui):
	global RX, Selected, setJDN
	if ui.sender() in [ui.btnWNL2, ui.btnGL]:  # 重设
		RX = 0
		setJDN = glDateInfo[RX][1]
		Selected = ui.labs[1][1]
		Selected.setStyleSheet("QLabel{ border:3px solid; border-radius: 5px; border-color:#1E90FF }")
	else:
		labs = sum(ui.labs, [])
		if ui.sender() == ui.cblCompare:
			if len(glDateInfo[RX]) != 0:
				currentJDN = glDateInfo[RX][1]
				RX -= currentJDN - setJDN
			else:
				while len(glDateInfo[RX]) == 0: RX -= 1
			if RX < 0: RX = 0
			row, col = divmod(RX, 10)
			Selected.setStyleSheet('')
			Selected = ui.labs[row*2+1][col+1]
			Selected.setStyleSheet("QLabel{ border:3px solid; border-radius: 5px; border-color:#1E90FF }")
		elif ui.sender() in labs:
			Selected.setStyleSheet('')
			if ui.sender().text() == '': return 0
			Selected = ui.sender()
			if Selected == labs[-1]:
				RX = 30
			else:
				row, col = divmod(labs.index(Selected), 11)
				RX = row // 2 * 10 + col - 1
			setJDN = glDateInfo[RX][1]
			Selected.setStyleSheet("QLabel{ border:3px solid; border-radius: 5px; border-color:#1E90FF }")
		elif ui.sender() == ui.editSearch and sc2glb != []:
			RX = sc2glb[-1] - glDateInfo[0][1]
			row, col = divmod(RX, 10)
			Selected.setStyleSheet('')
			Selected = ui.labs[row*2+1][col+1]
			Selected.setStyleSheet("QLabel{ border:3px solid; border-radius: 5px; border-color:#1E90FF }")
		else:  # 跳转月历（新月无该日时改为最后一日）
			lab = [ui.lab59, ui.lab5a, ui.lab7a]
			if Selected in lab[1:]:
				RX = lab.index(Selected) + 28
				while RX > 28 and glDateInfo[RX] == []:
					lab[RX - 28].setStyleSheet('')
					RX -= 1
					Selected = lab[RX - 28]
					Selected.setStyleSheet("QLabel{ border:3px solid; border-radius: 5px; border-color:#1E90FF }")
			setJDN = glDateInfo[RX][1]
	getDate = glDateInfo[RX]  # re.findall(r'<font style.*?>(.*?)<', Selected.text())
	if ui.cblCompare.currentText() != '无':
		glrq, jd, dbrq = getDate
	else:
		glrq, jd = getDate
	glrqx = -1 if glrq == '' else nlrq.index(glrq)
	rgz = ganzhiJD(jd)
	glqm = getQM(glrqx, glDateInfo[-1][:5])
	dbqm = getQM(glrqx, glDateInfo[-1][5:])
	text = ui.cblDynasty.currentText() + ui.cblEmperor.currentText() + ui.cblReign.currentText()[:-3] + ui.cblYue.currentText()[:-3] + glrq + rgz + glqm
	if len(jsxyb.gvar) != 0 and glrq == '初一':
		if Year == 725: ydy, yxy, jsz = jsxyb.gvar[Month+1]  # 人为改月序
		else: ydy, yxy, jsz = jsxyb.gvar[Month]
		comop = '＜' if yxy < jsz else '≥'
		text += '\t  ' + gz[ydy] + str(ydy) + '.' + str(yxy) + comop + str(jsz)
	year, month, day = JD2date(jd)[:-9].split('/')
	weekday = weeks[math.floor(jd % 7)]
	day = gyjnBC(year) + '.' + month.lstrip('0') + '.' + day.lstrip('0')
	if len(glyb[0]) > 3:
		if len(glyb[0]) == 4: text += '\n    该朝此年行用历法不明，参考用' + glyb[0][0:3]
		if len(glyb[0]) == 5: text += '\n    该朝此年行用历法不明，可能是用' + glyb[0][0:3]
		if len(glyb[0]) == 7: text += '\n    该朝此年用' + glyb[0][-3:] + '失传，参考用' + glyb[0][0:3]
		if getDate[0] == '': text += '：该月无' + rgz + '日'
	elif getDate[0] == '':
		text += '\n    按当时行用历法：该月无' + rgz + '日'
	text1 = '\n    对应公历为：' + day + '（' + rgz + '日 星期' + weekday + '）'
	text += text1 + '{0:>{1}}'.format('JDN：'+str(jd), 55-len(text1))
	# 对比信息
	dbsJD, dbyr, dby = glMonthInfo[2:5]  # re.findall(r'<font style.*?>(.*?)<', ui.labs[1][0].text())[2]
	jd0 = glDateInfo[0][1]  # 表首日
	if ui.rbAll.isChecked() or ui.cblCompare.currentText() not in ['无', '实历']:
		glm, gly2, glsJD2, glyr2, ry, qb2 = compareInfo
		ckrc = []
		for i in range(len(glm)):
			jd2 = JDN(glsJD2[i])
			ckrc.append(jd2 - jd0)
		cd, dh, nh, nx = mCdnhb
		if len(cd) != 0:
			append = ''
			for i in range(len(cd)):
				era = cd[i] + dh[i] + nh[i] + sz2hz(nx[i]) + '年'
				text1 = '\n    对应' + era
				count = calcChar(text1)
				glmry = '（' + glm[i][0][:3] + ry[i] + '）'  # ' '*(4-len(ry[i]))*2
				if ui.cblCompare.currentText() == cd[i]:  # 选中优先
					if getDate[2] == '': text += text1 + ' ' * (30-count) + dby + '无' + rgz + '日' + ' ' * (14-calcChar(dby)) + glmry
					else: text += text1 + ' ' * (30-count) + dby + dbrq + dbqm + ' ' * (22-calcChar(dby+dbrq+dbqm)) + glmry
				elif ui.rbAll.isChecked():  # 不在月历显示的参考信息
					if RX - ckrc[i] < 0 or RX - ckrc[i] >= glyr2[i]:
						append += text1 + ' ' * (30-count) + dby + '无' + rgz + '日' + ' ' * (14-calcChar(gly2[i][:-3])) + glmry
					else:
						ckqm = getQM(RX - ckrc[i], qb2[i])
						yrq = gly2[i][:-3] + nlrq[RX - ckrc[i]] + ckqm
						append += text1 + ' ' * (30-count) + yrq + ' ' * (22-calcChar(yrq)) + glmry
			text += append
	if ui.cblCompare.currentText() == '实历' or ui.rbAll.isChecked():
		slrc = JDN(dbsJD) - jd0
		if ui.cblCompare.currentText() != '实历':
			slsJD, slyr, sly = glMonthInfo[2:5]
			qb = getQSXW(slsJD, [slyr, 2])
			dbqm = getQM(RX - slrc, qb)
		if RX - slrc < 0 or RX - slrc >= dbyr:
			text += '\n    对应实际合天历法（寅正）' + ' ' * 2 + dby + '无' + ganzhiJD(dbsJD + RX - slrc) + '日'
		else:
			text += '\n    对应实际合天历法（寅正）' + ' ' * 2 + dby + nlrq[RX - slrc] + dbqm
	ui.labDateInfo.setText(text)


########################################  界面跳转 ##########################################
############ 按左右键上下跳转逻辑（前后朝仅为朝代表内顺序，非接续顺序）：
# 帝号跳转：
# 		1-1：首帝前朓时跳往前朝末帝，年号为最先，月份为首月。
# 		1-2：末帝后跳时跳往后朝首帝，年号为最先，月份为首月。
# 		1-3：其他为本朝代内前后跳转，年号为最先，月份为首月。
# 年号跳转：
# 		2-1-1：首年号前朓时跳往前帝末年号，月份为首月。2-1-2：遇首帝时跳往前朝末帝，年号为最末，月份为首月。
# 		2-2-1：末年号后朓时跳往后帝首年号，月份为首月。2-2-2：遇末帝时跳往后朝首帝，年号为最先，月份为首月。
# 		2-3：其他为本帝号内前后跳转，跳转后月份为该年号内首月。
# 月份跳转：
# 		3-1-1：首月前朓时跳往前年号末月。3-1-2：遇首年号时跳往前帝末年号末月。3-1-3：遇首帝首年号时跳往前朝末帝末年号末月。
# 		3-2-1：末月后朓时跳往后年号首月。3-2-2：遇末年号时跳往后帝首年号首月。3-2-3：遇末帝末年号时跳往后朝首帝首年号首月。
# 		3-3：其他为本年号内前后跳转。
# flag标志当前按键，为False时表示当前函数为其他按键引用，不往下跳转。

def lastEmperor(ui, flag=True):
	idx1 = ui.cblDynasty.currentIndex()
	idx2 = ui.cblEmperor.currentIndex()
	if idx2 == 0:  # 首帝前朓（1-1、2-1-2、3-1-3）
		if idx1 != 0:
			ui.cblDynasty.setCurrentIndex(idx1 - 1)  # 前朝
			addEmperorItems(ui, flag)
			ui.cblEmperor.setCurrentIndex(ui.cblEmperor.count() - 1)  # 末帝
			if idx2 != 0:
				ui.cblReign.setCurrentIndex(ui.cblReign.count() - 1)
	else:  # 前帝（1-3、2-1-1、3-1-2）
		ui.cblEmperor.setCurrentIndex(idx2 - 1)
	if flag:
		ui.updateRYY()
	return idx1, idx2

def nextEmperor(ui, flag=True):
	idx = ui.cblEmperor.currentIndex()
	if idx == ui.cblEmperor.count() - 1:  # 末帝后跳（1-2、2-2-2、3-2-3）
		idx1 = ui.cblDynasty.currentIndex()
		if idx1 != ui.cblDynasty.count() - 1:
			ui.cblDynasty.setCurrentIndex(idx1 + 1)  # 后朝
			addEmperorItems(ui, flag)  # 首帝
	else:  # 后帝（1-3、2-2-1、3-2-2）
		ui.cblEmperor.setCurrentIndex(idx + 1)
	if flag:
		ui.updateRYY()

def lastReign(ui, flag=True):
	idx3 = ui.cblReign.currentIndex()
	if idx3 == 0:  # 首年号前跳（2-1、3-1-2、3-1-3）
		idx1, idx2 = lastEmperor(ui, False)  # 前帝
		addReignItems(ui)  # 更新帝号即更新年号表
		if not (idx1 == idx2 == 0): ui.cblReign.setCurrentIndex(ui.cblReign.count() - 1)  # 末年号
	else:  # 前年号（2-3、3-1-1）
		idx1 = ui.cblDynasty.currentIndex()
		idx2 = ui.cblEmperor.currentIndex()
		idx3 -= 1
		ui.cblReign.setCurrentIndex(idx3)
	addYueItems(ui)  # 首月
	if flag: updateYue(ui)
	return idx1, idx2, idx3

def nextReign(ui, flag=True):
	idx = ui.cblReign.currentIndex()
	if idx == ui.cblReign.count() - 1:  # 末年号后跳（2-1、3-2-2、3-2-3）
		nextEmperor(ui, False)  # 后帝
		addReignItems(ui)  # 更新帝号即更新年号表、首年号
	else:  # 后年号（2-3、3-2-1）
		ui.cblReign.setCurrentIndex(idx + 1)
	addYueItems(ui)  # 首月
	if flag: updateYue(ui)


def lastYue(ui):
	idx = ui.cblYue.currentIndex()
	if idx == 0:  # 首月前跳（3-1）
		idx1, idx2, idx3 = lastReign(ui, False)
		if not (idx1 == idx2 == idx3 == 0): ui.cblYue.setCurrentIndex(ui.cblYue.count() - 1)  # 末月
	else:  # 前月（3-3）
		ui.cblYue.setCurrentIndex(idx - 1)
	updateYue(ui)

def nextYue(ui):
	idx = ui.cblYue.currentIndex()
	if idx == ui.cblYue.count() - 1:  # 末月后跳（3-2）
		nextReign(ui, False)  # 首月
	else:  # 后月（3-3）
		ui.cblYue.setCurrentIndex(idx + 1)
	updateYue(ui)

def wnl2(ui):
	ui.windowChange(ui.wnlWidget)
	if ui.wnlWidget.isClosed:
		ui.setupCalendar()
		ui.glUI()
	elif ui.uiType == True:
		ui.glUI()

