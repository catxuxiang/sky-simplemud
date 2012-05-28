# -*- coding: gbk -*- 
'''
Created on 2012-5-26

@author: Sky
'''
from redis.client import StrictRedis
Sr = StrictRedis(host='localhost', port=6379, db=0)
Sr.set('foo', 'bar')
#print(str(Sr.get('foo'), encoding = "utf-8") == 'bar')
print(Sr.get('foo'))
Sr.hset("MyHash", "field1", "许翔")
print(Sr.hget("MyHash", "field11"))
Sr.rpush("list", "one")
Sr.rpush("list", "two")
print(Sr.llen("list"))
Sr.ltrim("list", 1, 0)
print(Sr.llen("list"))
Sr.hset("MyHash", "Key1", "Value1")
Sr.hset("MyHash", "Key2", "Value2")
for i in Sr.hkeys("MyHash"):
    print(i)
print(Sr.hlen("PlayerHash"))
print(Sr.get("XXX"))
print(type(Sr.smembers("EnemyTemplate:16:LOOT")))
for i in Sr.smembers("EnemyTemplate:16:LOOT"):
    print(i)

