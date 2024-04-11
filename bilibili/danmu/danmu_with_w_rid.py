"""
python采集B站视频弹幕, 实现词云图分析

[模块使用]:
    import requests 数据请求
    import jieba 分词
    import wordcloud  词云
    import re 正则

采集B站视频弹幕:
    1. 简单 <√>
    2. 复杂

通过爬虫程序采集数据
    1. 分析数据在什么地方
        - 通过浏览器开发者工具进行抓包分析
            I.打开开发者工具:  F12 / 右键点击检查选择选择network<网络>
            II. 直接点击弹幕列表
            III. 找到链接 seg.so
    发送请求
    获取数据
    解析数据
    保存数据

发送请求->模拟浏览器对于url地址发送请求
    - 模拟浏览器 <没有伪装>
        提醒你没有登陆账号
    - w_rid <加密参数 没有做解密>
        你没有访问权限

爬虫内容稍微核心点知识点: JS逆向
    参数加密 --> 解密分析加密规则

"ea1db124af3c7062474693fa704f4ff8" <固定参数>
"oid=1330002174&pe=360000&pid=748271512&ps=120000&pull_mode=1&segment_index=1&type=1&web_location=1315873&wts=1699879323"
"oid=1330002174&pid=748271512&segment_index=2&type=1&web_location=1315873&wts=1699879379ea1db124af3c7062474693fa704f4ff8"
"oid=1330002174&pid=748271512&segment_index=3&type=1&web_location=1315873&wts=1699879405"
"oid=1330002174&pid=748271512&segment_index=4&type=1&web_location=1315873&wts=1699879416"
"""

import requests
import re
# 导入加密模块
import hashlib
import time

def Hash(num, date_time):
    """
    :param num: 页码
    :param date_time: 时间戳
    :return:
    webpack -> 扣代码
    根据经验: 了解到是MD5 --> 可以直接写出来
    """
    string = f'oid=1330002174&pid=748271512&segment_index={num}&type=1&web_location=1315873&wts={date_time}ea1db124af3c7062474693fa704f4ff8'
    MD5 = hashlib.md5()
    MD5.update(string.encode('utf-8'))
    w_rid = MD5.hexdigest()
    return w_rid


for page in range(2, 13):
    date_time = int(time.time())
    w_rid = Hash(page, date_time)
    print(w_rid)
    """发送请求"""
    url = f'https://api.bilibili.com/x/v2/dm/wbi/web/seg.so?type=1&oid=1330002174&pid=748271512&segment_index={page}&web_location=1315873&w_rid={w_rid}&wts={date_time}'
    # 模拟浏览器 <请求头>
    headers = {
        "Cookie":"buvid3=F20F4B52-ACB8-A021-3E0B-C346082E75AE97990infoc; b_nut=1697433797; CURRENT_FNVAL=4048; _uuid=B6E5D859-ECB4-5374-CEB3-ED2BCF41AF61098925infoc; buvid4=A0796219-8C0D-3CEA-74F0-BC1577B4BAAF99316-023101613-j+EVJ7V9TtLMVIMXjUkPKw%3D%3D; rpdid=|(kmJYmkk~k)0J'uYm~RJJ~mm; enable_web_push=DISABLE; header_theme_version=CLOSE; fingerprint=302abb9d1feb7abe011384358e53e1a6; buvid_fp_plain=undefined; SESSDATA=4d5c41d1%2C1713344487%2C042a1%2Aa2CjDCrSgSlisDAAfV8MGqQQGsXpmE5uLZGIM5sfxFreMgKnOnB4mI_UG7YyE6i6-_gqoSVklzTE44cmlJRmxCQnB3b0dLd25GTXBLb0lodWpfUFpPY0lnUUJqX2R2S19fT1hmOVYzRW12VVZaMktnODQwM2FseG9aQmNJak1NY2NpS2dfTFQwUmt3IIEC; bili_jct=d67ef1713484af58707c12c1697b1a8a; DedeUserID=406732493; DedeUserID__ckMd5=48c43aca436bb747; buvid_fp=302abb9d1feb7abe011384358e53e1a6; bp_video_offset_406732493=858548088305877015; LIVE_BUVID=AUTO9616989170857857; CURRENT_QUALITY=80; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTk5NDkxNTEsImlhdCI6MTY5OTY4OTg5MSwicGx0IjotMX0.LgcasmNZYUOxswBAJk2xWPmZ4ZYep-AbnhRucwu3c8A; bili_ticket_expires=1699949091; b_lsid=AE210A71E_18BC86FBB01; PVID=1; home_feed_column=5; browser_resolution=1707-861; sid=8ncrwo4o",
        "Referer":"https://search.bilibili.com/all?",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    # 发送请求
    response = requests.get(url=url, headers=headers)
    response.encoding = 'utf-8'
    """获取数据"""
    html_data = response.text
    """解析数据"""
    content_list = re.findall(':(.*?)@', html_data)
    for index in content_list:
        print(index[1:])
