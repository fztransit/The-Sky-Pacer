from UI import *


dateInfo = [[]] * 42
selected = None
recordCurrentSelected = []
startCentury = -30
endCentury = 30
start_century = startCentury if startCentury <= 0 else startCentury - 1
setYear = ''

def font(text, size=12, color="gray", bold="normal"):
	text = "<font style='font-size:" + str(size) + "px; text-align:center; color:" + color + ";font-weight:" + str(bold) + ";'>" + str(text) + "</font><br/>"
	return text


def wnlHint(ui):
	if ui.labHint.text() == "":
		ui.labHint.setText('本页为一合天历法，如需查看古代历法情况，点击"古历"按钮')
	elif "古历" in ui.labHint.text():
		ui.labHint.setText('年列表中可直接输入年份后按回车键跳转')
	else:
		ui.labHint.setText('')

def borderDay(ui, month, day):  # 选中后加框
	firstDay = int(re.findall(r'(\d+)</font>', ui.labs[0][0].text())[0])
	if firstDay == 1:
		idx = - firstDay + day
	else:
		idx = days[month - 1] - firstDay + day
	global selected
	selected = ui.labs[idx // 7][idx % 7]
	selected.setStyleSheet("QLabel{ border:3px solid; border-radius: 5px; border-color:#1E90FF }")


def yearItems(ui):
	century = ui.cblCentury.currentIndex() + start_century + 1
	ui.cblYear.clear()
	for i in range(100):
		if century == 1 and i == 0: continue
		if century <= 0:
			ui.cblYear.addItem('BC' + str(abs(century) * 100 + 100 - i) + '年')
		else:
			ui.cblYear.addItem(str((century-1) * 100 + i) + '年')
	ui.cblYear.setCurrentIndex(0)

def lastYear(ui):
	idx = ui.cblYear.currentIndex()
	if idx == 0:
		century = ui.cblCentury.currentIndex()
		ui.cblCentury.setCurrentIndex(century - 1)
		ui.cblYear.setCurrentIndex(ui.cblYear.count()-1)
	elif idx != -1:
		ui.cblYear.setCurrentIndex(idx - 1)

def nextYear(ui):
	idx = ui.cblYear.currentIndex()
	century = ui.cblCentury.currentIndex()
	if idx == -1 or century == endCentury - start_century - 1:
		getYearMonth(ui, wheel=1)
	elif ui.cblYear.count() > 0 and idx == ui.cblYear.count() - 1:
		ui.cblCentury.setCurrentIndex(century + 1)
	else:
		ui.cblYear.setCurrentIndex(idx + 1)

def jumpYear(ui):  # 本世纪首年或末年时跳转上世纪或下世纪
	idx = ui.cblYear.currentIndex()
	century = ui.cblCentury.currentIndex()
	if idx == 0:
		if century == 0: pass
		else:
			ui.cblCentury.setCurrentIndex(century - 1)
			ui.cblYear.setCurrentIndex(ui.cblYear.count()-1)
	elif idx != -1 and idx == ui.cblYear.count() - 1:
		if century == endCentury - start_century - 1: pass
		else: ui.cblCentury.setCurrentIndex(century + 1)
	displayDate(ui)

def lastMonth(ui):
	idx = ui.cblMonth.currentIndex()
	if idx == 0:
		lastYear(ui)
		ui.cblMonth.setCurrentIndex(11)
	else:
		ui.cblMonth.setCurrentIndex(idx - 1)

def nextMonth(ui):
	idx = ui.cblMonth.currentIndex()
	if idx == 11:
		nextYear(ui)
		ui.cblMonth.setCurrentIndex(0)
	else:
		ui.cblMonth.setCurrentIndex(idx + 1)

def jumpMonth(ui):
	idx = ui.cblMonth.currentIndex()
	if idx == 0:
		lastYear(ui)
		ui.cblMonth.setCurrentIndex(11)
	elif idx == 11:
		nextYear(ui)
		ui.cblMonth.setCurrentIndex(0)
	displayDate(ui)



def findSZY(JD, shuoJD):  # 查找JD所在的农历月份
	szy = -1
	for i in range(len(shuoJD)):
		if DateCompare(JD, shuoJD[i]):
			szy += 1  # date所在的阴历月序，起冬至朔
	return szy

def getSolorTerms(year):
	jqb = [[i] for i in range(12)]  # [月序，[日序， 节气序] * n]
	for i in range(26):
		if i < 2: jq = SolarTermsDate(year-1, 255 + i * 15)
		else: jq = SolarTermsDate(year, 255 + i * 15)
		jqn, jqy, jqr = jq[:-9].split('/')
		jqy = int(jqy) - 1
		if (i < 2 and jqy == 0) or (i >= 24 and jqy > 0) or 2 <= i < 24:  # 月份在本年内
			jqb[jqy].append([int(jqr), (i-1) % 24])
	for j in range(len(jqb)): jqb[j].pop(0)
	return jqb

def getEraName(year):
	if -841 <= year <= 1911:
		eraname = eranames[841 + year]
		ji_nian = eraname.replace('、', '<br/>')
		return ji_nian
	else:
		return ""

def setNYE(festival, ymb, shuoJD):  # 重设节日日期
	yx = ymb.index(festival[0])
	if dateDiffer(shuoJD[yx + 1], shuoJD[yx]) == 29:
		festival[1] = '廿九'
	else:
		festival[1] = '三十'
	return festival

def getYearMonth(ui, wheel=0): # 根据输入重设年月
	edit = ui.cblYear.currentText()
	try:
		year = int(re.search(r'-?\d+', edit).group())
	except:
		return 0, 0  # 异常输入
	if year == 0: return 0, 0
	if 'BC' in ui.cblYear.currentText() or 'bc' in edit:
		year = -year
	year += wheel
	century = year // 100
	if start_century * 100 <= year < endCentury * 100:
		ui.cblCentury.setCurrentIndex(century - start_century)
		if century == 0: ui.cblYear.setCurrentIndex(year % 100 - 1)
		else: ui.cblYear.setCurrentIndex(year % 100)
	else:
		ui.cblCentury.setCurrentIndex(-1)
		ui.cblYear.clear()
		if wheel == 0: ui.cblYear.setCurrentText(edit)
		else: ui.cblYear.setCurrentText(str(year))
	month = ui.cblMonth.currentIndex()
	global setYear
	if year != setYear or setYear == '':
		setYear = year
		updateYear()
	return year, month


def updateYear():
	global yearYMB, yearSJD, yearST
	yearYMB, yearSJD = currentCalendar(setYear, 0)
	yearST = getSolorTerms(setYear)


def displayMonth(ui):
	year, month = getYearMonth(ui)
	if year == 0: return 0, 0
	ymb, shuoJD, jqb = yearYMB, yearSJD, yearST
	if DateCompare(date2JD(year+1) - 1, shuoJD[-2] + 29):
		ymb1, shuoJD1 = currentCalendar(year + 1)
		ymb = ymb[:-2] + ymb1[:2]
		shuoJD = shuoJD[:-2] + shuoJD1[:3]
	days[1] = 29 if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0 else 28
	i = month
	ysJD = date2JD(str(year) + '/' + str(i+1) + '/1')
	szy = findSZY(ysJD, shuoJD)  # 每月1日对应的农历月
	ysRQ = dateDiffer(ysJD, shuoJD[szy])  # 每月1日的农历日期
	yue0 = dateDiffer(shuoJD[szy + 1], shuoJD[szy])
	yue1 = dateDiffer(shuoJD[szy + 2], shuoJD[szy + 1])
	yx = szy
	blank = int((ysJD + 0.5) % 7)
	for j in range(6):
		for k in range(7):
			# 计算日期
			day = j * 7 + k - blank + 1
			rqx = ysRQ + (j+1) * 7 - 7 + k - blank
			if rqx < 0:  # 月首日所在农历月上月
				yue = dateDiffer(shuoJD[szy], shuoJD[szy - 1])
				rq = nlrq[rqx % yue]
				yx = szy - 1
			elif 0 <= rqx < yue0:
				rq = nlrq[rqx]
				yx = szy
			elif yue0 <= rqx < yue0 + yue1:
				rq = nlrq[rqx - yue0]
				yx = szy + 1
			elif rqx >= yue0 + yue1:
				rq = nlrq[rqx - yue0 - yue1]
				yx = szy + 2
			if day == 1:
				yx1 = yx
				rq1 = rq
			if day == days[i]:
				yx2 = yx
				rq2 = rq
			dateInfo[j * 7 + k] = [day, ymb[yx], rq, ysJD+day-1, jqb[i]]
			if year == 1582 and i == 9: dateInfo[j * 7 + k][-1] = [jqb[i][0], jqb[i-1][1]]  # 该月无节气，月干支序从上月获取
			if rq == '初一': rq = ymb[yx]
			# 显示月历
			if j == 0 and k < blank:  # 上月
				ui.labs[j][k].setText(font(days[i-1]-blank+k+1, 20) + font(rq))
			else:
				if day <= days[i]:
					if year == 1582 and i == 9 and day > 4:
						if day < 15: continue
						else: ui.labs[j+(k-10)//7][k-3].setText(font(day, 20, "black", 800) + font(rq))
					else:
						ui.labs[j][k].setText(font(day, 20, "black", 800) + font(rq))  # "500;font-family:微软雅黑"
				else:
					if year == 1582 and i == 9:
						ui.labs[j+(k-10)//7][k-3].setText(font(day - days[i], 20) + font(rq))
						if day - days[i] == 11:
							for m in range(10): ui.labs[j-1+(m+k-2)//7][(m+k-2)%7].setText("")
					else: ui.labs[j][k].setText(font(day-days[i], 20) + font(rq))
	# 显示节日
	qmDay = 0
	for jq in jqb[i]:  # 节气
		jqrx = jq[0] + blank - 1
		if year == 1582 and i == 9: jqrx -= 10
		ui.labs[jqrx//7][jqrx%7].setText(font(jq[0], 20, "black", 800) + font(jieqi[jq[1]], 12, "red"))
		if jq[1] == 7: qmDay = jq[0]
	if year >= 1949:  # 公历节日起始年
		if qmDay: ui.labs[(qmDay+blank-1)//7][(qmDay+blank-1)%7].setText(font(qmDay, 20, "red", 800) + font("清明", 12, "red"))
		for fes in scfestivals:
			if fes[0] == month + 1:
				jqrx = fes[1] + blank - 1
				ui.labs[jqrx // 7][jqrx % 7].setText(font(fes[1], 20, "red", 800) + font(fes[2], 12, "red"))
	if year > 1911:  # 农历节日起始年
		rqx1 = nlrq.index(rq1)
		for fes in lcfestivals:
			if fes[2] == '除夕': fes = setNYE(fes, ymb, shuoJD)
			jqrx = nlrq.index(fes[1])
			if fes[0] == ymb[yx1] and jqrx >= rqx1:  # 该月农历首日
				jqrx += -rqx1 + blank
				ui.labs[jqrx // 7][jqrx % 7].setText(font(jqrx-blank+1, 20, "red", 800) + font(fes[2], 12, "red"))
			elif fes[0] == ymb[yx1+1] and jqrx <= nlrq.index(rq2):  # 该月农历末日
				jqrx += dateDiffer(shuoJD[yx1 + 1], shuoJD[yx1]) - rqx1 + blank
				ui.labs[jqrx // 7][jqrx % 7].setText(font(jqrx - blank + 1, 20, "red", 800) + font(fes[2], 12, "red"))
			elif yx2 - yx1 == 2 and fes[0] == ymb[yx2]:  # 跨2月
				jqrx += dateDiffer(shuoJD[yx1 + 2], shuoJD[yx1]) - rqx1 + blank
				if 0 < jqrx <= days[i] + blank: ui.labs[jqrx // 7][jqrx % 7].setText(font(jqrx - blank + 1, 20, "red", 800) + font(fes[2], 12, "red"))
	return year, month


def displayDate(ui, today=False):
	global selected, recordCurrentSelected
	try:
		selected.setStyleSheet("")
	except:
		pass
	if today:  # 设为今日
		year, month, day = time.localtime(time.time())[0:3]
		month -= 1
		ui.cblCentury.setCurrentIndex(-start_century + year // 100)
		ui.cblYear.setCurrentIndex(year % 100)
		ui.cblMonth.setCurrentIndex(month % 12)
		displayMonth(ui)
		borderDay(ui, month, day)
	else:
		if ui.sender() in [ui.cblCentury, ui.cblYear, ui.cblMonth, ui.btnLastMonth, ui.btnNextMonth, ui.btnLastYear, ui.btnNextYear]:  # 设为原公历日
			year, month = displayMonth(ui)
			day = int(re.findall(r'(\d+)</font>', ui.labInfo.text())[0])  # 公历日期
			if day > days[month]: day = days[month]  # 跳到上月底
			borderDay(ui, month, day)
		else:  # 点击日期跳转
			year, month = getYearMonth(ui)
			if year == 0: return 0
			selected = ui.sender()
			if selected.text() == "": return 0  # 1582年被删除的日期
			day = int(re.findall(r'(\d+)</font>', selected.text())[0])  # 公历日期
			if not re.search(r"<font style='font-size:20px; text-align:center; color:gray", selected.text()):  # 本月内
				ui.sender().setStyleSheet("QLabel{ border:3px solid; border-radius: 5px; border-color:#1E90FF }")  # 1E90FF 9400D3
			else:   # 跳转前后月
				if day > 20: lastMonth(ui)
				else: nextMonth(ui)
				year, month = displayMonth(ui)  # 更新月历
				borderDay(ui, month, day)
	# 日期相关显示信息
	jdn, weekday = getWeekday(year, str(month+1), day)
	ym, rq, JD, jqrq = dateInfo[day-dateInfo[0][0]][1:]
	nian = year
	if month < 3 and yuefen.index(ym.split('闰')[-1]) >= 10: nian -= 1
	if nian < 0: ngz = gz[(nian - 3) % 60]
	else: ngz = gz[(nian - 4) % 60]
	nm = gyjn(year)
	sxm = zodiac[(nian - 4) % 12]
	ji_nian = getEraName(year)
	if year < 0: year += 1
	jqr = 99
	for i in range(len(jqrq)):
		if jqrq[i][1] % 2 == 1: jqr = jqrq[i][0]
	if day >= jqr: ygz = gz[(year * 12 + 13 + month) % 60]
	else: ygz = gz[(year * 12 + 12 + month) % 60]
	ui.labInfo.setText("JDN {}<br/><br/>{}<br/>{}月 星期{}<br/>{}{}{}年 〖{}〗<br/>{}月 {}日<br/><br/>{}".format(
		jdn, nm, month+1, weekday, font(day,50,"black"), font(ym+rq,17,"black"), ngz, sxm, ygz, ganzhiJD(JD), font(ji_nian,12,"black")))

def getClosedText(ui):
	global selectedText
	selectedText = ui.sender().text()

def toToday(ui):
	displayDate(ui, True)

def wnl(ui):
	ui.windowChange(ui.wnlWidget)
	if ui.wnlWidget.isClosed:
		ui.setupCalendar()
		ui.calendarUI()
		displayDate(ui, True)
	elif ui.uiType == False:
		ui.calendarUI()
		displayDate(ui, True)

