import arrow
import os
import sys
import getpass

ATM_PATH = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
# print(ATM_PATH)
# print(os.path.isabs(ATM_PATH))
sys.path.append(ATM_PATH)
from modules.credit import auth
from conf import settings
from utils import utils


DB_PATH = os.path.join(ATM_PATH, "db")
CREDIT_PATH = os.path.join(DB_PATH, "credit")
USER_PATH = os.path.join(CREDIT_PATH, "users")
# print(DB_PATH, USER_PATH)

ADMIN_INFO = {
    "username": None,
    "login_flag": 0,
    "err_list": []
}


def login_page():
    menu = "欢迎来到管理员登录页面"
    print(menu)
    inp_user = input("请输入管理员账号：")
    inp_pwd = getpass.getpass("请输入您的密码：")
    return login(inp_user, inp_pwd)


def check_login():
    global ADMIN_INFO
    if ADMIN_INFO["username"] and ADMIN_INFO["login_flag"]:
        return
    else:
        return login_page()


def login(username, password):
    global ADMIN_INFO
    admin_path = os.path.join(DB_PATH, "credit", "admin", "admin.json")
    ad_info = utils.load_file(admin_path)
    #print(ad_info)
    password = utils.encrypt(password)
    if ad_info.get(username):
        if ad_info[username]["lock_flag"] == 0:
            if password == ad_info[username]["password"]:
                ADMIN_INFO["username"] = username
                ADMIN_INFO["login_flag"] = 1
                return ADMIN_INFO
            elif ADMIN_INFO["err_list"].count(username) == 3:
                return lock(username)
            else:
                ADMIN_INFO["err_list"].append(username)
                print("用户名或密码不正确，请重新输入！")
                return login_page()
        else:
            print("您的账户已锁定。")
            return "已锁定！"
    else:
        print("用户不存在")
        return login_page()


def lock(username):
    ad_path = os.path.join(DB_PATH, "credit", "admin", "admin.json")
    ad_info = utils.load_file(ad_path)
    if ad_info.get(username):
        ad_info[username]["lock_flag"] = 1
        utils.dump_to_file(ad_path, ad_info)
    else:
        return "不存在此管理员"


@auth.auth(check_login)
def create_account(card_num,
                   username,
                   role,
                   credit_total=settings.CREDIT_TOTAL,
                   pwd=settings.DEFAULT_PWD,
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
                    "pwd": utils.encrypt(pwd),
                    "state": 0,
                    "deposit": 0,
                    "statement_date": statement_date,
                    "repayment_date": repayment_date}
        username_list.append(username)
        usersdate[str(statement_date)].append(card_num)
        utils.dump_to_file(sdate_path, usersdate)
        utils.dump_to_file(acc_path, acc_info)
        utils.dump_to_file(name_path, username_list)
        card_path = os.path.join(USER_PATH, "card.json")
        if os.path.exists(card_path):
            card = utils.load_file(card_path)
        else:
            card = list()
        card.append(card_num)
        utils.dump_to_file(card_path, card)


@auth.auth(check_login)
def del_account(card_num):
    num_path = os.path.join(USER_PATH, card_num)
    acc_path = os.path.join(num_path, "account.json")
    #name_path = os.path.join(USER_PATH, "username.json")
    sdate_path = os.path.join(USER_PATH, "usersdate.json")
    acc = utils.load_file(acc_path)
    #name_list = utils.load_file(name_path)
    sdate = utils.load_file(sdate_path)
    balance = acc["credit_balance"]
    if balance < acc["credit_total"]:
        return "该用户有欠款未还清，不能注销！"
    else:
        acc["state"] = 2
        for d in sdate:
            num_list = sdate[d]
            if card_num in num_list:
                num_list.remove(card_num)
        utils.dump_to_file(acc_path, acc)
        utils.dump_to_file(sdate_path, sdate)


@auth.auth(check_login)
def modify_account(card_num, new_total=None, new_date=None, new_state=None):
    acc_path = os.path.join(USER_PATH, card_num, "account.json")
    acc = utils.load_file(acc_path)
    if new_total:
        temp = acc["credit_total"]
        ran = new_total - temp
        acc["credit_total"] = new_total
        acc["credit_balance"] += ran
    if new_date:
        acc["STATEMENT_DATE"] = new_date
    if state:
        acc["state"] = new_state
    utils.dump_to_file(acc_path)


if __name__ == "__main__":
    create_account("6222123409580004",
                   "zhangyy4",
                   "user")
