#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : 邓军
# @time    : 2023/9/240 16:19
# @function: 数据库迁移
# @version : V1.0.0
from sqlalchemy import text
from tqdm import tqdm

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
    for table in tqdm(table_list, desc=f"{database}库结构迁移".rjust(30), unit='个'):
        table_name = table['table_name']
        # 获取建表语句
        query_create_sql = f"SHOW CREATE TABLE `{database}`.`{table_name}`"
        query_create_sql_result = origin_mysql.execute(query_create_sql)
        create_table_statement = query_create_sql_result.fetchone()[1]
        # 目标数据库创建表
        try:
            # 创建 语句调整为创建不存在的表
            create_table_statement = create_table_statement.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS')
            # 替换符号 sqlalchemy中冒号为参数占位符，转义
            create_table_statement = create_table_statement.replace(':', '\:')
            target_mysql.execute(create_table_statement)
        except Exception as e:
            print(f"创建{database}.{table_name}表失败，原因：{e.args[0]}")


def transfer_table_data(database, table, where_sql='', batch_size=5000):
    """
    迁移表数据
    :param database: 迁移范围定义
    :param table:  表名称
    :param where_sql: 迁移条件
    :param batch_size: 一次迁移数据量
    :return:
    """
    # 1. 计算数据总量
    count_sql = f"""
        SELECT count(1)
        FROM `{database}`.`{table}`
        {where_sql}
    """
    data_total = origin_mysql.execute(count_sql).fetchone()[0]
    # 2. 数据迁移
    for offset in range(0, data_total, batch_size):
        # 从原始库查询一个批次的数据
        query_sql = f"""
            SELECT *
            FROM `{database}`.`{table}`
            {where_sql}
            LIMIT {batch_size}
            OFFSET {offset}
        """
        query_results = origin_mysql.execute(query_sql)
        # 拼接入库SQL语句及参数
        columns = ','.join(query_results.keys())
        columns_param = ','.join([f':{column}' for column in query_results.keys()])
        insert_sql = f"""
                INSERT INTO `{database}`.`{table}` ({columns})
                VALUES ({columns_param})
            """
        params = [dict(zip(query_results.keys(), result)) for result in query_results]

        # 存入目标库
        target = target_mysql.session
        target.begin()
        target.execute(text(insert_sql), params)
        target.commit()


if __name__ == '__main__':
    transfer_table_data('db_user', 't_user')
