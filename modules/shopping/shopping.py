#! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import getpass
import hashlib
import json
import re
import os
import sys
ATM_PATH = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ATM_PATH)
from utils import utils

ATM_PATH = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
MALL_PATH = os.path.join(ATM_PATH, "db", "mall")
ACC_PATH = os.path.join(MALL_PATH, "account.json")
GOODS_PATH = os.path.join(MALL_PATH, "goods.json")


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


# def acc_load(acc_file):
#     """
#     加载完整的账户文件内容
#     :param acc_file:账户文件
#     :return:返回账户信息
#     """
#     usrname = []
#     password = []
#     balance = []
#     locked_flag = []
#     with open(acc_file, "r") as f:
#         acc = json.load(f)
#         if len(acc["user"]) > 0:
#             usrname = acc["user"]
#             password = acc["pwd"]
#             balance = acc["balance"]
#             locked_flag = acc["locked_flag"]
#             return usrname, password, balance, locked_flag  # 返回4个列表对象
#         else:
#             return None, None, None, None


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


def showdir1():
    """
    输出商品一级目录
    :param goods_file:接收存有商品数据的文件
    :return: 返回商品的一级目录
    """
    goods_dict = utils.load_file(GOODS_PATH)
    dir1 = str()
    num = 1
    for key in goods_dict:
        dir1 += "%s: %s " % (num, key)
        num += 1
    chodir1 = input(dir1)
    return chodir1

showdir1()


def showdir2(dir1):
    """
    输出商品小类
    :param goods_file:接收存有商品数据的文件
    :param dir_1:接收一级目录列表
    :param input_dir1:接收用户输入的一级目录
    :return:返回商品二级目录
    """
    goods_dict = utils.load_file(GOODS_PATH)


def showgoods(goods_file, input_dir1_num, input_dir2_num, dir_1, dir_2):
    """
    输出商品信息
    :param goods_file:接收存有商品数据的文件
    :param input_dir1_num:接收用户选择的一级目录
    :param input_dir2_num:接收用户选择的二级目录
    :param dir_1:接收一级目录列表
    :param dir_2:接收二级目录列表
    :return:返回商品信息
    """
    product_list = []
    with open(goods_file) as f:
        if f:
            goods = json.load(f)
            if input_dir2_num.isdigit():
                input_dir2_num = int(input_dir2_num)
                input_dir1_num = int(input_dir1_num)
                if input_dir2_num < len(dir_2):
                    input_dir2 = dir_2[input_dir2_num]
                    input_dir1 = dir_1[input_dir1_num]
                    # for pro in goods[input_dir1][input_dir2]:
                    # product_list.append(pro)
                    #proinfo = goods[input_dir1][input_dir2]
                    pro_dict = goods[input_dir1][input_dir2]
                    return pro_dict
                else:
                    return False
            else:
                return False
        else:
            return None


def add_to_cart(goods_file, username, input_dir1_num, input_dir2_num, input_pro_num, input_pro_cou, cart):
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
    input_dir1_num = int(input_dir1_num)
    input_dir2_num = int(input_dir2_num)
    if input_pro_cou.isdigit():
        input_pro_cou = int(input_pro_cou)
    else:
        return 0  # 数量不是数字
    with open(goods_file) as f:
        goods = json.load(f)
        dir1_list = list(goods.keys())
        dir1 = dir1_list[input_dir1_num]
        dir2_list = list(goods[dir1].keys())
        dir2 = dir2_list[input_dir2_num]
        pro_list = list(goods[dir1][dir2].keys())
    if input_pro_num.isdigit():
        input_pro_num = int(input_pro_num)
        if input_pro_num < len(pro_list):
            input_pro = pro_list[input_pro_num]
            pro_price = goods[dir1][dir2][input_pro][0]
            pro_count = goods[dir1][dir2][input_pro][1]
            if cart:
                if input_pro_cou <= pro_count:
                    if input_pro not in cart[username]["product"]:

                        cart[username]["product"].append(input_pro)
                        cart[username]["price"].append(pro_price)
                        cart[username]["count"].append(input_pro_cou)
                    else:
                        product_index = cart[username][
                            "product"].index(input_pro)
                        cart[username]["count"][product_index] += input_pro_cou
                else:
                    return "loq"
            else:
                cart[username] = {"product": [], "price": [], "count": []}
                cart[username]["product"].append(input_pro)
                cart[username]["price"].append(pro_price)
                cart[username]["count"].append(input_pro_cou)
                print(cart)
            return [input_pro, input_pro_cou]  # 添加成功
        else:
            return False  # 商品编号不正确
    else:
        return False  # 商品编号不正确


def subcount(goods_file, cart, username):
    """
    减库存
    :param goods_file:接收存放商品的文件
    :param cart:接收购物车
    :param username:接收用户名
    :return:成功-True,数量不足-返回[商品名称，库存数量，购买数量]
    """
    with open(goods_file) as f:
        goods = json.load(f)
        for cf1 in goods:
            for cf2 in goods[cf1]:
                for pro_g in goods[cf1][cf2]:
                    for pro_c in cart[username]["product"]:
                        if pro_c == pro_g:
                            pro_g_ind = cart[username]["product"].index(pro_c)
                            if goods[cf1][cf2][pro_g][1] >= cart[username]["count"][pro_g_ind]:
                                goods[cf1][cf2][pro_g][
                                    1] -= cart[username]["count"][pro_g_ind]
                            else:
                                g_pro_count = goods[cf1][cf2][pro_g][1]
                                c_pro_cpunt = art[username]["count"][pro_g_ind]
                                return [pro_g, g_pro_count, c_pro_cpunt]
                        else:
                            pass
    with open(goods_file, 'w') as f:
        json.dump(goods, f, ensure_ascii=False)
    return True


def pay(goods_file, acc_file, username, cart):
    """
    结算支付
    :param goods_file:接收商品文件
    :param acc_file:接收账户文件
    :param username:接收用户名
    :return:成功-Ture，库存数量不足-"loq",余额不足-"lob"
    """
    print(cart)
    bill = 0
    with open(acc_file) as f:
        acc = json.load(f)
        bal_ind = acc["user"].index(username)
        balance = acc["balance"][bal_ind]
    for i in range(len(cart[username]["product"])):
        product_price = cart[username]["price"][i]
        product_count = cart[username]["count"][i]
        subtotal = product_price * product_count
        bill += subtotal
    if balance >= bill:
        balance -= bill
        print(balance)
        s_ret = subcount(goods_file, cart, username)  # 减库存
        # goods_file,cart,username
        #:return:成功-True,数量不足返回[商品名称，库存数量，购买数量]
        if s_ret == True:
            with open(acc_file, 'w') as f:
                acc["balance"][bal_ind] = balance
                json.dump(acc, f, ensure_ascii=False)
            return True
        else:
            return s_ret  # 返回库存数量不足
    else:
        return [balance, bill]  # 返回余额不足


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


def shopping_log(cart, username, logfile):
    """
    购物历史记录
    :param username:用户名
    :param cart:当前的购物车
    :param logfile:购物历史文件
    """
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # if cart
    """
    if logfile:
        with open(logfile) as f:
            buy_log_old = json.load(f)
            buy_log_new = buy_log_old[t] = cart
        with open(logfile,'a') as f:
            json.dump(buy_log_new,f,ensure_ascii = False)

    else:
    {"zhangyy": {"product": ["UnpluggedinNewYork"], "price": [80], "count": [1]}}}
    """
    pro = cart[username]["product"]
    pri = cart[username]["price"]
    cou = cart[username]["count"]
    with open(logfile, "a", encoding="utf-8") as f:
        for i in range(len(pro)):
            log = username + "|" + t + "|" + \
                str(pro[i]) + "|" + str(pri[i]) + "|" + str(cou[i]) + "\n"
            f.write(log)


def load_log(username, logfile):
    """
    加载购物历史
    :param username:用户名
    :param logfile:购物历史文件
    :return:有历史返回购物历史，无历史返回None
    """
    with open(logfile, 'r+') as f:
        for line in f.readlines():
            log = line.split("|")
            if log[0] == username:
                print("%s，您在%s购买了%s，单价%s，数量%s" %
                      (log[0], log[1], log[2], log[3], log[4]))


def showcart(cart):
    """
    输入购物车信息
    :param cart:购物车
    """
    if cart:
        for user in cart:
            for i in len(cart[user]["product"]):
                pro = cart[username]["product"][i]
                pri = cart[username]["price"][i]
                cou = cart[username]["count"][i]
                print("商品:%s,单价:%s,数量%s" % (pro, pri, cou))
        return True
    else:
        return None

# if __name__ == "__main__":
#     goods_file = ("goods.json")
#     acc_file = ("account.json")
#     logfile = ("shop.log")
#     cart = dict()
#     print("欢迎来到逆光穿行购物商城，祝您购物愉快！".center(40, "*"))
#     exit_flag1 = 1
#     exit_flag2 = 1
#     exit_flag3 = 1
#     login_flag = 0
#     while exit_flag1:
#         d1_list = showdir1(goods_file)
#         if d1_list:
#             while exit_flag2:
#                 print("商品大类".center(30, "*"))
#                 for i1, d1 in enumerate(d1_list):
#                     print("编号：%s,分类:%s" % (i1, d1))
#                 print("商品大类".center(30, "*"))
#                 input_dir1_num = input("请输入商品大类编号【q-退出】-->：").strip()
#                 if input_dir1_num == "q":
#                     exit_flag1 = 0
#                     exit_flag2 = 0
#                     showcart(cart)
#                 else:
#                     d2_list = showdir2(goods_file, d1_list, input_dir1_num)
#                     if d2_list is False:
#                         print("请输入正确的编号！")
#                         continue
#                     elif d2_list is None:
#                         print("商品还没准备好！")
#                         break
#                     else:
#                         while exit_flag3:
#                             print("商品小类".center(30, "*"))
#                             for i2, d2 in enumerate(d2_list):
#                                 print("编号：%s,分类:%s" % (i2, d2))
#                             print("商品小类".center(30, "*"))
#                             input_dir2_num = input(
#                                 "请输入商品小类编号【b-返回上级，q-退出】：-->").strip()
#                             if input_dir2_num == "b":
#                                 break
#                             elif input_dir2_num == "q":
#                                 exit_flag3 = 0
#                                 exit_flag2 = 0
#                                 exit_flag1 = 0
#                                 showcart(cart)
#                             else:
#                                 exit_flag4 = 1
#                                 while exit_flag4:
#                                     pro_list = showgoods(
#                                         goods_file, input_dir1_num,
#                                         input_dir2_num,
#                                         d1_list, d2_list)
#                                     if pro_list is False:
#                                         print("请输入正确的编号！")
#                                         continue
#                                     elif pro_list == None:
#                                         print("抱歉商品还没准备好！")
#                                         break
#                                     else:
#                                         print("商品信息".center(30, "*"))
#                                         for pro_ind, pro in enumerate(pro_list):
#                                             price = pro_list[pro][0]
#                                             p_c = pro_list[pro][1]
#                                             print("商品编号:%s.%s,单价:%s,库存数量%s" %
#                                                   (pro_ind, pro, price, p_c))
#                                         print("商品信息".center(30, "*"))
#                                         input_pro_num = input(
#                                             "请输入商品编号将商品添加到购物车【b-返回上一级，q-退出】:-->").strip()

#                                         user_login_failcount = {
#                                             "user": [], "failcount": []}
#                                         if input_pro_num == "b":
#                                             break
#                                         elif input_pro_num == "q":
#                                             exit_flag4 = 0
#                                             exit_flag3 = 0
#                                             exit_flag2 = 0
#                                             exit_flag1 = 0
#                                             showcart(cart)
#                                         else:
#                                             input_pro_cou = input(
#                                                 "请输入购买数量:-->")
#                                             while login_flag == 0:
#                                                 input_l_or_r = input(
#                                                     "加入购物车前必须登录，r-注册,任意键登录--->")
#                                                 input_username = input(
#                                                     "请输入用户名:-->").strip()
#                                                 input_password = getpass.getpass(
#                                                     "请输入密码：-->").strip()
#                                                 if input_l_or_r == "r":
#                                                     register(
#                                                         acc_file, input_username,
#                                                         input_password)
#                                                 else:
#                                                     if input_username in user_login_failcount["user"]:
#                                                         fc_ind = user_login_failcount[
#                                                             "user"].index(input_username)
#                                                         fc = user_login_failcount[
#                                                             "failcount"][fc_ind]
#                                                     else:
#                                                         user_login_failcount[
#                                                             "user"].append(input_username)
#                                                         user_login_failcount[
#                                                             "failcount"].append(0)
#                                                         fc = user_login_failcount[
#                                                             "failcount"][0]
#                                                     if fc < 2:
#                                                         login_ret = login(
#                                                             acc_file, input_username, input_password)
#                                                         if login_ret:
#                                                             print("登陆成功！")
#                                                             login_flag = 1
#                                                             load_log(
#                                                                 input_username, logfile)
#                                                         elif login_ret is None:
#                                                             print("用户名不存在！")
#                                                             continue
#                                                         elif login_ret == "locked":
#                                                             print("用户处于锁定状态！")
#                                                             continue
#                                                         else:
#                                                             print("用户名或密码错误！")
#                                                             ind_fc = user_login_failcount[
#                                                                 "user"].index(input_username)
#                                                             user_login_failcount[
#                                                                 "failcount"][ind_fc] += 1
#                                                             continue
#                                                     else:
#                                                         print(
#                                                             "尝试的次数过多，用户已被锁定！")
#                                                         locking(
#                                                             account_file, input_username)
#                                                         exit_flag4 = 0
#                                                         exit_flag3 = 0
#                                                         exit_flag2 = 0
#                                                         exit_flag1 = 0
#                                                         showcart(cart)
#                                             else:
#                                                 # goods_file,username,input_dir1_num,input_dir2_num,input_pro_num,input_pro_cou,cart
#                                                 a_ret = add_to_cart(
#                                                     goods_file, input_username, input_dir1_num, input_dir2_num, input_pro_num, input_pro_cou, cart)
#                                                 if a_ret == "loq":
#                                                     print("购买数量大于库存，无法添加至购物车！")
#                                                     continue
#                                                 elif a_ret == False:
#                                                     print("请输入正确的编号！")
#                                                     continue
#                                                 elif a_ret == 0:
#                                                     print("购买数量必须是整数！")
#                                                     continue
#                                                 else:
#                                                     print("您已成功将%s个%s加入购物车！" %
#                                                           (a_ret[1], a_ret[0]))
#                                                     pay_flag = 1
#                                                     while pay_flag == 1:
#                                                         pay_or_cbuy = input(
#                                                             "p-去结算，任意键继续购物！")
#                                                         if pay_or_cbuy == "p":
#                                                             p_ret = pay(
#                                                                 goods_file, acc_file, input_username, cart)
#                                                             #:return:成功-Ture，库存数量不足-"loq",余额不足-"lob"
#                                                             if p_ret == True:
#                                                                 print("支付成功！")
#                                                                 pay_flag = 0
#                                                                 shopping_log(
#                                                                     cart, input_username, logfile)
#                                                                 load_log(
#                                                                     input_username, logfile)
#                                                             elif type(p_ret[0]) == int:
#                                                                 print("您的余额为%s，订单金额为%s,不足以支付您的订单！" % (
#                                                                     p_ret[0], p_ret[1]))
#                                                                 while True:
#                                                                     input_r = input(
#                                                                         "r-充值,任意键-退出 -->")
#                                                                     if input_r == "r":
#                                                                         input_r_amount = input(
#                                                                             "请输入充值金额！")
#                                                                         r_ret = recharge(
#                                                                             acc_file, input_username, input_r_amount)
#                                                                         if r_ret == True:
#                                                                             print(
#                                                                                 "充值成功！")
#                                                                             break
#                                                                         else:
#                                                                             print(
#                                                                                 "充值失败！")
#                                                                             continue
#                                                                     else:
#                                                                         showcart(
#                                                                             cart)
#                                                                         exit(
#                                                                             "谢谢惠顾！")
#                                                         else:
#                                                             break
#         else:
#             print("没有商品谢谢光临！")
#             break
