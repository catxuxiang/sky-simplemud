'''
Created on 2012-4-14

@author: Sky
'''
import os.path
from BasicLib import BasicLibTime
from BasicLib.Redis import sr

class TextDecorator:
    @staticmethod
    def FileHeader(p_title):
        return ("==================================================\n"
                "" + p_title + "\n"
                "==================================================\n\n")   
        
    @staticmethod
    def SessionOpen():
        return "\n"
    
    @staticmethod
    def SessionClose():
        return "\n"   
    
    @staticmethod
    def Decorate(p_string):
        return p_string + "\n"     
    
class Logger:
    def __init__(self, p_filename, p_logtitle, p_timestamp = False, p_datestamp = False):
        fileexist = os.path.isfile(p_filename)
        self.m_logfile = open(p_filename, 'at')
        if (not fileexist):
            self.m_logfile.write(TextDecorator.FileHeader(p_logtitle))

        self.m_timestamp = True
        self.m_datestamp = True
        self.m_logfile.write(TextDecorator.SessionOpen())
        self.Log( "Session opened." )        
        self.m_timestamp = p_timestamp
        self.m_datestamp = p_datestamp
        
    def __del__(self):
        self.m_timestamp = True
        self.m_datestamp = True
        self.Log( "Session closed." )
        self.m_logfile.close()
        
    def Log(self, p_entry):
        message = "";
        if(self.m_datestamp):
            message += "[" + BasicLibTime.DateStamp() + "] "
        if(self.m_timestamp):
            message += "[" + BasicLibTime.TimeStamp() + "] " 
        message += p_entry
        self.m_logfile.write(message + "\n")   
        
class DbLogger:
    def __init__(self, p_logtitle, p_timestamp = False, p_datestamp = False):
        self.m_logtitle = p_logtitle
        self.m_timestamp = True
        self.m_datestamp = True
        self.Log("Session opened.")        
        self.m_timestamp = p_timestamp
        self.m_datestamp = p_datestamp
        
    def __del__(self):
        self.m_timestamp = True
        self.m_datestamp = True
        self.Log("Session closed.")
        
    def Log(self, p_entry):
        message = "";
        if(self.m_datestamp):
            message += "[" + BasicLibTime.DateStamp() + "] "
        if(self.m_timestamp):
            message += "[" + BasicLibTime.TimeStamp() + "] " 
        message += p_entry
        sr.rpush(self.m_logtitle, message)
        
#ERRORLOG = Logger("errors.log", "Error Log", True, True)
#USERLOG = Logger("users.log", "User Log", True, True)
ERRORLOG = DbLogger("ErrorLog", True, True)
USERLOG = DbLogger("UserLog", True, True)


'''
def test():
    i = Logger("111.txt", "file title")
    i.Log("test")
    
test()
'''




