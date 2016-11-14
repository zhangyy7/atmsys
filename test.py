#!/usr/bin/env pytohn
# -*-coding: utf-8 -*-

import re


def deal_brackets(expression):
    expression = expression.replace(" ", "")
    patt = r"\(([^()]+)\)"
    ret = re.search(patt, expression)
    if ret:
        left, me, right = re.split(patt, expression, 1)
        print(me)
        tem = calculate(me)
        new_expression = "%s%s%s" % (left, tem, right)
        print(new_expression)
        return deal_brackets(new_expression)
    else:
        return expression


def calculate_div_mul(expression):
    # print(expression.replace(" ", ''))
    expression = expression.replace(" ", "")
    patt = r"(\d+\.?\d*[\*|\/]\d+\.?\d*)"
    tem = re.search(patt, expression)
    if tem:
        # print("乘除第一步", tem.group())
        left, me, right = re.split(patt, expression, 1)
        l, m, r = re.split(r"([(\*|\/)])", me)
        print(l, r)
        if m == "*":
            val = float(l) * float(r)
        if m == "/":
            val = float(l) / float(r)
        new_expression = "%s%s%s" % (left, val, right)
        return calculate_div_mul(new_expression)
    else:
        return expression


def calculate_add_sub(expression):
    expression = expression.replace(" ", "")
    patt = r"(\d+\.?\d*[+|-]\d+\.?\d*)"
    tem = re.search(patt, expression)
    if tem:
        left, me, right = re.split(patt, expression, 1)
        l, m, r = re.split(r'([+|-])', me)
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
    result_tem = calculate_div_mul(expression)
    result = calculate_add_sub(result_tem)
    print(result)


exp = "5 * 6 + 3 + 5 - (4 + 5 / (3 * 3 + 4))"
print(deal_brackets(exp))
