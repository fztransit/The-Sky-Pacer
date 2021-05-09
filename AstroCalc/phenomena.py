from AstroCalc.planet import *
from AstroCalc.moon import *

def HeRi(ui):
	try:
		year = int(ui.editYear.text())
		for i in range(5):
			if ui.planetGroup.button(i).isChecked():
				p = ui.planetGroup.button(i).text()
				date1 = InferiorConjunct(year, p)  # 下合/合日
				if p in ['水','金']:
					date2 = InferiorConjunct(year, p, 1)  # 上合
					jd1 = date2JD(date1)
					jd2 = date2JD(date2)
					if jd1 < jd2 :
						ui.edit.append(ui.editYear.text() + '年\t' + p + '星下合时间为：' + date1)
						ui.edit.append('\t    上合时间为：' + date2)
						flag = True
					else:
						ui.edit.append(ui.editYear.text() + '年\t' + p + '星上合时间为：' + date2)
						ui.edit.append('\t    下合时间为：' + date1)
						flag = False
					if p == '水':
						if flag == True:
							for i in range(3):
								date1 = InferiorConjunct(year + 0.3 * (i + 1), p)  # 下合
								date2 = InferiorConjunct(year + 0.3 * (i + 1), p, 1)  # 上合
								ui.edit.append('\t其后下合时间为：' + date1)
								ui.edit.append('\t    上合时间为：' + date2)
						else:
							for i in range(3):
								date1 = InferiorConjunct(year + 0.3 * (i + 1), p)  # 下合
								date2 = InferiorConjunct(year + 0.3 * (i + 1), p, 1)  # 上合
								ui.edit.append('\t其后上合时间为：' + date2)
								ui.edit.append('\t    下合时间为：' + date1)
				else:
					ui.edit.append(ui.editYear.text() + '年\t' + p + '星合日时间为：' + date1)
	except:
		ui.edit.append(ErrorHint)
	ui.edit.append("")

def ChongRi(ui):
	try:
		year = int(ui.editYear.text())
		for i in range(5):
			if i < 2: continue
			if ui.planetGroup.button(i).isChecked():
				if i == 2: ui.edit.append(ui.editYear.text() + '年 ')
				p = ui.planetGroup.button(i).text()
				if p in ['木', '火', '土']:
					JDE = pp_it(year, p, 180)  # 冲日
					ui.edit.insertPlainText('\t' + p + '星冲日时间为：'+ td2date(JDE) + '\n')
	except:
		ui.edit.append('输入错误，请输入年份\n')

def DaJu(ui):
	try:
		year = int(ui.editYear.text())
		for i in range(2):
			if ui.planetGroup.button(i).isChecked():
				p = ui.planetGroup.button(i).text()
				result = pp(year, p, 2) # 大距
				ui.edit.append(ui.editYear.text() + '年  '+ p + '星东大距：' + result[0][:-3] + ' 距角：' + str(result[1]) + '°')
				ui.edit.append('            西大距：' + result[2][:-3] + ' 距角：' + str(result[3]) + '°')
				if p == '水':
					for i in range(3):
						result = pp(year + 0.3 * (i+1), p, 2)
						ui.edit.append('        其后东大距：' + result[0][:-3] + ' 距角：' + str(result[1]) + '°')
						ui.edit.append('            西大距：' + result[2][:-3] + ' 距角：' + str(result[3]) + '°')
	except:
		ui.edit.append(ErrorHint)
	ui.edit.append("")

def Liu(ui):
	try:
		year = int(ui.editYear.text())
		for i in range(5):
			if ui.planetGroup.button(i).isChecked():
				p = ui.planetGroup.button(i).text()
				date = pp(year, p, 3) # 留
				if p in ['水', '金']:
					ui.edit.append(ui.editYear.text() + '年 ' + p + '星\t顺留（上合后）为：' + date[0] + '\n\t逆留（下合后）为：' + date[1])
				else:
					ui.edit.append(ui.editYear.text() + '年 ' + p + '星\t顺留（合日后）为：' + date[0] + '\n\t逆留（冲日后）为：' + date[1])
	except:
		ui.edit.append(ErrorHint)
	ui.edit.append("")

def YYX(ui):
	try:
		year = ui.editYear.text()
		for i in range(5):
			if ui.planetGroup.button(i).isChecked():
				p = ui.planetGroup.button(i).text()
				date = LunarOccultation(year, p)
				if len(date) == 0:
					ui.edit.append(year + '年  未发生月掩' + p + '星')
				else:
					ui.edit.append(ui.editYear.text() + '年  月掩' + p + '星时间为：')
					for i in range(len(date)):
						ui.edit.append('\t' + str(date[i]))
		if ui.planetGroup.button(8).isChecked():
			yyhxm = ['角宿一','心宿二','毕宿五','北河三','轩辕十四']
			yyhxb = [jiao, Antares, bi_5, bh_3, xy_14]
			for star in yyhxb:  # 月掩恒星
				date = LunarOccultation(year, star)
				if len(date) == 0:
					ui.edit.append(year + '年  未发生月掩' + yyhxm[yyhxb.index(star)])
				else:
					ui.edit.append(ui.editYear.text() + '年  月掩' + yyhxm[yyhxb.index(star)] + '时间为：')
					for i in range(len(date)):
						ui.edit.append('\t' + str(date[i]))
	except:
		ui.edit.append('输入错误，请勾选行星或恒星')
	ui.edit.append("")

