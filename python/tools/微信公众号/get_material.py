#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : 邓军
# @time    : 2023/9/29 15:09
# @function: 获取微信公众号素材列表
# @version : V1.0.0
import json

import requests

from get_access_token import get_access_token

# 1. 获取访问许可
access_token = get_access_token("1", "1")
get_material_url = f"https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token={access_token}"

# 组装参数
params = {"type": 'image', "offset": 0, "count": 20}
body = json.dumps(params).encode("utf-8")
headers = {"Content-Type": "application/json;charset=UTF-8"}
response = requests.post(get_material_url, headers=headers, data=body)

print(response.content.decode("utf-8"))
