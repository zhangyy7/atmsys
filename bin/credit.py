#!/usr/bin/env python
# --coding: utf-8 --
"""
信用卡主程序
"""
import os
import sys

MY_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(MY_PATH)

from conf import settings
from modules.credit import users, admin, auth
from utils import utils


def show(page_num):
    num_func = {
        "1": users.draw_cash,
        "2": users.transfer_accounts,
        "3": users.repayment
    }

    if hasattr(users, num_func[page_num]):
        func = getattr(users, num_func[page_num])
        func()
    return f_page


def draw_api():
    inp_amount = input("请输入取现金额>>>")
    inp_pwd = input("请输入取款密码>>>")
    card_num = users.USER_INFO["username"]
    users.draw_cash(card_num, inp_pwd, inp_amount)


def main():
    pass
