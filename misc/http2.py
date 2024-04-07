"""
http2.0 crawler solutions

url: https://spa16.scrape.center/api/book/ is using http2.0 protocol, so 'requests' cannot crawl data successfully.
when you find you cannot crawl data, you can use 'httpx' or the webpage is anti-crawling.
"""

# import requests

# url = 'https://spa16.scrape.center/api/book/?limit=18&offset=36'
# response = requests.get(url)
# print(response)


import httpx

client = httpx.Client(http2=True)
response = client.get('https://spa16.scrape.center/api/book/?limit=18&offset=36')
print(response)