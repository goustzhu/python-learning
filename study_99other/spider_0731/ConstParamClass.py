#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2017/6/10 12:43
# @Author  : goustzhu <goustzhu@gmail.com>
# @File    : ConstParamClass.py
import sys, os, time, datetime
from CommonUtil import MySQLClient, MongoClient

reload(sys)
sys.setdefaultencoding('utf-8')

class Env(object):
    '''
    数据库环境配置
    '''
    def __init__(self, env='dev'):
        self.env = env
        if env == 'online':
            self.Mongo_Host = DB.Const_Online_Mongo_Host
            self.Mongo_Port = DB.Const_Online_Mongo_Port
            self.Mongo_DBName = DB.Const_Online_Mongo_DbName
            self.Mongo_User = DB.Const_Online_Mongo_User
            self.Mongo_Password = DB.Const_Online_Mongo_Password
            self.MySQL_Host = DB.Const_Online_MySQL_Host
            self.MySQL_Port = DB.Const_Online_MySQL_Port
            self.MySQL_DBName = DB.Const_Online_MySQL_DbName
            self.MySQL_User = DB.Const_Online_MySQL_User
            self.MySQL_Password = DB.Const_Online_MySQL_Password
        else:
            self.Mongo_Host = DB.Const_Dev_Mongo_Host
            self.Mongo_Port = DB.Const_Dev_Mongo_Port
            self.Mongo_DBName = DB.Const_Dev_Mongo_DbName
            self.Mongo_User = DB.Const_Dev_Mongo_User
            self.Mongo_Password = DB.Const_Dev_Mongo_Password
            self.MySQL_Host = DB.Const_Dev_MySQL_Host
            self.MySQL_Port = DB.Const_Dev_MySQL_Port
            self.MySQL_DBName = DB.Const_Dev_MySQL_DbName
            self.MySQL_User = DB.Const_Dev_MySQL_User
            self.MySQL_Password = DB.Const_Dev_MySQL_Password

    def getMySQLClient(self):
        return MySQLClient(host=self.MySQL_Host, port=self.MySQL_Port, dbname=self.MySQL_DBName,
                           user=self.MySQL_User, password=self.MySQL_Password)

    def getMongoClient(self):
        return MongoClient(host=self.Mongo_Host, port=self.Mongo_Port, dbname=self.Mongo_DBName,
                           user=self.Mongo_User, password=self.Mongo_Password)

class DB(object):
    '''
    MySQL中table name
    Mongo中collection name
    MySQL读取配置常量名称
    '''

    Table_config = 'dbconfig'
    Table_BuildCert = 'floor_cert'
    Table_FloorDiscount = 'floor_discount'
    Table_FLoorBase = 'floor_base_info'
    Table_FloorDetail = 'floor_detail_info'
    Table_FloorSimilar = 'floor_similar_info'
    Table_FloorExport = 'floor_export_score'
    Table_CompanyComplaint = 'company_complaint_info'

    Coll_floor_list = 'floor_list'
    Coll_floor_search = 'floor_search'
    Coll_floor_open = 'floor_open'
    Coll_floor_news = 'floor_news'
    Coll_Company_info = 'company_info'
    Coll_Company_Complaint = 'company_complaint'

    Key1_Build_Cert = 'build_cert'
    Key1_Floor_List = 'floor_list_info'
    Key1_Floor_Open = 'floor_open'
    Key1_Floor_Discount = 'floor_discount'
    Key1_Floor_Info = 'floor_info'
    Key1_Company_develop = 'complaint_develop'
    Key1_Company_agency = 'complaint_agency'
    Key1_Company_property = 'complaint_property'
    Key1_Company_decoration = 'complaint_decoration'
    Key1_Company_info = 'company_info'

    Key2_record_sum = 'record_sum'
    Key2_record_cur = 'record_cur'
    Key2_page_sum = 'page_sum'
    Key2_page_cur = 'page_cur'

    key2_Build_record_sum = Key2_record_sum
    key2_Build_page_sum = Key2_page_sum
    key2_Build_record_cur = Key2_record_cur
    key2_Build_page_cur = Key2_page_cur

    key2_Floor_List_record_sum = Key2_record_sum
    key2_Floor_List_page_sum = Key2_page_sum
    key2_Floor_List_page_cur = Key2_page_cur

    key2_Floor_Open_Itemid_cur = 'itemid_cur'

    key2_Floor_Discount_record_sum = Key2_record_sum
    key2_Floor_Discount_page_sum = Key2_page_sum
    key2_Floor_Discount_page_cur = Key2_page_cur

    key2_Floor_info_record_cur = Key2_record_cur

    # online model
    Const_Online_MySQL_Host = '192.168.199.31'
    Const_Online_MySQL_Port = 3306
    Const_Online_MySQL_User = 'goust'
    Const_Online_MySQL_Password = '1234'
    Const_Online_MySQL_DbName = 'floor0731'

    Const_Online_Mongo_Host = '192.168.199.41'
    Const_Online_Mongo_Port = 27017
    Const_Online_Mongo_DbName = 'floor0731'
    Const_Online_Mongo_User = ''
    Const_Online_Mongo_Password = ''

    # dev model
    Const_Dev_MySQL_Host = '192.168.199.31'
    Const_Dev_MySQL_Port = 3306
    Const_Dev_MySQL_User = 'goust'
    Const_Dev_MySQL_Password = '1234'
    Const_Dev_MySQL_DbName = 'floor0731'

    Const_Dev_Mongo_Host = '192.168.199.41'
    Const_Dev_Mongo_Port = 27017
    Const_Dev_Mongo_DbName = 'floor0731'
    Const_Dev_Mongo_User = ''
    Const_Dev_Mongo_Password = ''

class Const(object):
    '''
    基本常量
    '''
