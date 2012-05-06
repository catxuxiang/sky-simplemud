'''
Created on 2012-4-24

@author: sky
'''
reset = "\x1B[0m"
bold = "\x1B[1m"
dim = "\x1B[2m"
under = "\x1B[4m"
reverse = "\x1B[7m"
hide = "\x1B[8m"

clearscreen = "\x1B[2J"
clearline = "\x1B[2K"

black = "\x1B[30m"
red = "\x1B[31m"
green = "\x1B[32m"
yellow = "\x1B[33m"
blue = "\x1B[34m"
magenta = "\x1B[35m"
cyan = "\x1B[36m"
white = "\x1B[37m"

bblack = "\x1B[40m"
bred = "\x1B[41m"
bgreen = "\x1B[42m"
byellow = "\x1B[43m"
bblue = "\x1B[44m"
bmagenta = "\x1B[45m"
bcyan = "\x1B[46m"
bwhite = "\x1B[47m"

newline = "\r\n\x1B[0m"


BUFFERSIZE = 1024

class Telnet:
    def __init__(self):
        self.m_buffersize = 0
        
    def Buffered(self):
        return self.m_buffersize
    
    def Translate(self, p_conn, p_buffer, p_size):
        for i in range(0, p_size):
            c = p_buffer[i]
            if ord(c) >= 32 and ord(c) != 127 and self.m_buffersize < BUFFERSIZE:
                self.m_buffer[self.m_buffersize] = c
                self.m_buffersize += 1
            elif ord(c) == 8 and self.m_buffersize > 0:
                self.m_buffersize -= 1
            elif c == '\n' or c == '\r':
                if self.m_buffersize > 0 and p_conn.Handler() != 0:
                    p_conn.Handler().Handle(self.m_buffer, self.m_buffersize)
                self.m_buffersize = 0
                
    def SendString(self, p_conn, p_string):
        p_conn.BufferData(p_string.data(), p_string.size())
        

    
