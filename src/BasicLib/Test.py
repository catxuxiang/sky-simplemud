'''
Created on 2012-4-14

@author: Sky
'''
a = {}
a["aaa"] = 1
a["bbb"] =2
for i in a:
    print(i)
for i in a.keys():
    print(i)

index = -1
tmp = 0
for i in a.keys():
    if i == "aaa":
        del a[i]
        
for i in a.values():
    print(i)        
