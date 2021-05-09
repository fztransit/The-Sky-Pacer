from BasicFunc.update import *
from PyQt5.QtWidgets import QMessageBox


def checkUpdate(ui):
	check = newVersion()
	try:
		link, pw, nv, fo, tv = check
		ui.edit.setText('链接：'+ link + '\n' + pw + '\n\n')
		QMessageBox.information(ui, '更新 ' + nv, '更新说明：\n' + fo)
	except:
		tv = check
		QMessageBox.information(ui, '暂无更新', '当前版本 ' + tv)
		if len(tv) > 15:
			ui.edit.setText('版本更新页：https://gitee.com/fztransit/version-update-record/raw/master/version-update-record')


def mandatoryUpdate(ui):
	try:
		link, pw, nv, fo, tv = newVersion()
		ui.edit.setText('有新版！    最新版本：' + nv + '    当前版本：' + tv + '\n更新说明：' + fo)
		ui.edit.append('链接：' + link + '\n' + pw)
	except:
		pass