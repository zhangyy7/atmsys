import datetime
import os
import sys
import time
import datetime
import arrow
ATM_PATH = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
# print(ATM_PATH)
sys.path.append(ATM_PATH)

from conf import settings
from utils import utils


DB_PATH = os.path.join(ATM_PATH, "db/credit/users/")
TODAY = arrow.now()


def recode_trade(card_num, trade_flag, opera_type, amount, commission=0):
    timenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    trade = utils.load_file(DB_PATH + card_num + "/trade.json")
    trade[timenow]["trade_flag"] = trade_flag
    trade[timenow]["opera_type"] = opera_type
    trade[timenow]["amount"] = amount
    trade[timenow]["commission"] = commission
    utils.dump_to_file(DB_PATH + card_num + "/trade.json", trade)


def charge_out():
    """
    出账
    """
    usersdate_dict = utils.load_file(DB_PATH + "/usersdate.json")
    pending_cardnum = usersdate_dict[str(TODAY.day)]
    last_month = TODAY.replace(months=-1)
    str_currentmonth = TODAY.strftime("%Y%m")
    str_lastmonth = last_month.strftime("%Y%m")
    if not pending_cardnum:
        return "今天没有要出账的账户"
    else:
        for cardnum in peding_cardnum:
            bill_data = utils.load_file(DB_PATH + cardnum + "/bill.json")
            trade_data = utils.load_file(DB_PATH + cardnum + "/trade.json")
            if bill_data.get(str_lastmonth):
                last_bill = float(bill_data[str_lastmonth].get("bill"))
            else:
                last_bill = 0.00
            repayment = 0.00
            spend = 0.00
            interest = 0.00
            late = 0.00
            for k in trade_data:
                trade_time = arrow.Arrow.strptime(k, "%Y-%m-%d %H:%M:%S")
                if last_month < trade_time < TODAY:
                    if trade_data[k]["trade_flag"] == "0":
                        rtemp = float(trade_data[k]["amount"]) + \
                            float(trade_data["commission"])
                        repayment += temp
                    else:
                        spend += float(trade_data[k]["amount"])
            bill_data["str_currentmonth"]["bill"] = last_bill - \
                repayment + spend + interest + late
            bill_data["str_currentmonth"]["repayment"] = repayment
            bill_data["str_currentmonth"]["spend"] = spend
            bill_data["str_currentmonth"]["interest"] = interest
            bill_data["str_currentmonth"]["late"] = late
            utils.dump_to_file(DB_PATH + cardnum + "/bill.json", bill_data)


def calculate_interest(card_num):
    bill_data = utils.load_file(DB_PATH + card_num + "/bill.json")
    trade_data = utils.load_file(DB_PATH + card_num + "/trade.json")
    lastmonth = TODAY.replace(months=-1).replace(days=+1)
    date_now = TODAY.date()
    date_last = lastmonth.date()
    str_lastmonth = lastmonth.format("YYYYMM")
    lastbill = bill_data[str_lastmonth]["bill"]
    c_total = 0
    r_total = 0
    for time in trade_data:
        time = arrow.Arrow.strptime(time, "%Y-%m-%d %H:%M:%S")
        time = time.date()
        if date_last <= time < date_now:
            if trade_data[time]["trade_flag"] == "1":
                ctemp = trade_data[time]["amount"] + \
                    trade_data[time]["commission"]
                c_total += ctemp
            else:
                rtemp = trade_data[time]["amount"]
                r_total += rtemp
    if r_total < lastbill:
        if r_total / lastbill >= 0.1:
            interest = (lastbill - r_total) * settings.EXPIRE_DAY_RATE * ()

if __name__ == '__main__':
    ret = charge_out()
    print(ret)
