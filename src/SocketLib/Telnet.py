'''
Created on 2012-4-24

@author: sky
'''
reset = chr(27) + "[0m"
bold = chr(27) + "[1m"
dim = chr(27) + "[2m"
under = chr(27) + "[4m"
reverse = chr(27) + "[7m"
hide = chr(27) + "[8m"

clearscreen = chr(27) + "[2J"
clearline = chr(27) + "[2K"

black = chr(27) + "[30m"
red = chr(27) + "[31m"
green = chr(27) + "[32m"
yellow = chr(27) + "[33m"
blue = chr(27) + "[34m"
magenta = chr(27) + "[35m"
cyan = chr(27) + "[36m"
white = chr(27) + "[37m"

bblack = chr(27) + "[40m"
bred = chr(27) + "[41m"
bgreen = chr(27) + "[42m"
byellow = chr(27) + "[43m"
bblue = chr(27) + "[44m"
bmagenta = chr(27) + "[45m"
bcyan = chr(27) + "[46m"
bwhite = chr(27) + "[47m"

newline = "\r\n" + chr(27) + "[0m"


BUFFERSIZE = 1024

class Telnet:
    def __init__(self):
        self.m_buffer =""
        
    def Buffered(self):
        return len(self.m_buffer) != 0
    
    def Translate(self, p_conn, p_buffer, p_size):
        for i in range(0, p_size):
            c = p_buffer[i]
            if c >= 32 and c != 127 and len(self.m_buffer) < BUFFERSIZE:
                self.m_buffer += chr(c)
            elif c == 8 and len(self.m_buffer) > 0:
                self.m_buffer[0:len(self.m_buffer) - 1]
            # c == "\r" or c == "\n"
            elif c == 10 or c == 13:
                if len(self.m_buffer) > 0 and p_conn.Handler() != 0:
                    p_conn.Handler().Handle(self.m_buffer)
                self.m_buffer = ""
                
    def SendString(self, p_conn, p_string):
        p_conn.BufferData(p_string)
        

    
