#!/usr/bin/env python
# --coding: utf-8 --
from conf import templates


def main():
    """
    侏罗纪
    """
    if hasattr(templates, "show_page"):
        f1 = getattr(templates, "show_page")
        f1()
    inp_page_num = input("请数据url：")
    if templates.PAGE_DICT.get(inp_page_num):
        pass
    else:
        pass


if __name__ == '__main__':
    main()
