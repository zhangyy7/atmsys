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
# print(DB_PATH)
LOG_PATH = os.path.join(ATM_PATH, "log/credit/")


def draw_cash(card_num, pwd, amount_of_money):
    """
    取现
    """
    credit_acc = utils.load_file(DB_PATH + card_num + "/account.db")
    if credit_acc["state"] == 0:
        if pwd != credit_acc["pwd"]:
            return "取款密码不正确"
        else:
            if amount_of_money <= credit_acc["deposit"]:
                credit_acc["deposit"] -= amount_of_money
                utils.dump_to_file(DB_PATH + card_num +
                                   "/account.db", credit_acc)
                credit_trade(DB_PATH + card_num + "/trade.db", "credit",
                             amount_of_money, 0)
            else:
                temp = amount_of_money - credit_acc["deposit"]
                if credit_acc["credit_balance"] >= temp:
                    credit_acc["deposit"] = 0
                    temp_final = temp + temp * settings.FETCH_MONEY_RATE
                    credit_acc["credit_balance"] -= temp_final
                    utils.dump_to_file(DB_PATH + card_num + "/account.db",
                                       credit_acc)
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
    credit_acc = utils.load_file(DB_PATH + num + "/account.db")
    try:
        to_credit_acc = utils.load_file(DB_PATH + to_num + "/account.db")
    except Exception as e:
        print(e)
    if credit_acc["deposit"] + credit_acc["credit_balance"] >= amount_of_money:
        temp = to_credit_acc["credit_balance"] + amount_of_money
        if credit_acc["deposit"] >= amount_of_money:
            credit_acc["deposit"] -= amount_of_money
            if temp <= to_credit_acc["credit_total"]:
                to_credit_acc["credit_balance"] += amount_of_money
            else:
                temp1 = temp - to_credit_acc["credit_total"]
                to_credit_acc["credit_balance"] = to_credit_acc["credit_total"]
                to_credit_acc["deposit"] += temp1
        else:
            temp2 = amount_of_money - credit_acc["deposit"]
            credit_acc["deposit"] = 0
            credit_acc["credit_balance"] -= temp2 + \
                temp2 * settings.FETCH_MONEY_RATE
            if temp <= to_credit_acc["credit_total"]:
                to_credit_acc["credit_balance"] += amount_of_money
            else:
                temp3 = temp - to_credit_acc["credit_total"]
                to_credit_acc["credit_balance"] = to_credit_acc["credit_total"]
                to_credit_acc["deposit"] += temp3
        utils.dump_to_file(DB_PATH + num + "/account.db", credit_acc)
        utils.dump_to_file(DB_PATH + to_num + "/account.db", to_credit_acc)
        credit_trade()
    else:
        return "余额不足！"


def spend(card_num, card_pwd, amount_of_money):
    """
    消费
    """
    credit_acc = utils.load_file(DB_PATH + card_num + "/account.db")
    if credit_acc["state"] == 0:
        if pwd != credit_acc["pwd"]:
            return "支付密码不正确"
        else:
            if credit_acc["credit_balance"] >= amount_of_money:
                credit_acc["credit_balance"] -= amount_of_money
                utils.dump_to_file(DB_PATH + card_num +
                                   "/account.db", credit_acc)
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
    credit_acc = utils.load_file(DB_PATH + card_num + "/account.db")
    amounts_owed = credit_acc[credit_total] - credit_acc[credit_balance]
    if amount_of_money >= amounts_owed:
        credit_acc[credit_balance] = credit_acc[credit_total]
        credit_acc[deposit] += (amount_of_money - amounts_owed)
        utils.dump_to_file(DB_PATH + card_num + "/account.db", credit_acc)
        credit_trade(card_num, "repayment", amount_of_money, 0)
    else:
        credit_acc[credit_balance] += amount_of_money
        utils.dump_to_file(DB_PATH + card_num + "/account.db", credit_acc)
        credit_trade(card_num, "repayment", amount_of_money, 0)


def deposit(card_num, amount_of_money):
    """
    存款
    """
    credit_acc = utils.load_file(DB_PATH + card_num + "/account.db")
    credit_acc["deposit"] += amount_of_money
    utils.dump_to_file(DB_PATH + card_num + "/account.db")
    credit_trade(card_num, "deposit", amount_of_money, 0)


def billing_query(card_num):
    """
    账单查询
    """
    credit_acc = utils.load_file(DB_PATH + card_num + "/account.db")
    credit_balance = credit_acc["credit_balance"]
    amounts_owed = credit_acc["credit_total"] - credit_acc["credit_balance"]
    return credit_balance, amounts_owed
