#!/usr/bin/env python
# --coding: utf-8 --
"""
信用卡主程序
"""
import os
import sys

from api import credit_api
from conf import templates

MY_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(MY_PATH)


def show(page_num):
    # print(page_num, type(page_num))
    """
    当用户选择了信用卡中心，接收用户选择要干的事情编号，利用字典和反射执行函数
    param page_num:用户选择的编号
    """
    num_func = {
        "1": {"module": credit_api, "func": "draw_api"},
        "2": {"module": credit_api, "func": "transfer_api"},
        "3": {"module": credit_api, "func": "repayment"}
    }
    # a = hasattr(credit_api, "draw_api")
    # print(a)
    print(num_func.get(page_num))
    if num_func.get(page_num):
        if hasattr(num_func[page_num]["module"], num_func[page_num]["func"]):
            obj = getattr(num_func[page_num]["module"],
                          num_func[page_num]["func"])
            if callable(obj):
                result = obj()
                return result
            else:
                print(obj)
        # else:
        #     print("404")
    else:
        print("404")


def main():
    choice = templates.show_index()
    choice = templates.show_page(choice)
    show(choice)
