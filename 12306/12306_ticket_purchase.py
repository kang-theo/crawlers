"""
Python实现12306购票程序 https://kyfw.12306.cn/otn/leftTicket/init

[模块使用]:
    requests --> pip install requests
    prettytable --> pip install prettytable
    selenium --> pip install selenium
    谷歌浏览器
    谷歌驱动

购票程序: 模拟人的行为进行购买
    1. 打开浏览器 访问网站
    2. 输入出发城市 目的城市 时间 点击查询
    3. 选择某一车次 点击预定 登陆
    4. 选择乘车人 座位
    5. 确定提交 下单
"""
# 导入数据请求模块
import requests
import prettytable as pt
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from password import account, Password
# 打开浏览器
driver = webdriver.Chrome()
# 访问网站
driver.get('https://kyfw.12306.cn/otn/leftTicket/init')
"""定位元素, 进行操作
selenium 3.0 语法版本定位元素:
    driver.find_element_by_id() 通过ID查找元素
    driver.find_element_by_class_name() 通过class类查找元素
    driver.find_element_by_css_selector() 通过css选择器查找元素
    driver.find_element_by_xpath() 通过xpath查找元素
selenium 4.0 语法版本定位元素:
    driver.find_element(By.ID, '')
    driver.find_element(By.CLASS_NAME, '')
    driver.find_element(By.CSS_SELECTOR, '')
    driver.find_element(By.XPATH, '')
- 输入出发城市
    1. 定位输入框位置
    2. 进行输入相关操作
"""
# 输入出发城市 先点击->清空->输入->回车
driver.find_element_by_id('fromStationText').click() # 点击
driver.find_element_by_id('fromStationText').clear() # 清空
driver.find_element_by_id('fromStationText').send_keys('长沙') # 输入
driver.find_element_by_id('fromStationText').send_keys(Keys.ENTER) # 回车

# 输入目的城市
driver.find_element_by_id('toStationText').click() # 点击
driver.find_element_by_id('toStationText').clear() # 清空
driver.find_element_by_id('toStationText').send_keys('上海') # 输入
driver.find_element_by_id('toStationText').send_keys(Keys.ENTER) # 回车
# 输入时间
driver.find_element_by_id('train_date').click() # 点击
driver.find_element_by_id('train_date').clear() # 清空
driver.find_element_by_id('train_date').send_keys('2023-12-30') # 输入
# 点击查询按钮
driver.find_element_by_id('query_ticket').click()
# 延时
time.sleep(0.5)
# 选择车次预定 1(1) 3(2) 5(3) 7(4) 9(5) 11(6)
driver.find_element_by_css_selector('#queryLeftTable tr:nth-child(3) .btn72').click()
# 延时
time.sleep(1)
# 输入账号
driver.find_element_by_id('J-userName').send_keys(account)
# 输入密码
driver.find_element_by_id('J-password').send_keys(Password)
# 点击登陆
driver.find_element_by_id('J-login').click()
# 延时
time.sleep(0.5)
# 输入验证
driver.find_element_by_id('id_card').send_keys('6551')
driver.find_element_by_id('verification_code').click()
yzm = input('验证码: ')
driver.find_element_by_id('code').send_keys(yzm)
driver.find_element_by_id('sureClick').click()
driver.implicitly_wait(10)
time.sleep(3)
# 返回上一级页面
driver.back()
# 点击查询按钮
driver.find_element_by_id('query_ticket').click()
# 延时
time.sleep(0.5)
# 选择车次预定 1(1) 3(2) 5(3) 7(4) 9(5) 11(6)
driver.find_element_by_css_selector('#queryLeftTable tr:nth-child(3) .btn72').click()
# 选择乘车人
driver.find_element_by_id('normalPassenger_0').click()
# 提交订单
driver.find_element_by_id('submitOrder_id').click()
time.sleep(2)
# 下单
driver.find_element_by_id('qr_submit_id').click()

# Search tickets
# # 输入出发城市
# from_city = input('输入出发城市: ')
# # 输入目的城市
# to_city = input('输入目的城市: ')
# # 输入出发时间
# date = '2023-12-30'
# # 读取城市文件 -> 返回json字符串
# f = open('city.json', encoding='utf-8').read()
# # 转json字典
# city_data = json.loads(f)
#
# """发送请求 -> 模拟浏览器对于url地址发送请求"""
# # 模拟浏览器: 请求头
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
# }
# # 请求网址
# url = f'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={date}&leftTicketDTO.from_station={city_data[from_city]}&leftTicketDTO.to_station={city_data[to_city]}&purpose_codes=ADULT'
# # 发送请求
# response = requests.get(url=url, headers=headers)
# """获取数据 -> 获取服务器返回响应数据"""
# json_data = response.json()
# """解析数据 -> 提取车次信息"""
# result = json_data['data']['result']
# # 实例化对象
# tb = pt.PrettyTable()
# # 添加表头
# tb.field_names = [
#     '序号',
#     '车次',
#     '出发时间',
#     '到达时间',
#     '耗时',
#     '特等座',
#     '一等',
#     '二等',
#     '软卧',
#     '硬卧',
#     '硬座',
#     '无座',
# ]
# page = 1
# # for 循环遍历 提取列表里面元素
# for i in result:
#     # 字符串分割方法
#     index = i.split('|')
#     num = index[3]  # 车次
#     start_time = index[8]  # 出发时间
#     end_time = index[9]  # 到达时间
#     use_time = index[10]  # 耗时
#     topGrade = index[32]  # 特等座
#     first_class = index[31]  # 一等
#     second_class = index[30]  # 二等
#     hard_sleeper = index[28]  # 硬卧
#     hard_seat = index[29]  # 硬座
#     no_seat = index[26]  # 无座
#     soft_sleeper = index[23]  # 软卧
#     dit = {
#         '车次': num,
#         '出发时间': start_time,
#         '到达时间': end_time,
#         '耗时': use_time,
#         '特等座': topGrade,
#         '一等': first_class,
#         '二等': second_class,
#         '软卧': soft_sleeper,
#         '硬卧': hard_sleeper,
#         '硬座': hard_seat,
#         '无座': no_seat,
#     }
#     tb.add_row([
#         page,
#         num,
#         start_time,
#         end_time,
#         use_time,
#         topGrade,
#         first_class,
#         second_class,
#         soft_sleeper,
#         hard_sleeper,
#         hard_seat,
#         no_seat,
#     ])
#     page += 1
#
# print(tb)
# # 请输入你要购买车次序号
# page_num = input('请输入你要购买车次序号: ')

