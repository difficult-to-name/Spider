# import pymysql
# from sqlalchemy import Column,String,ForeignKey,create_engine
# from sqlalchemy.orm import sessionmaker,relationship
# from sqlalchemy.ext.declarative import declarative_base

# #连接数据库
# db = pymysql.connect('localhost','root','password','test',charset='utf8')
#
# #创建游标对象
# cursor = db.cursor()
#
# #预处理
# cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
#
# #创建表
# sql1 = """CREATE TABLE EMPLOYEE(ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#          FIRST_NAME VARCHAR(20),
#          LAST_NAME VARCHAR(20),
#          AGE INT,
#          SEX VARCHAR(10),
#          INCOME int )"""



#插入数据
# sql2 = """insert into employee(FIRST_NAME,
#           LAST_NAME, AGE, SEX, INCOME)
#           value ('林','小明',25,'男',5000)"""
#
# #执行语句
# # cursor.execute(sql1)
# cursor.execute(sql2)
# db.commit()
# cursor.close()
# db.close()

#创建对象的基类
# Base = declarative_base()
#
# #定义User对象
# class User(Base):
#     #表名
#     __tablename__ = 'user'
#
#     #表的结构
#     id = Column(String(20), primary_key=True)
#     name = Column(String(20))
#
#     books = relationship('Book')
#
# class Book(Base):
#
#     __tablename__ = 'Book'
#
#     id = Column(String(20),primary_key=True)
#     name = Column(String(20))
#
#     user_id = Column(String(20),ForeignKey('user.id'))
#
#
# #初始化数据库连接
# engine = create_engine('mysql+pymysql://root:password@localhost:3306/test',
#                        encoding='utf-8')
#
# #创建DBSession类型
# DBSession = sessionmaker(bind=engine)
#
# #添加session对象
# session = DBSession()
#
# #插入数据
# try:
#     new_user = User(id='5',name='bob')
#     session.add(new_user)
#     session.commit()
# except:
#     session.rollback()
#
# #查询数据
# user = session.query(User).filter(User.id =='5').one()
# session.close()
#
# print('type:',type(user),'name:',user.name)
#
# import urllib.request
# import urllib.parse
# import http.cookiejar

# data = bytes(urllib.parse.urlencode({'word':'hello'}),encoding='utf8')
# response = urllib.request.urlopen('http://httpbin.org/post',data=data)
# print(response.read().decode('utf8'))
#
# cookie = http.cookiejar.CookieJar()
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# response = opener.open('http://www.baidu.com')
# for item in cookie:
#     print(item.name+"="+item.value)
#
# print(response.read().decode('utf8'))
#
# from urllib import request,error
# try:
#     response = request. urlopen('https://cuiqingcai.com/index.htm')
# except error. HTTPError as e:
#     print(e.reason,e.code,e.headers,sep='\n')



# headers = {
#         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
#                       'Chrome/71.0.3578.98 Safari/537.36'
# }

# r = requests.get('https://www.zhihu.com/explore',headers=headers)
# pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>',re.S)
# titles = re.findall(pattern, r.text)
# for i in titles:
#     print(i)

# a = requests.get("https://github.com/favicon.ico")
# print(type(a))
# with open('favicon.ico','wb') as f:
#     f.write(a.content)

# content = """Hello 1234567 World_This
#         is a Regex Demo"""
# result = re.match('^He.*?(\d+)(.*?)Demo$',content,re.S)
# print(result.group(1))
# print(result.group(2))

# with open('a.html',encoding='utf-8') as f:
#     html = f.read()
# html = re.sub('<a.*?>|</a>','',html)
# result = re.findall('<li.*?>(.*?)</li>', html, re.S)
# for i in result:
#     print(i.strip())
#
# print(html)

# import requests
# import re
# import json
# import time
# from requests.exceptions import RequestException
#
# def get_one_page(url):
#     try:
#         headers = {
#             #浏览器标识
#             'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
#                          ' Chrome/71.0.3578.98 Safari/537.36'
#         }
#         response = requests.get(url, headers=headers)
#         #判断请求是否成功
#         if response.status_code == 200:
#             return response.text
#         return None
#     except RequestException:
#         return None
#
# def write_to_file(content):
#     # os.remove('result.txt')
#     with open('result.txt','a',encoding='utf-8') as f:
#         # print(type(json.dumps(content)))
#         #写入文件必须是str类型，所以要先序列化
#         f.write(json.dumps(content, ensure_ascii=False)+'\n\n')
#
#
# def parse_one_page(html):
#     pattern = re.compile(
#         '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.'
#         '*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',
#         re.S)
#     items = re.findall(pattern,html)
#     #整理数据结构，转变为字典
#     for item in items:
#         yield {
#             '排名':item[0],''
#             '图片':item[1],''
#             '标题':item[2],''
#             '主演':item[3].strip()[3:],''
#             '时间':item[4].strip()[5:],''
#             '分数':item[5] + item[6]
#         }
#
# def main(offset):
#     url = 'http://maoyan.com/board/4?offset='+str(offset)
#     html = get_one_page(url)
#     # print(html)
#     # fp = open('maoyan.html','w',encoding='utf-8')
#     # fp.write(html)
#     # fp.close()
#     for item in parse_one_page(html):
#         write_to_file(item)
#
# if __name__ == '__main__':
#     for i in range(10):
#         main(offset=i*10)
#         time.sleep(1)

# import pymongo
# client = pymongo.MongoClient(host='localhost', port=27017)
#
# db = client.test    #指定数据库
#
# collection = db.student
#
# student = {
#     'id':'1810262060',
#     'name':'lin',
#     'age':20,
#     'gender':'male'
# }
# student1 = {
#     'id':'201441302428',
#     'name':'lin',
#     'age':'24',
#     'gender':'male'
# }
# result = collection.insert(student)
# collection.insert(student1)
# print(result)

# import tesserocr
# from PIL import Image
#
# img = Image.open('code.jpg')
#
# img = img.convert('L')
# threshold = 127
# table = []
#
# for i in range(256):
#     if i < threshold:
#         table.append(0)
#     else:
#         table.append(1)
# img.show()
# img = img.point(table, '1')
# img.show()
# result = tesserocr.image_to_text(img)
# print(result)

import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#登陆需要的账号密码
email = '1810262060@email.szu.edu.cn'
password = 'a757664220'

#Seleniun对象的初始化
class CrackGeetest():

    def __init__(self):
        self.url = 'https://account.geetest.com/login'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)
        self.email = email
        self.password = password


#获取验证按钮
def get_geetest_button(self):

    button = self.wait.until(EC.element_to_be_clickable(
        (By.CLASS_NAME,'geetest_radar_tip')))
    return  button

#模拟点击
button = get_geetest_button()
button.click()

#获取验证码位置
def get_position(self):

    #等待验证码滑块加载
    img = self.wait(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
    time.sleep(2)
    location = img.location
    size = img.size
    top,bottom,left,right = location['y'], location['y']+size['height'],\
                            location['x'], location['x']+size['width']
    return (top, bottom, left, right)

#获取验证码图片
def get_geetest_image(self, name='captcha.png'):

    top, bottom, left, right = self.get_position()
    print('验证码:', top, bottom, left, right)

    #获取网页截图
    screenshot = self.get_screenshot()
    captcha = screenshot.crop((left,top,right,botton))   #裁剪需左上角和右下角坐标
    return captcha

#获取滑块
def get_slider(self):

    slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
    return slider

slider = self.get_slider()
slider.click()


