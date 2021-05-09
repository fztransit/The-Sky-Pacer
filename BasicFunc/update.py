##################################
# 功能：更新提示
# 当前版本：手动记录
# 获得更新：爬取网页信息
# 提示更新：消息框
# 缺点：依赖论坛服务器，网页无法连接时提示无更新
##################################

import requests
import re

def getHTMLText(url): # 从链接获取网页文本
	try:
		r = requests.get(url, timeout=2)
		r.raise_for_status()  # 状态码
		r.encoding = r.apparent_encoding  # 编码改为可视
		return r.text
	except:
		return '网页内容异常'


def newVersion():
	try:
		this_version = 'beta3.4'
		url = 'https://gitee.com/fztransit/version-update-record/raw/master/version-update-record'
		html = getHTMLText(url)
		versionInfo = re.findall(r'start(.*?)end', html, re.S)[-1].split('\r\n')
		new_version = versionInfo[2][9:]
		if float(new_version[4:]) > float(this_version[4:]):
			update_info = versionInfo[3][8:]
			link = versionInfo[4][6:]
			pw = '提取码：' + versionInfo[5][6:]
			return link, pw, new_version, update_info, this_version
		else:  # 当前版本即最新
			return this_version
	except:
		return this_version + '\n无法获取更新信息，请手动在更新页查找。'
