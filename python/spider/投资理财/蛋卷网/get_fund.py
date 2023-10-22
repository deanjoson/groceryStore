#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : 邓军
# @time    : 2023/10/22 14:05
# @function: 根据基金代码查询获取基金信息
# @version : V1.0.0
import requests


def get_fund(fund_code):
    """
    从蛋卷基金数据
    :param fund_code: 基金代码
    :return:
    """
    url = "https://danjuanfunds.com/djapi/fund/detail/{}".format(fund_code)
    response = requests.get(
        url,
        headers={
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Referer": "https://danjuanfunds.com/funding/110011?channel=1300100141",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
            "elastic-apm-traceparent": "00-ce58f82d3f8e8e6fcd54397fd0f38574-adb2e157029a1192-01"},
        cookies={
            "Hm_lpvt_d8a99640d3ba3fdec41370651ce9b2ac": "1603885299",
            "Hm_lvt_d8a99640d3ba3fdec41370651ce9b2ac": "1602344637,1602344758,1602344764,1603369369",
            "_ga": "GA1.2.1397406205.1593612461",
            "acw_tc": "2760822016038852981828649e5a0c60b368285cb530c1a2e8d169c1867d83",
            "channel": "1300100141",
            "device_id": "web_SkS2df508",
            "gr_user_id": "2ac24d8b-927e-475d-8f29-27589058f70f",
            "timestamp": "1603885317702",
            "xq_a_token": "c2974070ad952835feab798d5278f70696c9f25c"},
    )
    if response.status_code == 200:
        print(response.content.decode('utf-8'))
    else:
        return None


if __name__ == '__main__':
    get_fund('110011')