'''
Created on 2012-5-5

@author: Sky
'''
b1 = b"\xff\xfb\x1f\xff\xfb \xff\xfb\x18\xff\xfb'\xff\xfd\x01\xff\xfb\x03\xff\xfd\x03"

string = ""
for i in b1:
    if i < 128:
        string += chr(i)
print(string)
    
