'''
Created on 2012-5-26

@author: Sky
'''
from redis.client import StrictRedis
r = StrictRedis(host='localhost', port=6379, db=0)
r.set('foo', 'bar')
#print(str(r.get('foo'), encoding = "utf-8") == 'bar')
print(r.get('foo'))

