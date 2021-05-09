from AncientAstro import *
from AstroCalc import *
from BasicFunc import *
from PyQt5.QtCore import *

def calendarAllSelect(ui):
	selectTab = ui.tabCalendar.currentIndex() + 1
	flag = False
	for i in range(len(ui.tqlf[selectTab])):
		if ui.tqlf[selectTab][i-1].isChecked():
			flag = True
	if flag == True:  # 存在选中时取消
		for i in range(len(ui.tqlf[selectTab])):
			ui.tqlf[selectTab][i-1].setChecked(False)
	else:
		for i in range(len(ui.tqlf[selectTab])):
			ui.tqlf[selectTab][i-1].setChecked(True)

def selectLB(ui):
	select_lb = []
	if ui.cbLB.isChecked():
		if ldlb[ui.cblZSLB.currentText()]:
			select_lb.append(ldlb[ui.cblZSLB.currentText()])
	else:
		selectTab = ui.tabCalendar.currentIndex() + 1
		for i in range(1, len(ui.tqlf[selectTab])+1):
			if ui.tqlf[selectTab][i-1].isChecked():
				select_lb.append(tqlb[selectTab][i-1])
	if not select_lb: ui.edit.append('')
	return select_lb

def basicInfo(ui):
	ui.edit.append("\t        基本说明\n"
	               "选项卡中提供同时期不同朝代颁行的历法\n"
	               "下拉列表前勾选项取消时，将从选项卡中同期历法取值\n"
	               "历表月份一律按无中气置闰法排序\n"
				   "月名或朔前后加*号表示朔进一日，弦望后加*号表示退一日。\n"
	               "古历与实历月份按月序对应，不按月名对应\n"
	               "月历表可直接输入yy/mm指定输出月份\n"
	               "历元起排时节气按月输出，岁首起排时按气输出\n"
	               "历名前朝代仅为首次颁行朝代，详细状况参见各历说明"
	              )

def lbInfo(ui):
	select_lb = selectLB(ui)
	if not select_lb:
		basicInfo(ui)
	for li in select_lb:
		li.sy = li.ly - li.jys * li.yf
		sym = '太极上元' if li.lm == '太初历' else '上元'
		ui.edit.append('{}：  {}{} {}，近元{}年\n        历元{}，正月建{}，岁首建{}'.format(li.lm, sym, li.sy, ganzhiYear(li.sy), li.ly, jieqi[li.qly], dizhi[li.jian], dizhi[li.suis]))
		# ui.edit.append(li.lm + '：  上元' + '  近元' + str(li.ly) + '\n        历元' + jieqi[li.qly] + '，正月建' + dizhi[li.jian])
		if li.lm == '鲁历1': ui.edit.insertPlainText('，蔀首闰余1')
		elif li.lm == '鲁历0': ui.edit.insertPlainText('，蔀首闰余0')
		ui.edit.append('        岁实：365又{}/{}日，即{}\n        朔策：{}又{}/{}日，即{}'.format(
			divide(li.sz, li.qrf)[1], li.qrf, round(li.sui,8), li.sdy, li.sxy, li.srf, round(li.yue,8)))
		bxqk = getLCLF(3, li.lm)
		if bxqk != '': ui.edit.append('        颁行年代：' + getLCLF(3, li.lm))
		else: ui.edit.append('        颁行情况：未知')
	ui.edit.append("")

def RBN(ui):
	try:
		year = int(ui.txtLyear.text())
		select_lb = selectLB(ui)
		for li in select_lb:
			li.syjn = li.getSyjn(year)
			if li.type < 5 and li.type != 3:
				li.rbn = li.syjn % li.bf  # 入蔀年
				if li.type == 1:
					li.rbs = li.syjn % li.jf // li.bf  # +1入蔀数
				else:
					li.rbs = li.syjn % li.yf // li.bf  # +1入蔀/纪数
				bsgz = gz[(li.bsgz[li.rbs]) % 60]
				rzs = li.rbn // li.zs
				rzn = li.rbn % li.zs
				ui.edit.append('{0}\t  {1:{4}<3}  上元{2}，积年{3} 算外'.format(gzYear(year), li.lm, ganzhiYear(li.sy), li.syjn, chr(12288)))
				if len(li.bm) > 1:
					ui.edit.append('\u3000\u3000入 {}{}{}第{}年\u3000即第{}章第{}年'.format(li.bm[li.rbs+1], li.bm[0], bsgz, li.rbn + 1, rzs + 1, rzn + 1))
				else:
					ui.edit.append('\u3000\u3000入 {}({:2d}){}第{:2d}年\u3000即第{:2d}章第{:2d}年'.format(bsgz, li.rbs + 1, li.bm[0], li.rbn + 1, rzs + 1, rzn + 1))
			else: ui.edit.append('{0}\t  {1:{4}<3}  上元{2}，积年{3} 算外'.format(gzYear(year), li.lm, ganzhiYear(li.sy), li.syjn, chr(12288)))
	except:
		ui.edit.append(ErrorHint)
	if len(select_lb) == 0: ui.edit.insertPlainText("（本项只计算古代历法，请先选取）")
	ui.edit.append("")

def TZS(ui):
	year = int(ui.txtLyear.text())
	select_lb = selectLB(ui)
	for li in select_lb:
		ydy, yxy, qdy, qxy, qxf = tzs(li, year, 0)
		if li.type > 4: ps2ds(li, 0)
		ui.edit.append('{} {}\t  天正朔{}{}   大余{:2d} 小余{:5>d}\n({})\t天正冬至{}   大余{:2d} 小余{:5>d}'
		                .format(gzYear(year)[:-4], li.lm, li.dygz(ydy), ['','*'][li.jsb[0][0]], (ydy-li.jsb[0][0])%60, yxy, ganzhiYear(year), li.dygz(qdy), qdy, qxy))
	if ui.tqlf[0].isChecked():
		dzs = dzs_find(year)
		dz = equinox_solstice(year-1, 270)
		ui.edit.append("{}  实历前冬至朔： {} {}\n({})\t前冬至： {} {}".format(gzYear(year)[:-4], dzs, ganzhiDate(dzs), ganzhiYear(year), dz,  ganzhiDate(dz)))
	ui.edit.append("")

def gldzsJD(li, liList, year, flag=False):
	dzs = dzs_find(year, 1)
	dzscy = PhaseJD(dzs, 1)
	m = -li.ssy if li.ssy < 0 else 0
	result = glDzsJD(li.dygz(liList[m][3]), dzs, dzscy, flag)
	if flag: result = list(result)
	else: result = [result]
	for i in range(m):
		result[0] -= dxy[liList[m - i - 1][2]]
	if flag: return [result[0]], result[1]
	else: return result

def yearlyCalendar(year, ym, shuo):
	ym1, shuo1 = currentCalendar(year + 1)
	m1 = 2 if ym[2] == '正月' else 3
	m2 = 2 if ym1[2] == '正月' else 3
	ym = ym[m1:] + ym1[:m2+1]
	shuo = shuo[m1:] + shuo1[:m2 + 1]
	return ym, shuo


def SWDXY(ui, kind):
	year = eval(ui.txtLyear.text())
	select_lb = selectLB(ui)
	if len(select_lb) == 0: ui.edit.insertPlainText("\t" + gzYear(year))
	for li in select_lb:
		floor = '      ' if li.type > 3 or li.yfa / 2 == li.yfa // 2 else '+' + str(round(li.yfa / 2 - li.yfa // 2,2)) + '   '
		if kind == 0: ui.edit.append('{}\t{} 大余 小余  合朔时刻    日期   JDN'.format(gzYear(year), li.lm))
		elif kind == 1: ui.edit.append('{}\t  {}   望   大余  小余{}日期   JDN'.format(gzYear(year), li.lm, floor))
		liList = calendar(li, year, LYSSstate[0])
		glsJD, yxc = gldzsJD(li, liList, year, True)
		if kind == 1: li.wdy, li.wxy = qyfs(li.yfa, li.srf, 1 / 2)
		p = 0
		if LYSSstate[0] and len(liList) == 15:  q = 4 if liList[13][0] != '闰' and liList[14][0] != '闰' else 5
		else: q = 4 if liList[1][0] != '闰' and liList[2][0] != '闰' else 5
		for j in range(len(liList)):
			month = liList[j][0] + yuefen[(liList[j][1]-li.jzy)%12] + liList[j][2]
			ydy, yxy = liList[j][3:5]
			glsJD.append(glsJD[j] + dxy[liList[j][2]])
			if kind == 0:
				if (LYSSstate[0] and j < 6 and liList[j][1] < 2) or (j == 0 and liList[j][0] == '闰'):
					p = -2
					continue
				ui.edit.append('{0:{5}>{10}}\u3000{1}{9}\u3000{2:2d}\u3000{3:>{6}}  {4}  {7} {8}'.format(
					month, li.dygz(ydy), (ydy-li.jsb[j][0])%60, yxy, heshuo(yxy,li.srf), chr(12288), len(str(li.srf)), JD2date(glsJD[j])[:-9], JDN(glsJD[j]), ['朔',' *'][li.jsb[j][0]], q))
			elif kind == 1:
				if LYSSstate[0] and j < 6 and liList[j][1] < 2: continue
				if li.type > 4 or li.lm == '戊寅历':
					wdy, wxy = ps2ds(li, j + 0.5)
				else:
					wdy, wxy = qy(ydy, yxy, li.srf, li.wdy, li.wxy)[:2]
					txw(li, wxy, j + 0.5)
				glwJD = glsJD[j] + (wdy+li.jsb[j][2] - ydy) % 60
				ui.edit.append('{0:{6}>{11}}  {1}{9}  {2}日{3}{10}{4:2d}  {5:>{7}}  {8}  {12}'.format(
					month, li.dygz(ydy), nlrq[(wdy+li.jsb[j][2] - ydy) % 60], li.dygz(wdy+li.jsb[j][2]), wdy, int(wxy), chr(12288), len(str(li.srf)), JD2date(glwJD)[:-9], ['朔',' *'][li.jsb[j][0]], ['  ','* '][li.jsb[j][2]], q, JDN(glsJD[j])))
	if ui.tqlf[0].isChecked():
		ym, shuo = currentCalendar(year, -1)
		syym = '前冬至'
		if LYSSstate[0]:
			ym, shuo = yearlyCalendar(year, ym, shuo)
			syym = '  正月'
		dzsw = PhaseJD(shuo[0], 2) if kind == 1 else shuo[0]
		for k in range(len(shuo)):
			if k == 0:
				ui.edit.append("实历{}{}： {:<21}{}".format(syym, ['朔', '望'][kind], JD2date(dzsw), ganzhiJD(dzsw)))
				if kind == 1: ui.edit.insertPlainText("{}".format(JDN(dzsw) - JDN(shuo[0])+1))
				ui.edit.insertPlainText('  ' + str(JDN(dzsw)))
			else:
				JD = shuo[k]
				if kind == 1:
					JDE = PhaseJDE(JD + 14, kind * 2)
					JD = td2jd(JDE)
				date = JD2date(JD)
				ui.edit.append("  {0:{4}>4}{1}： {2:<21}{3}".format(ym[k], ['朔', '望'][kind], date, ganzhiDate(date), chr(12288)))
				if kind == 1: ui.edit.insertPlainText("{}".format(JDN(JD)-JDN(shuo[k])+1))
				ui.edit.insertPlainText('  ' + str(JDN(JD)))
			# if len(select_lb) and kind == 0: ui.edit.insertPlainText("       {:2d}".format(k-yxc+1))
	ui.edit.append("")

def XDXY(ui):
	year = int(ui.txtLyear.text())
	select_lb = selectLB(ui)
	if len(select_lb) == 0: ui.edit.insertPlainText(gzYear(year) + "\t实历")
	for li in select_lb:
		liList = calendar(li, year, LYSSstate[0])
		glsJD = gldzsJD(li, liList, year)
		length = lenXY(li.yfa, 4)
		if LYSSstate[0] and len(liList) == 15:  q = 4 if liList[13][0] != '闰' and liList[14][0] != '闰' else 5
		else: q = 4 if liList[1][0] != '闰' and liList[2][0] != '闰' else 5
		ui.edit.append(gzYear(year) + '    ' + li.lm + '\t  大余   小余    日期     JDN')
		li.sxdy, li.sxxy = qyfs(li.yfa, li.srf, 1/4)
		li.xxdy, li.xxxy = qyfs(li.yfa, li.srf, 3/4)
		for j in range(len(liList)):
			month = liList[j][0] + yuefen[(liList[j][1]-li.jzy)%12] + liList[j][2]
			ydy, yxy = liList[j][3:5]
			if li.type > 4 or li.lm == '戊寅历':
				sxdy, sxxy = ps2ds(li, j + 0.25)
				xxdy, xxxy = ps2ds(li, j + 0.75)
			else:
				sxdy, sxxy = qy(ydy, yxy, li.srf, li.sxdy, li.sxxy)[:2]
				xxdy, xxxy = qy(ydy, yxy, li.srf, li.xxdy, li.xxxy)[:2]
			glsJD.append(glsJD[j] + dxy[liList[j][2]])
			if LYSSstate[0] and j < 6 and liList[j][1] < 2: continue
			ui.edit.append('{0:{5}>{9}}{7} 上弦  {1}日{2}{8} {3:2d} {4:>{6}}' .format(month, nlrq[(sxdy+li.jsb[j][1]-ydy)%60], li.dygz(sxdy+li.jsb[j][1]), sxdy, round(sxxy,2), chr(12288), length, [' ','*'][li.jsb[j][0]], [' ','*'][li.jsb[j][1]],q))
			ui.edit.insertPlainText("  " + JD2date((glsJD[j] + (sxdy+li.jsb[j][1] - ydy) % 60))[:-9] + '  ' + str(JDN(glsJD[j] + (sxdy+li.jsb[j][1] - ydy) % 60)))
			ui.edit.append(' '*(q*2+2) + '下弦  {}日{}{} {:2d} {:>{}}'.format(nlrq[(xxdy+li.jsb[j][3]-ydy)%60], li.dygz(xxdy+li.jsb[j][3]), [' ','*'][li.jsb[j][3]], xxdy, round(xxxy,2), length))
			ui.edit.insertPlainText('  ' + JD2date((glsJD[j] + (xxdy+li.jsb[j][3] - ydy) % 60))[:-9] + '  ' + str(JDN(glsJD[j] + (xxdy+li.jsb[j][1] - ydy) % 60)))
	if ui.tqlf[0].isChecked() and not len(select_lb):
		ym, shuo = currentCalendar(year, -1)
		if LYSSstate[0]:
			ym, shuo = yearlyCalendar(year, ym, shuo)
		for j in range(len(shuo)):
			for k in range(2):
				JDE = PhaseJDE(shuo[j], 1 + k * 2)
				JD = td2jd(JDE)
				if k == 0: ui.edit.append("{0:{1}>4}".format(ym[j], chr(12288)))
				else: ui.edit.append("")
				ui.edit.insertPlainText('{}{}弦：{}  {}{:2d}  {}'.format(['  ', ' '*10][k], ['上','下'][k], JD2date(JD), ganzhiJD(JD), JDN(JD)-JDN(shuo[j])+1, JDN(JD)))
	ui.edit.append("")


def QDXY(ui, kind):
	year = int(ui.txtLyear.text())
	select_lb = selectLB(ui)
	name = ["中气", "节气", "24节气", "分至", "八节"][kind]
	n = 24 // [12, 12, 24, 4, 8][kind]
	rem = 1 if kind == 1 else 0
	first = 3 if LYSSstate[0] else 0  # 寅正节气起自立春
	jqDate = []
	for i in range(32):  # 起立冬终雨水（实历多输出此年雨水）
		angle = (225 + 15 * i) % 360
		if i < 4 and angle <= 270: date = SolarTermsDate(year - 1, angle)
		elif i > 25 and angle > 270: date = SolarTermsDate(year + 1, angle)
		else: date = SolarTermsDate(year, angle)
		jqDate.append(date)
	if select_lb:
		for li in select_lb:
			liList = calendar(li, year, LYSSstate[0], True)  # 按月排序的历表，有闰时输出13月
			qx = 0  # 起冬至
			jqx = liList[0][-1][-1]  # 首月节气序
			liJqDate = jqDate   # 各历法对应节气日期表
			if li.ssy != -1:
				liJqDate = liJqDate[2:]  # 古历表与实历表对齐（大雪起算）
			if jqx == 0: liJqDate = liJqDate[1:]  # 大雪/小寒起算
			jqb = []  # 按节气排序的历表
			for j in range(len(liList)):
				for k in range(2):
					if k == 0:  # 中气
						ydy, yxy, qdy, qxy = liList[j][3:7]
						leap = False
						if qdy == None:
							leap = True
							continue
						qrq = yuefen[(liList[j][1] - li.jzy) % 12] + nlrq[(qdy - ydy) % 60]
						date = glDate(year, liJqDate[qx], gz.index(li.dygz(qdy)))[0]
						jqb.append([qrq, qdy, qxy, date])
					elif k == 1:  # 节气
						ydy = liList[j][3]
						qdy, qxy = liList[j][-1][0:2]
						if qdy == None: continue
						qrq = liList[j][0] + yuefen[(liList[j][1] - li.jzy) % 12] + nlrq[(qdy - ydy) % 60]
						date = glDate(year, liJqDate[qx], gz.index(li.dygz(qdy)))[0]
						if nlrq.index(qrq[-2:]) > nlrq.index(jqb[-1][0][-2:]) or leap:  # 节气在中气后或有闰情况下追加
							jqb.append([qrq, qdy, qxy, date])
						else: jqb.insert(-1, [qrq, qdy, qxy, date])
					qx += 1
			# 输出部分
			ui.edit.append('{}{:>4} {}\t大余  小余   公历日期'.format(gzYear(year), name, li.lm))
			if ui.tqlf[0].isChecked(): ui.edit.insertPlainText('\t    实历')
			if LYSSstate[0]: first -= jqx
			for q in range(qx - 27 + (3 - first) - (len(liList) - 12)): jqb.pop()  # 截止到十月
			x=0
			for m in range(first, len(jqb)):  # 按月输出
				if (m + jqx) % n == rem:
					if select_lb:
						ui.edit.append('{7:2d} {0} {1:{6}>6}  {2} {3:>4} {4:>6}  {5}'.format(
							jieqi[(m+jqx+li.ssy*2)%24], jqb[m][0], li.dygz(jqb[m][1]), jqb[m][1], jqb[m][2], jqb[m][3], chr(12288), x))
					if ui.tqlf[0].isChecked():
						ui.edit.insertPlainText('  ' + liJqDate[m] + ' ' + ganzhiDate(liJqDate[m]))
					else: ui.edit.insertPlainText('  ' + str(JDN(date2JD(liJqDate[m]))))
					x+=1
	else:  # 未选历法时单独生成实历节气表
		if ui.tqlf[0].isChecked():
			ui.edit.insertPlainText('    ' + gzYear(year) + '  实历' + name)
			if kind == 1 and not LYSSstate[0]: first -= 1  # 历元起大雪
			num = 0
			for m in range(first+2, first+28):
				if m % n == rem:
					num += 1
					ui.edit.append(str(num).rjust(2, ' ') + '  ' + jieqi[(m-2)%24] + '    ' + jqDate[m+1] + '  ' + ganzhiDate(jqDate[m+1]) + '  ' + str(JDN(date2JD(jqDate[m+1]))))
	ui.edit.append("")

def setLeap(ui):
	select_lb = selectLB(ui)
	if len(select_lb) > 1: select_lb = [select_lb[0]]
	for li in select_lb:
		for i in range(4):
			ui.cblLzr.setItemData(i, QVariant(1 | 32), Qt.UserRole - 1)
		if li.type > 1:  # 不设年终闰
			ui.cblLzr.setItemData(3, QVariant(0), Qt.UserRole - 1)
		if li.type > 2:  # 不设年中闰
			ui.cblLzr.setItemData(2, QVariant(0), Qt.UserRole - 1)

def Leap(ui):
	year = int(ui.txtLyear.text())
	select_lb = selectLB(ui)
	for li in select_lb:
		ui.edit.append(str(year) + li.lm)
		flag = False
		if ui.cblLzr.currentText() in ['无中闰', '全部']:  # 无中闰
			liList = calendar(li, year, LYSSstate[0])
			for j in range(len(liList)):
				if LYSSstate[0] and liList[j][1] < 2 and j < 3: continue
				if liList[j][5] == None:
					flag = True
					ui.edit.insertPlainText('\t无中闰' + yuefen[liList[j][1]-li.jzy])
					break
		if ui.cblLzr.currentText() in ['闰余法', '年终闰', '全部'] and li.type < 3:
			syx = 2 if LYSSstate[0] else 0
			tzs(li, year)
			yry = li.ry * 12
			if yry != 0:
				zry = (li.zq - yry) // li.zr
				if zry == 12: zry -= 1
				if 0+syx <= zry < 12+syx:
					flag = True
					if ui.cblLzr.currentText() in ['闰余法', '全部']: ui.edit.insertPlainText('\t年中闰{}（闰余{}）'.format(yuefen[int(zry) - li.jzy], yry+li.zr*int(zry+1)))
					if ui.cblLzr.currentText() in ['年终闰', '全部'] and li.type == 1:
						if li.lm == '颛顼历':
							ui.edit.insertPlainText('\t后九月（闰余' + str(li.ry) + '）')
						else:
							ui.edit.insertPlainText('\t再十二月（闰余' + str(li.ry) + '）')
		if flag == False:
			ui.edit.insertPlainText('\t无闰\t（闰余' + str(li.ry) + '）')
	if len(select_lb) == 0: ui.edit.insertPlainText("（本项只计算古代历法，请先选取）")
	ui.edit.append("")


def monthlyCalendar(ui):
	try:
		year = int(ui.txtLyear.text())
		m = 0
		flag = False
	except:  # 指定月份
		year, m = GetDate(ui.txtLyear.text())[:2]
		flag = True
	select_lb = selectLB(ui)
	eraname = eranameSearch(ui, year)
	ui.edit.append(gyjnBC(year) + '年：' + eraname + '\n')
	for li in select_lb:
		liList = calendar(li, year, LYSSstate[0])
		run = "无闰"
		first = 2 if LYSSstate[0] else 0  # 输出首月序（寅正）
		for i in range(len(liList)):
			if liList[i][0] == "闰":
				if i > 2: run = liList[i][0] + yuefen[(liList[i][1] - li.jzy) % 12]
				else: m += 1  # 闰月序
		glsJD = gldzsJD(li, liList, year)
		for i in range(len(liList)):
			glsJD.append(glsJD[i] + dxy[liList[i][2]])
			if liList[i][0] == "闰": first += 1  # 正月前有闰
			if i >= first:
				month = liList[i][0] + yuefen[(liList[i][1] - li.jzy) % 12]
				if flag and i != (m + 1 + [-2,-1,0][first]): continue  # 指定月份
				ui.edit.insertPlainText('  ' + gzYear(year) + '  ' + li.lm + '(寅正)  ' + month + ['','*'][li.jsb[i][0]] + '（本年' + run + '）\n')
				for j in range(10):
					for k in range(3):
						if j == 9 and k == 2 and liList[i][2] == '小': break
						ui.edit.insertPlainText(nlrq[k*10+j] + " " + JD2date(glsJD[i]+k*10+j)[-14:-9] + " " + li.dygz((liList[i][3]+k*10+j)%60) + "   ")
					ui.edit.append("")
	if not len(select_lb) and ui.tqlf[0].isChecked():
		ym, shuo = currentCalendar(year)
		ym1, shuo1 = currentCalendar(year+1)
		i = 0
		while ym1[i] != '正月':
			ym.append(ym1[i+1])
			shuo.append(shuo1[i+1])
			i += 1
		for i in range(len(shuo)-1):
			ui.edit.insertPlainText('  ' + gzYear(year) + '    现行农历（寅正）       ' + ym[i] + '\n')
			for j in range(10):
				for k in range(3):
					if DateCompare(shuo[i+1], shuo[i]+k*10+j+1):
						ui.edit.insertPlainText(nlrq[k*10+j] + " " + JD2date(shuo[i]+k*10+j)[-14:-9] + " " + ganzhiJD(shuo[i]+k*10+j) + "   ")
				ui.edit.append("")


def qishuoTable(ui):
	year = int(ui.txtLyear.text())
	select_lb = selectLB(ui)
	for li in select_lb:
		liList = calendar(li, year, LYSSstate[0], True)
		li.wdy, li.wxy = qyfs(li.yfa, li.srf, 1 / 2)
		li.sxdy, li.sxxy = qyfs(li.yfa, li.srf, 1 / 4)
		li.xxdy, li.xxxy = qyfs(li.yfa, li.srf, 3 / 4)
		ui.edit.append(gzYear(year) + '    （*为进朔或退弦望，数字为月内日期）' + '\n  ' + li.lm + '   朔' + '   上弦    望      下弦       中气         节气')
		if LYSSstate[0] and len(liList) == 15:  q = 4 if liList[13][0] != '闰' and liList[14][0] != '闰' else 5
		else: q = 4 if liList[1][0] != '闰' and liList[2][0] != '闰' else 5
		qx = 0
		for j in range(len(liList)):
			month = liList[j][0] + yuefen[(liList[j][1] - li.jzy) % 12] + liList[j][2]
			ydy, yxy, qdy, qxy, jdxy = liList[j][3:]
			if j == 0: jdy, jxy, jqx = jdxy
			else: jdy, jxy = jdxy
			if li.type > 4 or li.lm == '戊寅历':
				sxdy, sxxy = ps2ds(li, j + 0.25)
				xxdy, xxxy = ps2ds(li, j + 0.75)
				wdy, wxy = ps2ds(li, j + 0.5)
				sxdy = (sxdy + li.jsb[j][1]) % 60
				xxdy = (xxdy + li.jsb[j][3]) % 60
				wdy = (wdy + li.jsb[j][2]) % 60
			else:
				sxdy, sxxy = qy(ydy, yxy, li.srf, li.sxdy, li.sxxy)[:2]
				xxdy, xxxy = qy(ydy, yxy, li.srf, li.xxdy, li.xxxy)[:2]
				wdy, wxy = qy(ydy, yxy, li.srf, li.wdy, li.wxy)[:2]
			if qdy == None:
				qm, qgz, qrq = '      ', ' 无 ', ' '
			else:
				qm, qgz, qrq = '('+jieqi[(qx+li.ssy)*2%24]+')', li.dygz(qdy), (qdy-ydy)%60+1
				qx += 1
			if jdy == None:
				jqm, jgz, jrq = '      ', ' 无 ', ' '
			else:
				jqm, jgz, jrq = '(' + jieqi[((jqx + 1 + li.ssy) * 2 - 1) % 24] + ')', li.dygz(jdy), (jdy - ydy) % 60 + 1
				jqx += 1
			if LYSSstate[0] and j < 6 and liList[j][1] < 2: continue
			ui.edit.append("{0:{7}>{10}}{16} {1}  {2}{11}{17} {3}{12}{18} {4}{13}{19} {8}{5}{14:>2}  {9}{6}{15:>2}".format(
				month, li.dygz(ydy), li.dygz(sxdy), li.dygz(wdy), li.dygz(xxdy), qgz, jgz, chr(12288), qm, jqm, q, (sxdy-ydy)%60+1,
				(wdy-ydy)%60+1, (xxdy-ydy)%60+1, qrq, jrq, [' ','*'][li.jsb[j][0]], [' ','*'][li.jsb[j][1]], [' ','*'][li.jsb[j][2]], [' ','*'][li.jsb[j][3]]))
	if len(select_lb) == 0: ui.edit.insertPlainText("（本项只计算古代历法，请先选取）")
	ui.edit.append("")
