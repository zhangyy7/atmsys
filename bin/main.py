#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import os
import sys

from conf import settings, templates
from modules import credit
from utils import utils

MY_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(MY_PATH)

PAGE_DICT = {
    "1": "show_shop",
    "2": "index_atm",
    "3": "index_admin"

}
