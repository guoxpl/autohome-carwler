# _*_ coding: utf-8 _*_
# author: guoxiaopolu

import urllib2
import sys
import json
from BeautifulSoup import *

reload(sys)
sys.setdefaultencoding('utf-8')

# 传入汽车所属url与所属国家，爬取指定url的汽车信息
def findcar(url, countryname):
    try:
        c = urllib2.urlopen(url)
    except:
        print "Could not open %s" % url
        return 0

    content = c.read()
    soup = BeautifulSoup(content)

    t = soup('script')

    if len(t) >= 7:
        script = t[7].string

        list = script.split('var ')

        var1 = list[3].strip()

        var2 = var1[9:-1]
        lists = []
        try:
            doc = json.loads(var2)
            pingpai = doc['result']['paramtypeitems'][0]['paramitems'][2]['valueitems']
            leixing = doc['result']['paramtypeitems'][0]['paramitems'][0]['valueitems']
            cheshengjiegou = doc['result']['paramtypeitems'][0]['paramitems'][7]['valueitems']
            zuoweishu = doc['result']['paramtypeitems'][1]['paramitems'][10]['valueitems']
            jibie = doc['result']['paramtypeitems'][0]['paramitems'][3]['valueitems']
            changshang = doc['result']['paramtypeitems'][0]['paramitems'][2]['valueitems']
            lists = zip(leixing, pingpai, cheshengjiegou, zuoweishu, jibie, changshang)
            print lists
        except:
            print 'Could not load  configure of the car!!!'

        print4txt(lists, countryname)

    else:
        print 'Could not find the car'
        return None

# 通过指定国家id，来获取对应页面的所有汽车id
def fromcountryid_getcarid(countryid):
    url = 'http://www.autohome.com.cn/car/%s/' % countryid
    try:
        c = urllib2.urlopen(url)
    except:
        print "Could not open %s" % url
        return None

    content = c.read()
    soup = BeautifulSoup(content)
	
    iditems = soup.findAll('li')

    ids = []
    for iditem in iditems:
        if 'id' in str(iditem):
            try:
                id = iditem['id'][1:]
                print 'index id of the car %s!!' % id
                ids.append(id)
            except:
                continue
    return ids

# 将获取的汽车信息解析，并写入一个文档中
def print4txt(lists, countryname):
    out = file('car4country.txt', 'a')
    if lists != None and lists != []:
        for list in lists:
            out.write('%s' % (countryname))
            temp = list[0]['value']
            idx = temp.find(u'款') + 1
            out.write('\t%s' % (temp[:idx]))
            out.write('\t%s' % (temp[idx + 1:]))
			
            for item in list[1:]:
                out.write('\t%s' % item['value'])
            out.write('\n')

# 通过执行getit（）函数，获取十三个国家所有汽车品牌的信息
def getit():
    countryids = ['0_0-0.0_0.0-0-0-0-0-0-1-0-0', '0_0-0.0_0.0-0-0-0-0-0-2-0-0', '0_0-0.0_0.0-0-0-0-0-0-3-0-0',
        '0_0-0.0_0.0-0-0-0-0-0-4-0-0', '0_0-0.0_0.0-0-0-0-0-0-5-0-0', '0_0-0.0_0.0-0-0-0-0-0-6-0-0', '0_0-0.0_0.0-0-0-0-0-0-7-0-0',
         '0_0-0.0_0.0-0-0-0-0-0-8-0-0', '0_0-0.0_0.0-0-0-0-0-0-9-0-0', '0_0-0.0_0.0-0-0-0-0-0-10-0-0', '0_0-0.0_0.0-0-0-0-0-0-11-0-0', '0_0-0.0_0.0-0-0-0-0-0-12-0-0']

    countrynames = ['中国', '德国', '日本', '美国', '韩国', '法国',
                   '英国', '意大利', '瑞典', '荷兰', '捷克', '西班牙']

    for i, countryid in enumerate(countryids):
        countryname = countrynames[i]
        print 'Now get the country: %s' % countryname
        for id in fromcountryid_getcarid(countryid):
            url = "http://car.autohome.com.cn/config/series/%s.html" % id
            print 'Indexing the url %s' % url
            findcar(url, countryname)
