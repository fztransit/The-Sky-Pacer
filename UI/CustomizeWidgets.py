from PyQt5.QtWidgets import QPushButton, QTextEdit, QComboBox, QLineEdit, QListView, QLabel, QWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sip

# 不移动焦点的按钮
class PushButton(QPushButton):
	def __init__(self, parent=None):
		super(PushButton, self).__init__(parent)
		self.setFocusPolicy(False)


# 支持单击的标签
class Label(QLabel):
	clicked = pyqtSignal()  # 设定信号名及参数类型

	def __init__(self, parent=None):
		super(QLabel, self).__init__(parent)
		self.setFont(QFont("family", 15))
		#self.setContentsMargins(15, 15, 15, 15)
		self.setAlignment(Qt.AlignCenter)


	def mousePressEvent(self, event):
		if event.buttons() == Qt.LeftButton:
			self.clicked.emit()  # 设置信号参数并传入槽函数


# 支持右击的按钮
class RightClickButton(PushButton):
	clickedSignal = pyqtSignal(bool)  # 设定信号名及参数类型

	def mousePressEvent(self, event):
		if event.buttons() == Qt.LeftButton:
			self.clickedSignal.emit(True)  # 设置信号参数并传入槽函数
		elif event.buttons() == Qt.RightButton:
			self.clickedSignal.emit(False)


# 默认可编辑、无省略、点击后从左显示的下拉列表
class ComboBox(QComboBox):
	wheeled = pyqtSignal()
	indexChanged = pyqtSignal()

	def __init__(self, parent=None):
		super(ComboBox, self).__init__(parent)
		self.setView(QListView())
		self.setStyleSheet("QComboBox {font: 13px} "
		                   "QComboBox QAbstractItemView::item {min-height: 18px; min-width: 80px; }")
		self.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.view().setTextElideMode(Qt.ElideNone)  # 取消省略
		self.setLineEdit(QLineEdit())  # 绑定文本框
		self.activated.connect(lambda: self.lineEdit().setCursorPosition(0))   # 选中后重设光标在左侧
		# self.setFocusPolicy(False)

	def wheelEvent(self, event):
		index = self.currentIndex()
		super().wheelEvent(event)
		if event.isAccepted() and (index == 0 or index == self.count() - 1):
			self.wheeled.emit()  # 在首尾滚动时发送信号


# insertPlainText时从末尾追加的文本框
class TextEdit(QTextEdit):
	def insertPlainText(self, text: str):
		self.moveCursor(QTextCursor.End)  # 光标移至末尾再追加
		super().insertPlainText(text)

	def append(self, text: str):
		super().append(text)
		self.moveCursor(QTextCursor.End)  # 追加后光标移至末尾


def closeWidgets(layout):  # 关闭本布局及子布局下所有控件，未删除对象本身
	if layout != None:
		for i in range(layout.count()):
			if layout.itemAt(i).widget() != None:  # 关闭控件
				layout.itemAt(i).widget().close()
			else:
				closeWidgets(layout.itemAt(i).layout())  # 子布局