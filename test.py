#!/usr/bin/env pytohn
# -*-coding: utf-8 -*-

import re

count = 1


def deal_brackets(expression):
    global count
    expression = expression.replace(" ", "")
    print("第%d次处理括号,表达式为%s" % (count, expression))
    patt = r"\(([^()]+)\)"
    # ret = re.search(patt, expression)
    if re.search(patt, expression):
        left, me, right = re.split(patt, expression, 1)
        print("第%d个括号:%s" % (count, me))
        tem = calculate(me)
        new_expression = "%s%s%s" % (left, tem, right)
        count += 1
        return deal_brackets(new_expression)
    else:
        print("第%d括号处理好了,处理后的表达式为%s" % (count, expression))
        return calculate(expression)


def calculate_div_mul(expression):
    # print(expression.replace(" ", ''))
    # print("乘除第%s次处理" % count)
    expression = expression.replace(" ", "")
    patt = r"(-?\d+\.?\d*[*|/]-?\d+\.?\d*)"
    # tem = re.search(patt, expression)
    if re.search(patt, expression):
        # print("乘除第一步", re.search(patt, expression).group())
        left, me, right = re.split(patt, expression, 1)
        # print(left)
        # print(me)
        # print(right)
        l, m, r = re.split(r"([*|/])", me, 1)
        # print("左边%s,运算符%s,右边%s" % (l, m, r))
        if m == "*":
            val = float(l) * float(r)
            # print(val)
        if m == "/":
            val = float(l) / float(r)
            # print(val)
        if left is None:
            new_expression = "%s+%s" % (val, right)
        if right is None:
            new_expression = "%s+%s" % (left, val)
        else:
            new_expression = "%s%s%s" % (left, val, right)
        # print("乘除后表达式", new_expression)
        # count += 1
        return calculate_div_mul(new_expression)
    else:
        # print("乘除处理完毕", expression)
        return expression


def calculate_add_sub(expression):
    # print("加减%s" % expression)
    expression = expression.replace(" ", "")
    patt = r"(-?\d+\.?\d*[+|-]-?\d+\.?\d*)"
    # tem = re.search(patt, expression)
    if re.search(patt, expression):
        # print(re.search(patt, expression).group())
        left, me, right = re.split(patt, expression, 1)
        # print("add_sub left:", left)
        # print("add_sub me:", me)
        # print("add_sub right:", right)
        # print(re.split(r'([+|-])', me, 1))
        l, m, r = re.split(r'([+|-])', me, 1)
        # print("l:", l)
        # print("m:", m)
        # print("r:", r)
        if not l:
            l1, m1, r1 = re.split(r"([+|-])", r, 1)
            l1 = "%s%s" % (m, l1)
            # print("l1:", l1)
            if m1 == "+":
                val = float(l1) + float(r1)
                # print("add_sub val:", val)
            if m1 == "-":
                val = float(l1) - float(r1)
                # print("add_sub val:", val)
        else:
            if m == "+":
                val = float(l) + float(r)
                # print("add_sub val:", val)
            if m == "-":
                val = float(l) - float(r)
                # print("add_sub val:", val)
        new_expression = "%s%s%s" % (left, val, right)
        # count += 1
        return calculate_add_sub(new_expression)
    else:
        # print("加减处理完毕", expression)
        return expression


def calculate(expression):
    # print("第%d次计算" % count)
    expression = expression.replace(" ", "")
    # patt1 = r"(\d+\.?\d*[\*|\/]\d+\.?\d*)"
    # patt2 = r"\d+\.?\d*[+|-]\d+\.?\d*"
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
    # print("ddddddddddddddddddddddd", expression)
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
    # main()
    print(calculate("1-2*-14969036.7968254"))

