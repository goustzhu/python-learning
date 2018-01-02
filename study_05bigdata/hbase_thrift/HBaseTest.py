#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2018/1/2 18:42
# @Author  : goustzhu <goustzhu@gmail.com>
# @File    : HBaseTest.py
# @Software: PyCharm
from __future__ import division, print_function
import sys, os, time, datetime, warnings
from hbase_connection import ConnectionPool, FeatureEntity
from thrift.packages.hbase.ttypes import *

warnings.filterwarnings("ignore")

def test1():
    host = "sparknn1"
    port = 9090
    tablename = "xin_feature:xin_item_car_feature_info"
    rowkey = "b0003s000000787m000031367c0011007797"
    pool = ConnectionPool(size=5, host=host, port=port)
    # with pool.get_connection() as conn:
    conn = pool.get_connection()
    entity = conn.get(tablename, rowkey)
    print("----"+str(entity))
    pool.return_connection(conn)

def test():
    host = "sparknn1"
    port = 9090
    table = "xin_feature:xin_item_level_feature_info"
    # conn = Connection(host=host, port=port)
    scan = TScan(filterString="(PrefixFilter('sb0084'))")
    # result = conn.scanNumber(table, scan)
    # print(result)
    pool = ConnectionPool(size=5, host=host, port=port)
    conn = pool.get_connection()
    result = conn.scanNumber(table, scan)
    pool.return_connection(conn)
    # conn.close()

if __name__ == "__main__":
    print("begin".center(100, "-"))
    for i in range(20):
        print("+++++++++%s++++++++++" % (i))
        test1()
        test()
    print(" end ".center(100, "-"))