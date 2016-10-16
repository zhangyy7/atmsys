import datetime
import os
import sys
import time

from conf import settings
from utils import utils

ATM_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(ATM_PATH)
sys.path.append(ATM_PATH)

DB_PATH = os.path.join(ATM_PATH, "db/credit/")

def create_account(card_num,
                   username,
                   role,
                   credit_total=15000,
                   pwd="12345",
                   statement_date=settings.STATEMENT_DATE):
    card_num = utils.to_num(card_num)
    username_list = utils.load_file(DB_PATH + "/username.db")
    if not card_num:
        return "卡号必须是16位数字"
    if username in username_list:
        return "用户名已存在"
    acc_path = DB_PATH + str(card_num)
    mkdir_ret = utils.mkdir(acc_path)
    if mkdir_ret:
        return "账户已存在"
    acc_info = {"num": card_num,
                "username": username,
                "role": role,
                "credit_total": credit_total,
                "credit_balance": credit_total,
                "pwd": pwd,
                "state": 0,
                "deposit": 0}
    utils.dump_to_file(acc_path + "/account.db", acc_info)
    username_list.append(username)
    utils.dump_to_file(DB_PATH + "/username.db", username_list)