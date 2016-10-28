import os
import sys

from modules.credit import users

MY_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(MY_PATH)


def draw_api():
    inp_amount = input("请输入取现金额>>>")
    inp_pwd = input("请输入取款密码>>>")
    users.draw_cash(inp_pwd, inp_amount)


def transfer_api():
    inp_to_num = input("请输入目标账号（卡号）>>>")
    inp_amount = input("请输入转账金额>>>")
    users.transfer_accounts(inp_to_num, inp_amount)
