#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2017/6/7 21:16
# @Author  : goustzhu <goustzhu@gmail.com>
# @File    : ExplainBuild.py
import sys, os, time, datetime
import CommonUtil as CU
import ConstParamClass as CPC
# from CommonUtil import MySQLClient

reload(sys)
dev_model='dev'

# main process
def explain_floor_cert(model='db', page_num=0, page_end=1):
    '''
    解析所有页面数据(从最后页面开始爬取)
    从数据库读取或者页面中读取页面数量
    :param model:       db:数据库中读取, page: 页面解析获取
    :param page_num:    获取页面数量
    :param page_end:    页面结束数
    :return:
    '''
    # mysql = MySQLClient(dev=model)
    mysql = CPC.Env(env=model).getMySQLClient()
    cur = mysql.get_cursor()
    page_begin = 1
    if model=='db':
        sql1 = "select val1 from %s where key1='%s' and key2='%s'" % \
               (CPC.DB.Table_config, CPC.DB.Key1_Build_Cert, CPC.DB.key2_Build_page_cur)
        res1 = mysql.query_one(sql1, cur)
        page_begin = int(res1[0])
        # print model, res1, page_begin
        CU.tolog('explain_floor_cert', 'model=%s' % (model), 'page_begin=%s' % (page_begin))
    elif model=='page':
        (num, page_begin) = explain_floor_cert_page_num(False)
        # print model, num, page_begin
        CU.tolog('explain_floor_cert', 'model=%s' % (model), 'page_begin=%s' % (page_begin))
    page_size = 1
    if page_num>0:
        if page_begin>page_num: page_size=page_num
        else: page_size = page_begin
    elif page_end>0: page_size = page_begin-page_end+1
    else: page_size = page_begin
    # print page_begin, page_size, page_num, page_end
    CU.tolog('explain_floor_cert', 'page_begin=%s' % (page_begin), 'page_size=%s' %(page_size))
    for i in range(page_size):
        page = page_begin - i
        explain_floor_cert_page(page, mysql, cur)

def explain_floor_cert_page(page, mysql, cur):
    '''
    解析楼盘发证情况，只有page=1时，解析页数
        并且当flag=True时，会将页数update到MySQL数据库中
    :param page:
    :param flag:
    :return:
    '''
    base_url = 'http://floor.0731fdc.com/builds.php'
    page_param = 'page=%s' % (page)
    html = CU.request_url('%s?%s' % (base_url, page_param))
    CU.tolog('explain_floor_cert_page', base_url, 'page=%s' % (page))
    # mysql = MySQLClient(dev='dev')
    # cur = mysql.get_cursor()
    list_floor = explain_floor_cert_list(html)
    if len(list_floor)>0:
        sql = 'insert into %s(floorid,floorname,buildno,pre_certno,cert_time,detail) values ' % (CPC.DB.Table_BuildCert)
        step = 0
        for floor in list_floor:
            if step>0:
                sql += ','
            (floor_id, floor_name, build_id, build_cert, build_cert_time) = floor
            sql += "(%s, '%s', '%s', '%s', '%s', '%s')" % (floor_id, floor_name, build_id, build_cert, build_cert_time, page)
            step += 1
        mysql.execute(sql, cur)
    sql1 = "update %s set val1=%s where key1='%s' and key2='%s'" % (CPC.DB.Table_config,
            page-1, CPC.DB.Key1_Build_Cert, CPC.DB.key2_Build_page_cur)
    mysql.execute(sql1, cur)
    return list_floor

def explain_floor_cert_page_num(flag=False):
    '''
    解析条数以及页数
    :param flag:
    :return:
    '''
    base_url = 'http://floor.0731fdc.com/builds.php'
    html = CU.request_url(base_url)
    page_div = CU.parser_html_by_class_one(html, 'ul', class_values='pageno')
    page_data = page_div.contents[0]
    # print page_data
    num_begin = 2
    num_end = page_data.find(u'条')
    sum_num = int(page_data[num_begin:num_end])
    page_begin = page_data.find(u'共') + 1
    page_end = page_data.rfind(u'页')
    # print page_begin, page_end, page_data[page_begin:page_end]
    sum_page = int(page_data[page_begin:page_end])
    if flag:
        mysql = CPC.Env(env=dev_model).getMySQLClient()
        cur = mysql.get_cursor()
        sql1 = "update %s set val1=%s where key1='%s' and (key2='%s' or key2='%s')" % (CPC.DB.Table_config,
                sum_page, CPC.DB.Key1_Build_Cert, CPC.DB.key2_Build_page_sum, CPC.DB.key2_Build_page_cur)
        CU.tolog('explain_floor_cert', 'mysql execute', sql1)
        mysql.execute(sql1, cur)
        sql2 = "update %s set val1='%s' where key1='%s' and key2='%s'" % (CPC.DB.Table_config,
               sum_num, CPC.DB.Key1_Build_Cert, CPC.DB.key2_Build_record_sum)
        CU.tolog('explain_floor_cert', 'mysql execute', sql2)
        mysql.execute(sql2, cur)
    return (sum_num, sum_page)

def explain_floor_cert_list(html):
    table_floor = CU.parser_html_by_class_one(html, 'table', 'textra')
    list_floor = []
    # tbody = table_floor.childs('to')
    for floor in table_floor.children:
        floor_name = ''
        floor_id = -1
        build_id = ''
        build_cert = ''
        build_cert_time = ''
        # print floor
        try:
            step = 0
            for td in floor.find_all('td'):
                # print step, td
                step += 1
                if step==1:
                    href = td.a['href']
                    floor_id = int(href[href.index('=')+1:])
                    floor_name = td.a.contents[0]
                elif step == 2:
                    tmp = td.a.contents
                    if len(tmp)>0: build_id = tmp[0]
                    else: build_id = ''
                elif step==3:
                    tmp = td.a.contents
                    if len(tmp)>0: build_cert = tmp[0]
                    else: build_cert = ''
                elif step == 4:
                    tmp = td.contents
                    if len(tmp)>0: build_cert_time = tmp[0]
                    else: build_cert_time = ''
            if floor_id > 0:
                list_floor.append((floor_id, floor_name, build_id, build_cert, build_cert_time))
                # print '--', floor_id, floor_name, build_id, build_cert, build_cert_time
        except Exception as e:
            # CU.tolog('Exception', e.message, floor)
            pass
    return list_floor

if __name__=='__main__':
    print datetime.datetime.now(), 'begin'.center(80, '-')
    # mysql = MySQLClient(dev='dev')
    # cur = mysql.get_cursor()
    # list_floor = explain_floor_cert_page(580,mysql,cur)
    # for floor in list_floor:
    #     print floor
    # (num, page) = explain_floor_cert_page_num(True)
    # print num, page
    explain_floor_cert(model='db', page_num=0)
    print datetime.datetime.now(), ' end '.center(80, '-')


