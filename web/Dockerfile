FROM python

LABEL description="python web server with redis and mysql"

RUN apt-get update && \
    apt-get install -y mariadb-server


RUN python3 -m pip install flask && \
    python3 -m pip install PyMySQL && \
    python3 -m pip install redis && \
    pip install mysql-connector-python

# 配置 MySQL
RUN mkdir -p /var/run/mysqld && \
    chown -R mysql:mysql /var/run/mysqld

# 初始化 MySQL 数据库, 错误，没有挂载本机目录，不要安装默认的数据库。
#RUN mysql_install_db --user=mysql --basedir=/usr --ldata=/var/lib/mysql
# RUN mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql

# 设置 MySQL 默认配置
COPY mysql.cnf /etc/mysql/my.cnf

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 创建工作目录
WORKDIR /app

# 复制当前目录下的所有文件到工作目录
# COPY flashDemo /app
RUN mkdir -p /web_files

# 设置默认启动命令
#CMD ["sh", "-c", "python app.py"]

RUN echo 'build complete'
