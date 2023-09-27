#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : 邓军
# @time    : 2023/9/27 16:59
# @function: 从数据库短信表中查询历史所有短信内容，逐条调用接口查询是否包含敏感词，并将结果输出到文件进行分析
# @version : V1.0.0
import json

import requests

from python.util.sql_helper import SqlHelper

sql_helper = SqlHelper(mysql_host='127.0.0.1',
                       mysql_port=3307,
                       mysql_user='root',
                       mysql_password='root',
                       mysql_db='',
                       echo_sql=False)

# 1. 从数据库中获取所有短信内容
select_sql = f'SELECT notice_id,content FROM db_notice.t_sms '
results = sql_helper.query_dict(select_sql)

for result in results:
    data = {
        "text": result['content']
    }
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(
        url='http://127.0.0.1:8003/sensitive/open/findAll',
        headers=headers,
        data=json.dumps(data)
    )
    # 响应成功
    if response.status_code == 200:
        response_json = json.loads(response.text)
        sensitive_words = response_json['data']
        print(','.join(sensitive_words))
