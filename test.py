#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import arrow

if __name__ == '__main__':
    now = arrow.now().for_json()
    dic = {now:"1"}
    with open("test.json","w") as f:
        json.dump(now, f)

    with open("test.json") as f:
        obj = json.load(f)
        t = arrow.Arrow.strptime(obj,'%Y-%m-%d %H:%M:%S')
        print(t)