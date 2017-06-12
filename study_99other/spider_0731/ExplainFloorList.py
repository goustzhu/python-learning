#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2017/6/10 12:41
# @Author  : goustzhu <goustzhu@gmail.com>
# @File    : ExplainFloorList.py
import sys, os, time, datetime, traceback
import CommonUtil as CU
import ConstParamClass as CPC

reload(sys)
sys.setdefaultencoding('utf-8')

dev_model='dev'
base_url = 'http://floor.0731fdc.com/'


# main process
def explain_floor_list(model='db', page_num=0, page_end=1):
    '''
    解析所有页面数据(从最后页面开始爬取)
    从数据库读取或者页面中读取页面数量
    :param model:       db:数据库中读取, page: 页面解析获取
    :param page_num:    获取页面数量
    :param page_end:    页面结束数
    :return:
    '''
    env = CPC.Env(env=model)
    mysql = env.getMySQLClient()
    cur = mysql.get_cursor()
    mongo = env.getMongoClient()
    page_begin = 1
    if model=='db':
        sql1 = "select val1 from %s where key1='%s' and key2='%s'" % \
               (CPC.DB.Table_config, CPC.DB.Key1_Floor_List, CPC.DB.key2_Floor_List_page_cur)
        res1 = mysql.query_one(sql1, cur)
        page_begin = int(res1[0])
        # print model, res1, page_begin
        CU.tolog('explain_floor_list', 'model=%s' % (model), 'page_begin=%s' % (page_begin))
    elif model=='page':
        (num, page_begin) = explain_floor_list_page_num(True)
        # print model, num, page_begin
        CU.tolog('explain_floor_list', 'model=%s' % (model), 'page_begin=%s' % (page_begin))
    page_size = 1
    if page_num>0:
        if page_begin>page_num: page_size=page_num
        else: page_size = page_begin
    elif page_end>0: page_size = page_begin-page_end+1
    else: page_size = page_begin
    # print page_begin, page_size, page_num, page_end
    CU.tolog('explain_floor_list', 'page_begin=%s' % (page_begin), 'page_size=%s' %(page_size))
    for i in range(page_size):
        page = page_begin - i
        explain_floor_list_page(page, mysql, cur, mongo)

def explain_floor_list_page(page, mysql, cur, mongo):
    '''
    解析楼盘发证情况，只有page=1时，解析页数
        并且当flag=True时，会将页数update到MySQL数据库中
    :param page:
    :param flag:
    :return:
    '''
    page_param = 'page=%s&tsort=tdesc' % (page)
    html = CU.request_url('%s?%s' % (base_url, page_param))
    CU.tolog('explain_floor_list_page', base_url, 'page=%s' % (page))
    # mongo = CPC.Env(env=dev_model).getMongoClient()
    # mysql = MySQLClient(dev='dev')
    # cur = mysql.get_cursor()
    list_floor = explain_floor_list_list(html, page)
    if len(list_floor)>0:
        for floor_info in list_floor:
            mongo.insert_record(floor_info, CPC.DB.Coll_floor_list)
        # sql = 'insert into %s(floorid,floorname,buildno,pre_certno,cert_time,detail) values ' % (CPC.DB.Table_Fl)
        # step = 0
        # for floor in list_floor:
        #     if step>0:
        #         sql += ','
        #     (floor_id, floor_name, build_id, build_cert, build_cert_time) = floor
        #     sql += "(%s, '%s', '%s', '%s', '%s', '%s')" % (floor_id, floor_name, build_id, build_cert, build_cert_time, page)
        #     step += 1
        # mysql.execute(sql, cur)
    sql1 = "update %s set val1=%s where key1='%s' and key2='%s'" % (CPC.DB.Table_config,
            page-1, CPC.DB.Key1_Floor_List, CPC.DB.key2_Build_page_cur)
    mysql.execute(sql1, cur)
    return list_floor

def explain_floor_list_page_num(flag=False):
    '''
    解析条数以及页数
    :param flag:
    :return:
    '''
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
                sum_page, CPC.DB.Key1_Floor_List, CPC.DB.key2_Floor_List_page_sum, CPC.DB.key2_Floor_List_page_cur)
        CU.tolog('explain_floor_list', 'mysql execute', sql1)
        mysql.execute(sql1, cur)
        sql2 = "update %s set val1='%s' where key1='%s' and key2='%s'" % (CPC.DB.Table_config,
               sum_num, CPC.DB.Key1_Floor_List, CPC.DB.key2_Floor_List_record_sum)
        CU.tolog('explain_floor_list', 'mysql execute', sql2)
        mysql.execute(sql2, cur)
    return (sum_num, sum_page)

def explain_floor_list_list(html, page):
    '''
    获取楼盘列表基本信息，
    :param html:
    :return:
    '''
    table_floor = CU.parser_html_by_class_one(html, 'ul', 'w100 zxslb-list')
    # print table_floor
    list_floor = []
    for li in table_floor.find_all('li', class_='w100'):
        try:
            div_tag = li.find('div', class_='zxslb-right')
            div_opa = li.find('span', class_='opa')
            if div_opa is not None and len(div_opa)>0:
                div_floor_name = div_tag.find('div', class_='w100 info-left over-h')
                div_floor_price = div_tag.find('div', class_='fr info-right-price test-ell')
                div_floor_click = div_tag.find('div', class_='zxslb-right-hit')
                click_detail = ''
                for p_rec in div_floor_click.find_all('p'):
                    click_detail += ' '+p_rec.get_text().strip()
                click_detail = click_detail.strip()

            else:
                div_floor_name = div_tag.find('div', class_='w100 info-left ')
                div_price_click = div_tag.find('div', class_='zxslb-right-price fr')
                div_floor_price = div_price_click.find('p', class_='price-info test-ell')
                div_click = div_price_click.find_all('p')[1]
                click_detail = div_click.get_text().strip()
            div_tags_list = li.find('div', class_='w100 info-con')
            list_zs = ''
            list_pt = ''
            list_ot = ''
            for p_tag in div_tags_list.find_all('span'):
                class_value = p_tag.get('class')
                # print class_value
                if class_value is not None:
                    if class_value[0]=='zs':
                        list_zs = p_tag.get_text().strip()
                    elif class_value[0]=='pt':
                        list_pt = p_tag.get_text().strip()
                else:
                    list_ot += ' '+p_tag.get_text().strip()

            # div_left = div_tag.find('div', class_='w100 zxslb-right-info')
            # div_right = div_tag.find('div', class_='zxslb-right-hit')
            # div_left_floor = div_floor_name.find('div', class_='w100 info-left over-h')
            floor_a = div_floor_name.h2.a
            floorname = floor_a.contents[0]
            detail_url = floor_a['href']
            floorid = int(detail_url[detail_url.rindex('/')+1:detail_url.rindex('.')])

            floor_addr = div_floor_name.p.span
            address = floor_addr.contents[0]
            # div_tag = div_left.find('div', class_='fr info-right-price test-ell')
            price_detail = div_floor_price.get_text().strip()
            div_price = div_floor_price.find('font')
            if div_price is None:
                price_value = u'待定'
            else:
                price_value = div_floor_price.font.get_text().strip()
            # print floorid, floorname, detail_url, address, price_detail
            # if price_detail.find(u'￥')>=0 and price_detail.find(u'元')>=0:
            #     price_value = price_detail[price_detail.index(u'￥')+1: price_detail.index(u'元')]
            #     if price_value.find(u'起')>=0:
            #         price_value = price_value[:price_value.find(u'起')]
            #     if price_value.find('-')>=0:
            #         price_value = price_value[:price_value.find('-')]
            #     if price_value.find(u'（')>=0:
            #         price_value = price_value[:price_value.find(u'（')]
            #     if price_value.find('(')>=0:
            #         price_value = price_value[:price_value.find('(')]
            #     price_value = int(price_value)
            # print '\t', price_detail
            # print '\t', price_value
            # print '\t', click_detail
            # print '\t', 'zs', list_zs
            # print '\t', 'pt', list_pt
            # print '\t', 'ot', list_ot.strip()
            dict_floor =  {'floorid':floorid, 'floorname':floorname, 'detail_url':detail_url, 'address':address,
                           'price_detail':price_detail, 'price':price_value, 'click_detail': click_detail,
                           'tag_onsale':list_zs, 'tag_type':list_pt, 'tag_advantage':list_ot.split(' '), 'page':page}
            list_floor.append(dict_floor)
            # print div_tag
        except Exception as e:
            print 'Exception', floorname, floorid, e.message
            print traceback.format_exc()
    return list_floor

if __name__=='__main__':
    print datetime.datetime.now(), 'begin'.center(80, '-')
    # (sum_num, sum_page) = explain_floor_list_page_num(True)
    # print sum_num, sum_page

    # page_param = 'page=%s&tsort=tdesc' % (2)
    # print '%s?%s' % (base_url, page_param)
    # html = CU.request_url('%s?%s' % (base_url, page_param))
    # # print html
    # print '*'*100
    # list_floor = explain_floor_list_list(html)
    # for record in list_floor:
    #     print record

    explain_floor_list('db', page_num=129)
    print datetime.datetime.now(), ' end '.center(80, '-')