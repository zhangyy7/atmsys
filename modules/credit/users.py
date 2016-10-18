import datetime
import os
import sys
import time

from conf import settings
from utils import utils
import system

ATM_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(ATM_PATH)
sys.path.append(ATM_PATH)

DB_PATH = os.path.join(ATM_PATH, "db")
CREDIT_PATH = os.path.join(DB_PATH, "credit")
USER_PATH = os.path.join(CREDIT_PATH, "users")
# print(DB_PATH)
#LOG_PATH = os.path.join(ATM_PATH, "log/credit/")


def draw_cash(card_num, pwd, amount_of_money):
    """
    取现
    """
    num_path = os.path.join(USER_PATH, card_num)
    acc_path = os.path.join(num_path, "account.json")
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
                    utils.dump_to_file(DB_PATH + card_num + "/account.db",
                                       acc)
                    credit_trade(DB_PATH + card_num + "/trade.db", "credit",
                                 amount_of_money, temp_final)
                else:
                    return "额度不足"
    else:
        return "您的账户已冻结"


def transfer_accounts(num, to_num, amount_of_money):
    """
    转账
    """
    acc = utils.load_file(DB_PATH + num + "/account.db")
    try:
        to_acc = utils.load_file(DB_PATH + to_num + "/account.db")
    except Exception as e:
        print(e)
    if acc["deposit"] + acc["credit_balance"] >= amount_of_money:
        temp = to_acc["credit_balance"] + amount_of_money
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
            acc["credit_balance"] -= temp2 + \
                temp2 * settings.FETCH_MONEY_RATE
            if temp <= to_acc["credit_total"]:
                to_acc["credit_balance"] += amount_of_money
            else:
                temp3 = temp - to_acc["credit_total"]
                to_acc["credit_balance"] = to_acc["credit_total"]
                to_acc["deposit"] += temp3
        utils.dump_to_file(DB_PATH + num + "/account.db", acc)
        utils.dump_to_file(DB_PATH + to_num + "/account.db", to_acc)
        credit_trade()
    else:
        return "余额不足！"


def spend(card_num, card_pwd, amount_of_money):
    """
    消费
    """
    acc = utils.load_file(DB_PATH + card_num + "/account.db")
    if acc["state"] == 0:
        if pwd != acc["pwd"]:
            return "支付密码不正确"
        else:
            if acc["credit_balance"] >= amount_of_money:
                acc["credit_balance"] -= amount_of_money
                utils.dump_to_file(DB_PATH + card_num +
                                   "/account.db", acc)
                credit_trade(DB_PATH + card_num + "/trade.db", "credit",
                             amount_of_money, amount_of_money)
            else:
                return "额度不足"
    else:
        return "您的账户已冻结"


def repayment(card_num, amount_of_money):
    """
    还款
    """
    acc = utils.load_file(DB_PATH + card_num + "/account.db")
    amounts_owed = acc[credit_total] - acc[credit_balance]
    if amount_of_money >= amounts_owed:
        acc[credit_balance] = acc[credit_total]
        acc[deposit] += (amount_of_money - amounts_owed)
        utils.dump_to_file(DB_PATH + card_num + "/account.db", acc)
        credit_trade(card_num, "repayment", amount_of_money, 0)
    else:
        acc[credit_balance] += amount_of_money
        utils.dump_to_file(DB_PATH + card_num + "/account.db", acc)
        credit_trade(card_num, "repayment", amount_of_money, 0)


def deposit(card_num, amount_of_money):
    """
    存款
    """
    acc = utils.load_file(DB_PATH + card_num + "/account.db")
    acc["deposit"] += amount_of_money
    utils.dump_to_file(DB_PATH + card_num + "/account.db")
    credit_trade(card_num, "deposit", amount_of_money, 0)


def billing_query(card_num):
    """
    账单查询
    """
    acc = utils.load_file(DB_PATH + card_num + "/account.db")
    credit_balance = acc["credit_balance"]
    amounts_owed = acc["credit_total"] - acc["credit_balance"]
    return credit_balance, amounts_owed
