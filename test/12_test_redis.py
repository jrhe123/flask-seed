import redis
import json
import time, random

from threading import Thread


class QueueThread(Thread):
    def __init__(
        self,
        connection,
        team_name,
        max_count=1000,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.connection = connection
        self.key = team_name
        self.max_count = max_count

    def run(self):
        i = 1
        while i <= self.max_count:
            member = f"{self.name}_{i}"
            print("member: ", member)
            self.connection.rpush(self.key, member)
            i += 1
            time.sleep(random.random())


class BaseRedisConnection(object):
    def __init__(self):
        pool = redis.ConnectionPool(
            host="localhost",
            password="",
            port=6379,
            db=0,
            max_connections=20,
            decode_responses=True,  # decode utf-8
        )
        connection = redis.Redis(
            connection_pool=pool,
        )
        self.connection = connection

    def __del__(self):
        try:
            print("destory now")
            self.connection.close()
        except Exception as e:
            print(e)


class TestRedis(BaseRedisConnection):
    def test_set(self):
        user1 = self.connection.set("user1", "Amy")
        print(user1)

    def test_get(self):
        user1 = self.connection.get("user1")
        # user1 = user1.decode("utf-8")
        print(user1)

    def test_mset(self):
        d = {
            "user1": 1,
            "user2": 2,
        }
        result = self.connection.mset(d)
        print(result)

    def test_mget(self):
        result = self.connection.mget(["user1", "user2"])
        print(result)

    def test_incr(self):
        """incr / decr"""
        # self.connection.set("age", 18)
        result = self.connection.incr("age")
        print(result)

    def test_del(self):
        result = self.connection.delete("age")
        print(result)

    def register(self, username, password, nickname):
        user_info = {
            "username": username,
            "password": password,
            "nickname": nickname,
        }
        value = json.dumps(user_info)
        key = f"user:{username}"
        result = self.connection.set(key, value)
        print(result)

    def login(self, username, password):
        key = f"user:{username}"
        result = self.connection.get(key)
        if result is None:
            print("user not found")
            return False
        user_info = json.loads(result)
        if user_info["password"] != password:
            print("incorrect password")
            return False

        print("logged in")
        return True

    def test_push(self):
        """lpush / rpush"""
        # t = ["Amy", "Bob"]
        # self.connection.lpush("user_list", *t)

        user_list = self.connection.lrange("user_list", 0, -1)
        print(user_list)

    def test_pop(self):
        """lpop/ rpop"""
        self.connection.lpop("user_list")
        user_list = self.connection.lrange("user_list", 0, -1)
        print(user_list)

    def test_llen(self):
        len = self.connection.llen("user_list")
        print(len)
        pass

    def queue_up(self):
        """test multi thread"""
        team_name = "team"
        self.connection.delete(team_name)
        t1 = QueueThread(
            name="T1",
            connection=self.connection,
            team_name=team_name,
            max_count=1000,
        )
        t2 = QueueThread(
            name="T2",
            connection=self.connection,
            team_name=team_name,
            max_count=1000,
        )
        t3 = QueueThread(
            name="T3",
            connection=self.connection,
            team_name=team_name,
            max_count=1000,
        )
        t1.start()
        t2.start()
        t3.start()
        #
        t1.join()
        t2.join()
        t3.join()
        # execute after three threads completed
        print("llen: ", self.connection.llen(team_name))

    def test_hset(self):
        result = self.connection.hset("stu:00001", "name", "roy1111")
        print(result)

        exists = self.connection.hexists("stu:00001", "name")
        print(exists)

        # insert only if not exists
        result = self.connection.hsetnx("stu:00001", "name", "roy1111")
        print(result)

    def test_hmset(self):
        m = {
            "name": "Bob",
            "age": 12,
            "grade": 90,
        }
        result = self.connection.hmset("stu:00003", mapping=m)
        print(result)
        keys = self.connection.hkeys("stu:00003")
        print("keys: ", keys)

    def test_hdel(self):
        length = self.connection.hlen("stu:00003")
        print("length: ", length)
        self.connection.hdel("stu:00003", "age")
        length = self.connection.hlen("stu:00003")
        print("length: ", length)

    def register_v2(self, username, password, nickname):
        user_info = {
            "username": username,
            "password": password,
            "nickname": nickname,
        }
        key = f"user_v2:{username}"
        result = self.connection.hset(key, mapping=user_info)
        print(result)

    def login_v2(self, username, password):
        key = f"user_v2:{username}"
        user_info = self.connection.hmget(key, "username", "password")
        print(user_info)
        # ['royroy', '123456']
        if user_info is None:
            print("user not found")
            return False
        if user_info[1] != password:
            print("incorrect password")
            return False

        print("logged in")
        return True

    def test_sadd(self):
        animals = ["dog", "cat"]
        result = self.connection.sadd("zoo1", *animals)
        print(result)
        members = self.connection.smembers("zoo1")
        print(members)

    def test_srem(self):
        result = self.connection.srem("zoo1", "dog")
        print(result)
        members = self.connection.smembers("zoo1")
        print(members)

    def course_analysis(self):
        science_stu_list = [
            "stu003",
            "stu022",
            "stu021",
            "stu012",
            "stu014",
        ]
        self.connection.sadd("science", *science_stu_list)
        english_stu_list = [
            "stu001",
            "stu021",
            "stu011",
            "stu012",
            "stu004",
        ]
        self.connection.sadd("english", *english_stu_list)

        # interset
        result = self.connection.sinter("science", "english")
        print(result)

    def test_zadd(self):
        rank = {
            "user1": 3,
            "user2": 2,
            "user3": 1,
        }
        result = self.connection.zadd("swiming", rank)
        count = self.connection.zcount("swiming", 0, 100)
        print(count)

    def test_zrem(self):
        result = self.connection.zrem("swiming", "user1")
        count = self.connection.zcount("swiming", 0, 100)
        print(count)

    def test_analysis(self):
        result1 = self.connection.zrange("swiming", 0, -1)
        result2 = self.connection.zrange("swiming", 0, 2)
        # first 3 rank
        print(result2)


def main():
    obj = TestRedis()
    # obj.test_del()
    # obj.register(
    #     "royroy",
    #     "123456",
    #     "jiarong",
    # )
    # obj.login(
    #     "royroy",
    #     "1234567",
    # )
    # obj.test_push()
    # obj.test_pop()
    # obj.test_llen()
    # obj.queue_up()
    # obj.test_hset()
    # obj.test_hmset()
    # obj.test_hdel()
    # obj.register_v2(
    #     "royroy",
    #     "123456",
    #     "jiarong",
    # )
    # obj.login_v2(
    #     "royroy",
    #     "123456",
    # )
    # obj.test_sadd()
    # obj.test_srem()
    # obj.course_analysis()
    # obj.test_zadd()
    # obj.test_zrem()
    obj.test_analysis()


if __name__ == "__main__":
    main()
