'''
Created on 2012-4-14

@author: Sky
'''
import time

def GetTimeMS():
    return int(time.time() * 1000)

def GetTimeS():
    return int(GetTimeMS() / 1000)

def GetTimeM():
    return int(GetTimeMS() / 60000)

def GetTimeH():
    return int(GetTimeMS() / 3600000)

def TimeStamp():
    return time.strftime("%H:%M:%S")

def DateStamp():
    return time.strftime("%Y.%m.%d")

def Seconds(t):
    return t * 1000

def Minutes(t):
    return t * 60 * 1000

def Hours(t):
    return t * 60 * 60 * 1000

def Days(t):
    return t * 24 * 60 * 60 * 1000

def Weeks(t):
    return t * 7 * 24 * 60 * 60 * 1000

def Years(t):
    return t * 365 * 24 * 60 * 60 * 1000

class Timer:
    def __init__(self):
        self.m_starttime = 0
        self.m_inittime = 0
        
    def Reset(self, p_timepassed = 0):
        self.m_starttime = p_timepassed
        self.m_inittime = GetTimeMS()

    def GetMS(self):
        return int((GetTimeMS() - self.m_inittime) + self.m_starttime)
    
    def GetS(self):
        return int(self.GetMS() / 1000)

    def GetM(self):
        return int(self.GetMS() / 60000)

    def GetH(self):
        return int(self.GetMS() / 3600000)

    def GetD(self):
        return int(self.GetMS() / 86400000)
    
    def GetY(self):
        return int(self.GetD() / 365)
   
    def GetString(self):
        string = ""
        y = self.GetY()
        d = self.GetD() % 365
        h = self.GetH() % 24
        m = self.GetM() % 60
        
        if y > 0:
            string += str(y) + " years, "
        if d > 0:
            string += str(d) + " days, "
        if h > 0:
            string += str(h) + " hours, "
        string += str(m) + " minutes"
        return string

'''    
t = Timer()
print(t.GetString())
print(TimeStamp())
print(DateStamp())
'''
        