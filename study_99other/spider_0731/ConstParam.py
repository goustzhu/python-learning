#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2017/6/9 21:48
# @Author  : goustzhu <goustzhu@gmail.com>
# @File    : ConstParam.py
import sys, os, time, datetime

reload(sys)
sys.setdefaultencoding('utf-8')

Const_MySQL_Table_config = 'dbconfig'
Const_MySQL_Table_BuildCert = 'floor_cert'

Const_Key1_Build_Cert = 'build_cert'
Const_key2_Build_record_sum = 'record_sum'
Const_key2_Build_page_sum = 'page_sum'
Const_key2_Build_record_cur = 'record_cur'
Const_key2_Build_page_cur = 'page_cur'

# online model
Const_Online_MySQL_Host = '192.168.199.31'
Const_Online_MySQL_Port = 3306
Const_Online_MySQL_User = 'goust'
Const_Online_MySQL_Password = '1234'
Const_Online_MySQL_Database_Name='floor0731'

Const_Online_Mongo_Host = '192.168.199.41'
Const_Online_Mongo_Port = 27017
Const_Online_Mongo_Database_Name='floor0731'
Const_Online_Mongo_User = ''
Const_Online_Mongo_Password = ''

# dev model
Const_Dev_MySQL_Host = '192.168.199.31'
Const_Dev_MySQL_Port = 3306
Const_Dev_MySQL_User = 'goust'
Const_Dev_MySQL_Password = '1234'
Const_Dev_MySQL_Database_Name='floor0731'

Const_Dev_Mongo_Host = '192.168.199.41'
Const_Dev_Mongo_Port = 27017
Const_Dev_Mongo_Database_Name='floor0731'
Const_Dev_Mongo_User = ''
Const_Dev_Mongo_Password = ''