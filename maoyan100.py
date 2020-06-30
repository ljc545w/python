import re,os
import requests
import time,openpyxl
headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
	}

def get_html(url,headers):
    r = requests.get(url,headers = headers)
    r.encoding = r.apparent_encoding
    if r.status_code == 200:
        return r.text
    else:
        print('error')

def view_data(x,html):
    pattern1 = re.compile('"\stitle=".*?"\sclass')
    data = re.findall(pattern1,html)
    #print(data)
    pattern2 = re.compile('>\d{1,3}\.?<',re.S)
    score = re.findall(pattern2,html)[0:30]
    item = []
    for i in range(10):
        item.append(data[i][9:-7])
        i *= 3
        item.append(score[i][1:-1])
        item.append(score[i+1][1:-1] + score[i+2][1:-1])
    for i in range(10):
        save_data(x + i,1,item[i*3+1])
        save_data(x + i,2,item[i*3])
        save_data(x + i,3,item[i*3+2])
    return data

def save_data(i,j,u):
    ws.cell(i + 2,j,value = u)

def save_images(j,html,headers,data):
    pattern = re.compile('-src=.*?\s')
    url_img = re.findall(pattern,html)
    for i in range(len(url_img)):
        path = root + '/' + str(i + j + 1) + '-' + data[i][9:-7] + '.jpg'
        try:
            if not os.path.exists(path):
                r_img = requests.get(url_img[i][6:-2],headers = headers)
                with open(path,'wb') as f:
                    f.write(r_img.content)
                    f.close()
        except Exception as e:
            print(e)

if __name__ == "__main__":
    begin_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    urls = ['https://maoyan.com/board/4?offset={}'.format(i * 10) for i in range(10)]
    j = 0
    root = 'maoyan/海报'
    if not os.path.exists('maoyan'):
        os.mkdir('maoyan')
    if not os.path.exists(root):
        os.mkdir(root)
    print('开始爬取：' + begin_time)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.cell(1,1,value = '排名')
    ws.cell(1,2,value = '电影')
    ws.cell(1,3,value = '评分')
    for x in range(len(urls)):
        html = get_html(urls[x],headers)
        data = view_data(x*10,html)
        save_images(j,html,headers,data)
        j += 10
        time.sleep(1)
    wb.save('maoyan/TOP100榜.xlsx')
    end_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print('爬取完毕：' + end_time)
