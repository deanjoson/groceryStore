#!/bin/bash

for dbname in ` ls | grep -Ei "db"`
do
    echo "开始导入数据库${dbname} `date '+%Y-%m-%d %H:%M:%S'`"
    gunzip < $dbname | mysql -uroot -p'root';
    echo "数据库导入完成${dbname} `date '+%Y-%m-%d %H:%M:%S'`"
done;

echo "数据库导入完成"