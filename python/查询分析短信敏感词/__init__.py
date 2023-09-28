#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : 邓军
# @time    : 2023/9/27 16:59
# @function: 从数据库短信表中查询历史所有短信内容，逐条调用接口查询是否包含敏感词，并将结果输出到文件进行分析
# @version : V1.0.0
import json

import pandas as pd
import requests
from tqdm import tqdm

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

# 短信内容及敏感词
sms_content = []
# 敏感词合集
sensitive_word = set()

# 2. 逐条内容调用接口，检查是否包含敏感词
# 将集合放入tqdm，显示执行进度
for result in tqdm(results, desc='短信内容分析'):
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
        # 如果存在敏感词，则整理短信
        if len(sensitive_words) > 0:
            # 收集出现的敏感词合集。
            [sensitive_word.add(item) for item in sensitive_words]
            # 将短信和敏感词组合在一起
            sms_content.append({
                "notice_id": result['notice_id'],
                "content": result['content'],
                "sensitive_word": ','.join(sensitive_words)
            })

# 3. 将结果输出到CSV文件。
sms_content_df = pd.DataFrame(sms_content)
sms_content_df.to_csv('sms_content.csv', index=False, encoding='utf-8')

# 4. 将敏感词输出到CSV文件。
sensitive_word_df = pd.DataFrame(sms_content)
sensitive_word_df.to_csv('sensitive_word.csv', index=False, encoding='utf-8')
