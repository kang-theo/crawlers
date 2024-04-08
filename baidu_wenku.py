"""
python实现百度文库VIp内容下载, 保存到word文档
[模块使用]:
    requests >>> 数据请求模块 pip install requests
    docx >>> 文档保存 pip install python-docx
    re 内置模块 不需要安装
ctrl + R 爬虫: 首先你得看得数据, 才能想办法获取

爬虫基本思路流程:

一. 分析数据来源
    找 文档数据内容, 是在那个url里面生成的
    - 通过开发者工具进行抓包分析
        1. 打开开发者工具: F12 / 鼠标右键点击检查选择network
        2. 刷新网页: 让本网页数据内容重新加载一遍
        https://wkimg.bdimg.com/img/67eec05ef18583d04864592d?new=1&w=500&p=1
    如果你是非VIP账号, 看数据, 图片形式 ---> 把数据<图片> 获取下来 ---> 做文字识别
        3. 分析文库数据内容, 图片所在地址

1. 获取所有图片内容: 文库数据 --> 图片形式 ---> 所有图片内容保存下载
2. 文字识别, 把图片文字识别出来, 保存word文档里面

二. 代码实现步骤
    1. 发送请求, 模拟浏览器对于url地址发送请求
        图片数据包:
    2. 获取数据, 获取服务器返回响应数据
        开发者工具: response
    3. 解析数据, 提取图片链接地址

    4. 保存数据, 把图片内容保存到本地文件夹

    5. 做文字识别, 识别文字内容

    6. 把文字数据信息, 保存word文档里面
"""
import requests
# 导入格式化输出模块
from pprint import pprint
import base64
import os
# 导入文档模块 pip install python-docx not docx in python3.x
from docx import Document
import re
import json

def get_content(file):
    """
    文字识别:
        1. 注册一个百度云API账号
        2. 创建应用 并且去免费领取资源
        3. 在技术文档里面 Access Token获取
        4. 调用API接口做文字识别
    """
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Gu7BGsfoKFZjLGvOKP7WezYv&client_secret=rGa2v2FcVnxBDFlerSW5H0D2eO7nRxdp'
    response = requests.get(host)
    access_token = response.json()['access_token']
    '''
    通用文字识别（高精度版）
    '''
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 二进制方式打开图片文件
    f = open(file, 'rb')
    img = base64.b64encode(f.read())
    params = {"image":img}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    json_data = requests.post(request_url, data=params, headers=headers).json()
    # 列表推导式
    words = '\n'.join([i['words'] for i in json_data['words_result']])
    return words

# # 读取文件夹里面所有图片内容
# content_list = []
# files = os.listdir('img\\')
# for file in files:
#     filename = 'img\\' + file
#     words = get_content(file=filename)
#     print(words)
#     content_list.append(words)
#
# # 保存word文档里面
# doc = Document()
# # 添加第一段文档内容
# content = '\n'.join(content_list)
# doc.add_paragraph(content)
# doc.save('data.docx')

# 浏览器中访问的页面地址
link = 'https://wenku.baidu.com/aggs/74d1a923482fb4daa58d4b8e?index=0&_wkts_=1712568519158&bdQuery=%E7%AD%94%E9%A2%98'
# 请求头
headers = {
    # 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    # 'Accept-Encoding':'gzip, deflate, br, zstd',
    # 'Accept-Language':'en-AU,en-GB;q=0.9,en;q=0.8,en-US;q=0.7',
    # 'Cache-Control':'max-age=0',
    # 'Connection':'keep-alive',
    # 'Sec-Ch-Ua':'"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
}

# Issue: 百度文库安全验证
# 1. https://blog.csdn.net/lavender_dream/article/details/115025362?spm=1001.2101.3001.6650.3&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-3-115025362-blog-132323334.235%5Ev43%5Epc_blog_bottom_relevance_base7&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-3-115025362-blog-132323334.235%5Ev43%5Epc_blog_bottom_relevance_base7&utm_relevant_index=6
# 2. https://blog.csdn.net/mkr67n/article/details/132323334
# cookies = {
#     'Cookie': 'bdsearchUnlogin=0; kunlunFlag=1; BIDUPSID=E372911FE493AC928F21E37428317842; PSTM=1696645730; BAIDUID=E372911FE493AC92FBF1ADD1776BABDE:FG=1; BAIDUID_BFESS=E372911FE493AC92FBF1ADD1776BABDE:FG=1; BDUSS=lMxWHFXREF3NFFNbHJZdWhyLU1sWE5ST29XQzB4Q2ZqRlRUWlpWWThsTjdZa3RsRVFBQUFBJCQAAAAAAAAAAAEAAACTVWEC1ebU1wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHvVI2V71SNld; BDUSS_BFESS=lMxWHFXREF3NFFNbHJZdWhyLU1sWE5ST29XQzB4Q2ZqRlRUWlpWWThsTjdZa3RsRVFBQUFBJCQAAAAAAAAAAAEAAACTVWEC1ebU1wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHvVI2V71SNld; H_PS_PSSID=40080_40369_40378_40415_40303_40458_40456_39662_40512_40445_60040_60029_60034_60046_40510; H_WISE_SIDS=40080_40369_40378_40415_40303_40458_40456_39662_40512_40445_60040_60029_60034_60046_40510; BCLID_BFESS=11231803714649917015; BDSFRCVID=y08OJeC62REShrotWtYl7NBhKsgCY77TH6aoLEWGBVXEnDI3f5LoEG0PNM8g0K4b6jBUogKKL2OTHm_F_2uxOjjg8UtVJeC6EG0Ptf8g0x5; BDSFRCVID_BFESS=y08OJeC62REShrotWtYl7NBhKsgCY77TH6aoLEWGBVXEnDI3f5LoEG0PNM8g0K4b6jBUogKKL2OTHm_F_2uxOjjg8UtVJeC6EG0Ptf8g0x5; H_BDCLCKID_SF=tbC8VCD5JC83eJjR2tvq-JDHqx5Ka43tHD7yWCvXtIncOR5Jj65CQqtJKxnJLb3kanvw5Jnc-b3ToD063MA--t4TQJJx3q5v3CoRaCODJlRosq0x0MTYe-bQyNOattTGQCOMahv1tq7xOb63QlPK5JkgMx6MqpQJQeQ-5KQN3KJmfbL9bT3WjjISKx-_tj_qJRTP; H_BDCLCKID_SF_BFESS=tbC8VCD5JC83eJjR2tvq-JDHqx5Ka43tHD7yWCvXtIncOR5Jj65CQqtJKxnJLb3kanvw5Jnc-b3ToD063MA--t4TQJJx3q5v3CoRaCODJlRosq0x0MTYe-bQyNOattTGQCOMahv1tq7xOb63QlPK5JkgMx6MqpQJQeQ-5KQN3KJmfbL9bT3WjjISKx-_tj_qJRTP; H_WISE_SIDS_BFESS=40080_40369_40378_40415_40303_40458_40456_39662_40512_40445_60040_60029_60034_60046_40510; ZFY=E:BcKzXJ4wb06sdgxHe0s2ISe1f2nN:BH6nMT3eTgPeuw:C; ZD_ENTRY=baidu; delPer=0; PSINO=7; BA_HECTOR=2h8l042lag840401a42h8l2g2gela91j15ea91t; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; ab_sr=1.0.1_MzdlMWU0NGVkZTUzMzQ0OGY4MTRmZGM1NzIxMDk2MTMyNzFkMGFlNDBlN2RkMTJmZTE0ZTAxMmRhYjQ4MjlhMTQ5ZDM0NDAyOGRjNTNiMWIzYjg5NjQ0Y2Q2Mzc4OGQ3MTg4OTU1YjY3MzJmZWRiYmY4NDFkZGJlNDgxN2I0ZGM0OTFmMmJhN2I2YzI0ZWUyYjAxZWY5N2YwOTc2NWRhYTYxY2M3NmZiYmMzNTVjZGJjZTAyOTY3YTAyNGQ5MWI5'
# }
response = requests.get(url=link, headers=headers)
response.encoding = 'utf-8'
html_data = response.text
print(html_data)
# json_data = json.loads(re.findall('var pageData = (.*?);', html_data)[0])
# pprint(json_data)
# for j in json_data['aggInfo']['docList']:
#     name = j['title']  # 名字
#     score = j['score'] # 评分
#     viewCount = j['viewCount'] # 阅读量
#     downloadCount = j['downloadCount'] # 下载量
#     docId = j['docId'] # 数据包ID
#     """
#     1. 发送请求, 模拟浏览器对于url地址发送请求
#          - 长链接, 可以分段写
#             问号前面: url链接
#             问号后面: 请求参数/查询参数
#     """
#     # 确定请求链接，这是经过 network 分析得到的链接，从 devtool 找到资源链接和 payload 中的请求参数
#     url = 'https://wenku.baidu.com/gsearch/rec/pcviewdocrec'
#     # 请求参数
#     data = {
#         'docId': docId,
#         'query': name,
#         'recPositions': ''
#     }
#     # 请求头
#     headers = {
#        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
#     }
#     #发送请求
#     response = requests.get(url=url, params=data, headers=headers)
#     # <Response [200]> 响应对象, 200 表示请求成功
#     print(response)
#     """
#     2. 获取数据, 获取服务器返回响应数据
#         开发者工具: response
#         response.json() 获取响应json字典数据, 但是返回数据必须是完整json数据格式 花括号 {}
#         response.text 获取响应文本数据, 返回字符串  任何时候都可以, 但是基本获取网页源代码的时候
#         response.content 获取响应二进制数据, 返回字节 保存图片/音频/视频/特定格式文件
    
#     print(response.json())  打印字典数据, 呈现一行
#     pprint(response.json()) 打印字典数据, 呈现多行, 展开效果
#     3. 解析数据, 提取图片链接地址
#         字典取值: 键值对 根据冒号左边内容[键], 提取冒号右边的内容[值]
#     """
#     # 定义文件名 整型
#     num = 1
#     # for循环遍历, 把列表里面元素一个一个提取出来
#     # 这里的 json 格式从浏览器发送请求得到的相应中都能得到
#     for index in response.json()['data']['relateDoc']:
#         # index 字典呀
#         pic = index['pic']
#         print(pic)
#         # # 4. 保存数据  发送请求 + 获取数据 二进制数据内容
#         # img_content = requests.get(url=pic, headers=headers).content
#         # # 'img\\'<文件夹名字> + str(num)<文件名> + '.jpg'<文件后缀>  mode='wb' 保存方式, 二进制保存
#         # # str(num) 强制转换成 字符串
#         # # '图片\\' 相对路径, 相对于你代码的路径 你代码在那个地方, 那个代码所在地方图片文件夹
#         # with open('图片\\' + str(num) + '.jpg', mode='wb') as f:
#         #     # 写入数据 保存数据  把图片二进制数据保存
#         #     f.write(img_content)
#         # # 每次循环 + 1
#         # print(num)
#         # num += 1
