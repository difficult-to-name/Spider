import requests
import re
import json
import time
from requests.exceptions import RequestException

def get_one_page(url):
    try:
        headers = {
            #浏览器标识
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/71.0.3578.98 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        #判断请求是否成功
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def write_to_file(content):
    # os.remove('result.txt')
    with open('result.txt','a',encoding='utf-8') as f:
        # print(type(json.dumps(content)))
        #写入文件必须是str类型，所以要先序列化
        f.write(json.dumps(content, ensure_ascii=False)+'\n\n')


def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.'
        '*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',
        re.S)
    items = re.findall(pattern,html)
    #整理数据结构，转变为字典
    for item in items:
        yield {
            '排名':item[0],''
            '图片':item[1],''
            '标题':item[2],''
            '主演':item[3].strip()[3:],''
            '时间':item[4].strip()[5:],''
            '分数':item[5] + item[6]
        }

def main(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    # print(html)
    # fp = open('maoyan.html','w',encoding='utf-8')
    # fp.write(html)
    # fp.close()
    for item in parse_one_page(html):
        write_to_file(item)

if __name__ == '__main__':
    for i in range(10):
        main(offset=i*10)
        time.sleep(1)