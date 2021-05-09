'''  输出用表  '''

from Data.OtherData import *
from Data.liTables import *
from AstroCalc.SolarTerms import *
from AstroCalc.StarTable import *
from BasicFunc import *

def GanZhiTable(ui, flag):
	ui.edit.append('\t      六十甲子表\n')
	for i in range(10):
		for j in range(6):
			ui.edit.insertPlainText(" {:02d}{} ".format(j * 10 + i + int(not (flag)), gz[j * 10 + i]))
		ui.edit.append('')


def XingCiTable(ui):
	ui.edit.append('\t《汉书·律历志》星次表\n            初          中         终     次度')
	L3 = 255
	for i in range(12):
		L1 = L3
		L2 = (L1 + xcb[i] // 2) % 365
		L3 = (L1 + xcb[i]) % 365
		ui.edit.append(xingci[i] + "     {:3d} {}     {:3d} {}     {:3d}     {}".format(L1, jieqi[(i*2-1)%24], L2, jieqi[(i*2)%24], L3, xcb[i]))
	ui.edit.append('')
	
def JieQiTable(ui, flag):
	k = 6 if flag else 0
	select1 = ui.lstCoordinate.currentItem().text()[0] + '经'
	select2 = '（' + ui.lstDegree.currentItem().text()[:2] + '）'
	ui.edit.append('\t二十四节气太阳' + select1+'表' + select2 + '\n')
	for i in range(12):
		for j in range(2):
			L = (i * 2 + j - (6-k)) * 15
			if ui.lstDegree.currentRow() == 1:
				L /= gdzh
			if ui.lstCoordinate.currentRow() == 0:
				e = 84381.448 / 3600  # 平黄赤交角
				B = 0
				L, B = ec2eq(L, B, e)
			if ui.lstDegree.currentRow() == 0 and ui.lstCoordinate.currentRow() == 1:
				ui.edit.insertPlainText(str(i*2).zfill(2) + "  {}  {:3d}\t".format(jieqi[(i * 2 + k + j) % 24], L))
			else: ui.edit.insertPlainText(str(i*2+j).zfill(2) + "  {}  {:9.5f}\t".format(jieqi[(i*2+k+j)%24],L))
		ui.edit.append("")

def SuiXingTable(ui):
	head = ['岁名', '岁阴', '岁星', '星次', '月']
	ui.edit.append('')
	for i in range(len(head)):
		ui.edit.insertPlainText('   ' + head[i])
	ui.edit.append('')
	for j in range(12):
		ui.edit.insertPlainText('{0:{1}<3}'.format(suiyin[j], chr(12288)))
		ui.edit.insertPlainText('     ' + dizhi[(j + 2) % 12])
		ui.edit.insertPlainText('     ' + dizhi[(12 - (j - 1)) % 12])
		ui.edit.insertPlainText('    ' + xingci[j])
		ui.edit.insertPlainText('   ' + dizhi[j])
		ui.edit.append('')

def GLB(ui):
	if ui.cblGLBtype.currentText() == '宿度表':
		select1 = ui.lstCoordinate.currentItem().text()[0] + '道'
		select2 = '（' + ui.lstDegree.currentItem().text()[:2] + '）'
		if ui.cblGLB.currentText() == "实际计算": # 真实宿度
			try:
				year = int(ui.editYear.text())
				date = equinox_solstice(year-1, 270, 0)
				T = (ut2td(date) - 2451545) / 36525  # 儒略世纪数
				e = nutation(T)[2]
				for star in esbx: StarPosition(star, T)
				if ui.lstCoordinate.currentRow() == 1:
					for star in esbx: star.ra, star.dec = eq2ec(star.ra, star.dec, e)  # 二十八宿黄经
				for i in range(28):
					xd = esbx[(i + 1) % 28].ra - esbx[i].ra
					if esbx[(i + 1) % 28].ra < esbx[i].ra:
						xd = esbx[(i + 1) % 28].ra + 360 - esbx[i].ra
					if ui.lstDegree.currentRow() == 1:
						xd = xd / gdzh
					if i == 0:
						ui.edit.append(gyjn(year) + '  前冬至  ' + select1 + '宿度' + select2)
					ui.edit.append('  {}宿：\t{:04.1f}'.format(esbx[i].name, xd))
			except: ui.edit.append("计算需要提供年份")
		else:  # 历代史料所载宿度表
			epoch = ui.cblGLB.currentText().split('-')[1]
			ui.edit.append('《' + epoch + '》' + select1 + '宿度表')
			try:
				if ui.lstCoordinate.currentRow() == 0:
					xdb = cdxdb[ui.cblGLB.currentText()]
				else:
					xdb = hdxdb[ui.cblGLB.currentText()]
				for i in range(28):
					ui.edit.append('{}    宿宿度：{:8.4f}'.format(xingxiu[(i - 8) % 28], xdb[i]).rstrip('0').rstrip('.'))  # 按小数点对齐
			except:
				ui.edit.insertPlainText('：无数据')
	ui.edit.append("")
