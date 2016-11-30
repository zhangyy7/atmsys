import os

import arrow

from conf import settings
from utils import utils

ATM_PATH = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(ATM_PATH, "db")
CREDIT_PATH = os.path.join(DB_PATH, "credit")
USER_PATH = os.path.join(CREDIT_PATH, "users")
TODAY = arrow.now()


def recode_trade(card_num, trade_flag, opera_type, amount, commission=0):
    """记录操作流水"""
    num_path = os.path.join(USER_PATH, card_num)
    trade_path = os.path.join(num_path, "trade.json")
    timenow = arrow.now().strftime("%Y-%m-%d %H:%M:%S")
    if os.path.exists(trade_path):
        trade = utils.load_file(trade_path)
    else:
        trade = dict()
    # print(trade)
    trade[timenow] = dict()
    trade[timenow]["trade_flag"] = trade_flag
    trade[timenow]["opera_type"] = opera_type
    trade[timenow]["amount"] = amount
    trade[timenow]["commission"] = commission
    print(trade_path)
    utils.dump_to_file(trade_path, trade)


def charge_out():
    """出账 """
    global TODAY
    sdate_path = os.path.join(USER_PATH, "usersdate.json")
    usersdate_dict = utils.load_file(sdate_path)
    pending_cardnum = usersdate_dict[str(TODAY.day)]
    # last_month = TODAY.replace(months=-1)
    # str_currentmonth = TODAY.strftime("%Y%m")
    # str_lastmonth = last_month.strftime("%Y%m")
    if not pending_cardnum:
        return "今天没有要出账的账户"
    else:
        for cardnum in pending_cardnum:
            num_path = os.path.join(USER_PATH, cardnum)
            acc_path = os.path.join(num_path, "account.json")
            bill_path = os.path.join(num_path, "bill.json")
            bill_data = utils.load_file(bill_path)
            acc = utils.load_file(acc_path)
            # trade_data = utils.load_file(trade_path)
            bill_temp = acc["credit_total"] - acc["credit_balance"]
            now = arrow.now().for_json()
            if bill_temp > 0:
                bill_data[TODAY.format("YYYYMM")]["dept"] = bill_temp
                bill_data[TODAY.format("YYYYMM")]["repayment"] = 0
                bill_data[TODAY.format("YYYYMM")]["bill_time"] = now
            else:
                bill_data[TODAY.format("YYYYMM")]["dept"] = bill_temp
                bill_data[TODAY.format("YYYYMM")]["repayment"] = 0
                bill_data[TODAY.format("YYYYMM")]["bill_time"] = now
            utils.dump_to_file(bill_path, bill_data)


def calculate_interest(card_num):
    num_path = os.path.join(USER_PATH, card_num)
    acc_path = os.path.join(num_path, "account.json")
    bill_path = os.path.join(num_path, "bill.json")
    trade_path = os.path.join(num_path, "trade.json")
    print(trade_path)
    bill_data = utils.load_file(bill_path)
    trade_data = utils.load_file(trade_path)
    acc = utils.load_file(acc_path)
    statement_date = acc["STATEMENT_DATE"]
    now_time = arrow.now()
    bill_date = now_time.replace(months=-1, day=statement_date)
    bill_key = bill_date.format("YYYYMM")
    if bill_data.get(bill_key):
        lower_str = bill_data[bill_key]["bill_time"]
        lower_time = arrow.Arrow.strptime(lower_str, "%Y-%m-%d %H:%M:%S")
    else:
        return "没有账单"
    repay_total = 0
    for k in trade_data:
        trade_time = arrow.Arrow.strptime(k, "%Y-%m-%d %H:%M:%S")
        if lower_time < trade_time <= now_time:
            if trade_data[k]["trade_flag"] == "0":
                repay = trade_data[k]["amount"]
                repay_total += repay
    last_dept = bill_data[bill_key]["dept"]
    last_repayment = bill_data[bill_key]["repayment"]
    startday = now_time.replace(months=-2, day=statement_date)
    endday = now_time
    days = endday - startday
    # print(days.days)
    if last_dept > 0:
        if last_dept <= last_repayment:
            return "已还清"
        else:
            commission = 0
            interest = (last_dept - last_repayment) * \
                settings.EXPIRE_DAY_RATE * days.days
            # print(interest)
            interest = round(interest, 2)
            # print(interest)
            if repay_total / last_dept < 0.1:
                if bill_data[bill_key]["commission_flag"] == 0:
                    repay_min = last_dept * 0.1
                    commission = (repay_min - repay_total) * 0.05
            trade_key = now_time.strftime("%Y-%m-%d %H:%M:%S")
            trade_data[trade_key] = dict()
            trade_data[trade_key]["opera_type"] = "1"
            trade_data[trade_key]["trade_flag"] = "1"
            trade_data[trade_key]["amount"] = 0
            trade_data[trade_key]["interest"] = interest
            trade_data[trade_key]["commission"] = commission
            utils.dump_to_file(bill_path, bill_data)
            utils.dump_to_file(trade_path, trade_data)
    else:
        return "欠款为0"


if __name__ == '__main__':
    ret = calculate_interest("6222123409580001")
    print(ret)
