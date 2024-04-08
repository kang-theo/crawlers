"""
Python实现12306购票程序 https://kyfw.12306.cn/otn/leftTicket/init

[模块使用]:
    requests --> pip install requests
    prettytable --> pip install prettytable
    selenium --> pip install selenium
    谷歌浏览器
    谷歌驱动

- 查票程序
    1. 分析查票数据接口 (链接) 浏览器进行操作
        - 打开开发者工具: F12 / 右键检查
        - 点击查询
        查票接口: https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2023-12-30&leftTicketDTO.from_station=CSQ&leftTicketDTO.to_station=SHH&purpose_codes=ADULT
    2. 发送请求 -> 模拟浏览器对于url地址发送请求
    3. 获取数据 -> 获取服务器返回响应数据
    4. 解析数据 -> 提取车次信息
    5. 数据输出效果
"""
# 导入数据请求模块
import requests
import prettytable as pt
import json

# 输入出发城市
from_city = input('输入出发城市: ')
# 输入目的城市
to_city = input('输入目的城市: ')
# 输入出发时间
date = '2023-12-30'
# 读取城市文件 -> 返回json字符串
f = open('city.json', encoding='utf-8').read()
# 转json字典
city_data = json.loads(f)

"""发送请求 -> 模拟浏览器对于url地址发送请求"""
# 模拟浏览器: 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
# 请求网址
url = f'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={date}&leftTicketDTO.from_station={city_data[from_city]}&leftTicketDTO.to_station={city_data[to_city]}&purpose_codes=ADULT'
# 发送请求
response = requests.get(url=url, headers=headers)
"""获取数据 -> 获取服务器返回响应数据"""
json_data = response.json()
"""解析数据 -> 提取车次信息"""
result = json_data['data']['result']
# 实例化对象
tb = pt.PrettyTable()
# 添加表头
tb.field_names = [
    '序号',
    '车次',
    '出发时间',
    '到达时间',
    '耗时',
    '特等座',
    '一等',
    '二等',
    '软卧',
    '硬卧',
    '硬座',
    '无座',
]
page = 1
# for 循环遍历 提取列表里面元素
for i in result:
    # 字符串分割方法
    index = i.split('|')
    num = index[3]  # 车次
    start_time = index[8]  # 出发时间
    end_time = index[9]  # 到达时间
    use_time = index[10]  # 耗时
    topGrade = index[32]  # 特等座
    first_class = index[31]  # 一等
    second_class = index[30]  # 二等
    hard_sleeper = index[28]  # 硬卧
    hard_seat = index[29]  # 硬座
    no_seat = index[26]  # 无座
    soft_sleeper = index[23]  # 软卧
    dit = {
        '车次': num,
        '出发时间': start_time,
        '到达时间': end_time,
        '耗时': use_time,
        '特等座': topGrade,
        '一等': first_class,
        '二等': second_class,
        '软卧': soft_sleeper,
        '硬卧': hard_sleeper,
        '硬座': hard_seat,
        '无座': no_seat,
    }
    tb.add_row([
        page,
        num,
        start_time,
        end_time,
        use_time,
        topGrade,
        first_class,
        second_class,
        soft_sleeper,
        hard_sleeper,
        hard_seat,
        no_seat,
    ])
    page += 1

print(tb)
# 请输入你要购买车次序号
page_num = input('请输入你要购买车次序号: ')

