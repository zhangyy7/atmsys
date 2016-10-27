import os
import sys

ATM_PATH = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
# print(ATM_PATH)
sys.path.append(ATM_PATH)
from modules.credit import auth
from conf import settings
from utils import utils
from modules.credit import system


DB_PATH = os.path.join(ATM_PATH, "db")
CREDIT_PATH = os.path.join(DB_PATH, "credit")
USER_PATH = os.path.join(CREDIT_PATH, "users")
# print(DB_PATH)
# LOG_PATH = os.path.join(ATM_PATH, "log/credit/")

USER_INFO = {
    "username": None,
    "login_flag": 0,
    "err_list": []
}


def login_page():
    menu = ">>>>>>>请登录<<<<<<<<"
    print(menu)
    inp_user = input("请输入您的卡号：")
    inp_pwd = input("请输入您的密码：")
    return login(inp_user, inp_pwd)


def check_login():
    global USER_INFO
    if USER_INFO["username"] and USER_INFO["login_flag"]:
        return
    else:
        return login_page()


def login(username, password):
    global USER_INFO
    num_path = os.path.join(DB_PATH, "credit", "users", username)
    if os.path.exists(num_path):
        acc_path = os.path.join(
            DB_PATH, "credit", "users", username, "account.json")
    else:
        return "账户不存在"
    acc_info = utils.load_file(acc_path)
    #print(acc_info)
    password = utils.encrypt(password)
    if password == acc_info["pwd"]:
        USER_INFO["username"] = username
        USER_INFO["login_flag"] = 1
        return USER_INFO
    elif USER_INFO["err_list"].count(username) == 3:
        return lock(username)
    else:
        USER_INFO["err_list"].append(username)
        return login_page()


def lock(username):
    num_path = os.path.join(DB_PATH, "credit", "users", username)
    if os.path.exists(num_path):
        acc_path = os.path.join(
            DB_PATH, "credit", "users", username, "account.json")
    else:
        return "账户不存在"
    acc_info = utils.load_file(acc_path)
    acc_info[username]["state"] = 1
    utils.dump_to_file(acc_path, acc_info)


@auth.auth(check_login)
def draw_cash(card_num, pwd, amount_of_money):
    """
    取现
    """
    acc_path = os.path.join(USER_PATH, card_num)
    acc_path = os.path.join(acc_path, "account.json")
    acc = utils.load_file(acc_path)
    if acc["state"] == 0:
        if pwd != acc["pwd"]:
            return "取款密码不正确"
        else:
            if amount_of_money <= acc["deposit"]:
                acc["deposit"] -= amount_of_money
                utils.dump_to_file(acc_path, acc)
                system.recode_trade(DB_PATH + card_num + "/trade.db", "credit",
                                    amount_of_money, 0)
            else:
                temp = amount_of_money - acc["deposit"]
                if acc["credit_balance"] >= temp:
                    acc["deposit"] = 0
                    temp_final = temp + temp * settings.FETCH_MONEY_RATE
                    acc["credit_balance"] -= temp_final
                    utils.dump_to_file(acc_path,
                                       acc)
                    credit_trade(DB_PATH + card_num + "/trade.db", "credit",
                                 amount_of_money, temp_final)
                else:
                    return "额度不足"
    else:
        return "您的账户已冻结"


@auth.auth(check_login)
def transfer_accounts(num, to_num, amount_of_money):
    """转账"""
    acc_path = os.path.join(USER_PATH, num)
    to_acc_path = os.path.join(USER_PATH, to_num)
    acc_path = os.path.join(acc_path, "account.json")
    to_acc_path = os.path.join(acc_path, "account.json")
    acc = utils.load_file(acc_path)
    try:
        to_acc = utils.load_file(to_acc_path)
    except Exception as e:
        print(e)
    if acc["deposit"] + acc["credit_balance"] >= amount_of_money:
        temp = to_acc["credit_balance"] + amount_of_money
        commission = 0
        if acc["deposit"] >= amount_of_money:
            acc["deposit"] -= amount_of_money
            if temp <= to_acc["credit_total"]:
                to_acc["credit_balance"] += amount_of_money
            else:
                temp1 = temp - to_acc["credit_total"]
                to_acc["credit_balance"] = to_acc["credit_total"]
                to_acc["deposit"] += temp1
        else:
            temp2 = amount_of_money - acc["deposit"]
            acc["deposit"] = 0
            commission = temp2 * settings.FETCH_MONEY_RATE
            acc["credit_balance"] -= temp2 + commission
            if temp <= to_acc["credit_total"]:
                to_acc["credit_balance"] += amount_of_money
            else:
                temp3 = temp - to_acc["credit_total"]
                to_acc["credit_balance"] = to_acc["credit_total"]
                to_acc["deposit"] += temp3
        utils.dump_to_file(acc_path, acc)
        utils.dump_to_file(to_acc_path, to_acc)
        system.recode_trade(num, "1", "1", amount_of_money, commission)
        system.recode_trade(to_num, "0", "0", amount_of_money)
    else:
        return "余额不足！"


@auth.auth(check_login)
def spend(card_num, card_pwd, amount_of_money):
    """消费"""
    acc_path = os.path.join(USER_PATH, card_num, "account.json")
    trade_path = os.path.join(USER_PATH, card_num, "trade.json")
    acc = utils.load_file(acc_path)
    if acc["state"] == 0:
        if pwd != acc["pwd"]:
            return "支付密码不正确"
        else:
            if acc["credit_balance"] >= amount_of_money:
                acc["credit_balance"] -= amount_of_money
                utils.dump_to_file(acc_path, acc)
                system.recode_trade(card_num, "1", "1", amount_of_money)
            else:
                return "额度不足"
    else:
        return "您的账户已冻结"


@auth.auth(check_login)
def repayment(card_num, amount_of_money):
    """还款"""
    acc_path = os.path.join(USER_PATH, card_num, "account.json")
    trade_path = os.path.join(USER_PATH, card_num, "trade.json")
    acc = utils.load_file(acc_path)
    amounts_owed = acc[credit_total] - acc[credit_balance]
    if amount_of_money >= amounts_owed:
        acc[credit_balance] = acc[credit_total]
        acc[deposit] += (amount_of_money - amounts_owed)
        utils.dump_to_file(acc_path, acc)
    else:
        acc[credit_balance] += amount_of_money
        utils.dump_to_file(acc_path, acc)
    system.recode_trade(card_num, "0", "0", amount_of_money)


@auth.auth(check_login)
def deposit(card_num, amount_of_money):
    """存款"""
    acc_path = os.path.join(USER_PATH, card_num, "account.json")
    acc = utils.load_file(acc_path)
    acc["deposit"] += amount_of_money
    utils.dump_to_file(acc_path, acc)
    system.recode_trade(card_num, "0", "0", amount_of_money)


@auth.auth(check_login)
def billing_query(card_num, date):
    """账单查询"""
    bill_path = os.path.join(USER_PATH, card_num, "bill.json")
    bill = utils.load_file(bill_path)
    bill_data = bill[date]
    dept = bill_data["dept"]
    repayment = bill_data["repayment"]
    return dept, repayment


# result = deposit('6222123409580004', 780)
# print(result)
