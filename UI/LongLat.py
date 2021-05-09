''' 入宿度、去极度相关输出 '''
from AstroCalc import *
from BasicFunc import *


# 恒星
def StarJD(ui, kind):  # 0为二十八宿，1为恒星表
	try:
		select1 = ui.lstCoordinate.currentItem().text()[0] + '经'
		select2 = '（' + ui.lstDegree.currentItem().text()[:2] + '）'
		year, flag, date, JDE, T = getInput(ui.editYear.text())
		if kind == 0: getStar = ui.cblMassion.currentText()
		elif kind == 1: getStar = ui.cblStar.currentText()
		starName = getStar[:getStar.find(' ')]
		if ui.cblSun.currentText() == "全年" and getStar != '全部':  # 单个行星全年优化排列
			if flag == True: ui.edit.append(ui.editYear.text() + '年\t')
			else: ui.edit.append('')  # 另起一行开始输出
			ui.edit.insertPlainText('时间\t' + starName + ['宿','星'][kind] + '视' + select1 + select2)
		for s in stTable:
			if s == "全年": continue # 无效值
			if ui.cblSun.currentText() == s or ui.cblSun.currentText() == "全年":  # 查找或遍历
				i = 0
				if flag == True: date, JDE, T = selectSTDate(s, year)  # 计算节气
				if kind == 0: starTable = esbx
				elif kind == 1: starTable = hxb
				for star in starTable:
					if star == "全部": continue # 无效值
					if starName == star.name or getStar == "全部":  # 查找或遍历
						StarPosition(star, T)
						if ui.lstCoordinate.currentRow() == 1:  # 黄经表示
							if i == 0: e = nutation(T)[2]
							star.ra, star.dec = eq2ec(star.ra, star.dec, e)  # 恒星黄经
							ha = '即：' + deg2dms(star.ra)
						else:
							ha = '即：' + deg2hms(star.ra)
						if ui.lstDegree.currentRow() == 1:  # 古度表示
							star.ra /= gdzh
						ra = star.ra
						if ui.cblSun.currentText() != "全年" or (ui.cblSun.currentText() == "全年" and getStar == "全部"):  # 按天体排序
							if i == 0:
								if flag == True: ui.edit.append("{}年 {}    ".format(int(ui.editYear.text()), s))
								else: ui.edit.append('')
								ui.edit.insertPlainText("{}{}".format(date[:-9], select2))
							ui.edit.append('{0:{5}>4}{1}视{2}：{3:8.4f}°    {4}'.format(star.name, ['宿','星'][kind], select1, ra, ha, chr(12288)))
						i += 1
				if ui.cblSun.currentText() == "全年" and getStar != "全部":  # 按节气排序
					if flag == True: ui.edit.append(chr(12288) * (3 - len(s)) + s)
					else: ui.edit.append('')
					ui.edit.insertPlainText(" {}    {:8.4f}°  {}".format(date[:-9], ra, ha))
			if ui.cblSun.currentText() == s or (flag == False and ((ui.cblSun.currentText() in stTable and ui.cblSun.currentText() == s) or ui.cblSun.currentText() == "全年")): break  # 查找或指定日期：在节气表中查找或全年只计算一次
	except:
		ui.edit.append(ErrorHint)
	ui.edit.append("")

def StarQJD(ui, kind):
	try:
		select1 = ui.lstCoordinate.currentItem().text()[0] + '纬'
		select2 = '（' + ui.lstDegree.currentItem().text()[:2] + '）'
		select3 = ''
		select4 = '黄道去极/北极距'
		if ui.lstCoordinate.currentRow() == 1: select4 = '黄道内外/极黄纬'
		year, flag, date, JDE, T = getInput(ui.editYear.text())
		if kind == 0: getStar = ui.cblMassion.currentText()
		elif kind == 1: getStar = ui.cblStar.currentText()
		starName = getStar[:getStar.find(' ')]
		if ui.cblSun.currentText() == "全年" and getStar != '全部':  # 单个行星全年优化排列
			if flag == True: ui.edit.append(ui.editYear.text() + '年')
			else: ui.edit.append('')
			ui.edit.insertPlainText('  时间 {0:{5}>3}{1}视{2}{3} {4}'.format(starName, ['宿','星'][kind], select1, select2, select4, chr(12288)))
		for s in stTable:
			if s == "全年": continue # 无效值
			if ui.cblSun.currentText() == s or ui.cblSun.currentText() == "全年":  # 查找或遍历
				i = 0
				if flag == True: date, JDE, T = selectSTDate(s, year)  # 计算节气
				if kind == 0: starTable = esbx
				elif kind == 1: starTable = hxb
				for star in starTable:
					if star == "全部": continue # 无效值
					if starName == star.name or getStar == "全部":  # 查找或遍历
						StarPosition(star, T)
						qjd = 90 - star.dec # QJD
						if ui.lstCoordinate.currentRow() == 1:  # 黄经表示
							if i == 0: e = nutation(T)[2]
							LT = atan2(tan(e) * sin(star.ra), 1)
							qjd = star.dec - LT  # ST
							select3 = '(内)'
							if qjd < 0: select3 = '(外)'
							star.ra, star.dec = eq2ec(star.ra, star.dec, e)  # 恒星黄经
						if ui.lstDegree.currentRow() == 1:  # 古度表示
							star.dec /= gdzh
							qjd /= gdzh
						dec = star.dec
						if ui.cblSun.currentText() != "全年" or (ui.cblSun.currentText() == "全年" and getStar == "全部"):  # 按天体排序
							if i == 0:
								if flag == True: ui.edit.append("{}年 {}    ".format(int(ui.editYear.text()), s))
								else: ui.edit.append("")
								ui.edit.insertPlainText("{}{}\n\t  视{}\t          {}".format(date[:-9], select2, select1, select4))
							ui.edit.append('{0:{6}>4}{1}：{2:7.3f}°即{3}   {4:8.4f}{5}'.format(star.name, ['宿','星'][kind], dec, deg2dms(dec), qjd, select3, chr(12288)))
						i += 1
				if ui.cblSun.currentText() == "全年" and getStar != "全部":  # 按节气排序
					if flag == True: ui.edit.append(chr(12288) * (3 - len(s)) + s)
					else: ui.edit.append('')
					ui.edit.insertPlainText(" {}   {:8.4f}°      {:8.4f}{}".format(date[:-9], dec, qjd, select3))
			if ui.cblSun.currentText() == s or (flag == False and ((ui.cblSun.currentText() in stTable and ui.cblSun.currentText() == s) or ui.cblSun.currentText() == "全年")): break
	except:
		ui.edit.append(ErrorHint)
	ui.edit.append("")


# 太阳sunLBR，月亮moonLBR：行星PlanetLBR，输入为JDE，输出为(L, B, R, RA, Dec)
def SunRXD(ui):
	select1 = ui.lstCoordinate.currentItem().text()[0] + '经'
	select2 = '（' + ui.lstDegree.currentItem().text()[:2] + '）'
	year, flag, date, JDE, T = getInput(ui.editYear.text())
	if flag == True and ui.cblSun.currentText() == "全年":
		ui.edit.append(ui.editYear.text() + '年\t')
		ui.edit.insertPlainText("    时间\t    太阳视{}{}".format(select1, select2))
	for s in stTable:
		if s == "全年": continue # 无效值
		if ui.cblSun.currentText() == s or ui.cblSun.currentText() == "全年":  # 查找或遍历
			if flag == True: date, JDE, T = selectSTDate(s, year)  # 计算节气
			L, B, R, ra, dec = sunLBR(JDE)
			for star in esbx: StarPosition(star, T)  # 指定节气的二十八宿经度
			ha = '\t  '
			if ui.lstCoordinate.currentRow() == 1:  # 黄经表示
				e = nutation(T)[2]
				ra, dec = L, B  # 太阳黄经
				for star in esbx: star.ra, star.dec = eq2ec(star.ra, star.dec, e)  # 二十八宿黄经
			else:
				ha = '（' + deg2hms(ra) + '）'
			srx, rxd = rxd_calc(ra)
			if ui.lstDegree.currentRow() == 1:  # 古度表示
				ra /= gdzh
				rxd /= gdzh
			if flag == True and ui.cblSun.currentText() == "全年":
				ui.edit.append(chr(12288) * (3 - len(s)) + s)
				ui.edit.insertPlainText(" {}  {:8.4f}° {}{:4.1f}度".format(date, ra, srx[:2], rxd))
			else:
				if flag == True: ui.edit.append("{}年  {}    ".format(int(ui.editYear.text()), s))
				else: ui.edit.append("")
				ui.edit.insertPlainText("{} {}\n  太阳视{}{:8.4f}°{} {}{:4.1f}度".format(date, select2, select1, ra, ha, srx, rxd))
		if ui.cblSun.currentText() == s or (flag == False and ((ui.cblSun.currentText() in stTable and ui.cblSun.currentText() == s) or ui.cblSun.currentText() == "全年")): break
	ui.edit.append("")

def SunQJD(ui):
	if ui.lstCoordinate.currentRow() == 1:
		ui.edit.append("太阳视黄纬恒为0°，黄道去极恒为90°（古度91.3125）\n")
		return 0
	select2 = ui.lstDegree.currentItem().text()[:2]
	year, flag, date, JDE, T = getInput(ui.editYear.text())
	if flag == True and ui.cblSun.currentText() == "全年":
		ui.edit.append(ui.editYear.text() + '年（' + select2 + '）')
		ui.edit.insertPlainText("    时间\t    太阳视赤纬   黄道去极")
	for s in stTable:
		if s == "全年": continue # 无效值
		if ui.cblSun.currentText() == s or ui.cblSun.currentText() == "全年":  # 查找或遍历
			if flag == True: date, JDE, T = selectSTDate(s, year)  # 计算节气
			dec = sunLBR(JDE)[4]
			qjd = round(90 - dec, 4)
			if ui.lstCoordinate.currentRow() == 1:  # 古度表示
				dec /= gdzh
				qjd /= gdzh
			if flag == True and ui.cblSun.currentText() == "全年":
				ui.edit.append(chr(12288) * (3 - len(s)) + s)
				ui.edit.insertPlainText(" {}  {:8.4f}°  {:8.4f}".format(date, round(dec, 4) % 360, qjd))
			else:
				if flag == True: ui.edit.append("太阳视赤纬   {}年 {}    ".format(int(ui.editYear.text()), s))
				else: ui.edit.append("")
				ui.edit.insertPlainText("{}  \n  {}：{:7.3f}°即{}  黄道去极{:7.3f}度".format(date, select2, dec, deg2dms(dec), qjd))
		if ui.cblSun.currentText() == s or (flag == False and ((ui.cblSun.currentText() in stTable and ui.cblSun.currentText() == s) or ui.cblSun.currentText() == "全年")): break
	ui.edit.append("")
	
	
# 获得输入：日期：year/month/day；月相：year/month+月相；指定节气：year+节气。
def MoonRXD(ui):
	select1 = ui.lstCoordinate.currentItem().text()[0] + '经'
	select2 = '（' + ui.lstDegree.currentItem().text()[:2] + '）'
	date_table = []
	date_name = []
	if ui.editYear.text().count('/') == 2:  # 日期格式
		date_table.append(ui.editYear.text())
		date_name.append('')
	elif ui.cblMoon.currentText() in phases[:5]:
		phase_name = ['朔', '上弦', '望', '下弦']
		date = ui.editYear.text()
		for m in phase_name:
			if ui.cblMoon.currentText() == '全部月相' or ui.cblMoon.currentText() == m:
				date = PhaseDate(date, phase_name.index(m))
				date_table.append(date)
				if ui.cblMoon.currentText() == '全部月相' and m != '朔': date_name.append('朔后'+ m)
				else: date_name.append(m)
	elif ui.cblMoon.currentText() == '指定节气':
		nian = int(ui.editYear.text().split('/')[0])
		for s in [stTable[0]] + stTable[2:]:
			if ui.cblSun.currentText() == '全年' or ui.cblSun.currentText() == s:
				date_table.append(selectSTDate(s, nian)[0])
				date_name.append(s)
	month_name = ''
	for k in range(len(date_table)):
		JDE, T = date2td(date_table[k])[1:]
		date = UTdate(date_table[k], -1)
		e = nutation(T)[2]
		L, B, R, ra, dec = moonLBR(JDE)
		for star in esbx: StarPosition(star, T)  # 指定节气的二十八宿经度
		ha = '\t'
		if ui.lstCoordinate.currentRow() == 1:  # 黄经表示
			ra, dec = L, B  # 月亮黄经
			for star in esbx: star.ra, star.dec = eq2ec(star.ra, star.dec, e)  # 二十八宿黄经
		else:
			ha = '（' + deg2hms(ra) + '）'
		srx, rxd = rxd_calc(ra)
		if ui.lstDegree.currentRow() == 1:  # 古度表示
			ra /= gdzh
			rxd /= gdzh
		if k == 0 and ui.cblMoon.currentText() != '指定节气': month_name = str(GetDate(date)[1]) + '月'
		if (ui.cblMoon.currentText() == '指定节气' and ui.cblSun.currentText() == '全年') or (ui.cblMoon.currentText() == '全部月相'):
			if k == 0: ui.edit.append(str(GetDate(ui.editYear.text())[0]) + '年' + month_name + '\t    时间\t    月亮视' + select1 + select2)
			ui.edit.append(chr(12288) * (4 - len(date_name[k])) + date_name[k] + ' {}  {:8.4f}° {}{:4.1f}度'.format(date, ra, srx[:2], rxd))
		else:
			ui.edit.append("{}年  {}{}    {} {}\n  月亮视{}{:8.4f}°{} {}{:4.1f}度".format(GetDate(ui.editYear.text())[0], month_name, date_name[k], date, select2, select1, ra, ha, srx, rxd))
	ui.edit.append("")


def PlanetJD(ui, kind):  # 0为星次，1为宿度
	select1 = ui.lstCoordinate.currentItem().text()[0] + '经'
	select2 = '（' + ui.lstDegree.currentItem().text()[:2] + '）'
	year, flag, date, JDE, T = getInput(ui.editYear.text())
	if ui.cblSun.currentText() == "全年" and ui.cblPlanet.currentText() != '全部':  # 单个行星全年优化排列
		if flag == True: ui.edit.append(ui.editYear.text() + '年')
		else: ui.edit.append('')
		ui.edit.insertPlainText('\t时间\t  ' + ui.cblPlanet.currentText() + '视' + select1 + select2)
	if kind == 1 and ui.lstCoordinate.currentRow() == 1:  e = nutation(T)[2]  # 计算恒星黄道坐标时一年内的误差小于精度
	for s in stTable:
		if s == "全年": continue # 无效值
		if ui.cblSun.currentText() == s or ui.cblSun.currentText() == "全年":  # 查找或遍历
			i = 0 # 仅在首行输出日期信息
			if flag == True: date, JDE, T = selectSTDate(s, year) # 计算节气
			for p in fivePlanets:
				if p == "全部": continue # 无效值
				if ui.cblPlanet.currentText() == p or ui.cblPlanet.currentText() == "全部":  # 查找或遍历
					L, B, R, ra, dec = PlanetLBR(p[0], JDE)
					if kind == 1:
						for star in esbx: StarPosition(star, T)  # 指定节气的二十八宿赤经
					type = 0  # 坐标系
					ha = '\t'  # 时角输出
					if ui.lstCoordinate.currentRow() == 1:  # 黄经表示
						type = 1
						#if kind == 1 and i == 0:  e = nutation(T)[2]
						ra, dec = L, B  # 行星黄经
						if kind == 1:
							for star in esbx: star.ra, star.dec = eq2ec(star.ra, star.dec, e)  # 二十八宿黄经
					else:
						ha = '（' + deg2hms(ra) + '）'
					if kind == 0: src, rcd = rcd_calc(ra, type)
					elif kind == 1: src, rcd = rxd_calc(ra)
					if ui.lstDegree.currentRow() == 1:  # 古度表示
						ra /= gdzh
						rcd /= gdzh
					if ui.cblSun.currentText() != "全年" or (ui.cblSun.currentText() == "全年" and ui.cblPlanet.currentText() == "全部"):  # 按天体排序
						if i == 0:
							if flag == True: ui.edit.append("{}年  {}    ".format(int(ui.editYear.text()), s))
							else: ui.edit.append("")
							ui.edit.insertPlainText("{} {}".format(date, select2))
						ui.edit.append("  {}视{}{:8.4f}°{} {}{:4.1f}度".format(p, select1, ra, ha, src, rcd))
					i += 1
			# 单一行星全年表提供不同的输出格式
			if ui.cblSun.currentText() == "全年" and ui.cblPlanet.currentText() != "全部":  # 按节气排序
				if flag == True: ui.edit.append(chr(12288) * (3 - len(s)) + s)
				else: ui.edit.append('')
				ui.edit.insertPlainText(" {}   {:8.4f}°  {}{:4.1f}度".format(date, ra, src[1:], rcd))
		if ui.cblSun.currentText() == s or (flag == False and ((ui.cblSun.currentText() in stTable and ui.cblSun.currentText() == s) or ui.cblSun.currentText() == "全年")): break
	ui.edit.append("")

def Position(ui):
	try:
		select1 = '赤经'
		select2 = '赤纬'
		date = ui.editYear.text()  # UT 8h
		date, JDE, T = date2td(date)
		for star in esbx: StarPosition(star, T)
		if ui.lstCoordinate.currentRow() == 1:  # 黄经表示
			e = nutation(T)[2]
			for star in esbx: star.ra, star.dec = eq2ec(star.ra, star.dec, e)  # 二十八宿黄经
		for i in range(7):
			if i == 0:  ui.edit.append("{}".format(date))
			if ui.planetGroup.button(i).isChecked():
				if i < 5: # 行星
					p = ui.planetGroup.button(i).text() + '星'
					L, B, R, ra, dec = PlanetLBR(p[0], JDE)
				if i == 5: # 日
					p = '太阳'
					L, B, R, ra, dec = sunLBR(JDE)
				if i == 6:
					p = '月亮'
					L, B, R, ra, dec = moonLBR(JDE)
				type = 0
				if ui.lstCoordinate.currentRow() == 1:  # 黄经表示
					type = 1
					ra, dec = L, B
					select1 = '黄经'
					select2 = '黄纬'
				srx, rxd = rxd_calc(ra)
				src, rcd = rcd_calc(ra, type)
				if ui.lstDegree.currentRow() == 1:  # 古度表示
					ra /= gdzh
					dec /= gdzh
					rxd /= gdzh
					rcd /= gdzh
				ui.edit.append(" {}视{}{:6.2f}°({}{:4.1f}，{}{:4.1f})  {}{:6.2f}°".format(
					p, select1, round(ra, 2), srx[1], round(rxd, 1), src[1:], round(rcd, 1), select2, round(dec, 2)))
	except:
		ui.edit.append(ErrorHint)
	ui.edit.append("")
