import requests
import re # built-in, regular expression
import parsel # pip install parsel, css selector

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
# print(response.text)
"""
Parse HTML:
- regular expression: parse string data directly
  - .*? --> match any text except '\n'
  - re.findall(pattern, response.text, re.S), match '\n'
- css selector: parse based on labels and attributes
- xpath node extraction: parse based on node labels
"""
# # regular expression
# # extract title
# pattern = '<span class="j_chapIdx">(.*?)</span> <span class="j_chapName">(.*?)</span>'
# title_list = re.findall(pattern, response.text)
# title = ' '.join(title_list[0])
# print(title)

# # extract content
# pattern = r'\\<p\\>(.*?)\\<\\/p\\>'
# content_list = re.findall(pattern, response.text)
# content_list_sanitized = [content.replace('\\', '') for content in content_list]
# # delete * and thereafter items from list
# del content_list_sanitized[content_list_sanitized.index('*'):]
# content = '\n'.join(content_list_sanitized)
# print(content)


# css selector
selector = parsel.Selector(response.text)
# css and xpath are copied from devtool
title = selector.css('h1.dib.mb0.fw700.fs24.lh1\.5::text').get()
content = selector.xpath('//*[@id="page"]/div[1]/div[2]/div/div[4]/div[1]/div[1]/div/p/text').getall()
print(title)
print(content)
