#!/bin/bash

# 数据目录
DATADIR="/var/lib/mysql"

# 检查数据目录是否为空
if [ ! -d $DATADIR/sys ]; then
    echo "Initializing database..."
    mariadb-install-db --user=mysql --basedir=/usr --datadir=$DATADIR
else
    echo "Database already initialized."
fi

# 启动 MariaDB
exec mysqld --defaults-file=/etc/mysql/my.cnf --user=mysql &

sleep 5
echo "mysqld should be running, entrypoint.sh arg is : $1"


# 检查是否有参数传入
if [ "$1" = "bash" ]; then
    /bin/bash
else
    exec python app.py
fi