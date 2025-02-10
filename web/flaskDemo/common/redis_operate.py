import redis
from config.setting import REDIS_SENTINEL_HOST, REDIS_SENTINEL_PORT, REDIS_PASSWD, EXPIRE_TIME


class RedisDb():

    def __init__(self, sen_host, sen_port, passwd):
        self.sentinel = redis.sentinel.Sentinel([(sen_host, sen_port)], socket_timeout=0.5)
        self.passwd=passwd
        self.master = self.sentinel.master_for('mymaster', password=passwd, socket_timeout=0.5) # 从连接池获取一个与maser的连接
        self.slave = self.sentinel.slave_for('mymaster', password=passwd, socket_timeout=0.5) # 从连接池获取一个与slave的连接

        print(self.master)
        print(self.slave)

        # 建立数据库连接
        # self.r = redis.Redis(
        #     host=host,
        #     port=port,
        #     password=passwd,
        #     decode_responses=True # get() 得到字符串类型的数据
        # )

    def handle_redis_token(self, key, value=None):
        if value: # 如果value非空，那么就设置key和value，EXPIRE_TIME为过期时间
            self.master = self.sentinel.master_for('mymaster', password=passwd, socket_timeout=0.5) # 从连接池获取一个与maser的连接
            self.master.set(key, value, ex=EXPIRE_TIME)
        else: # 如果value为空，那么直接通过key从redis中取值
            self.slave = self.sentinel.slave_for('mymaster', password=passwd, socket_timeout=0.5) # 从连接池获取一个与slave的连接
            redis_token = self.slave.get(key)
            return redis_token

    def get_value_by_key(self, key):
        self.slave = self.sentinel.slave_for('mymaster', password=self.passwd, socket_timeout=0.5) # 从连接池获取一个与slave的连接
        redis_token = self.slave.get(key)
        return redis_token

    def save_value_of_key(self, key, value):
        self.master = self.sentinel.master_for('mymaster', password=self.passwd, socket_timeout=0.5) # 从连接池获取一个与maser的连接
        self.master.set(key, value, ex=EXPIRE_TIME)


# 提供sentinel的host和端口
redis_db = RedisDb(REDIS_SENTINEL_HOST, REDIS_SENTINEL_PORT, REDIS_PASSWD)