#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2017/6/20 8:38
# @Author  : goustzhu <goustzhu@gmail.com>
# @File    : ExplainCompany.py
import sys, os, time, datetime
import CommonUtil as CU
import ConstParamClass as CPC

reload(sys)
sys.setdefaultencoding('utf-8')

dev_model='dev'
root_url='http://gov.0731fdc.com'
base_url = '%s/company' % (root_url)
develop_url='%s/develop-company' % (base_url)   # 房地产开发企业
agency_url='%s/agency-company' % (base_url)     # 房地产中介企业
property_url = '%s/property-company' % (base_url)   # 物业服务企业
decoration_url = '%s/decoration-company' % (base_url)   # 装饰装修企业

def explain_company_info(id, mysql, cur, mongo, model='db', size=10):
    '''
    解析公司信息，从MySQL数据库中获取
    :param id:
    :param mysql:
    :param cur:
    :param mongo:
    :return:
    '''
    if model=='db':
        sql2 = "select val1 from %s where key1='%s' and key2='%s'" % (CPC.DB.Table_config, CPC.DB.Key1_Company_info, CPC.DB.Key2_record_cur)
        id = int(mysql.query_one(sql2, cur)[0])
    sql1 = 'select id, company_type, companyid, companyname,num_year, company_url, detail_url from %s where id>%s limit %s' % \
           (CPC.DB.Table_CompanyComplaint, id, size)
    list_record = mysql.query(sql1, cur)
    for record in list_record:
        (id, type, cid,cname, num, curl, durl) = record
        request_url = '%s%s' % (root_url, curl)
        html = CU.request_url_encode(request_url, encode='utf-8')
        soup = CU.parse_html(html)
        tag_dl = soup.find('dl', attrs={'class':'base-info'})
        tags_dd = tag_dl.find_all('dd', attrs={'class':'item'})
        step = 0
        dict_value = {'id':id, 'company_type':type, 'companyid':cid, 'companyname':cname, 'company_url':curl}
        print id, type, cid, num, curl, durl
        for i in range(len(tags_dd)):
            tag_value = tags_dd[i].get_text().strip().replace('\\','').replace('\n', '<br/>')
            tag_value = tag_value[tag_value.find('：')+1:]
            if i==0:
                dict_value['addr'] = tag_value
            elif i==1:
                dict_value['legal_man'] = tag_value
            elif i==2:
                dict_value['bussiness_no'] = tag_value
            elif i==3:
                dict_value['registe_type'] = tag_value
            elif i==4:
                dict_value['registe_money'] = tag_value
            elif i==5:
                dict_value['registe_date'] = tag_value
            elif i==6:
                dict_value['contact_man'] = tag_value
            elif i==7:
                dict_value['contact_phone'] = tag_value
            elif i==8:
                dict_value['cert_no'] = tag_value
            elif i ==9:
                dict_value['cert_institutions'] = tag_value
            elif i==10:
                dict_value['cert_date_begin'] = tag_value
            elif i==11:
                dict_value['cert_date_end'] = tag_value
            elif i==12:
                dict_value['buss_range'] = tag_value
            elif i==13:
                list_link = tags_dd[i].find_all('a')
                list_floor = []
                for link in list_link:
                    dict_link_floor = {}
                    url = link['href']
                    dict_link_floor['url'] = url
                    floor_name = link.get_text().strip()
                    dict_link_floor['floor_name'] = floor_name
                    try:
                        info = CU.request_url_encode(url, encode='GBK')
                        soup = CU.parse_html(info)
                        tag_div = soup.find('div', attrs={'class':'header_nav'}).find('a')
                        floor_url = tag_div['href']
                        floorid = int(floor_url[floor_url.rfind('=')+1:])
                        dict_link_floor['floorid'] = floorid
                        # print '\t',floor_name, url, floor_url, floorid
                    except Exception as e:
                        CU.tolog('explain_company_info', 'exception %s' % (url), e.message)
                    list_floor.append(dict_link_floor)
                dict_value['list_floor'] = list_floor
        mongo.insert_record(dict_value, CPC.DB.Coll_Company_info)
    sql3 = "update %s set val1='%s' where key1='%s' and key2='%s'" % (CPC.DB.Table_config, id, CPC.DB.Key1_Company_info,
                                                                      CPC.DB.Key2_record_cur)
    mysql.execute(sql3, cur)

def explain_develop_info():
    env = CPC.Env(env=dev_model)
    mysql = env.getMySQLClient()
    cur = mysql.get_cursor()
    sum_page = explain_page_by_type(1, mysql, cur)
    for i in range(sum_page):
        explain_develop_info_bypage(i+1, mysql, cur)

def explain_agency_info():
    env = CPC.Env(env=dev_model)
    mysql = env.getMySQLClient()
    cur = mysql.get_cursor()
    sum_page = explain_page_by_type(2, mysql, cur)
    for i in range(sum_page):
        explain_agency_info_bypage(i+1, mysql, cur)

def explain_property_info():
    env = CPC.Env(env=dev_model)
    mysql = env.getMySQLClient()
    cur = mysql.get_cursor()
    sum_page = explain_page_by_type(3, mysql, cur)
    for i in range(sum_page):
        explain_property_info_bypage(i+1, mysql, cur)
        time.sleep(2)

def explain_decoration_info():
    env = CPC.Env(env=dev_model)
    mysql = env.getMySQLClient()
    cur = mysql.get_cursor()
    sum_page = explain_page_by_type(4, mysql, cur)
    for i in range(sum_page):
        explain_decoration_info_bypage(i+1, mysql, cur)

def explain_develop_info_bypage(page, mysql, cur):
    list_info = explain_company_list_info(develop_url, page)
    for info in list_info:
        sql = "insert into %s(company_type,companyid,companyname,level,num_total,num_year,company_url, detail_url) values " \
              "(%s, %s, '%s', '%s', %s, %s, '%s', '%s') on DUPLICATE KEY UPDATE num_total=%s, num_year=%s" % \
              (CPC.DB.Table_CompanyComplaint, 1, info[1], info[0], info[3], info[4], info[5], info[2], info[6], info[4], info[5])
        mysql.execute(sql, cur)
    sql1 = "update %s set val1=%s where key1='%s' and key2='%s'" % \
           (CPC.DB.Table_config, page+1, CPC.DB.Key1_Company_develop, CPC.DB.Key2_page_cur)
    mysql.execute(sql1, cur)

def explain_agency_info_bypage(page, mysql, cur):
    list_info = explain_company_list_info(agency_url, page)
    for info in list_info:
        sql = "insert into %s(company_type,companyid,companyname,level,num_total,num_year,company_url, detail_url) values " \
              "(%s, %s, '%s', '%s', %s, %s, '%s', '%s') on DUPLICATE KEY UPDATE num_total=%s, num_year=%s" % \
              (CPC.DB.Table_CompanyComplaint, 2, info[1], info[0], info[3], info[4], info[5], info[2], info[6], info[4], info[5])
        mysql.execute(sql, cur)
    sql1 = "update %s set val1=%s where key1='%s' and key2='%s'" % \
           (CPC.DB.Table_config, page+1, CPC.DB.Key1_Company_agency, CPC.DB.Key2_page_cur)
    mysql.execute(sql1, cur)

def explain_property_info_bypage(page, mysql, cur):
    list_info = explain_company_list_info(property_url, page)
    for info in list_info:
        sql = "insert into %s(company_type,companyid,companyname,level,num_total,num_year,company_url, detail_url) values " \
              "(%s, %s, '%s', '%s', %s, %s, '%s', '%s') on DUPLICATE KEY UPDATE num_total=%s, num_year=%s" % \
              (CPC.DB.Table_CompanyComplaint, 3, info[1], info[0], info[3], info[4], info[5], info[2], info[6], info[4], info[5])
        mysql.execute(sql, cur)
    sql1 = "update %s set val1=%s where key1='%s' and key2='%s'" % \
           (CPC.DB.Table_config, page+1, CPC.DB.Key1_Company_property, CPC.DB.Key2_page_cur)
    mysql.execute(sql1, cur)

def explain_decoration_info_bypage(page, mysql, cur):
    list_info = explain_company_list_info(decoration_url, page)
    for info in list_info:
        sql = "insert into %s(company_type,companyid,companyname,level,num_total,num_year,company_url, detail_url) values " \
              "(%s, %s, '%s', '%s', %s, %s, '%s', '%s') on DUPLICATE KEY UPDATE num_total=%s, num_year=%s" % \
              (CPC.DB.Table_CompanyComplaint, 4, info[1], info[0], info[3], info[4], info[5], info[2], info[6], info[4], info[5])
        mysql.execute(sql, cur)
    sql1 = "update %s set val1=%s where key1='%s' and key2='%s'" % \
           (CPC.DB.Table_config, page+1, CPC.DB.Key1_Company_decoration, CPC.DB.Key2_page_cur)
    mysql.execute(sql1, cur)

def explain_company_list_info(url, page):
    request_url = url
    if page>1:
        request_url = '%s/%s.html' % (request_url, page*20)
    html = CU.request_url_encode(request_url, encode='utf-8')
    soup = CU.parse_html(html)
    tag_div_page = soup.find('div', attrs={'class':'company-list-cont'})
    tags_dd = tag_div_page.find_all('dd')
    list_record = []
    for dd in tags_dd:
        list_span = dd.find_all('span')
        span1= list_span[0].a
        title = span1.get_text().strip()
        company_url = span1['href']
        company_id = company_url[company_url.find('-')+1:company_url.rfind('.')]
        # print title, company_id, company_url
        level = list_span[1]['title']
        num_total = list_span[2].get_text().strip()
        span3 = list_span[3].a
        num_year = span3.get_text().strip()
        detail_url = span3['href']
        # print level, num_total, num_year, detail_url
        list_record.append((title, company_id, company_url, level, num_total, num_year, detail_url))
    return list_record

def get_number_page(url):
    '''
    获取 总条数以及总页数
    :param url:
    :return:
    '''
    html = CU.request_url_encode(url, encode='utf-8')
    soup = CU.parse_html(html)
    tag_div_page = soup.find('div', attrs={'class':'pagination'})
    page_data = tag_div_page.contents[0]
    num_begin = 2
    num_end = page_data.find(u'条')
    sum_num = int(page_data[num_begin:num_end].strip())
    page_begin = page_data.find(u'共') + 1
    page_end = page_data.rfind(u'页')
    sum_page = int(page_data[page_begin:page_end].strip())
    return (sum_num, sum_page)

def explain_page_by_type(type, mysql, cur, flag=True):
    '''
    解析页面数量，判断是否插入数据库
    :param type:
    :param flag:
    :return:
    '''
    request_url = develop_url
    key1_value = CPC.DB.Key1_Company_develop
    if type==1:
        request_url = develop_url
        key1_value = CPC.DB.Key1_Company_develop
    elif type==2:
        request_url = agency_url
        key1_value = CPC.DB.Key1_Company_agency
    elif type==3:
        request_url = property_url
        key1_value = CPC.DB.Key1_Company_property
    elif type==4:
        request_url = decoration_url
        key1_value = CPC.DB.Key1_Company_decoration
    (sum_num, sum_page) = get_number_page(request_url)
    if flag:
        sql1 = "update %s set val1=%s where key1='%s' and key2='%s'" % (CPC.DB.Table_config, sum_num, key1_value, CPC.DB.Key2_record_sum)
        mysql.execute(sql1, cur)
        sql2 = "update %s set val1=%s where key1='%s' and key2='%s'" % (CPC.DB.Table_config, sum_page, key1_value, CPC.DB.Key2_page_sum)
        mysql.execute(sql2, cur)
    return sum_page

if __name__=='__main__':
    print datetime.datetime.now(), 'begin'.center(80, '-')
    # (sum_num, sum_page) = get_number_page(develop_url)
    # print sum_num, sum_page
    env = CPC.Env(env=dev_model)
    mysql = env.getMySQLClient()
    cur = mysql.get_cursor()
    # explain_page_by_type(1, mysql, cur)
    # explain_develop_info()
    # explain_agency_info()
    # explain_property_info()
    # explain_decoration_info()

    mongo = env.getMongoClient()
    explain_company_info(0, mysql, cur, mongo, model='db', size=3000)

    print datetime.datetime.now(), ' end '.center(80, '-')
