#!/usr/bin/env python
# --coding: utf-8 --
"""
系统菜单模板
"""
import os
import sys

import arrow

MY_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(MY_PATH)


# 主菜单
INDEX_MEMU = """
-------------------------------------------------------------------------
                             ATM 模拟程序

{0}                                        今天 {1}   星期{2}
-------------------------------------------------------------------------
        【1】进入商城 【2】信用卡中心 【4】退出系统
"""

# 商城用户中心
SHOP_USER_CENTER = """
-------------------------------------------------------------------------
                             购物商城

{0}                                        今天 {1}   星期{2}
-------------------------------------------------------------------------
        【1】进入商城 【3】信用卡中心 【4】后台管理 【5】退出系统
"""

# 信用卡中心
INDEX_ATM = """
------------------------------------------------------------------------------
{0}                                        今天 {1}   星期{2}
                               信用卡中心


------------------------------------------------------------------------------
        【1】提现    【2】转账    【3】还款   【4】返回
"""

# 信用卡后台管理
INDEX_ADMIN = """
------------------------------------------------------------------------------
{0}                                        今天 {1}   星期{2}
                               信用卡后台管理

用户:{username}
------------------------------------------------------------------------------
【1】创建用户    【2】删除用户    【3】解锁用户   【5】冻结信用卡  【0】退出后台管理
"""


def format_page(page):
    """
    导航页面
    """
    week_day = {
        1: "一",
        2: "二",
        3: "三",
        4: "四",
        5: "五",
        6: "六",
        7: "日"
    }
    now = arrow.now()
    hmm = now.strftime("%H:%M:%S")
    ymd = now.strftime("%Y-%m-%d")
    wday = now.isoweekday()
    wday = week_day[wday]
    f_page = page.format(hmm, ymd, wday)
    return f_page


def show_index():
    chioce = input("{}>>".format(format_page(INDEX_MEMU)))
    return chioce


def show_atm():
    choice = input("{}>>".format(format_page(INDEX_ATM)))
    return choice


def show_shop():
    choice = input("{}>>".format(format_page(INDEX_ATM)))
    return choice


def show_page(chioce):
    page = {
        "1": show_shop,
        "2": show_atm
    }
    func = page.get(chioce)
    # print(k)
    if func:
        func()
    else:
        print("404")
