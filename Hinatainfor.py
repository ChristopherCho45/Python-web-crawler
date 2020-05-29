import requests as rq
from bs4 import BeautifulSoup as bs
import time
import re

#通配
url = 'https://www.hinatazaka46.com/s/official/media/list?ima=0000&dy='
#伪装
headers = {'User-Agent':'Chrome/72.0'}

def geturl(url):#获取待搜寻文本
    r = rq.get(url, headers = headers)
    r.encoding = 'UTF-8'
    txt = r.text
    cates = ['shakehands','event','birthday','release']
    for v in range(len(cates)):
        txt = txt.replace(cates[v],'media')
    return txt
#r.status_code

def souping(txt):
    soup = bs(txt,'html.parser')
    return soup

def getdate():#获取年月
    yon = 0
    while(yon != 1):
        date = str(input('请输入六位数的年月代码。示例：202001(2020年01月)\n'))
        rec = re.findall(r'^[0-9]\d{4}[0-9]$',date)#待完善
        if len(rec) != 0:
            yon = 1
        else:
            print('输入有误，请重新输入。\n')
            time.sleep(1)
    return date
da = getdate()

#打印当前时刻
currenttime = str(time.strftime('\n本日程表截至 %Y年%m月%d日 %H时%M分%S秒 有效。',time.localtime()))
print(currenttime)

dayn = []

def dist(soup):#给不同的安排分类存放
    global dayn
    tem = []
    for d in soup.find_all(attrs = {'class':'p-schedule__list-group'}):
        tem.append(d)
    for tems in tem:
        s = bs(str(tems),'html.parser')
        dayt = s.find('span').string
        week = s.find('b').string
        weekc = ['一','二','三','四','五','六']
        weekj = ['月','火','水','木','金','土']
        for cs in range(6):
            if week == weekj[cs]:
                week = weekc[cs]
        count = len(s.find_all(attrs = {'class':'c-schedule__category category_media'}))
        tt = []
        ttem0 = []
        tweek = []
        ttem1 = []
        ttem2 = []
        ttem3 = []
        #事务日期（重复）
        for u in range(count):
            ttem0.append(dayt)
            tweek.append(week)
        #事务类型
        for s0 in s.find_all(attrs = {'class':'c-schedule__category category_media'}):
            kae = ['テレビ','リリース','ラジオ','雑誌','WEB','誕生日','舞台']
            des = ['电视节目','单曲/专辑发售日','电台广播节目','刊物','在线活动','成员生日','舞台剧']
            s0 = s0.string
            for w in range(len(kae)):
                s0 = s0.replace(' ','').replace('\n','').replace(kae[w],des[w])
            ttem1.append(s0)
        #事务时间段
        for s1 in s.find_all(attrs = {'class':'c-schedule__time--list'}):
            if s1.string.replace(' ','').replace('\n','') == '':
                ttem2.append('/')
            else:
                ttem2.append(s1.string.replace(' ','').replace('\n',''))
        #事务内容
        for s2 in s.find_all(attrs = {'class':'c-schedule__text'}):
            ttem3.append(s2.string.replace(' ','').replace('\n',''))

        for k in range(len(ttem0)):
            tt.append([ttem0[k],tweek[k],ttem1[k],ttem2[k],ttem3[k]])
        dayn.append(tt)

try:
    dist(souping(geturl(url+da)))
except:
    print('运行失败！程序即将退出')
    time.sleep(2)
    exit(1)

#dayn:列表 dayn[items] 列表 dayn[items][itemss] 列表 dayn[i][j][1]

if len(dayn) == 0:
    print('您所查询的时段： {}年{}月 暂无计划在册的事务！'.format(da[:4],da[4:]))
else:      
    #准备打印安排所属的年月
    datestr = '{}年{}月 日程安排如下：'.format(da[:4],da[4:])
    print('\n' + datestr)
    print('*时间为24时以后的，表示标注当天次日的凌晨时分\n')
    for i in range(len(dayn)):
        for j in range(len(dayn[i])):
            consul = '日期：{}月{}日 星期{}\n事务类型：{} \n时间：{} \n内容：{}\n'.format(da[4:],str(dayn[i][j][0]).zfill(2),dayn[i][j][1],dayn[i][j][2],dayn[i][j][3],dayn[i][j][4])
            print(consul)
