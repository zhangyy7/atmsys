#! /usr/bin/env python
# -*- coding: utf-8 -*-
import getpass
from modules.shopping import shopping as sp


def register_api():
    username = input("请输入用户名：")
    password = getpass.getpass("请输入密码：")
    sp.register(username, password)
