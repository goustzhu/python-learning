#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2017/6/14 23:04
# @Author  : goustzhu <goustzhu@gmail.com>
# @File    : ExplainFloorDetail.py
import sys, os, time, datetime
import CommonUtil as CU
import ConstParamClass as CPC

reload(sys)
sys.setdefaultencoding('utf-8')

dev_model='dev'
base_url='http://floor.0731fdc.com/content'
detail_url='http://floor.0731fdc.com/?action=detail&id='
news_url='http://floor.0731fdc.com/?action=news&id='

def get_list_floorid(mysql, cur, mongo, model='db', num_begin=0, list_size=10):
    '''
    获取
    :param model:
    :return:
    '''
    if model=='db':
        sql1 = "select val1 from %s where key1='%s' and key2='%s'" % (
            CPC.DB.Table_config, CPC.DB.Key1_Floor_Info, CPC.DB.key2_Floor_info_record_cur)
        res1 = mysql.query_one(sql1, cur)
        num_begin = int(res1[0])
    if num_begin > 0:
        list_records = mongo.conn.get_collection(CPC.DB.Coll_floor_list).find(
                {}, {'floorid':1,'_id':0}).skip(num_begin).limit(list_size)
    else:
        list_records = mongo.conn.get_collection(CPC.DB.Coll_floor_list).find(
                {}, {'floorid':1,'_id':0}).limit(list_size)
    list_floorids = []
    for record in list_records:
        # print record
        floorid = record['floorid']
        list_floorids.append(floorid)
    CU.tolog('get_list_floorid', ','.join(map(str, list_floorids)))
    return list_floorids

def explain_floor_list(list_floorids, mysql, cur, mongo):
    '''
    解析列表
    :param list_floorid:
    :param mysql:
    :param cur:
    :param mongo:
    :return:
    '''
    step = 0
    num_step = len(list_floorids)
    for floorid in list_floorids:
        step += 1
        CU.tolog('explain_floor_list', 'step=%s/%s' %(step, num_step), 'floorid=%s' %(floorid))
        explain_floor_info(floorid, mysql=mysql, cur=cur, mongo=mongo)
        if step % 12 ==0:
            CU.tolog('explain_floor_list', 'sleep 20s...', step)
            time.sleep(20)
            CU.tolog('explain_floor_list', 'sleep over.', step)
    sql2 = "update %s set val1 = cast(CAST(val1 as SIGNED)+%s as CHAR) where key1='%s' and key2='%s'" % \
           (CPC.DB.Table_config, len(list_floorids), CPC.DB.Key1_Floor_Info, CPC.DB.key2_Floor_info_record_cur)
    CU.tolog('explain_floor_list', sql2)
    mysql.execute(sql2, cur)

def explain_floor_info(floorid, mysql, cur, mongo):
    '''
    解析楼盘信息
    :param floorid:
    :param mysql:
    :param cur:
    :param mongo:
    :return:
    '''
    CU.tolog('explain_floor_info', floorid)
    fc = explain_floor_content(floorid)
    fd = explain_floor_detail(floorid)
    fn = explain_floor_news(floorid)

    CU.tolog('explain_floor_info', floorid, 'step1: floor base...')
    sql1 = "insert IGNORE into %s(floorid, floorname, tag_onsale, tag_type, tag_advantage, num_visits, info_update_time, " \
           "price_detail, open_date, area_addr, sum_area, sum_area_building, rate_area, rate_greening, price_property, " \
           "company_property, company_developer, floor_addr, traffic_condition) values (%s, '%s', '%s', '%s', '%s', " \
           "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
           (CPC.DB.Table_FLoorBase, floorid, fc[1], fc[2], fc[3], fc[4], fc[5], fc[6], fc[7], fc[8], fc[9], fc[10],
            fc[11], fc[12], fc[13], fc[14], fc[15], fc[16], fc[17], fc[18])
    mysql.execute(sql1, cur)
    es = fc[19]
    ts = fc[20]
    ev = fc[21]
    sql1_1 = "insert IGNORE into %s(floorid,flooridname,score_brand,score_unit,score_area,score_build,score_community," \
             "score_traffic,score_live,score_property,score_summary,export_reviews) values (%s, '%s', %s, %s, %s," \
             "%s, %s, %s, %s, %s, %s, '%s')" % (CPC.DB.Table_FloorExport, floorid, fc[1], es[0], es[1], es[2],es[3],
                                              es[4],es[5],es[6],es[7], ts, ev)
    CU.tolog('explain_floor_info', floorid, 'step2: floor detail...')
    mysql.execute(sql1_1, cur)
    sql2 = "insert IGNORE into %s(floorid,floorname,price_detail,primary_type,area_addr,fit_status,num_set,finish_date,num_car,open_date," \
           "sum_area_building,sum_area,rate_area,rate_green,design_unit,price_property,company_property,company_project," \
           "company_developer,floor_addr,traffic_condition,round_env,project_info) " \
           "values (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', " \
           "'%s', '%s', '%s','%s', '%s', '%s', '%s')" % (CPC.DB.Table_FloorDetail, floorid, fc[1], fd[0], fd[1], fd[2], fd[3],
                                                   fd[4], fd[5], fd[6], fd[7], fd[8], fd[9], fd[10], fd[11], fd[12],
                                                   fd[13], fd[14], fd[15], fd[16], fd[17], fd[18], fd[19], fd[20])
    # print sql2
    mysql.execute(sql2, cur)
    list_same_area = fd[21]
    list_same_price = fd[22]
    # print list_same_area, list_same_price
    for area in list_same_area:
        sql2_t = 'insert into %s(floorid, type, similar_floorid) values (%s, 2, %s)' % \
                 (CPC.DB.Table_FloorSimilar, floorid, area)
        mysql.execute(sql2_t, cur)
    for price in list_same_price:
        sql2_p = 'insert into %s(floorid, type, similar_floorid) values (%s, 1, %s)' % \
                 (CPC.DB.Table_FloorSimilar, floorid, price)
        mysql.execute(sql2_p, cur)
    CU.tolog('explain_floor_info', floorid, 'step3: floor news...')
    for news in fn:
        record = {'floorid':floorid, 'floorname':fc[1], 'title':news[2], 'publish_date':news[1], 'info':news[2]}
        mongo.insert_record(record, CPC.DB.Coll_floor_news)

def explain_floor_content(floorid):
    '''
    29657.shtml
    解析楼盘基本内容
        楼盘名称、在售状态、标签列表、到访人数、在售套数、
        参考价格、开盘时间、所属区域、总占地面积、总建筑面积、容积率、绿化率、物业费、物业管理、开发商、楼盘地址、交通状况
    :param floorid:
    :return:
    '''
    request_url = '%s/%s.shtml' % (base_url, floorid)
    html = CU.request_url_encode(request_url)
    soup = CU.parse_html(html)
    # base info
    base_info = soup.find('div', class_='floor_info')
    title_info = base_info.find('div', attrs={'class':'info_title'})
    floorname = title_info.h2.get_text().strip()
    tag_base = title_info.find('div', attrs={'class':'i_con'})
    tag_onsale = tag_base.find('span', attrs={'class':'i1'})
    onsale_tags = tag_onsale.get_text().strip()
    tag_type = tag_base.find('span', attrs={'class':'i2'})
    type_tags = tag_type.get_text().strip()
    tag_adv = title_info.find('div', attrs={'class':'info_type'})
    list_adv_tags = []
    if tag_adv :
        for span in tag_adv.find_all('span'):
            list_adv_tags.append(span.get_text().strip())
    adv_tags = ' '.join(list_adv_tags)
    # print floorname, onsale_tags, type_tags, adv_tags
    info_update = base_info.find('div', attrs={'class':'info_r'}).get_text().strip().split('\n')
    visits_num = info_update_time = ''
    for i in range(len(info_update)):
        value = info_update[i].strip()
        str_value = value[value.find(u'：')+1:]
        if i == 0:
            visits_num = str_value
        elif i == 1:
            info_update_time = str_value
    content_info = soup.find('div', attrs={'class':'floor-fr mt12'}).find('div', attrs={'class':'info'})
    price_info = content_info.find('p', attrs={'class':'price'}).get_text().strip()
    price_value = price_info[price_info.find(u'：')+1:]
    # print visits_num, info_update_time, price_value
    list_p = content_info.find_all('p')[1:]
    step = 0
    open_date = area_addr = sum_area = sum_area_building = ''
    rate_area = rate_greening = price_property = company_property = ''
    company_developer = floor_addr = traffic_condition = ''
    for p in list_p:
        step += 1
        if step < 5:
            span_list = p.find_all('span')
            span_value = span_list[0].get_text().strip().replace('\\','')
            span_value2 = span_list[1].get_text().strip().replace('\\','')
            value1 = span_value[span_value.find(u'：')+1:]
            value2 = span_value2[span_value2.find(u'：')+1:]
            if step == 1:
                open_date = value1
                area_addr = value2
            elif step == 2:
                sum_area = value1
                sum_area_building = value2
            elif step == 3:
                rate_area = value1
                rate_greening = value2
            elif step == 4:
                price_property = value1
                company_property = value2
        else:
            p_value = p.get_text().strip().replace('\\','')
            value = p_value[p_value.find(u'：')+1:]
            if step == 5:
                company_developer = value
            elif step == 6:
                floor_addr = value
            elif step == 7:
                traffic_condition = value
    # print open_date, area_addr, sum_area, sum_area_building
    # print rate_area, rate_greening, price_property, company_property
    # print company_developer
    # print floor_addr
    # print traffic_condition

    div_export_tag = soup.find('div', attrs={'class':'pl-left mt12'})
    div_export_pt_tag = div_export_tag.find('div', attrs={'class':'pl-t'})
    div_export_pb_tag = div_export_tag.find('div', attrs={'class':'pl-b'})
    list_li_tag = div_export_pt_tag.ul.find_all('li')
    list_score_value = []
    for li_tag in list_li_tag:
        pf_value = int(li_tag.find('div', attrs={'class':'right'}).get_text().strip())
        list_score_value.append(pf_value)
    total_value = div_export_pt_tag.find('div', attrs={'class':'total'}).find('font').get_text().strip()[:-1]
    total_score = 0.0
    try:
        total_score = float(total_value)
    except Exception as e:
        pass
    # print total_score
    export_value = div_export_pb_tag.p.get_text().strip()
    # print list_score_value
    # print total_score, export_value
    return (floorid, floorname, onsale_tags, type_tags, adv_tags, visits_num, info_update_time, price_value, open_date,
            area_addr, sum_area, sum_area_building, rate_area, rate_greening, price_property, company_property,
            company_developer, floor_addr, traffic_condition, list_score_value, total_score, export_value)

def explain_floor_detail(floorid):
    '''
    解析楼盘详细信息
    price_detail, primary_type, area_addr, fit_status, num_set, finish_date, num_car, open_date
    sum_area_building, sum_area, rate_area, rate_green, design_unit, price_property, company_property
    company_project, company_developer, floor_addr, traffic_condition, round_env, project_info
    :param floorid:
    :return:
    '''
    request_url = '%s%s' % (detail_url, floorid)
    html = CU.request_url_encode(request_url)
    soup = CU.parse_html(html)
    price_detail = primary_type = area_addr = fit_status = num_set = finish_date = num_car = open_date = ''
    sum_area_building = sum_area = rate_area = rate_green = design_unit = price_property = company_property = ''
    company_project = company_developer = floor_addr = traffic_condition = round_env = project_info = ''
    div_base_info = soup.find('div', attrs={'class':'project mt12'})
    list_tr_tag = div_base_info.find_all('tr')
    for i in range(len(list_tr_tag)):
        list_td_tag = list_tr_tag[i].find_all('td')
        if i < 8:
            tag_v1 = list_td_tag[1].get_text().strip().replace('\r\n', '<br/>').replace('\\','')
            tag_v2 = list_td_tag[3].get_text().strip().replace('\r\n', '<br/>').replace('\\','')
            if i ==0:
                price_detail = tag_v1
                primary_type = tag_v2
            elif i==1:
                area_addr = tag_v1
                fit_status = tag_v2
            elif i==2:
                num_set = tag_v1
                finish_date = tag_v2
            elif i==3:
                num_car = tag_v1
                open_date = tag_v2
            elif i==4:
                sum_area_building=tag_v1
                sum_area = tag_v2
            elif i==5:
                rate_area = tag_v1
                rate_green = tag_v2
            elif i==6:
                design_unit = tag_v1
                price_property = tag_v2
            elif i==7:
                company_property = tag_v1
                company_project = tag_v2
        else:
            tag_value = list_td_tag[1].get_text().strip().replace('\r\n', '<br/>').replace('\\','')
            if i==8:
                company_developer = tag_value
            elif i==9:
                floor_addr = tag_value
            elif i==10:
                traffic_condition = tag_value
    tag_info = soup.find_all('div', attrs={'class':'xm-info'})
    env_value = tag_info[0].get_text().strip()
    round_env = env_value.replace('\r\n', '<br>').replace('\'', '').replace('\n', '')
    project_value = tag_info[1].get_text().strip()
    project_info = project_value.replace('\r\n', '<br>').replace('\'', '').replace('\n', '')
    # print price_detail, primary_type, area_addr, fit_status, num_set, finish_date, num_car, open_date
    # print sum_area_building, sum_area, rate_area, rate_green, design_unit, price_property, company_property
    # print company_project, company_developer, floor_addr, traffic_condition
    # print round_env
    # print project_info

    list_same_area = []
    list_same_price = []
    tag_fr_news = soup.find('div', attrs={'class':'fr_news'})
    list_tags = tag_fr_news.find_all('div', attrs={'class':'floor_phb'})
    for i in range(len(list_tags)):
        list_floor_tmp = []
        tags_ul = list_tags[i].find('ul', attrs={'class':'phb-list'})
        list_li_tags = tags_ul.find_all('li')
        for tags_li in list_li_tags:
            url = tags_li.a['href']
            similar_floorid = url[url.rfind('=')+1:]
            list_floor_tmp.append(int(similar_floorid))
        if i == 0:
            list_same_price.extend(list_floor_tmp)
        elif i==1:
            list_same_area.extend(list_floor_tmp)
    # print list_same_area
    # print list_same_price
    return (price_detail, primary_type, area_addr, fit_status, num_set, finish_date, num_car, open_date,
            sum_area_building, sum_area, rate_area, rate_green, design_unit, price_property, company_property,
            company_project, company_developer, floor_addr, traffic_condition, round_env, project_info,
            list_same_area, list_same_price)

def explain_floor_news(floorid):
    '''
    解析楼盘快讯资料
    :param floorid:
    :return:
    '''
    request_url = '%s%s' % (news_url, floorid)
    html = CU.request_url_encode(request_url)
    soup = CU.parse_html(html)
    (sum_num, sum_page) = explain_floor_news_page(soup.find('ul', attrs={'class':'pageno'}))
    list_fast_news = []
    for i in range(sum_page):
        list_news = explain_floor_news_by_page(floorid, i+1)
        list_fast_news.extend(list_news)
    return list_fast_news

def explain_floor_news_by_page(floorid, page):
    '''
    按页数解析楼盘快讯
    :param floorid:
    :param page:
    :return:
    '''
    request_url = '%s%s&page=%s' % (news_url, floorid, page)
    html = CU.request_url_encode(request_url)
    soup = CU.parse_html(html)
    ul_tag = soup.find('ul', attrs={'class':'fast_news'})
    list_fast_news = []
    for li in ul_tag.find_all('li'):
        # print li
        news_title = li.div.find('h2').get_text().strip().replace('\r\n', '<br/>')
        news_date = li.div.find('span').get_text().strip().replace('\r\n', '<br/>')
        news_info = li.p.get_text().strip().replace('\r\n', '<br/>')
        list_fast_news.append((news_title, news_date, news_info))
    return list_fast_news

def explain_floor_news_page(div_page):
    '''
    解析楼盘快讯中条数，及页数
    :param div_page:
    :return:
    '''
    page_data = div_page.contents[0]
    # print page_data
    num_begin = 2
    num_end = page_data.find(u'条')
    sum_num = int(page_data[num_begin:num_end])
    page_begin = page_data.find(u'共') + 1
    page_end = page_data.rfind(u'页')
    sum_page = int(page_data[page_begin:page_end])
    return (sum_num, sum_page)

if __name__=='__main__':
    print datetime.datetime.now(), 'begin'.center(80, '-')
    # floorid = '29657'
    # explain_floor_content(floorid)
    # explain_floor_detail(floorid)
    # list_news = explain_floor_news(floorid)
    # for news in list_news:
    #     print '\n\t'.join(news)

    env = CPC.Env(env=dev_model)
    mysql = env.getMySQLClient()
    cur = mysql.get_cursor()
    mongo = env.getMongoClient()
    list_floorids = get_list_floorid(mysql, cur, mongo, model='db', list_size=100)
    # print ' '.join(map(str, list_floorids))
    explain_floor_list(list_floorids, mysql=mysql, cur=cur, mongo=mongo)

    print datetime.datetime.now(), ' end '.center(80, '-')