import arrow
import os
import sys
ATM_PATH = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
# print(ATM_PATH)
# print(os.path.isabs(ATM_PATH))
sys.path.append(ATM_PATH)
from conf import settings
from utils import utils


DB_PATH = os.path.join(ATM_PATH, "db")
CREDIT_PATH = os.path.join(DB_PATH, "credit")
USER_PATH = os.path.join(CREDIT_PATH, "users")
# print(DB_PATH, USER_PATH)


def create_account(card_num,
                   username,
                   role,
                   credit_total=15000,
                   pwd="12345",
                   statement_date=settings.STATEMENT_DATE):
    acc_path = os.path.join(USER_PATH, card_num, "account.json")
    name_path = os.path.join(USER_PATH, "username.json")
    sdate_path = os.path.join(USER_PATH, "usersdate.json")
    num_path = os.path.join(USER_PATH, card_num)
    username_list = utils.load_file(name_path)
    usersdate = utils.load_file(sdate_path)
    today = arrow.now()
    card_num = utils.to_num(card_num)
    repayment_date = today.replace(days=+settings.GRACE_PERIOD).format("DD")

    if not card_num:
        # print("卡号必须是16位数字")
        return "卡号必须是16位数字"
    if username in username_list:
        # print("用户名已存在")
        return "用户名已存在"
    mkdir_ret = utils.mkdir(num_path)
    if mkdir_ret:
        # print("账户已存在")
        return "账户已存在"
    else:
        acc_info = {"num": card_num,
                    "username": username,
                    "role": role,
                    "credit_total": credit_total,
                    "credit_balance": credit_total,
                    "pwd": pwd,
                    "state": 0,
                    "deposit": 0,
                    "statement_date": statement_date,
                    "repayment_date": repayment_date}
        username_list.append(username)
        usersdate[str(statement_date)].append(card_num)
        utils.dump_to_file(sdate_path, usersdate)
        utils.dump_to_file(acc_path, acc_info)
        utils.dump_to_file(name_path, username_list)


create_account("6222123409580003", "zhang1", "user", statement_date=18)
