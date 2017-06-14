#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2017/6/13 22:13
# @Author  : goustzhu <goustzhu@gmail.com>
# @File    : ExplainFloorOpen.py
import sys, os, time, datetime, traceback
import CommonUtil as CU
import ConstParamClass as CPC

reload(sys)
sys.setdefaultencoding('utf-8')

dev_model='dev'
base_url = 'http://home.0731fdc.com/dbear/cindex.php'

def explain_open_floor(start_page=150, model='db', page_num=10):
    env = CPC.Env(env=dev_model)
    mysql = env.getMySQLClient()
    cur = mysql.get_cursor()
    mongo = env.getMongoClient()
    if model == 'db':
        sql1 = "select val1 from %s where key1='%s' and key2='%s'" % \
               (CPC.DB.Table_config, CPC.DB.Key1_Floor_Open, CPC.DB.key2_Floor_Open_Itemid_cur)
        res1 = mysql.query_one(sql1, cur)
        start_page = int(res1[0])
    (next_page, list_pages) = explain_open_floor_item(start_page, page_num)
    for page in list_pages:
        explain_open_floor_page(page, mongo)
    sql1 = "update %s set val1=%s where key1='%s' and key2='%s'" % (CPC.DB.Table_config,
            page-1, CPC.DB.Key1_Floor_Open, CPC.DB.key2_Floor_Open_Itemid_cur)
    mysql.execute(sql1, cur)

def explain_open_floor_page(page, mongo):
    list_items = explain_open_floor_list(page)
    if list_items and len(list_items)>0:
        for items in list_items:
            mongo.insert_record(items, CPC.DB.Coll_floor_open)

def explain_open_floor_list(page):
    '''
    解析页面
    :param page:
    :return:
    '''
    page_url = '%s?item_id=%s' % (base_url, page)
    html = CU.request_url_encode(page_url)
    tag_html = CU.parse_html(html)
    title = tag_html.find('title').get_text().strip()
    print page, title
    div_list = tag_html.find('div', class_='cnt')
    list_li = div_list.find_all('li')
    list_items = []
    for li in list_li:
        try:
            link_more = li.find('a', class_='more')
            floor_url = link_more['href']
            floor_id = floor_url[floor_url.rfind('=')+1:]
            floor_name = link_more.get_text().strip()
            # print floor_id, floor_url, floor_name
            td_tag_list = li.find_all('td', attrs={'colspan':'2', 'height':'20'})[:4]
            address = ''; telephone=''; price=''; open_date=''
            for i in range(len(td_tag_list)):
                tag_value = td_tag_list[i].get_text().strip()
                if i ==0:
                    address = tag_value
                elif i==1:
                    telephone = tag_value
                elif i==2:
                    price = tag_value
                elif i==3:
                    open_date = tag_value
            # telephone = td_tag_list[1].get_text().strip()
            # price = td_tag_list[2].get_text().strip()
            # open_date = td_tag_list[3].get_text().strip()
            # print floor_name, address, telephone, price, open_date
            dict_floor = {'floorid': int(floor_id), 'floorname':floor_name, 'floor_url':floor_url, 'item_id':page,
                          'item_title': title, 'address': address, 'telephone': telephone, 'price':price, 'open_date':open_date}
            list_items.append(dict_floor)
        except Exception as e:
            print 'Exception', e.message, link_more
            print traceback.format_exc()
    return list_items

def explain_open_floor_item(page=150, size=10):
    '''
    解析所有页面数据
    :param page:
    :return:
    '''
    html = CU.request_url('%s?item_id=%s' % (base_url, page))
    item_select_tag = CU.parser_html_by_attrs(html, 'select', attrs={'id':'item_id', 'name':'item_id'})
    list_itemid = []
    next_itemid = 0
    list_item_tags = item_select_tag.find_all('option')
    for option in list_item_tags:
        item_value = int(option['value'])
        if page>=item_value:
            if len(list_itemid)<size:
                list_itemid.append(item_value)
            elif len(list_itemid)==size:
                next_itemid = item_value
                break
        # print item_value
    # print item_select_tag
    return (next_itemid, list_itemid)

if __name__=='__main__':
    print datetime.datetime.now(), 'begin'.center(80, '-')
    # (next_itemid, list_itemid) = explain_open_floor_item(115)
    # print  next_itemid
    # print list_itemid
    # list_items = explain_open_floor_list(131)
    # for item in list_items:
    #     print item
    explain_open_floor(model='db', page_num=10)
    print datetime.datetime.now(), ' end '.center(80, '-')