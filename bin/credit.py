#!/usr/bin/env python
# --coding: utf-8 --
"""
信用卡主程序
"""
import sys

from api import credit_api as ca
from conf import templates as tl


def main():
    """
    当用户选择了信用卡中心，接收用户选择要干的事情编号，利用字典和反射执行函数
    param p_num:用户选择的编号
    """
    menu = {
        "1": {"module": ca, "func": "draw_api"},
        "2": {"module": ca, "func": "transfer_api"},
        "3": {"module": ca, "func": "repayment"},
        "4": {"module": ca, "func": "admin_api"},
        "5": {"module": sys, "func": "eixt"}
    }
    p_num = input(tl.format_page(tl.INDEX_ATM))
    if menu.get(p_num):
        if hasattr(menu[p_num]["module"], menu[p_num]["func"]):
            func = getattr(menu[p_num]["module"],
                           menu[p_num]["func"])
            if callable(func):
                result = func()
                return result
            else:
                print(func)
        else:
            print("404")
            return "没有这个页面"
    else:
        print("404")
        return "没有这个页面"
