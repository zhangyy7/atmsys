import os
import sys
import getpass

from modules.credit import users
from utils import utils

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


def repayment_api():
    inp_cardnum = input("请输入卡号：>>")
    inp_amount = input("请输入还款金额：>>")
    users.repayment(inp_cardnum, inp_amount)


def spend_api(amount):
    card_num = input("请输入信用卡卡号：")
    card_pwd = getpass.getpass("请输入支付密码：")
    card_pwd = utils.encrypt(card_pwd)
    users.spend(card_num, card_pwd, amount)
