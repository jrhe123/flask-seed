1. table plus
2. redis-cli -h host -p port -a password
3. check status
ping
4. value type
String / List / Hash / Set / zSet
5. set key value
set a abc
get a
keys *
type a
6. select db (0-15) - default 0
select 1
7. move key db
move a 1
8. exists
exists a
9. rename
rename a aa
10. del
del a
11. expire / pexpire / expireat
expire a 1 (1 second)
12. ttl / pttl : check expire time
ttl a -> seconds, if -2 is expired, -1 is not set

=========String==========

13. mset key1 val1 key2 val2
mset a 1 b 2
mget a b
14. append
append a "123"
15. atomic increase / decrease
set a 10
incr a -> 11
decr a -> 9
incrby a 2 -> 12
decrby a 2 -> 8
16. expire auto delete
set a ex 10 (sec)
set a px 10000 (millsec)
17. if not exist and set
set a 1 nx
18. if exist and set
set a 1 xx

=========List==========

19. lpush / rpush -> add
lpush list a
rpush list b
20. llen -> check length
llen list
21. lpop / rpop -> remove
lpop list
rpop list
22. lrange -> search by index
[a, b, c, d]
=> [0, 1, 2, 3] indexes
lrange key 0 5
23. lset -> set value by index
lset list 0 aaa
=> [aaa, b, c, d]
24. ltrim -> sub list
ltrim list 1 2
=> [b, c]
25. lpushx / rpushx -> execute only if exists

=========Hash==========

26. hset key field value
hset a username roytest
hset a password 123456
27. hget key field
hget a username
hget a password
28. hdel key field1 field2
hdel a username
29. hmset key field1 value1 field2 value2
hmset a username roytest2 password 111111
30. hmget key field1 field2
hmget a username password
31. hlen key -> check how many fields
hlen a -> 2
32. hkeys key -> get all keys
33. hvals key -> get all values
34. hexists key field
hexists a username
35. hsetnx -> set if not exists
hsetnx a username roytest222
36. hsetxx -> set if exists
hsetxx a username roytest222
37. hincrby -> increment by "1"
hset a score 90
hincrby a score 1

=========Set (no ordered)==========

38. sadd key member1 member2
sadd a 123 321
39. srem key member1 member2
srem a 123 321
40. smembers key
smembers a
=> 123 321
41. sismember key member
sismember a 123 -> 1 / 0
42. sunion a b -> get union set
43. sinter a b -> get interset set
44. sdiff a b -> get diff set
sadd zoo1 pig dog cat
sadd zoo2 cat bird

sunion zoo1 zoo2 -> pig dog cat bird
sinter zoo1 zoo2 -> dog cat
sdiff zoo1 zoo2 -> pig
sdiff zoo2 zoo1 -> bird

=========zSet (ordered)==========

45. zadd key score1 member1 score2 member2 -> add
zadd grades 1 User1 2 User2 3 User3
46. zincrby key n member -> increment
47. zrem key member1 member2 -> remove
zrem grade User3
48. zcard key -> number of member
zcard grades => 3
49. zcount key min max -> count number of member in this score range
zcount grades 0 3 => 3
50. zscore key -> check score
zscore grade User1 => 1 
51. zrange key start stop -> start: index, stop: index (asc)
zrange grades 0 3 => User1 User2 User3
zrange grades 0 -1 => everything
52. zrevrange key start stop -> start: index, stop: index (desc)
53. zrank / zrevrank -> check ranking
zrank grades User2 => 1
[0, 1, 2]