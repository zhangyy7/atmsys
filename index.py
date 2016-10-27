#!/usr/bin/env python
# --coding: utf-8 --
from conf import templates
from bin import main
from modules.credit import admin, system, auth, users


def run():
    """
    侏罗纪
    """
    index_memu = {
        "1": "shop",
        "2": templates.INDEX_ATM
    }
    atm_menu = {
        "1": "draw",
        "2": "transf",
        "3": "repayment",
        "4": "back"
    }
    if hasattr(templates, "format_page"):
        f1 = getattr(templates, "format_page")
        inp1 = input("%s>>>" % f1())
        inp2 = input("%s>>>" % f1())

if __name__ == '__main__':
    run()
