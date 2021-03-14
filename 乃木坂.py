import requests as rq
from bs4 import BeautifulSoup as bs
import time
import xlwt

url = 'http://www.nogizaka46.com/member/'
#url_2 = 'http://www.nogizaka46.com/member/detail/'

#3_48

#开始计时
start = time.perf_counter()
print('现在时刻：{}，程序开始运行。'.format(str(time.strftime("%Y{0}%m{1}%d{2} %H{3}%M{4}%S{5}",time.localtime()).format("年","月","日","时","分","秒"))))

headers = {'User-Agent':'Chrome/72.0'}
r = rq.get(url, headers = headers)
if r.status_code == 200:
    r.encoding = 'UTF-8'
    text = r.text
else:
    print('拒绝访问。')
    exit()
soup = bs(text,'html.parser')
memberbox = []
for tags in soup.find_all('img'):
    memberbox.append(tags)

newbox = []
for i in range(3,49):
    newbox.append(memberbox[i])

#infor = []
name = []
enname = []
hiragana = []
birthday = []
constellation = []
bloodtype = []
height = []

for j in range(len(newbox)):
    po = str(newbox[j]).split(' ')[3].replace('class=\"','').replace(" ","").replace('\"','')
    nurl = url + 'detail/' + po + '.php'
    #print(nurl)
    enname.append(po)
    #imageurl = 'https://img.nogizaka46.com/www/member/img/'+ po + '_prof.jpg'
    nr = rq.get(nurl,headers = headers)
    if nr.status_code == 200:
        nr.encoding = 'UTF-8'
        te = nr.text
    else:
        #print('出现错误。')
        #exit()
        continue
    o = []
    so = bs(te,'html.parser')
    for u in so.find_all('dd'):
        o.append(u)
    birthday.append(o[0].string)
    bloodtype.append(o[1].string)
    constellation.append(o[2].string)
    height.append(o[3].string)
    native = str(so.find(attrs = {'class':'txt'}))
    sou = bs(native,'html.parser')
    g = sou.find('span')
    g1 = g.string.strip(' ')
    hiragana.append(g1)
    h = str(sou.find('h2').contents[1])
    name.append(h)

#for k in range(len(name)):
    #print(name[k],enname[k],hiragana[k],birthday[k],constellation[k],bloodtype[k],height[k])

def write_excel():
    f = xlwt.Workbook(encoding = 'UTF-8')
    worksheet = f.add_sheet('乃木坂46成员信息',cell_overwrite_ok = True)
    row0 = ['日文姓名','英文姓名','平假名注记','生日','身高','血型','星座']
    for t in range(len(row0)):
        worksheet.write(0,t,label = row0[t])
    for p in range(len(name)):
        worksheet.write(p+1,0,label = name[p])
        worksheet.write(p+1,1,label = enname[p])
        worksheet.write(p+1,2,label = hiragana[p])
        worksheet.write(p+1,3,label = birthday[p])
        #worksheet.write(p+1,4,label = birthplace[p])
        worksheet.write(p+1,4,label = height[p])
        worksheet.write(p+1,5,label = bloodtype[p])
        worksheet.write(p+1,6,label = constellation[p])
    worksheet.write(len(name)+1,0,label = '资料截止目前：{}'.format(str(time.strftime("%Y{0}%m{1}%d{2}%H:%M:%S",time.localtime()).format('年','月','日'))))
    f.save(r'D:/Nogizaka46Member {}.xls'.format(str(time.strftime("%Y%m%d%H%M%S",time.localtime()))))

write_excel()

#结束运行
end = time.perf_counter()
print('本次运行时间:{:.2f}秒。'.format(end - start))
    
    
                         
    

