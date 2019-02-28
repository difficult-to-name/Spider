import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery


browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)
keyword = 'iPad'

def index_page(page):
    """
    抓取商品列表页
    :param page:页码
    """
    print('正在抓取第',page,'页...')
    try:
        url = 'https://s.taobao.com/search?q=' + quote(keyword)
        browser.get(url)

        #指定页码>1(非首页)则跳转
        if page > 1:
            #等待页码输入框加载，并赋值给input对象
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')
            ))
            #等待跳转确认键加载，并赋值给submit对象
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')
            ))
            #清空页码，重新输入并跳转
            input.clear()
            input.send_keys(page)
            submit.click()
        #等待指定文本(page)出现，可判断跳转页面无误
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'),
                str(page)))
        #等待商品信息加载
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))

        get_products()

    except TimeoutException:
        index_page(page)


def get_products():
    """
    提取商品信息
    """
    html = browser.page_source
    doc = PyQuery(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            '图片':item.find('.pic .img').attr('data-src'),
            '价格':item.find('.price').text(),
            '销量':item.find('.deal-cnt').text(),
            '标题':item.find('.title').text(),
            '商店':item.find('.shop').text(),
            '地点':item.find('.location').text()
        }
        print(product)
        save_to_Mongo(product)



#构造数据库变量
Mongo_url = 'localhost'
Mongo_db = 'taobao'
Mongo_collection = 'products'
client = pymongo.MongoClient(Mongo_url)
db = client[Mongo_db]

def save_to_Mongo(result):
    """
    保存到MongoDB
    """
    #删除集合
    #db.Mongo_collection.drop()

    try:
        if db[Mongo_collection].insert_one(result):
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')

max_page = 10
def main():
    """
    遍历前10页的商品
    """
    for i in range(1,max_page + 1):
        index_page(i)


if __name__ == '__main__':
    main()