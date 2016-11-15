#!/usr/bin/env pytohn
# -*-coding: utf-8 -*-

import re

count = 1  # 全局变量，计数器


def deal_brackets(expression):
    """
    递归的处理扩号，直到没有括号为止
    param expression:计算表达式
    return:计算结果
    """
    global count  # 计数器
    expression = expression.replace(" ", "").strip()  # 出去表达式中的空格和换行
    print("第%d次处理括号,表达式为%s" % (count, expression))
    patt = r"\(([^()]+)\)"  # 正则表达式，匹配(开头)结尾，中间不包含括号的表达式
    if re.search(patt, expression):  # 此代码块实现只要存在patt规则的表达式，那么就递归的处理括号，直到没有括号为止
        left, me, right = re.split(patt, expression, 1)
        print("第%d个括号:%s" % (count, me))
        tem = calculate(me)
        new_expression = "%s%s%s" % (left, tem, right)
        print("第%d个括号处理后的新表达式为:%s" % (count, new_expression))
        count += 1
        return deal_brackets(new_expression)
    else:
        return calculate(expression)


def calculate_div_mul(expression):
    """
    处理乘除运算
    param expression:不包含括号的表达式
    return: 若表达式中存在由*或者/连接起来的表达式，递归的计算乘除，知道处理掉所有的乘除后返回乘除计算结果
    """
    expression = expression.replace(" ", "").strip()
    while True:
        if expression.__contains__("+-") or\
           expression.__contains__("-+") or\
           expression.__contains__("--") or\
           expression.__contains__("++"):
            expression = expression.replace("+-", "-")
            expression = expression.replace("-+", "-")
            expression = expression.replace("++", "+")
            expression = expression.replace("--", "+")
        else:
            break
    patt = r"(-?\d+\.?\d*[*|/]-?\d+\.?\d*)"  # 正则表达式，匹配*或/符号链接的算式
    if re.search(patt, expression):
        left, me, right = re.split(patt, expression, 1)
        l, m, r = re.split(r"([*|/])", me, 1)
        if m == "*":
            val = float(l) * float(r)
        if m == "/":
            val = float(l) / float(r)
        new_expression = "%s+%s%s" % (left, val, right)
        return calculate_div_mul(new_expression)
    else:
        return expression


def calculate_add_sub(expression):
    """
    处理加减运算
    param expression:不含括号的，处理完乘除后的表达式
    return: 如果存在+或-号连接的表达式，递归的处理加减运算，最终返回加减运算结果
    """
    expression = expression.replace(" ", "")
    while True:  # 处理正负号
        if expression.__contains__("+-") or\
           expression.__contains__("-+") or\
           expression.__contains__("--") or\
           expression.__contains__("++"):
            expression = expression.replace("+-", "-")
            expression = expression.replace("-+", "-")
            expression = expression.replace("++", "+")
            expression = expression.replace("--", "+")
        else:
            break
    patt = r"(-?\d+\.?\d*[+|-]-?\d+\.?\d*)"
    if re.search(patt, expression):
        left, me, right = re.split(patt, expression, 1)
        l, m, r = re.split(r'([+|-])', me, 1)
        if not l:
            l1, m1, r1 = re.split(r"([+|-])", r, 1)
            l1 = "%s%s" % (m, l1)
            if m1 == "+":
                val = float(l1) + float(r1)
            if m1 == "-":
                val = float(l1) - float(r1)
        else:
            if m == "+":
                val = float(l) + float(r)
            if m == "-":
                val = float(l) - float(r)
        new_expression = "%s%s%s" % (left, val, right)
        return calculate_add_sub(new_expression)
    else:
        return expression


def calculate(expression):
    expression = expression.replace(" ", "")
    if re.search(r"[*|/]", expression):
        expression = calculate_div_mul(expression)
    if re.search(r"[+|-]", expression):
        expression = calculate_add_sub(expression)
    return expression


def main():
    expression = input("请输入计算表达式（只能计算加减乘除）>>")
    result = deal_brackets(expression)
    print("最终计算结果:", result)

if __name__ == "__main__":
    main()
