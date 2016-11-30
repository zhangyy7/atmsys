#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import os
import hashlib
import datetime
import calendar
import functools


def to_str(str_or_bytes):
    """bytes类型转str类型"""
    if isinstance(str_or_bytes, bytes):
        value = str_or_bytes.decode("utf-8")
    else:
        value = str_or_bytes
    return value


def to_bytes(str_or_bytes):
    """str类型转bytes类型"""
    if isinstance(str_or_bytes, str):
        value = str_or_bytes.encode("utf-8")
    else:
        value = str_or_bytes
    return value


def load_file(filename):
    """加载json格式的文件，返回对象"""
    if os.path.isfile(filename):
        with open(filename, encoding="utf-8") as f:
            obj = json.load(f)
        return obj
    else:
        return "文件不存在"


def open_file(filename, mo):
    """打开文件，返回文件句柄"""
    if os.path.isfile(filename):
        f = open(filename, mo, encoding="utf-8")
        return f
    else:
        pass


def dump_to_file(filename, obj):
    """将json格式的对象dump到文件"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(obj, f, sort_keys=True, ensure_ascii=False)


def to_num(str):
    """将数字型的字符串转换成数字"""
    if str.isdigit():
        if len(str) == 16:
            value = int(str)
            return value
        else:
            False
    else:
        False


def mkdir(path):
    """判断文件是否存在，若不存在则创建文件"""
    path = path.strip()
    path = path.rstrip("\\")
    if os.path.exists(path):
        return "账号已存在"
    else:
        os.makedirs(path)


def encrypt(str, pwd=None):
    """以md5方式加密字符串"""
    hash = hashlib.md5()
    hash.update(bytes(str, encoding='utf-8'))
    value = hash.hexdigest()
    return value


def get_lastmonth(date):
    """获取上个月的今天"""
    year = date.year
    month = date.month
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1
    ndays = calendar.monthrange(year, month)[1]
    last_month = date - datetime.timedelta(days=ndays)
    return last_month


def auth(before_func, after_func=None):
    """一个通用的装饰器"""
    def outer(main_func):
        @functools.wraps(main_func)
        def warpper(*args, **kwargs):
            before_func()
            print("开始执行被装饰的函数")
            main_result = main_func(*args, **kwargs)
            if not main_result:
                return main_result
        return warpper
    return outer
