"""

selenium 去操作驱动然后控制浏览器

"""
from selenium import webdriver
import csv

f = open('python_1.csv', mode='a', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
    '职位',
    '地区',
    '公司',
    '薪资待遇',
    '学历经验',
    '公司领域',
    '详情页',
])
csv_writer.writeheader()
driver = webdriver.Chrome()
driver.get('https://www.zhipin.com/job_detail/?query=python&city=100010000&industry=&position=')

def get_info():
    lis = driver.find_elements_by_css_selector('.search-job-list-wrap .job-list li')
    for li in lis:
        title = li.find_element_by_css_selector('.job-title .job-name a').text  # 获取a标签里面文本数据
        href = li.find_element_by_css_selector('.job-title .job-name a').get_attribute('href')  # 详情页
        area = li.find_element_by_css_selector('.job-area').text  # 地区
        company_name = li.find_element_by_css_selector('.company-text .name a').text  # 公司
        money = li.find_element_by_css_selector('.job-limit .red').text  # 薪资
        info = li.find_element_by_css_selector('.job-limit p').text  # 学历经验
        company_type = li.find_element_by_css_selector('.company-text p a').text  # 公司领域
        dit = {
            '职位': title,
            '地区': area,
            '公司': company_name,
            '薪资待遇': money,
            '学历经验': info,
            '公司领域': company_type,
            '详情页': href,
        }
        csv_writer.writerow(dit)
        print(title, area, company_name, money, info, company_type, href)


for page in range(1, 11):
    print(f'正在采集第{page}页的数据内容')
    get_info()
    driver.find_element_by_css_selector('.next').click()
