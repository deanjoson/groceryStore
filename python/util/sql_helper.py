#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : 邓军
# @time    : 2023/10/1 11:59
# @function: SQL语句执行操作助手
# @version : V1.0.0

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


class SqlHelper:
    """
        SQL操作助手
    """

    def __init__(self,
                 mysql_host='127.0.0.1',
                 mysql_port=3306,
                 mysql_user='root',
                 mysql_password='root',
                 mysql_db='',
                 echo_sql=False) -> None:
        engine = create_engine(
            url=f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}?charset=utf8mb4',
            echo=echo_sql  # 日志打印sql执行语句
        )
        self.session = sessionmaker(bind=engine).__call__()

    def query(self, sql, params=None):
        """
        查询数据
        :param sql:  SQL语句
        :param params: SQL语句参数
        :return:  返回结果
        """
        return self.session.execute(text(sql), params).fetchall()

    def query_dict(self, sql, params=None):
        """
        查询数据（以DICT结构返回）
        :param sql: SQL语句
        :param params: SQL语句参数
        :return:  返回结果
        """
        results = self.execute(sql, params)
        return [dict(zip(results.keys(), result)) for result in results]

    def execute(self, sql, params=None):
        """
        执行SQL语句
        :param sql: SQL语句
        :param params:  SQL语句参数
        :return:
        """
        result = self.session.execute(text(sql), params)
        self.session.commit()
        self.session.close()
        return result
