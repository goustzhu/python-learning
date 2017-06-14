#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2017/6/6 22:37
# @Author  : goustzhu <goustzhu@gmail.com>
# @File    : CommonUtil.py
import sys, os, time, datetime
import requests
from bs4 import BeautifulSoup
import pymongo
import pymysql

def request_url_encode(url, encode='gb2312'):
    '''
    从URL获取数据
    :param url:
    :return:
    '''
    html = requests.get(url)
    html.encoding=encode
    return html.text

def request_url(url):
    html = requests.get(url).content
    return html

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    # print soup.title.prettify()
    # print soup.title.prettify('gb18030')
    return soup

def parser_html_by_attrs(html, tag_name, attrs, encode='gb18030'):
    soup = BeautifulSoup(html, 'html.parser', from_encoding=encode)
    tag = soup.find(tag_name, attrs=attrs)
    return tag

def parser_html_by_class_one(html, tags_name, class_values):
    soup = BeautifulSoup(html, 'html.parser', from_encoding='gb18030')
    tag = soup.find(tags_name, class_=class_values)
    return tag

def parser_html_by_class(html, tags_name, class_values):
    soup = BeautifulSoup(html, 'html.parser', from_encoding='gb18030')
    tags = soup.find_all(tags_name, class_=class_values)
    # print tags
    return tags

def tolog(s1='-', s2='-', s3='-', s4='-', s5='-', s6='-', s7='-', s8='-', debug_log=True):
    # t = time.strftime("%Y-%m-%d %H:%M:%S")
    t = '%s' % datetime.datetime.now()
    ss = '] ['.join([str(s) for s in [s1, s2, s3, s4, s5, s6, s7, s8] if s != '-'])
    str_log = '%s [%s]' % (t, ss)
    if debug_log:
        print >> sys.stderr, str_log

class MongoClient(object):
    '''
    连接Mongo Client类
    '''
    def __init__(self, host, port, dbname, user, password):
        self.conn = self.connect_mongo(host, port, dbname, user, password)

    def connect_mongo(self, host, port, dbname, user=None, password=None):
        tolog('connect Mongo info', 'host=%s' % (host), 'port=%s' % (port), 'dbname=%s' % (dbname))
        db_client = pymongo.MongoClient('%s:%s'%(host, port), connect=False)
        db = db_client[dbname]
        if user is not None and len(user)>0:
            db.authenticate(user, password)
        return db

    def insert_record(self, record, collname):
        self.conn[collname].save(record)

class MySQLClient(object):
    '''
    连接MySQL Client类
    '''
    def __init__(self, host, port, dbname, user, password):
        # self.dev = dev
        self.conn = self.connect_mysql(host, port, dbname, user, password)

    def connect_mysql(self, host, port, dbname, user, password):
        '''
        连接到mysql
        :return:
        '''
        tolog('connect MySQL info', 'host=%s' % (host), 'port=%s' % (port), 'dbname=%s' % (dbname))
        conn = pymysql.connect(host=host, port=port, user=user, password=password, db=dbname, charset='utf8')
        return conn

    def get_cursor(self):
        return self.conn.cursor()

    def query(self, query, cur):
        '''
        从MySQL数据库中查询结果集
        :param conn:
        :param query:
        :return:
        '''
        cur.execute(query)
        result = cur.fetchall()
        # cur.close()
        return result

    def query_one(self, query, cur):
        '''
        查询一条记录
        :param query:
        :param cur:
        :return:
        '''
        cur.execute(query)
        result = cur.fetchone()
        return result

    def execute(self, query, cur):
        '''
        执行sql语句
        :param query:
        :return:
        '''
        tolog('MySQL execute', query)
        cur.execute(query)
        self.conn.commit()

    def connect_close(self):
        self.conn.close()

