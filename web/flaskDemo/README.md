# flaskDemo

本接口项目的技术选型：Python+Flask+MySQL+Redis，通过 Python+Falsk 来开发接口，使用 MySQL 来存储用户信息，使用 Redis 用于存储token，目前为纯后端接口，暂无前端界面，可通过 Postman、Jmeter、Fiddler 等工具访问请求接口。

## 项目部署

```

docker build -t web_mysql:v1 .

# 不执行默认的entrypoint命令，执行shell
docker-compose run --entrypoint /bin/bash web_sql

# 添加mysql用户，创建默认数据库和表
/app/mysql_db_init.sh

# 运行docker
docker-compose up -d
```

## 数据库设计

数据库建表语句如下：

```
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` tinyint(1) NOT NULL,
  `sex` tinyint(1) DEFAULT NULL,
  `telephone` varchar(255) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `telephone` (`telephone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

user表中各字段对应含义如下：

```
id：用户id号，自增长
username：用户名
password：密码
role：用户角色，0表示管理员用户，1表示普通用户
sex：性别，0表示男性，1表示女性，允许为空
telephone：手机号
address：联系地址，允许为空
```

## 接口请求示例

```
验证web服务器正常运行
curl http://172.19.0.5:9999


查看users列表
curl http://172.19.0.5:9999/users


添加用户
curl -X POST http://172.19.0.5:9999/register -H "Content-Type: application/json" -d '{"username": "bob", "password": "123456", "sex": "1", "telephone":"13500010006", "address": "上海市"}
'

测试用户登录
~$ curl -X POST http://172.19.0.5:9999/login -H "Content-Type: application/x-www-form-urlencoded" -d 'username=bob&password=123456'
{
  "code": 0,
  "login_info": {
    "from": "db",   --redis未存储该用户，通过数据库查询匹配
    "login_time": "2025/02/10 07:32:40",
    "username": "bob"
  },
  "msg": "login success db"
}


$ curl -X POST http://172.19.0.5:9999/login -H "Content-Type: application/x-www-form-urlencoded" -d 'username=bob&password=123456'
{
  "code": 0,
  "login_info": {
    "from": "redis",   -- redis中匹配成功
    "login_time": "2025/02/10 07:38:04",
    "username": "bob"
  },
  "msg": "login success"
}

```
