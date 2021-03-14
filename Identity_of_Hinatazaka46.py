import requests as rq
from bs4 import BeautifulSoup as bs
import time
import xlwt

#Hinatazaka46
pathroot = 'https://www.hinatazaka46.com/s/official/artist/'

def fullpath(num): #补全网址
    return (pathroot + str(num))

headers = {'User-Agent':'Mozilla/5.0'}

textbox = []
#dic = {}

Is = 0
#Not = 0
start = time.perf_counter()
for i in range(24):
    r = rq.get(fullpath(i+1),headers = headers)
    if r.status_code == 200:
        r.encoding = 'UTF-8' #查看源代码，发现为原网页字符代码为UTF-8
        newtext = r.text
        textbox.append(newtext)
        Is += 1
        #print('成功1条：编号为{}的成员仍然在籍！'.format(i+1))
    else:
        #print('失败1条：编号为{}的成员已毕业！'.format(i+1))
        #Not += 1
        continue
end = time.perf_counter()
print('共检测到{}名成员的信息。'.format(Is))
print('收集信息用时{:.2f}秒。'.format(end - start))
    #dic[i] = newtext

name = []
#enname = []
birthday = []
hiragana = []
length = []
bloodtype = []
birthplace = []

#newtextbox = []

#soup = bs(textbox[0],'html.parser')
for i in range(len(textbox)):
    soup = bs(textbox[i],'html.parser')
    Name = soup.find(attrs = {'class':'c-member__name--info'})
    #enName = soup.find(attrs = {'class':'en'})
    try:
        name.append(Name.string.replace('\n','').replace(' ',''))
        #cd = enName.text.replace(u'\u3000',' ').split(' ')
        #enname.append(cd[1] + ' ' + cd[0])
    except:
        #print('{}出现了崩溃'.format(i+1))
        continue
    rinji = []
    for pl in soup.find_all(attrs = {'class':'c-member__info-td__text'}):
        rinji.append(pl.string.replace('\n','').replace(' ',''))
    birthday.append(rinji[0])
    length.append(rinji[2])
    birthplace.append(rinji[3])
    bloodtype.append(rinji[4])
    hiragana.append(soup.find(attrs = {'class':'c-member__kana'}).string.replace('\n','').replace(' ',''))

#print(len(name),len(birthday),len(hiragana),len(birthplace),len(bloodtype))

#for j in range(len(name)):
    #print(name[j],hiragana[j],birthday[j],birthplace[j],bloodtype[j])
    
def write_excel():
    f = xlwt.Workbook(encoding = 'UTF-8')
    worksheet = f.add_sheet('成员信息',cell_overwrite_ok = True)
    row0 = ['日文姓名','平假名注记','生日','出生地','身高','血型']
    for t in range(len(row0)):
        worksheet.write(0,t,label = row0[t])
    for p in range(len(name)):
        worksheet.write(p+1,0,label = name[p])
        #worksheet.write(p+1,1,label = enname[p])
        worksheet.write(p+1,1,label = hiragana[p])
        worksheet.write(p+1,2,label = birthday[p])
        worksheet.write(p+1,3,label = birthplace[p])
        worksheet.write(p+1,4,label = length[p])
        worksheet.write(p+1,5,label = bloodtype[p])
    worksheet.write(len(name)+1,0,label = '本xls于{}创建。'.format(str(time.strftime("%Y年%m月%d日%H:%M:%S",time.localtime()))))
    f.save('D:/Hinatazaka46Member.xls')
    
write_excel()
