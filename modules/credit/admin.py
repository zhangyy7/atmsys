import arrow
import os
import sys
ATM_PATH = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
#print(ATM_PATH)
#print(os.path.isabs(ATM_PATH))
sys.path.append(ATM_PATH)
from conf import settings
from utils import utils


DB_PATH = os.path.join(ATM_PATH, "db/credit/")
USER_PATH = os.path.join(DB_PATH, "users/")
#print(DB_PATH, USER_PATH)
def create_account(card_num,
                   username,
                   role,
                   credit_total=15000,
                   pwd="12345",
                   statement_date=settings.STATEMENT_DATE):
    card_num = utils.to_num(card_num)
    username_list = utils.load_file(USER_PATH + "/username.json")
    today = arrow.now()
    repayment_date = today.replace(days=+settings.GRACE_PERIOD).format("DD")
    if not card_num:
        #print("卡号必须是16位数字")
        return "卡号必须是16位数字"
    if username in username_list:
        #print("用户名已存在")
        return "用户名已存在"
    acc_path = os.path.join(USER_PATH, str(card_num))
    print(acc_path)
    mkdir_ret = utils.mkdir(acc_path)
    if mkdir_ret:
        #print("账户已存在")
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
    utils.dump_to_file(acc_path + "/account.json", acc_info)
    username_list.append(username)
    utils.dump_to_file(DB_PATH + "users/username.json", username_list)
    usersdate = utils.load_file(DB_PATH + "users/usersdate.json")
    usersdate[str(statement_date)].append(card_num)
    utils.dump_to_file(DB_PATH + "users/usersdate.json", usersdate)


create_account("6222123409580002", "zhang", "user", statement_date=18)
