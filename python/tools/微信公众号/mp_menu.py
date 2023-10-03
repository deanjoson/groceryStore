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


def set_mp_menu(access_token):
    """
    设置微信公众号菜单
    :param access_token:
    :return:
    """

    url = f"https://api.weixin.qq.com/cgi-bin/menu/create?access_token={access_token}"

    params = {
        "button": [
            {
                "name": "我的服务",
                "sub_button": [
                    {
                        "name": "我的百度",
                        "type": "view",
                        "url": "https://h5.baidu.com/authorize"
                    },
                    {
                        "pagepath": "pages/index/index",
                        "appid": "wx04sssss8",
                        "name": "小程序",
                        "type": "miniprogram",
                        "url": "https://www.baidu.com"
                    }
                ]
            },
            {
                "name": "会议文章",
                "type": "view",
                "url": "https://mp.weixin.qq.com/mp/homepage?__biz=MzU0MDgxNjAzMw==&hid=1&sn=bee8fb817d0ssssc1371967"
            },
            {
                "name": "关于我们",
                "sub_button": [
                    {
                        "name": "加入我们",
                        "type": "view",
                        "url": "https://m.zhipin.com/mpa/html/weijd/weijd-boss/9db5c3a6456867ssssssss=qr_self"
                    },
                    {
                        "name": "商务合作",
                        "type": "media_id",
                        "media_id": "pgzTr7pkg59QjeMPFq2Jsssss-Ey4k363zXD55xj3BHKtcRlGp10v_OqC18y"
                    }
                ]
            }
        ]
    }
    body = json.dumps(params, ensure_ascii=False).encode('utf-8')
    response = requests.post(url.format(access_token), data=body)
    content = response.json()
    print(content)


if __name__ == '__main__':
    access_token = get_access_token('1', '1')
    get_mp_menu(access_token)
    # set_mp_menu(access_token)
