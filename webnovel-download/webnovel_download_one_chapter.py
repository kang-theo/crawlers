import os
import requests
import re # built-in, regular expression
import parsel # pip install parsel, css selector

# 1. Get html
url = 'https://www.webnovel.com/book/an-extra%E2%80%99s-pov_28157900908731405/how-it-all-began_75585827798831128###'
# url = 'https://www.xbiqugu.info/47/47167/20703737.html'

headers = {
  # Identity of the browser
  # 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
  'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

# response = requests.get(url)
response = requests.get(url=url, headers = headers)
# response.encoding = 'utf-8'  # garbled characters
# response.encoding = response.apparent_encoding # convert to utf-8
# print(response.text)

# 2. Parse html
"""
Parse HTML:
- regular expression: parse string data directly
  - .*? --> match any text except '\n'
  - re.findall(pattern, response.text, re.S), match '\n'
- css selector: parse based on labels and attributes
- xpath node extraction: parse based on node labels
"""
# 2.1 regular expression
# extract title
pattern = '<span class="j_chapIdx">(.*?)</span> <span class="j_chapName">(.*?)</span>'
title_list = re.findall(pattern, response.text)
title = ' '.join(title_list[0])
print(title)
# extract content
pattern = r'\\<p\\>(.*?)\\<\\/p\\>'
content_list = re.findall(pattern, response.text)
content_list_sanitized = [content.replace('\\', '') for content in content_list]
# delete * and thereafter items from list
del content_list_sanitized[content_list_sanitized.index('*'):]
content = '\n'.join(content_list_sanitized)
print(content)

# # 2.2 css selector and xpath
# Issue: this does not work for webnovel.com
# selector = parsel.Selector(response.text)
# # css and xpath are copied from devtool
# title = selector.css('h1.dib.mb0.fw700.fs24.lh1\.5::text').get()
# content = selector.xpath('//*[@id="page"]/div[1]/div[2]/div/div[4]/div[1]/div[1]/div/p/text').getall()
# print(title)
# print(content)

# 3. Store data
folder_path = './results/'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

file_path = os.path.join(folder_path, title + '.txt')
with open(file_path, mode='a', encoding='utf-8') as f:
  f.write(title)
  f.write('\n')
  f.write(content)
  f.write('\n')