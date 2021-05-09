from AstroCalc import *

def ChenHun(ui):  # 日升日落
	try:
		nian = int(ui.editYear.text())
		flag = True
	except:
		date = UTdate(ui.editYear.text(), -1)
		flag = False  # 指定日期计算
	diqu, long, lat = GetGeoCoord(ui)
	for s in stTable:
		if s == "全年": continue  # 无效值
		if ui.cblSun.currentText() == s or ui.cblSun.currentText() == "全年":  # 查找或遍历
			if flag == True:
				date = selectSTDate(s, nian)[0]
				ui.edit.append("{}{}：".format(nian, s))
			else:
				ui.edit.append("")
			ui.edit.insertPlainText("{}  （{}{}°E, {}°N）".format(date[:-9], diqu, round(long, 1), round(lat, 1)))
			for i in range(5):
				Rt, St, Ut, Lt = rst(date, long, lat, sandhyaLat[sandhya[i]])
				zhou = round((date2JD(St) - date2JD(Rt)) * 24, 1) % 24
				ye = round((date2JD(Rt) + 1 - date2JD(St)) * 24, 1) % 24
				if i == 0:
					ui.edit.append(' 上中天：' + Ut.split(' ')[1] + ' 下中天：' + Lt.split(' ')[1] + '         地方平时')
					ui.edit.append(
						"   日出：{}   日没：{}  昼{:4.1f}h 夜{:4.1f}h".format(Rt.split(' ')[1], St.split(' ')[1], zhou, ye))
				else:
					ui.edit.append(
						" {}晨：{} {}昏：{}  昼{:4.1f}h 夜{:4.1f}h".format(sandhya[i][:2], Rt.split(' ')[1], sandhya[i][:2], St.split(' ')[1], zhou, ye))
		if ui.cblSun.currentText() == s or (flag == False and ((ui.cblSun.currentText() in stTable and ui.cblSun.currentText() == s) or ui.cblSun.currentText() == "全年")): break
	ui.edit.append("")


def MoonRiseSet(ui):
	diqu, long, lat = GetGeoCoord(ui)
	date_table = []
	date_name = []
	phase_name = ['朔', '上弦', '望', '下弦']
	if ui.editYear.text().count('/') == 2:  # 日期格式
		date_table.append(UTdate(ui.editYear.text(), -1))
		date_name.append('')
	elif ui.cblMoon.currentText() in phases[:5]:
		date = ui.editYear.text()
		for m in phase_name:
			if ui.cblMoon.currentText() == '全部月相' or ui.cblMoon.currentText() == m:
				date = PhaseDate(date, phase_name.index(m))
				date_table.append(date)
				if ui.cblMoon.currentText() == '全部月相' and m != '朔':
					date_name.append('朔后' + m)
				else:
					date_name.append(m)
	elif ui.cblMoon.currentText() == '指定节气':
		nian = int(ui.editYear.text().split('/')[0])
		for s in [stTable[0]] + stTable[2:]:
			if ui.cblSun.currentText() == '全年' or ui.cblSun.currentText() == s:
				date_table.append(selectSTDate(s, nian)[0])
				date_name.append(s)
	month_name = ''
	for k in range(len(date_table)):
		date = date_table[k]
		Rt, St, Ut, Lt = rst(date, long, lat, 0.125)  # ut8时
		if k == 0 and ui.cblMoon.currentText() != '指定节气': month_name = str(date[1]) + '月'
		ui.edit.append("{}年{} {}  {} （{}{}°E, {}°N）".format(GetDate(date)[0], month_name, date_name[k], date[:-9], diqu, round(long, 1), round(lat, 1)))
		ui.edit.append('地方平时\t    月出： ' + Rt + '\n\t    月没： ' + St + '\n\t  上中天： ' + Ut + '\n\t  下中天： ' + Lt)
	ui.edit.append("")


def HDZX(ui, kind):  # 0为旦中星，1为昏中星，3为夜半中星
	diqu, gL, lat = GetGeoCoord(ui)
	head = True
	year, flag, date, JDE, T = getInput(ui.editYear.text())
	for s in [stTable[0]] + stTable[2:]:
		if ui.cblSun.currentText() == '全年' or ui.cblSun.currentText() == s:
			if flag == True: date, JDE, T = selectSTDate(s, year)  # JDE儒略世纪数，忽略date为ut8时
			for star in esbx: StarPosition(star, T)  # 二十八宿赤经
			RSt = rst(date, gL, lat, sandhyaLat[ui.cblSandhya.currentText()])[kind]  # 古历旦/昏/夜半时
			JD = date2JD(RSt)
			JDE = jd2td(JD, gL)
			angle = sunLBR(JDE)[3]  # 昏时赤经
			ra = (jd2st(JD - gL / 360) + gL) % 360  # 中天星赤经=昏旦时本地恒星时
			srx, rxd = rxd_calc(ra)  # 代入今度比较
			select = '(今度)'
			hdzxd = (ra - angle) % 360
			if ui.lstDegree.currentRow() == 1:  # 古度表示
				ra /= gdzh
				rxd /= gdzh
				hdzxd /= gdzh
				select = '(古度)'
			rsName = ['旦', '昏', '', '夜半'][kind]
			if head:
				ui.edit.append(
					'{0}年  {2}{3}{4}    （{1}{5:5.1f}°E, {6:4.1f}°N）\n  节气    日期     {3}中星赤经  {3}中星  {3}中星度'.format(
						GetDate(ui.editYear.text())[0], diqu, ui.cblSandhya.currentText()[:2], rsName, select, gL, lat))
				head = False
			if flag == False: s = '  无  '
			ui.edit.append(
				'{0:{6}>3}  {1}    {2:6.2f}   {3}{4:4.1f}   {5:6.2f}'.format(s, date[:-9], ra, srx[1], rxd, hdzxd,  chr(12288)))
		if ui.cblSun.currentText() == s or (flag == False and ((ui.cblSun.currentText() in stTable and ui.cblSun.currentText() == s) or ui.cblSun.currentText() == "全年")): break  # 指定日期计算完成或查找到后退出循环
	ui.edit.append("")


def hdzxYear(ui, kind):
	diqu, long, lat = GetGeoCoord(ui)
	try:
		try:
			rxd = int(ui.txtHdzxYear.text())  # 输入为古度，计算需转为今度
			num = 2
		except:
			rxd = 0
			num = 1
		if ui.cbZXstar.isChecked():
			hx = hxzb[ui.cblStar.currentText()[:ui.cblStar.currentText().find(' ')]]
			xm = ui.cblStar.currentText()[:ui.cblStar.currentText().find(' ')] + '星'
			num = 1
		else:
			hx = esbxzb[ui.cblMassion.currentText()[0]]
			xm = ui.cblMassion.currentText()[0] + '宿距星'
		t2 = int(ui.editYear.text()) / 100 - 20  # 儒略世纪数
		year = []
		for i in range(num):
			if ui.cblSun.currentText() == '前冬至':
				angle = (270 - (rxd + i * 1) * gdzh) % 360  # 黄经
			else:
				angle = (270 + jieqi.index(ui.cblSun.currentText()) * 15 - (rxd + i * 1) * gdzh) % 360
			e = 84381.448 / 3600
			angle, dec = ec2eq(angle, 0, e)  # 赤经，赤纬
			# angle = (angle + 90) % 360 # 中天星赤经：中天后90°（日没恒为6h）
			h = sandhyaLat[ui.cblSandhya.currentText()]
			if h == -7:
				h = -50 / 60
				H = HourAngle(h, dec, lat) + 2.5 / 100 * 360
			else:
				H = HourAngle(h, dec, lat)  # - HourAngle(0, dec, lat) # 地平纬度时角差值
			if kind == 0: angle = (angle + H) % 360  # 昏时中天星赤经 = 昏时本地恒星时 - 中天星时角0° = 太阳昏时赤经（不同年份误差小于1°） + 太阳昏时时角
			if kind == 1: angle = (angle - H) % 360  # 旦时中天星赤经
			year.append(YearItera(hx, angle, t2))  # 恒星在该时角的时间
			t2 = int((year[i]).split('\n')[0]) / 100 - 20  # 计算结果作为下次估值
		rsName = ['昏', '晨'][kind]
		if num == 1:
			ui.edit.append(
				'{}地区：{}赤经(今度){:.1f}° \n\t在({}){}时中天年份为：{}'.format(diqu, xm, angle, ui.cblSandhya.currentText()[:2], rsName, year[0]))
		else:
			ui.edit.append(
				'{}地区：{} {}{}度（赤经(今度){}°）\n\t于({})昏时中天年代范围为：{}到{}'.format(diqu, ui.cblSun.currentText(), xm, gdb[rxd], round(angle, 1), ui.cblSandhya.currentText()[:2], year[0], year[1]))
	except:
		ui.edit.append('计算此项需给出年代估值、太阳节气及所在星宿')
	ui.edit.append("")


def SunPosition(ui):  # 已知太阳位置逆求时间
	try:
		hx = esbxzb[ui.cblMassion.currentText()[0]]
		t2 = int(ui.editYear.text()) / 100 - 20  # 儒略世纪数
		year = []
		try:
			rxd = int(ui.txtHdzxYear.text())
			num = 2
		except:
			rxd = 0
			num = 1
		for i in range(num):
			if ui.cblSun.currentText() == '前冬至':
				angle = (270 - (rxd + i * 1) * gdzh) % 360
			else:
				angle = (270 + jieqi.index(ui.cblSun.currentText()) * 15 - (rxd + i * 1) * gdzh) % 360
			B = 0
			e = 84381.448 / 3600
			angle, B = ec2eq(angle, B, e)  # 应求节气日太阳中天时经度，但对于不同年份结果不同，与定气误差约0.5°
			angle %= 360
			year.append(YearItera(hx, angle, t2))
			t2 = int((year[i]).split('\n')[0]) / 100 - 20  # 计算结果作为下次估值
		if num == 1:
			ui.edit.append(
				'太阳赤经%.1f(今度)中天时在%s宿距星处的年代为:%s\n' % (round(angle, 1), ui.cblMassion.currentText()[0], year[0]))
		else:
			ui.edit.append(
				ui.cblSun.currentText() + '太阳在' + ui.cblMassion.currentText()[0] + '宿' + gdb[rxd] + '度内的年代范围为：' + year[
					0] + '到' + year[1] + '\n')
	except:
		ui.edit.append('计算此项需给出年代估值、太阳节气及所在星宿\n')