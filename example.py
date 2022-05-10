#!/usr/bin/env python

"""
Rev-1ファイルをパースし、
分散共分散行列を核種と反応の種類の情報をキーとしてjson化する。
"""

from __future__ import annotations
import json

import rev1
import zaid

rev1path = "REV1.01v"
rev1data = rev1.load(rev1path)

covinfos = rev1data.xss.ix_cov
row_len = rev1data.nxs.ng
column_len = rev1data.nxs.ng
mat_slice = rev1data.ix_cov_data_slice

rev1_parsed = list()
for covinfo in covinfos:
    base = covinfo.ix_dat
    rev1_parsed.append({
        "covinfo": {
            "za1": zaid.decode(covinfo.za1),
            "mt1": str(covinfo.mt1),
            "za2": zaid.decode(covinfo.za2),
            "mt2": str(covinfo.mt2),
        },
        "covmat": [mat_slice(base+i*row_len, base+i*row_len+row_len) for i in range(column_len)],
    })

with open("converted.json", mode="wt") as f:
    json.dump(rev1_parsed, f)
