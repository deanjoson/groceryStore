#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : 邓军
# @time    : 2023/9/29 14:15
# @function: 获取微信公众号访问许可
# @version : V1.0.0
import json
import re

import requests

APP_ID = "wx0000000000000"
APP_SECRET = "0000000000000000000"

ACCESS_TOKEN_URL = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"

response = requests.get(ACCESS_TOKEN_URL)
if response.status_code == 200:
    response_json = json.loads(response.text)
    if response_json['errcode'] == 40164:
        errmsg = response_json['errmsg']
        ipv4 = re.findall(r'ip(.*?)ipv6', errmsg)[0].strip()
        print(f"请先前往mp.weixin.qq.com配置IP白名单: {ipv4}")
    # print(response.text)
