# 全局变量读写，方便跨module调用

class GolVar:
    def __init__(self, initVal):
        self.gvar = initVal
        self.flag = 0

    def reset(self, initVal):
        self.gvar = initVal
        self.flag = 1

    def setValue(self, val, kind=0):
        if isinstance(self.gvar, list):
            if kind == 0:
                self.gvar.append(val)
            elif kind == 1:
                self.gvar = [self.gvar[val]] + self.gvar[:val]

    def setFlag(self):
        self.flag = 0


