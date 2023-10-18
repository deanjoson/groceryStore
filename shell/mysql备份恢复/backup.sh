#!/bin/bash

# 需要使用mysql自带的mysqldump工具

for dbname in ` mysql -uroot -p'root' -e "show databases;" | grep -Ei "db"`
do
    echo '开始备份数据库${dbname} `date '+%Y-%m-%d %H:%M:%S'`'
    mysqldump -uroot -p'root' --events --single-transaction --default-parallelism=5 -B $dbname | gzip > data/${dbname}_bak.sql.gz
    echo '数据库备份完成${dbname} `date '+%Y-%m-%d %H:%M:%S'`'
done;

echo '数据库全量备份完成'