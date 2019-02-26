import requests,os
from urllib.parse import urlencode
from hashlib import md5
from multiprocessing.pool import Pool

headers = {
    #请求资源主机
    # 'Host':'m.weibo.cn',
    # #请求来源
    # 'Referer':'https://m.weibo.cn/u/2830678474',
    #浏览器标识
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
    ' Chrome/71.0.3578.98 Safari/537.36',
    #标记Ajax请求
    'X-Requested-With':'XMLHttpRequest'
}

#请求函数
def get_page(offset):
    params = {
        'aid':24,
        'app_name':'web_search',
        'offset':offset,
        'format':'json',
        'keyword':'街拍',
        'autoload':'true',
        'count':20,
        'en_qc':1,
        'from':'search_tab',
        'pd':'synthesis'
    }
    #构造请求源
    url = 'https://www.toutiao.com/api/search/content/?' + urlencode(params)
    try:
        response = requests.get(url,headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError :
        return None

#解析函数
def get_image(json):
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            #获取图片源
            images = item.get('image_list')
            if images == None:
                continue
            for image in images:
                yield {
                    'image':image.get('url'),
                    'title':title
                }

#保存图片
def save_image(item):
    #建立文件保存图片
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            #借助MD5算法命名
            file_path = '{0}/{1}.{2}'.format(item.get('title'),
                        md5(response.content).hexdigest(),'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already Download',file_path)
    except requests.ConnectionError:
        print('Failed to save images')

#主函数
def main(offset):
    json = get_page(offset)
    for item in get_image(json):
        print(item)
        save_image(item)


GROUP_START = 1
GROUP_END = 20

if __name__ == '__main__':
    #采用多进程下载
    pool = Pool()
    group = ([x * 20 for x in range(GROUP_START,GROUP_END + 1)])
    pool.map(main,group)
    pool.close()
    pool.join()