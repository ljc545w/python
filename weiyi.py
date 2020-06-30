#用到的包
from bs4 import BeautifulSoup as bs
import requests
import os,re
from urllib import request

#定义请求头
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}

#创建目标文件夹
if not os.path.exists('图片/weiyi'):
        os.mkdir('图片/weiyi')

#网站主要url
URL = 'https://www.mmonly.cc/gqbz/'

#主函数
def run():
    #获取网页数据
    req = requests.get(url=URL, headers=headers)
    req.encoding = req.apparent_encoding
    html = req.text
    #用BeautifulSoup抓取网页数据
    bf = bs(html,'lxml')
    photos = bf.find('div',class_="Clbc_Game_l_a").find_all('a',target = '_blank')
    #循环获取图库地址并保存壁纸
    for i in range(len(photos)):
        if i % 2 == 0:
            parse_photo(photos,i)

def parse_photo(photos,i):
    j = 2
    #获取图库地址
    photo = photos[i]
    url = photo.get('href')
    p_h = requests.get(url = url,headers = headers)
    p_h.encoding = p_h.apparent_encoding
    text = p_h.text
    #获取第二张到最后一张的url特征
    pages = get_pages(text)
    #创建图库路径并保存第一张
    path = get_path(photo,text)
    #从第二张开始保存
    for page in pages:
        if j <= 10:
            #保存壁纸
            save_photo(url,page,j,path)
            #这个j是为了方便命名
            j+=1

def get_pages(text):
    #利用正则表达式提取信息
    pattern = re.compile("<li><a\shref=.*?>\d{1,2}<")
    pages = re.findall(pattern,text)
    #返回特征信息
    return pages

def get_path(photo,text):
    bf = bs(text,'lxml')
    #获取第一张壁纸的网页地址
    imgs = bf.find('div',class_="photo").find_all('a',class_ = 'down-btn')
    img_url = imgs[0].get('href')
    #创建第一张壁纸所属图库路径
    path = '图片/weiyi/' + photo.img.get('alt')
    if not os.path.exists(path):
        os.mkdir(path)
    #保存第一张
    filename = '1' + '.jpg'
    request.urlretrieve(img_url,path + '/' + filename)
    #返回图库路径
    return path

def save_photo(url,page,j,path):
    #构建壁纸所在网页的url
    url = url[0:32] + page[13:-4]
    #从网页中获取壁纸地址
    ph = requests.get(url = url,headers = headers)
    ph.encoding = ph.apparent_encoding
    bf = bs(ph.text,'lxml')
    imgs = bf.find('div',class_="photo").find_all('a',class_ = 'down-btn')
    img_url = imgs[0].get('href')
    #保存壁纸到其所属图库路径
    filename = str(j) + '.jpg'
    request.urlretrieve(img_url,path + '/' + filename)   

if __name__ == '__main__':
    print('begin')
    run()
    print('end')
