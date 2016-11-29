#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
from bin import credit as ct
from bin import shopping as sp
from modules.credit import system
from conf import templates as tl


def main():
    menu = {
        "1": {"module": sp, "func": "main"},
        "2": {"module": ct, "func": "main"},
        "3": {"module": sys, "func": "exit"}
    }
    print("开始出账")
    system.charge_out()
    print("出账完毕")
    while True:
        c_menu = input(tl.format_page(tl.INDEX_MEMU))
        if menu.get(c_menu):
            if hasattr(menu[c_menu]["module"], menu[c_menu]["func"]):
                func = getattr(menu[c_menu]["module"], menu[c_menu]["func"])
                func()
            else:
                print("没有这个页面！")
                return main()
        if c_menu == "b":
            continue
        else:
            print("没有这个页面！")
            return main()
