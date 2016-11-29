#! /usr/bin/env python
# -*- coding: utf-8 -*-
from modules.shopping import shopping as msp
from conf import templates as tl
from api import shopping as asp
from bin import main as m


def main():
    menu = {
        "1": {"module": msp, "func": "showdir1"},
        "2": {"module": asp, "func": "register_api"},
        "b": {"module": m, "func": "main"}
    }
    p_num = input(tl.format_page(tl.SHOP_CENTER))
    if menu.get(p_num):
        if hasattr(menu[p_num]["module"], menu[p_num]["func"]):
            func = getattr(menu[p_num]["module"], menu[p_num]["func"])
            func()
        else:
            return "404"
    else:
        print("请输入正确的编号！")
        return main()
