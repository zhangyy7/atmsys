import arrow
import os
import sys
ATM_PATH = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
# print(ATM_PATH)
sys.path.append(ATM_PATH)
from conf import settings
from utils import utils


DB_PATH = os.path.join(ATM_PATH, "db/credit/")


def create_account(card_num,
                   username,
                   role,
                   credit_total=15000,
                   pwd="12345",
                   statement_date=settings.STATEMENT_DATE):
    card_num = utils.to_num(card_num)
    username_list = utils.load_file(DB_PATH + "/username.json")
    today = arrow.now()
    repayment_date = today.replace(days=+settings.GRACE_PERIOD).format("DD")
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
                "deposit": 0,
                "statement_date": statement_date,
                "repayment_date": repayment_date}
    utils.dump_to_file(acc_path + "/account.db", acc_info)
    username_list.append(username)
    utils.dump_to_file(DB_PATH + "/username.db", username_list)
    usersdate = utils.load_file(DB_PATH + "/usersdate.json")
    usersdate[card_num] = statement_date
    utils.dump(DB_PATH + "/usersdate.json", usersdate)


create_account("6223123490908768", "zhang", "user", statement_date=18)
