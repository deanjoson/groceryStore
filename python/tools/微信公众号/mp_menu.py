#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : 邓军
# @time    : 2024/1/31 16:16
# @function: 微信公众号菜单
# @version : V1.0.0
import json

import requests

from get_access_token import get_access_token


def get_mp_menu(access_token):
    """
    获取现有公众号菜单配置信息
    :param access_token:
    :return:
    """
    url = f"https://api.weixin.qq.com/cgi-bin/menu/get?access_token={access_token}"
    response = requests.get(url)
    response_json = json.loads(response.content.decode("utf-8"))
    if 'errcode' not in response_json:
        print(json.dumps(response_json, indent=2))
    else:
        print(f"获取公众号菜单配置失败:{response_json['errmsg']}")


if __name__ == '__main__':
    access_token = get_access_token('1', '1')
    get_mp_menu(access_token)
