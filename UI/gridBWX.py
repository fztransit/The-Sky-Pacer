from AncientAstro import *
from AstroCalc import *

def planetAllSelect(ui):
	flag = False
	for i in range(5):
		if not ui.planetGroup.button(i).isChecked():  # 未选中状态
			flag = True
			ui.planetGroup.button(i).setChecked(True)
	if flag == False:
		for i in range(5):
			ui.planetGroup.button(i).setChecked(False)


def stlSuiShu(ui):
	try:
		year = GetDate(ui.editYear.text())[0]
		ui.edit.append(SuiShu(year))
		date = SolarTermsDate(year-1,270,0)
		JDE = ut2td(date)
		jL = PlanetLBR('木', JDE)[0]
		src, rcd = rcd_calc(jL, 1)
		ui.edit.append('\t是年真实前冬至日期为：' + UTdate(date,8)[:-9] + '\n\t此时木星真实位置为：' + src + str(round(rcd,4)) + '度\n')
	except:
		ui.edit.append('输入错误，请输入年份\n')

def ChenShiXian(ui):
	try:
		year = GetDate(ui.editYear.text())[0]
		for i in range(5):
			if ui.planetGroup.button(i).isChecked():
				p = ui.planetGroup.button(i).text()
				chenxian, jd, dzjr, cjzc, rzd = JiShu(int(year),p)
				ui.edit.append(chenxian)
				if ui.planetGroup.button(7).isChecked():
					date = JD2date(jd - 8/24)
					JDE = ut2td(date)
					sL = sunLBR(JDE)[0]
					pL = PlanetLBR(p, JDE)[0]
					qrd = {'金': 13, '木': 13, '水': 15, '火': 15, '土': 15, }
					if sL - pL < qrd[p]: zt = '伏'
					if sL - pL >= qrd[p]: zt = '现'
					ui.edit.append('  *三统历晨始见日太阳真实黄经为%d°\n   %s星真实黄经为%d°\t 表现为：%s' % (round(sL), p, round(pL), zt))
					JDE, pL, sL = HeliacalRiseSet(year-1, p) # ut8时间
					T = (JDE - 2451545) / 36525
					for star in esbx: StarPosition(star, T)
					e = nutation(T)[2]
					for star in esbx: star.ra, star.dec = eq2ec(star.ra, star.dec, e)  # 二十八宿黄经
					srx1, rxd1 = rxd_calc(sL)
					srx2, rxd2 = rxd_calc(pL)
					ui.edit.append('  *实历晨始见日为：{}，（去日{}°）\n   此时太阳黄经{}({}{})  {}星黄经{}({}{})'.format(td2date(JDE)[:-9],qrd[p], round(sL,1),srx1[1],round(rxd1,1),p,round(pL,1),srx2[1],round(rxd2,1)))
	except:
		ui.edit.append('输入错误，请输入年份')
	ui.edit.append("")

def WuBu(ui):
	try:
		date = ui.editYear.text()
		for i in range(5):
			if ui.planetGroup.button(i).isChecked():
				p = ui.planetGroup.button(i).text()
				xingdu = BuShu(date, p)
				ui.edit.append(UTdate(date, -1)[:-9] + '夜半（' + ganzhiDate(date) + '）   ' + xingdu)
				if ui.planetGroup.button(7).isChecked():
					JDE = ut2td(date)
					sL = sunLBR(JDE)[0]
					pL = PlanetLBR(p, JDE)[0]
					ui.edit.append('   是日太阳真实黄经为%d° %s星真实黄经为%d°' % (round(sL), p, round(pL)))
	except:
		ui.edit.append('输入错误，请输入日期')
	ui.edit.append("")

def HeChenXingDu(ui):
	try:
		year, month = GetDate(ui.editYear.text())[:2]
		ui.edit.append(TongShu(year, month))
		if ui.planetGroup.button(7).isChecked():
			if month == 1:
				year -= 1
				month = 12
			else:
				month -= 1
			JD = date2JD(str(year) + '/' + str(month))
			JDE = PhaseJDE(JD, 0)
			date = td2date(JDE)
			T = (JDE - 2451545) / 36525
			ra = sunLBR(JDE)[3]
			for star in esbx: StarPosition(star, T)
			srx, rxd = rxd_calc(ra)
			ui.edit.append('实朔时间为：'+ date + '，合辰在' + srx[1:] + str(round(rxd)) + '度\n')
	except:
		ui.edit.append('输入错误，请输入年月（此项冬至月为1月，依次后推）\n')

def stlJiaoShi(ui):
	try:
		year = GetDate(ui.editYear.text())[0]
		shuchu = JiaoShi(year)
		ui.edit.append(shuchu)
	except:
		ui.edit.append('输入错误，请输入年份\n')
