'''
Created on 2012-4-16

@author: sky
'''
class A:
    def __init__(self, cc):
        self.cc = "111"
        
class B(A):
    aaa= "12121"
    def __init__(self, cc):
        A.__init__(self, cc)
        
a = B("222")
print(a.cc)
    
