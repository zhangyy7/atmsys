#!/usr/bin/env python
# --coding: utf-8 --
"""
信用卡主程序
"""
import os
import sys
MY_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(MY_PATH)
from api import credit_api


def show(page_num):
    num_func = {
        "1": {"module": credit_api, "func": "draw_api"},
        "2": {"module": credit_api, "func": "transfer_api"},
        "3": {"module": credit_api, "func": "repayment"}
    }
    # a = hasattr(credit_api, "draw_api")
    # print(a)
    if hasattr(num_func[page_num]["module"], num_func[page_num]["func"]):
        obj = getattr(num_func[page_num]["module"], num_func[page_num]["func"])
        if callable(obj):
            result = obj()
            return result
        else:
            print(obj)
    else:
        print("404")


# show("1")
