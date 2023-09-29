#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : 邓军
# @time    : 2023/9/29 14:15
# @function: 获取微信公众号访问许可
# @version : V1.0.0
import json
import re

import requests


def get_access_token(app_id, app_secret):
    """
    获取访问许可令牌
    :return:
    """
    access_token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    response = requests.get(access_token_url)
    if response.status_code == 200:
        response_json = json.loads(response.text)
        # print(response.text)
        if 'access_token' in response_json:
            print(f"获取到访问许可令牌：{response_json['access_token']}")
            return response_json['access_token']
        if 'errcode' in response_json:
            if response_json['errcode'] == 40013:
                print(f'不正确的AppID或AppSecret，请检查配置')
            elif response_json['errcode'] == 40164:
                errmsg = response_json['errmsg']
                ipv4 = re.findall(r'ip(.*?)ipv6', errmsg)[0].strip()
                print(f"请先前往mp.weixin.qq.com配置IP白名单: {ipv4}")
            else:
                print(f"获取访问许可失败：{response_json['errmsg']}")
            return None


if __name__ == '__main__':
    get_access_token('1', '1')
