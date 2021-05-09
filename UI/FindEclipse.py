from AstroCalc import *

def FastFindEclipse(ui, type):
	s = ui.txtEditScope.text().split('*')
	lower = int(s[0])
	try:
		upper = int(s[1])
	except:
		upper = lower
	JDE = date2JD(str(lower)) - 29
	if type == 2: JDE = PhaseJDE(JDE, 1)  # 转到上弦防止漏算
	JD = date2JD(upper + 1)
	x = type // 2 + 1
	day = 29 / x
	while JDE < JD:
		for i in range(x):
			if type == 1: i = 1  # 月食时重设食类型参数
			JDE, kind, shifen = eclipse(JDE + day, i) # 发生日食为UT+8h的食甚时刻（保证再求date1为下月朔），未发生为UT的合朔时刻
			if '未发生%s食' % (['日','月'][i]) not in kind and '不可见' not in kind:
				date = JD2date(JDE - deltaT(JDE) / 86400 + 8 / 24)
				if (ganzhiDate(date) == ui.txtEditFEgz.text()) or ui.txtEditFEgz.text() == "": # 已知干支时只输出该干支的日食
					ui.edit.append(date + '  ' + ganzhiDate(date) + '   ' + kind + '  ' + shifen)
	ui.edit.append("")