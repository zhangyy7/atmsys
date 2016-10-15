#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import os
import sys


def to_str(str_or_bytes):
    if isinstance(str_or_bytes,bytes):
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
