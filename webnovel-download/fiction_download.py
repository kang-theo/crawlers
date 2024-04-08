"""
Environment setup:
requests >>> pip install requests
parsel >>> pip install parsel
pandas >>> pip install pandas
tqdm >>> pip install tqdm
"""
import requests  # pip install requests
import parsel  # 数据解析 pip install parsel
import pandas as pd # pip install pandas
from tqdm import tqdm  # pip install tqdm

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}


def get_response(html_url):
    '''发送请求'''
    response = requests.get(url=html_url, headers=headers)
    response.encoding = response.apparent_encoding
    return response


def save(name, title, content):
    """保存小说"""
    with open(name + '.txt', mode='a', encoding='utf-8') as f:
        f.write(title)
        f.write('\n')
        f.write(content)
        f.write('\n')
        # print(title)


def get_novel_url(html_url):
    """获取小说章节url"""
    response = get_response(html_url)
    # 把获取到的html字符串数据 转成 selector 对象
    selector = parsel.Selector(response.text)
    name = selector.css('#info h1::text').get()
    href = selector.css('#list dd a::attr(href)').getall()
    # https://www.biquges.com/10_10770/6896120.html
    href = ['https://www.biquges.com/' + i for i in href]
    for index in tqdm(href):
        """获取小说的内容"""
        response = get_response(index)
        selector = parsel.Selector(response.text)
        title = selector.css('.bookname h1::text').get()
        # getall() 获取所有的标签内容 返回的是列表 get 获取一个 返回的是字符串
        content_list = selector.css('#content::text').getall()
        # 把列表转换成字符串
        content = ''.join(content_list)
        save(name, title, content)


if __name__ == '__main__':
    # url = 'https://www.biquges.com/10_10770/index.html'
    # get_novel_url(url)
    # print(response.text)
    while True:
        print('输入0即可退出程序')
        word = input('请输入你要下载的小说名字(作者): ')
        if word == '0':
            break
        search_url = 'https://www.biquges.com/modules/article/search.php'
        data = {
            'searchkey': word,
            'searchtype': 'articlename'
        }
        response_1 = requests.post(url=search_url, data=data, headers=headers)
        response_1.encoding = response_1.apparent_encoding
        selector_1 = parsel.Selector(response_1.text)
        # 第一次提取
        trs = selector_1.css('#nr')
        lis = []
        if trs:
            for tr in trs:
                novel_name = tr.css('td:nth-child(1) a::text').get()
                novel_id = tr.css('td:nth-child(1) a::attr(href)').get().replace('/', '')
                author = tr.css('td:nth-child(3)::text').get()
                dit = {
                    '书名': novel_name,
                    '作者': author,
                    '书ID': novel_id,
                }
                lis.append(dit)
            print(f'一共搜索到{len(lis)}数据内容')
            search_result = pd.DataFrame(lis)
            print(search_result)
            num = input('请输入你要下载的小说序号: ')
            # 序号对应的就是列表里面索引位置
            num_id = lis[int(num)]['书ID'] # 直接获取小说ID
            link_url = f'https://www.biquges.com/{num_id}/index.html'
            get_novel_url(link_url)
            print(f"{lis[int(num)]['书名']}已经下载完成了")
        else:
            print('抱歉，搜索没有结果^_^')