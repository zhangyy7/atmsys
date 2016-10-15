#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import os
import sys
MY_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(MY_PATH)
from conf import settings
from modules import credit
from utils import utils


def main():
    ret = credit.create_account("6223123490908767", "test", "user")

if __name__ == '__main__':
    main()
