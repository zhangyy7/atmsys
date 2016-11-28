#! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import hashlib
import json
import os
import re

from utils import utils
from api import credit_api


ATM_PATH = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
MALL_PATH = os.path.join(ATM_PATH, "db", "mall")
ACC_PATH = os.path.join(MALL_PATH, "account.json")
GOODS_PATH = os.path.join(MALL_PATH, "goods.json")
TRADE_PATH = os.path.join(MALL_PATH, "trade.json")
CART = {}
USER_INFO = {"username": None, "fail_list": []}


def locking(username):
    """
    锁定用户函数
    :param acc_file:账户文件
    :param username:用户名
    :return:
    """
    global ACC_PATH
    acc = utils.load_file(ACC_PATH)
    user_info = acc[username]
    user_info["locked_flag"] = 1
    utils.dump_to_file(ACC_PATH, acc)


def register(username, password):
    """
    用户注册
    :param username:用户名
    :param password:密码
    :return:注册成功返回username，失败返回False
    """
    patt1 = "[^(\w|_)]"
    patt2 = "^[^a-zA-Z]+"
    m = hashlib.md5()
    m.update(bytes(password, encoding='utf-8'))
    m_password = m.hexdigest()
    if re.search(patt1, username) or re.match(patt2, username):
        print("用户名只能为英文字母开头的数字、字母、下划线的组合！")
        return False
    else:
        acc = utils.load_file(ACC_PATH)
        if acc.get(username):
            print("用户名已存在！")
            return False
        else:
            acc[username] = {}
            acc[username]["username"] = username
            acc[username]["pwd"] = m_password
            acc[username]["balance"] = 0
            acc[username]["locked_flag"] = 0
            utils.dump_to_file(ACC_PATH, acc)
            return username


def login(username, password):
    """用户登录
    :param acc_file:账户文件
    :param username:用户名
    :param password:密码
    :return:成功-True，密码不对-False，用户不存在-None,已锁定-"locked"
    """
    password = utils.encrypt(password)
    acc = utils.load_file(ACC_PATH)
    if not acc.get(username):
        return "用户名不存在！"
    else:
        if username == acc[username]["username"] and\
           password == acc[username]["pwd"]:
            return acc[username]
        else:
            return "用户名或密码不正确"


def showgoods(dir1, dir2, dir1_dict, dir2_dict):
    """
    输出商品信息
    :param goods_file:接收存有商品数据的文件
    :param input_dir1_num:接收用户选择的一级目录
    :param input_dir2_num:接收用户选择的二级目录
    :param dir_1:接收一级目录列表
    :param dir_2:接收二级目录列表
    :return:返回商品信息
    """
    goods_dict = utils.load_file(GOODS_PATH)
    goods = str()
    goods_info = goods_dict[dir1_dict[dir1]][dir2_dict[dir2]]
    num = 1
    good_dict = {}
    for key in goods_info:
        goods += "%s: %s,单价%s " % (num, key, goods_info[key]["price"])
        good_dict[str(num)] = key
        num += 1
    chogood = input("""输入编号将商品加入购物车
    商品信息如下：
    %s
    按b返回上级菜单
    """ % (goods))
    if chogood == "b":
        return showdir2(dir1, dir1_dict)
    if goods_info.get(good_dict[chogood]):
        buy_num = input("请输入购买数量：")
        return add_to_cart(dir1,
                           dir2,
                           dir1_dict,
                           dir2_dict,
                           chogood,
                           good_dict,
                           buy_num)
    else:
        return "没有这个页面"


def showdir2(dir1, dir1_dict):
    """
    输出商品小类
    :param goods_file:接收存有商品数据的文件
    :param dir_1:接收一级目录列表
    :param input_dir1:接收用户输入的一级目录
    :return:返回商品二级目录
    """
    goods_dict = utils.load_file(GOODS_PATH)
    dir2 = str()
    if dir1_dict.get(dir1):
        dir2_info = goods_dict[dir1_dict[dir1]]
    else:
        return showdir1()
    dir2_dict = {}
    num = 1
    for key in dir2_info:
        dir2 += "%s: %s " % (num, key)
        dir2_dict[str(num)] = key
        num += 1
    chodir2 = input(dir2)
    if dir2_dict.get(chodir2):
        print(dir2_dict)
        return showgoods(dir1, chodir2, dir1_dict, dir2_dict)
    if chodir2 == "b":
        return showdir1()


def showdir1():
    """
    输出商品一级目录
    :param goods_file:接收存有商品数据的文件
    :return: 返回商品的一级目录
    """
    goods_dict = utils.load_file(GOODS_PATH)
    dir1 = str()
    num = 1
    dir1_dict = {}
    for key in goods_dict:
        dir1 += "%s: %s " % (num, key)
        dir1_dict[str(num)] = key
        num += 1
    chodir1 = input(dir1)
    return showdir2(chodir1, dir1_dict)


def add_to_cart(dir1, dir2, dir1_dict, dir2_dict, chogood, good_dict, buy_num):
    """
    将商品添加至购物车
    :param goods_file:商品数据文件
    :param username:接收已登录的用户
    :param input_dir1_num:用户输入的一级目录编号
    :param input_dir2_num:用户输入的二级目录编号
    :param input_pro_num:用户输入的商品编号
    :param input_pro_cou:接收用户输入的购买数量
    :return:添加成功-True，商品编号不正确-False，库存不够-"loq"
    """
    global CART
    goods_dict = utils.load_file(GOODS_PATH)
    good = good_dict[chogood]
    g_info = goods_dict[dir1_dict[dir1]][dir2_dict[dir2]][good_dict[chogood]]
    if buy_num.isdigit():
        buy_num = int(buy_num)
        g_qty = g_info["qty"]
        if buy_num <= g_qty:
            g_price = g_info["price"]
            if CART.get(good_dict[chogood]):
                CART[good]["qty"] += buy_num
            else:
                CART[good] = {}
                CART[good]["price"] = g_price
                CART[good]["qty"] = buy_num
            goods_dict[dir1_dict[dir1]][dir2_dict[dir2]][
                good_dict[chogood]]["qty"] -= buy_num
            utils.dump_to_file(GOODS_PATH, goods_dict)
            return showcart()
        else:
            return "库存不足"
    else:
        return "数量必须为数字"


# def pay(goods_file, acc_file, username, cart):
#     """
#     结算支付
#     :param goods_file:接收商品文件
#     :param acc_file:接收账户文件
#     :param username:接收用户名
#     :return:成功-Ture，库存数量不足-"loq",余额不足-"lob"
#     """
#     print(cart)
#     bill = 0
#     with open(acc_file) as f:
#         acc = json.load(f)
#         bal_ind = acc["user"].index(username)
#         balance = acc["balance"][bal_ind]
#     for i in range(len(cart[username]["product"])):
#         product_price = cart[username]["price"][i]
#         product_count = cart[username]["count"][i]
#         subtotal = product_price * product_count
#         bill += subtotal
#     if balance >= bill:
#         balance -= bill
#         print(balance)
#         s_ret = subcount(goods_file, cart, username)  # 减库存
#         # goods_file,cart,username
#         #:return:成功-True,数量不足返回[商品名称，库存数量，购买数量]
#         if s_ret == True:
#             with open(acc_file, 'w') as f:
#                 acc["balance"][bal_ind] = balance
#                 json.dump(acc, f, ensure_ascii=False)
#             return True
#         else:
#             return s_ret  # 返回库存数量不足
#     else:
#         return [balance, bill]  # 返回余额不足


def recharge(acc_file, username, amount):
    """
    充值
    :param acc_file:账户文件
    :param username:用户名
    :param amount:充值金额
    :return:成功-True,失败-False
    """
    if amount.isdigit():
        amount = int(amount)
        with open(acc_file) as f:
            acc = json.load(f)
            ind = acc["user"].index(username)
            acc["balance"][ind] += amount
        with open(acc_file, 'w') as f:
            json.dump(acc, f, ensure_ascii=False)
        return True
    else:
        return False


def shopping_log():
    """
    购物历史记录
    :param username:用户名
    :param cart:当前的购物车
    :param logfile:购物历史文件
    """
    global CART
    global USER_INFO
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    info = ""
    for good in CART:
        info += "%s|%s|%s|%s" % (USER_INFO["username"], t, good,
                                 CART[good]["price"], CART[good]["qty"])
    with open(TRADE_PATH, "a+", encoding="utf-8") as f:
        f.write(info)


def load_log(username, trade_path):
    """
    加载购物历史
    :param username:用户名
    :param trade_path:购物历史文件
    :return:有历史返回购物历史，无历史返回None
    """
    with open(trade_path, 'r+') as f:
        for line in f:
            log = line.strip().split("|")
            if log[0] == username:
                print("%s，您在%s购买了%s，单价%s，数量%s" %
                      (log[0], log[1], log[2], log[3], log[4]))


def showcart():
    """
    输入购物车信息
    :param cart:购物车
    """
    global CART
    info = ""
    if CART:
        for good in CART:
            info += "商品名称：{name}, 单价：{price}, 数量：{qty}\n".format(
                name=good, price=CART[good]["price"], qty=CART[good]["qty"])
    else:
        pass
    print(info)
    act = {
        "1": showdir1,
        "2": settle
    }
    c_act = input("1:继续购物 ，2:结算").strip()
    if act.get(c_act):
        return act[c_act]()
    else:
        return showcart()


def settle():
    global CART
    total_amount = 0
    for good in CART:
        amount = CART[good]["price"] * CART[good]["qty"]
        total_amount += amount
    return credit_api.spend_api(total_amount)
