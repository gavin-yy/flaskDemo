from flask import Flask, jsonify, request
from common.mysql_operate import db
from common.redis_operate import redis_db
from common.md5_operate import get_md5
import re, time

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False  # jsonify返回的中文正常显示


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/users", methods=["GET"])
def get_all_users():
    """获取所有用户信息"""
    sql = "SELECT * FROM user"
    data = db.select_db(sql)
    print("获取所有用户信息 == >> {}".format(data))
    return jsonify({"code": 0, "data": data, "msg": "查询成功"})


@app.route("/users/<string:username>", methods=["GET"])
def get_user(username):
    """获取某个用户信息"""
    sql = "SELECT * FROM user WHERE username = '{}'".format(username)
    data = db.select_db(sql)
    print("获取 {} 用户信息 == >> {}".format(username, data))
    if data:
        return jsonify({"code": 0, "data": data, "msg": "查询成功"})
    return jsonify({"code": "1004", "msg": "查不到相关用户的信息"})


@app.route("/register", methods=['POST'])
def user_register():
    """注册用户"""
    username = request.json.get("username", "").strip()  # 用户名
    password = request.json.get("password", "").strip()  # 密码
    sex = request.json.get("sex", "0").strip()  # 性别，默认为0(男性)
    telephone = request.json.get("telephone", "").strip()  # 手机号
    address = request.json.get("address", "").strip()  # 地址，默认为空串

    if username and password and telephone: # 注意if条件中 "" 也是空, 按False处理
        sql1 = "SELECT username FROM user WHERE username = '{}'".format(username)
        res1 = db.select_db(sql1)
        print("查询到用户名 ==>> {}".format(res1))
        sql2 = "SELECT telephone FROM user WHERE telephone = '{}'".format(telephone)
        res2 = db.select_db(sql2)
        print("查询到手机号 ==>> {}".format(res2))

        if res1:
            return jsonify({"code": 2002, "msg": "用户名已存在，注册失败！！！"})
        elif not (sex == "0" or sex == "1"):
            return jsonify({"code": 2003, "msg": "输入的性别只能是 0(男) 或 1(女)！！！"})
        elif not (len(telephone) == 11 and re.match(r"^1[3578]\d{9}$", telephone)):
            return jsonify({"code": 2004, "msg": "手机号格式不正确！！！"})
        elif res2:
            return jsonify({"code": 2005, "msg": "手机号已被注册！！！"})
        else:
            password = get_md5(username, password) # 把传入的明文密码通过MD5加密变为密文，然后再进行注册
            sql3 = "INSERT INTO user(username, password, role, sex, telephone, address) " \
                  "VALUES('{}', '{}', '1', '{}', '{}', '{}')".format(username, password, sex, telephone, address)
            db.execute_db(sql3)
            print("新增用户信息SQL ==>> {}".format(sql3))
            return jsonify({"code": 0, "msg": "恭喜，注册成功！"})
    else:
        return jsonify({"code": 2001, "msg": "用户名/密码/手机号不能为空，请检查！！！"})


@app.route("/login", methods=['POST'])
def user_login():
    """登录用户"""
    username = request.values.get("username", "").strip()
    password = request.values.get("password", "").strip()

    login_info = { # 构造一个字段，将 id/username/token/login_time 返回
                "username": username,
                "from": "redis/db",
                "login_time": time.strftime("%Y/%m/%d %H:%M:%S")
    }

    if username and password: # 注意if条件中空串 "" 也是空, 按False处理
        md5_password = get_md5(username, password)

        v = redis_db.get_value_by_key(username)
        if ( v ) :
            login_info["from"] = "redis"

            # redis 中存储了这个user，匹配redis中的值.
            if v.decode("utf-8") == md5_password:
                return jsonify({"code": 0, "login_info": login_info, "msg": "login success"})
            else:
                print("value from redis is:{}".format(v))
                print("value from request is:{}".format(md5_password), flush=True)
                return jsonify({"code": -1, "login_info": login_info, "msg": "login failed"})
        else:
            login_info["from"] = "db"
            sql2 = "SELECT * FROM user WHERE username = '{}' and password = '{}'".format(username, md5_password)
            res2 = db.select_db(sql2)
            if res2:
                #更新值到redis中
                redis_db.save_value_of_key(username, md5_password )
                return jsonify({"code": 0, "login_info": login_info, "msg": "login success db"})
            else:
                return jsonify({"code": -1, "login_info": login_info, "msg": "login failed db"})
    else:
        return jsonify({"code": -1, "login_info": login_info, "msg": "should provide username & passwd"})

