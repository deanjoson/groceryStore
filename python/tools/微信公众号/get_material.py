#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : 邓军
# @time    : 2023/9/29 15:09
# @function: 获取微信公众号素材列表
# @version : V1.0.0
import json
import os

import pandas as pd
import requests

from get_access_token import get_access_token


def get_material(access_token, material_type, offset=0, full=True):
    """
    获取素材列表
    :param access_token: 微信公众号访问许可令牌
    :param material_type:  素材类型
    :param offset: 素材偏移位置
    :param full: 是否全部素材
    :return:
    """
    url = f"https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token={access_token}"
    # 组装参数
    material_list = []
    while True:
        params = {"type": material_type, "offset": offset, "count": 20}
        body = json.dumps(params).encode("utf-8")
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        response = requests.post(url, headers=headers, data=body)
        if response.status_code == 200:
            response_json = json.loads(response.content.decode("utf-8"))
            materials = response_json["item"]
            for material in materials:
                print(f"media_id: {material['media_id']}, name: {material['name']}")
                material_list.append(material)
            total_count = response_json["total_count"]
            item_count = response_json["item_count"]
            # 是否查询所有素材
            if full:
                if offset + item_count < total_count:
                    offset += item_count
                else:
                    break
            else:
                break

    # 将素材结果输出到CSV文件。
    df = pd.DataFrame(material_list)
    # 如果目录不存在则创建
    if not os.path.exists('data'):
        os.makedirs('data')
    df.to_csv(f'data/material_{material_type}.csv', index=False, encoding='utf-8')


if __name__ == '__main__':
    access_token = get_access_token("1", "1")
    get_material(access_token, "image")
