#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import os
import hashlib
import datetime


def to_str(str_or_bytes):
    if isinstance(str_or_bytes, bytes):
        value = str_or_bytes.decode("utf-8")
    else:
        value = str_or_bytes
    return value


def to_bytes(str_or_bytes):
    if isinstance(str_or_bytes, str):
        value = str_or_bytes.encode("utf-8")
    else:
        value = str_or_bytes
    return value


def load_file(filename):
    with open(filename, encoding="utf-8") as f:
        obj = json.load(f)
    return obj


def dump_to_file(filename, obj):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(obj, f)


def to_num(str):
    if str.isdigit():
        if len(str) == 16:
            value = int(str)
            return value
        else:
            False
    else:
        False


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    if os.path.exists(path):
        return "账号已存在"
    else:
        os.makedirs(path)


def encrypt(str, pwd=None):
    hash = hashlib.md5()
    hash.update(bytes(str, encoding='utf-8'))
    value = hash.hexdigest()
    return value


def get_lastmonth(date):
    """获取上个月的今天"""
    year = date.year
    month = date.month
    day = date.day
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1
    ndays = calendar.monthrange(year, month)[1]
    last_month = date - datetime.timedelta(days=ndays)
    return last_month
