#!/bin/bash

# MySQL root 用户的密码
MYSQL_ROOT_PASSWORD="rootpassword"

# 新用户信息
NEW_USER="yyy"
NEW_PASSWORD="8899!@cd00"

# 数据库名称
DB_NAME="flask_demo"

# 创建用户和数据库的 SQL 脚本
SQL_SCRIPT=$(cat <<EOF

DROP USER IF EXISTS '$NEW_USER'@'%';

CREATE USER '$NEW_USER'@'%' IDENTIFIED BY '$NEW_PASSWORD';

GRANT ALL PRIVILEGES ON flash_demo.* TO '$NEW_USER'@'%' WITH GRANT OPTION;

-- 创建数据库
CREATE DATABASE IF NOT EXISTS $DB_NAME;

-- 使用数据库
USE $DB_NAME;

-- 删除 user 表（如果存在）
-- DROP TABLE IF EXISTS user;

-- 创建表
CREATE TABLE IF NOT EXISTS user (
  id int(11) NOT NULL AUTO_INCREMENT,
  username varchar(20) NOT NULL,
  password varchar(255) NOT NULL,
  role tinyint(1) NOT NULL,
  sex tinyint(1) DEFAULT NULL,
  telephone varchar(255) NOT NULL,
  address varchar(255) DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY telephone (telephone)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 刷新权限
FLUSH PRIVILEGES;
EOF
)

# 执行 SQL 脚本
echo "$SQL_SCRIPT" | mysql -u root -p"$MYSQL_ROOT_PASSWORD"


#DROP USER IF EXISTS '$NEW_USER'@'%';
#CREATE USER '$NEW_USER'@'%' IDENTIFIED BY '$NEW_PASSWORD';
#GRANT ALL PRIVILEGES ON flash_demo.* TO '$NEW_USER'@'%' WITH GRANT OPTION;

#SQL_CREATE_USER="
#GRANT ALL PRIVILEGES ON flash_demo.* TO '$NEW_USER'@'%' WITH GRANT OPTION;
#FLUSH PRIVILEGES;
#"

# 执行 SQL 脚本
#echo "$SQL_CREATE_USER" | mysql -u root -p"$MYSQL_ROOT_PASSWORD"

