#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2017/6/14 21:15
# @Author  : goustzhu <goustzhu@gmail.com>
# @File    : ExplainFloorDiscount.py
import sys, os, time, datetime
import CommonUtil as CU
import ConstParamClass as CPC

reload(sys)
sys.setdefaultencoding('utf-8')

dev_model='dev'
base_url = 'http://news.0731fdc.com/?catid=75&mod=list&act=news'
'''
解析打折信息
'''

def explain_floor_discount(model='db', start_page=1, page_num=10):
    '''
    从数据库读取当前解析page,
    :param model:
    :param size:
    :return:
    '''
    env = CPC.Env(env=dev_model)
    mysql = env.getMySQLClient()
    cur = mysql.get_cursor()
    if model == 'db':
        sql1 = "select val1 from %s where key1='%s' and key2='%s'" % \
               (CPC.DB.Table_config, CPC.DB.Key1_Floor_Discount, CPC.DB.key2_Floor_Discount_page_cur)
        res1 = mysql.query_one(sql1, cur)
        start_page = int(res1[0])
    for i in range(page_num):
        cur_page = start_page-i
        if cur_page>0:
            list_contents = explain_floor_discount_list(cur_page)
            for record in list_contents:
                sql = "insert into %s(page, record_date, link_url, title) values (%s, '%s', '%s', '%s')" % \
                      (CPC.DB.Table_FloorDiscount, cur_page, record[0], record[1], record[2])
                mysql.execute(sql, cur)
            sql1 = "update %s set val1=%s where key1='%s' and key2='%s'" % (CPC.DB.Table_config,
                    cur_page - 1, CPC.DB.Key1_Floor_Discount, CPC.DB.key2_Floor_Discount_page_cur)
            mysql.execute(sql1, cur)

def explain_floor_discount_page(flag=False):
    '''
    解析打折信息数量及页数
    :return:
    '''
    html = CU.request_url_encode(base_url)
    soup = CU.parse_html(html)
    page_ul = soup.find('ul', class_='pageno')
    page_data = page_ul.contents[0]
    # print page_data
    num_begin = 2
    num_end = page_data.find(u'条')
    sum_num = int(page_data[num_begin:num_end])
    page_begin = page_data.find(u'共') + 1
    page_end = page_data.rfind(u'页')
    sum_page = int(page_data[page_begin:page_end])
    if flag:
        mysql = CPC.Env(dev_model).getMySQLClient()
        cur = mysql.get_cursor()
        sql1 = "update %s set val1=%s where key1='%s' and (key2='%s' or key2='%s')" % (CPC.DB.Table_config,
                sum_page, CPC.DB.Key1_Floor_Discount, CPC.DB.key2_Floor_Discount_page_sum, CPC.DB.key2_Floor_Discount_page_cur)
        CU.tolog('explain_floor_list', 'mysql execute', sql1)
        mysql.execute(sql1, cur)
        sql2 = "update %s set val1='%s' where key1='%s' and key2='%s'" % (CPC.DB.Table_config,
                sum_num, CPC.DB.Key1_Floor_Discount, CPC.DB.key2_Floor_Discount_record_sum)
        CU.tolog('explain_floor_list', 'mysql execute', sql2)
        mysql.execute(sql2, cur)
    return (sum_num, sum_page)

def explain_floor_discount_list(page):
    '''
    解析列表数据
    :param page:
    :return:
    '''
    html = CU.request_url_encode('%s&page=%s' % (base_url, page))
    soup = CU.parse_html(html)
    tag_ul = soup.find('ul', class_='list')
    list_contents = []
    for li in tag_ul.find_all('li'):
        span = li.find('span').get_text().strip().replace('[','').replace(']', '')
        tag_a = li.find('a')
        link_url = tag_a['href']
        title = tag_a.get_text().strip().replace('\\','')
        # print span, title, link_url
        list_contents.append((span, link_url, title))
    return list_contents

if __name__=='__main__':
    print datetime.datetime.now(), 'begin'.center(80, '-')
    # (num, page) = explain_floor_discount_page(True)
    # print num, page
    # explain_floor_discount_list(1)
    explain_floor_discount(model='db', page_num=100)
    print datetime.datetime.now(), ' end '.center(80, '-')
