'''
Created on 2012-4-14

@author: Sky
'''
def UpperCase(string):
    return str(string).upper()

def LowerCase(string):
    return str(string).lower()

def SearchAndReplace(string, old, new):
    return str(string).replace(old, new)

def TrimWhitespace(string):
    return str(string).strip()

def ParseWord(string, index):
    string = str(string).strip()
    while string.replace("  "," ") != string:
        string = string.replace("  "," ")
    tmp = string.split(' ')
    return tmp[index].strip()

def RemoveWord(string, index):
    string = str(string).strip()
    while string.replace("  "," ") != string:
        string = string.replace("  "," ")
    tmp = string.split(' ') 
    str1 = "";   
    for i in range(len(tmp)):
        if i != index :
            str1 += tmp[i] + " "
    return str1.strip()
        

#print (RemoveWord("   111                 222    33  ", 0))
