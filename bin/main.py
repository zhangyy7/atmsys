#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import os
import sys

from conf import settings
from modules import credit
from utils import utils

MY_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(MY_PATH)


def main():
    ret = credit.draw_cash("6222123409580001", "12345", 500)
    print(ret)
