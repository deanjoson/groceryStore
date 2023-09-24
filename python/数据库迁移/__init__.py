#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : 邓军
# @time    : 2023/9/240 16:19
# @function: 数据库迁移
# @version : V1.0.0

from python.util.sql_helper import SqlHelper

origin_mysql = SqlHelper(mysql_host='192.168.255.222', mysql_port=3307, mysql_user='root', mysql_password='root')
target_mysql = SqlHelper(mysql_host='192.168.255.222', mysql_port=3310, mysql_user='root', mysql_password='root')


def transfer_table_structure(database, table_regex='.*'):
    """
    迁移数据库结构
    :param database: 数据库名称
    :param table_regex: 需要迁移的表名称正则表达式(默认迁移所有表)
    :return:
    """
    # 1. 在目标库中创建数据库
    target_mysql.execute(f"CREATE DATABASE IF NOT EXISTS `{database}`")

    # 2. 切换至目标数据库
    target_mysql.execute(f"USE `{database}`")

    # 3. 从原数据库获取符合条件的表。
    query_table_sql = f"""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = '{database}'
          AND table_name REGEXP '{table_regex}'
        """
    table_list = origin_mysql.query_dict(query_table_sql)
    # 4. 从原始表获取创建表语句，并逐个表在目标库中创建
    for table in table_list:
        table_name = table['table_name']
        # 获取建表语句
        query_create_sql = f"SHOW CREATE TABLE `{database}`.`{table_name}`"
        query_create_sql_result = origin_mysql.execute(query_create_sql)
        create_table_statement = query_create_sql_result.fetchone()[1]
        # 目标数据库创建表
        try:
            # 创建 语句调整为创建不存在的表
            create_table_statement = create_table_statement.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS')
            target_mysql.execute(create_table_statement)
        except Exception as e:
            print(f"创建{database}.{table_name}表失败，原因：{e.args[0]}")


if __name__ == '__main__':
    transfer_table_structure('db_user')
