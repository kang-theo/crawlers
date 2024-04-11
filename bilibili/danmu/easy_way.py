import requests
import re

"""发送请求 视频网页源代码中是存在 oid --> cid"""
url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=1330002174' # 通过 ibilibili 获取弹幕地址
response = requests.get(url)
# 转码
response.encoding = 'utf-8'
"""获取数据"""
html_data = response.text
"""解析数据
- re.findall('数据', '数据源') --> 找到所有数据
"""
content_list = re.findall('<d p=".*?">(.*?)</d>', html_data)
# 列表合并成字符串
content = '\n'.join(content_list)
with open('弹幕.txt', mode='a', encoding='utf-8') as f:
    f.write(content)
    f.write('\n')
print(content)
