from AncientAstro.liData import *


def getLCLF(kind, arg):
    for i in range(len(lclb)):
        if arg == lclb[i][0]:  # 对应朝代
            if kind == 1: return lclb[i][1:]  # 返回原表
            if kind == 2:  # 返回颁行历法信息
                s = ''
                for j in range(1, len(lclb[i])):
                    if len(s) > 15: s += '\n\t'
                    sy, ey, lf = lclb[i][j][:3]
                    s += gyjnBC(sy) + '-' + gyjnBC(ey) + '：' + lf.lm
                    s += '（即' + lclb[i][j][3][:3] + '）；' if len(lclb[i][j]) == 4 and isinstance(lclb[i][j][3], str) else '；'
                return s[:-1]
    if kind == 3:  # 根据历法返回使用朝代信息
        ss = ''
        for i in range(len(lclb)):
            k = 0
            for j in range(1, len(lclb[i])):
                if arg == lclb[i][j][2].lm and not (isinstance(lclb[i][j][-1], str) and '*' in lclb[i][j][-1]):
                    if k == 0: sy = lclb[i][j][0]
                    ey = lclb[i][j][1]
                    k = j
            if k:
                s = lclb[i][0] + gyjnBC(sy) + '-' + gyjnBC(ey) + '年'
                if len(lclb[i][k]) == 4 and isinstance(lclb[i][k][3], str): s += '（' + lclb[i][k][3][:3] + '）'
                length = 26 if '\n\t' in ss else 24
                ss += '\n\t' + s if len(ss.split('\n\t')[-1] + s) > length else '、' + s
        if ss == '、唐619-665年': ss = '、唐619-644（定朔）、645-665（平朔）'
        return ss[1:]
    if kind == 4:  # 根据年代返回用历表
        lf, cd = [], []
        for i in range(len(lclb)):
            for j in range(1, len(lclb[i])):
                if lclb[i][j][0] <= arg <= lclb[i][j][1]:
                    if lclb[i][j][2] not in lf:
                        lf.append(lclb[i][j][2])
                        if len(lf) > len(cd): cd.append([])
                    cd[len(cd) - 1].append(lclb[i][0])
        return lf, cd


def getYongLi(dynasty, year):
    lbs = getLCLF(1, dynasty)
    lib, sgz = [], []
    for lb in lbs:  # 同一朝代同一年有改历
        if lb[0] <= year <= lb[1]:
            lib.append(lb[2])
            if len(lb) == 3:
                sgz.append([lb[2].lm, 2])
            elif len(lb) == 4:
                if isinstance(lb[3], int):  # 指定建正
                    sgz.append([lb[2].lm, lb[3]])
                else:  # 指定历名
                    sgz.append([lb[2].lm + lb[3], 2])
            elif len(lb) == 5:  # 指定建正和历名
                sgz.append([lb[2].lm + lb[4], lb[3]])
    return lib, sgz


def findBxlf(year, dynasty=None):  # 起子月前一月
    if 690 <= year <= 700: yfb = yuefen2
    elif year == 762: yfb = yuefen3
    else: yfb = yuefen
    if not dynasty:
        lf, cd = getLCLF(4, year)  # 未指定历法，根据适用年代选取
        sgz = [[lf[i].lm] for i in range(len(lf))]
        for i in range(len(sgz)):
            d = '('
            for j in cd[i]: d += j + '、'
            sgz[i][0] = d[:-1] + ')' + sgz[i][0]
        lib = [lf[i] for i in range(len(sgz))]
        if 9 <= year <= 23: jz = 1
        elif 690 <= year <= 700 or year == 762: jz = 0  # 月名表起子月
        else: jz = 2
    else:
        lib, sgz = getYongLi(dynasty, year)
        qgz = [[]] * len(sgz)
        xwgz = [[]] * len(sgz)
    for i in range(len(lib)):
        if dynasty: jz = sgz[i][1]
        li = lib[i]
        liList = calendar(li, year, True, True, True)  # 算到次年冬至月后次月
        n = 1 if dynasty else 2
        for j in range(n):
            liList.append(addMonth(li, liList[-1][3:], liList[-1][1], 1, len(liList)))  # 次年首月，用于古历转公历（古历多闰）
        liList.insert(0, addMonth(li, liList[0][3:], liList[0][1], -1))  # 上年末月（古历月后天），插入月后进朔表与月序不对齐
        zqc, jqc = 0, 0
        for k in range(len(liList)):  # 提取月序和干支
            sgz[i].append(liList[k][0] + yfb[(liList[k][1] - jz) % 12] + liList[k][2] + li.dygz(liList[k][3]))
            if dynasty and k > 0:  # 弦望起冬至朔
                xwgz[i].append([[]] * 3)
                for j in range(3):
                    if li.type > 4 or li.lm == '戊寅历':
                        xwdy, xwxy = ps2ds(li, k-1 + (j + 1) / 4)
                    else:
                        xwdy, xwxy = qy(liList[k][3], liList[k][4], li.srf, li.sdy, li.sxy, 0, 0, 1, (j + 1) / 4)[:2]
                    txw(li, xwxy, k-1 + (j + 1) / 4)
                    xwrq = (xwdy+li.jsb[k-1][j+1] - liList[k][3]) % 60  # 进朔表朔多弦望一月
                    xwgz[i][k - 1][j] = [xwrq, ['上弦', '望', '下弦'][j]]
                if liList[k][5] == None:
                    qgz[i].append([['']])
                    zqc = -2
                else:
                    qgz[i].append([[(liList[k][5] - liList[k][3]) % 60, jieqi[(k * 2 - 2 + zqc) % 24]]])
                if liList[k][7][0] == None:
                    qgz[i][k - 1].append([''])
                    jqc = -2
                else:
                    qgz[i][k - 1].append(
                        [(liList[k][7][0] - liList[k][3]) % 60, jieqi[(k * 2 - 1 + jqc + liList[1][-1][-1] * 2) % 24]])
    if dynasty:
        return sgz, qgz, xwgz
    else:
        return sgz


def getFEMonth(year, dynasty, emperor, reign, sgz):
    if 690 <= year <= 700: yfb = yuefen2
    elif year == 762: yfb = yuefen3
    else: yfb = yuefen
    bx = i = -1
    flag = True
    if len(sgz) == 1:
        sgz, jz, flag = sgz[0], sgz[0][1], False
        m1 = 0 if sgz[jz + 3][:-3] in ['正月', '建子月'] else 1
        m2 = 11 if sgz[jz + 15][:-3] == '正月' else 12
    if dynasty in nhsmb:  # 非全年年号截取，及一年多年号拼接
        for nhnyb in nhsmb[dynasty]:
            nyb = nhnyb[-1]
            if nyb[0] <= year <= nyb[2]:
                if len(nhnyb) > 1:  # 指定帝号及年号
                    if flag and len(sgz) > 1: i += 1
                    if nhnyb[0] != reign: continue
                    if len(nhnyb) == 3 and nhnyb[1] != emperor: continue
                bx = i
                if flag: sgz, jz = sgz[i], sgz[i][1]  # 当前年号用历
                m1 = 0 if sgz[jz + 3][:-3] in ['正月', '建子月'] else 1
                if year == nyb[0]:
                    m1 = nyb[1] - 1   # 该年首月
                    if sgz[m1+jz+3][:-3] != yfb[m1] and year != 698: m1 += 1  # 首月前有闰（人为删闰月）
                    if len(nyb) == 5 and nyb[-1] == '*': m1 += 1  # 首月闰
                m2 = nyb[3] - 1 if year == nyb[2] else 11
                if sgz[m2 + jz + 3][:-3] != yfb[m2]: m2 += 1  # 末月前有闰
                if m2 + jz + 4 < len(sgz) - 1:  # 须截断
                    if sgz[m2 + jz + 4][0] == '闰': m2 += 1  # 该末月后有闰
                    if len(nyb) == 5 and nyb[-1] == '**': m2 -= 1  # 闰月算外
    return m1 + jz, m2 + 3 + jz, bx  # yb[m+3+yb[1] :]  # m起的历表


def autoBxlf(year, dynasty, emperor, reign):  # 自动判定历法适用年月
    sgz, qgz, xwgz = findBxlf(year, dynasty)  # 起子月前一月终次年丑月（含闰）
    m1, m2, bx = getFEMonth(year, dynasty, emperor, reign, sgz)
    sgz, qgz, xwgz = sgz[bx], qgz[bx], xwgz[bx]
    jz = sgz[1]
    if dynasty in lbxd:
        for newMonth in lbxd[dynasty]:
            if newMonth[0] == reign and newMonth[1] == year:
                flag = newMonth[2]
                if flag in [1, 2]:  # 修改气朔
                    for s in range(len(sgz)-3):
                        if sgz[s+2][:-3] == newMonth[3][0][:-3]:
                            sgz[s+2] = newMonth[3][0]
                            for i in range(5):
                                if i < 3:
                                    xwgz[s-1][i][0] = newMonth[3][1][i] - 1
                                else:
                                    if isinstance(newMonth[3][1][i], list): qgz[s-1][i-3] = newMonth[3][1][i]
                                    else: qgz[s-1][i-3][0] = newMonth[3][1][i] - 1
                elif flag == 5:  # 删闰月
                    sgz.pop(newMonth[-1])
                    xwgz.pop(newMonth[-1] - 3)
                    qgz.pop(newMonth[-1] - 3)
                    m2 -= 1
                elif flag in [3, 4]:
                    if flag == 4:
                        for n in range(newMonth[3][0]):
                            m2 += 1
                            sgz[m2] = newMonth[3][n+1] + sgz[m2][-3:]
                    elif flag == 3:
                        yx = 18 - 5 - (2-jz) + 1
                        if sgz[yx][:-3] == yuefen[yx-6]: yx += 1
                        sgz.insert(newMonth[-1], newMonth[3][0])
                        m2 += 1
                        for i in range(len(newMonth[3][1])):
                            if i < 3: xwgz[yx][i][0] = newMonth[3][1][i] - 1
                            else: qgz[yx][i-3] = newMonth[3][1][i]
    return sgz, qgz, xwgz, m1, m2+1

