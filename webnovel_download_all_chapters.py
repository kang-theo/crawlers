import os
import requests
import re # built-in, regular expression
import parsel # pip install parsel, css selector

# 1. Get html
# get the toc, using js to get the toc, not SEO friendly
index_url = 'https://www.webnovel.com/book/an-extra%E2%80%99s-pov_28157900908731405/catalog'

headers = {
  # Identity of the browser
  'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

response = requests.get(url=index_url, headers = headers)
print(response.text)

# to be done with selenium
