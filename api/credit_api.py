#! /usr/bin/env python
# -*-coding: utf-8 -*-
import getpass

from modules.credit import users
from modules.credit import admin
from utils import utils
from bin import credit as bc


def draw_api():
    inp_amount = input("请输入取现金额>>>")
    inp_pwd = getpass.getpass("请输入取款密码>>>")
    users.draw_cash(inp_pwd, inp_amount)


def transfer_api():
    inp_to_num = input("请输入目标账号（卡号）>>>")
    inp_amount = input("请输入转账金额>>>")
    users.transfer_accounts(inp_to_num, inp_amount)


def repayment_api():
    inp_cardnum = input("请输入卡号：>>")
    inp_amount = input("请输入还款金额：>>")
    users.repayment(inp_cardnum, inp_amount)


def spend_api(amount):
    card_num = input("请输入信用卡卡号：")
    card_pwd = getpass.getpass("请输入支付密码：")
    card_pwd = utils.encrypt(card_pwd)
    users.spend(card_num, card_pwd, amount)


def create_account_api():
    print("""请输入账户信息，卡号、用户名为必填
             信用度默认为15000
             初始密码为12345
             账单日默认为22号
    """)
    cart_num = input("请输入卡号：")
    username = input("请输入用户名：")
    admin.create_account(cart_num, username)


def del_account_api():
    cart_num = input("请输入要删除的账户卡号：")
    admin.del_account(cart_num)


def modify_account_api():
    card_num = input("请输入要修改的卡号：")
    new_total = input("请输入新信用额度：")
    new_date = input("请输入新账单日：")
    new_state = input("请输入新的账户状态：")
    admin.modify_account(card_num, new_total, new_date, new_state)


def admin_api():
    act = {
        "1": create_account_api,
        "2": del_account_api,
        "3": modify_account_api,
        "b": bc.main
    }
    menu = "1.开户  2.删除账户  3.修改账户"
    i_act = input("%s >>" % menu)
    if act.get(i_act):
        return act[i_act]()
    else:
        return admin_api()
