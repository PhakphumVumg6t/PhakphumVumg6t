# coding=utf-8
"""
https://github.com/MZCretin/RollToolsApi#指定日期的节假日及万年历信息
指定日期的节假日及万年历信息
"""
import requests
from datetime import datetime

# Twenty-four solar terms list 二十四节气名称
STFT = (
    "冬至", "小寒", "大寒", "立春", "雨水", "惊蛰",
    "春分", "清明", "谷雨", "立夏", "小满", "芒种",
    "夏至", "小暑", "大暑", "立秋", "处暑", "白露",
    "秋分", "寒露", "霜降", "立冬", "小雪", "大雪")

WEEK_DICT = {1: '星期一', 2: '星期二', 3: '星期三', 4: '星期四', 5: '星期五', 6: '星期六', 7: '星期日'}


def get_rtcalendar(date=''):
    """
    获取指定日期的节假日及万年历信息
     https://github.com/MZCretin/RollToolsApi#指定日期的节假日及万年历信息
    :param data: str 日期 格式 yyyyMMdd
    :rtype str
    """
    date = date or datetime.now().strftime('%Y%m%d')
    print('获取 {} 的日历...'.format(date))
    try:
        resp = requests.get('https://www.mxnzp.com/api/holiday/single/{}'.format(date))
        if resp.status_code == 200:
            """
            {"code":1,"msg":"数据返回成功","data":{
            "date":"2019-06-27","weekDay":4,"yearTips":"己亥",
            "type":0,"typeDes":"工作日","chineseZodiac":"猪","solarTerms":"夏至后",
            "avoid":"移徙.入宅.安葬","lunarCalendar":"五月廿五",
            "suit":"订盟.纳采.出行.祈福.斋醮.安床.会亲友",
            "dayOfYear":178,"weekOfYear":26,"constellation":"巨蟹座"}}
            """
            # print(resp.text)
            if resp.json()['code'] == 1:
                data_dict = resp.json()['data']

                solarTerms = data_dict['solarTerms']
                solarTerms = ' ' + solarTerms if solarTerms in STFT else ''

                suit = data_dict['suit']
                suit = suit if suit else '无'
                avoid = data_dict['avoid']
                avoid = avoid if avoid else '无'

                return_text = '{data} {week} 农历{lunarCalendar}{solarTerms}\n【宜】{suit}\n【忌】{avoid}'.format(
                    data=data_dict['date'],
                    week=WEEK_DICT[data_dict['weekDay']],
                    lunarCalendar=data_dict['lunarCalendar'],
                    solarTerms=solarTerms,
                    suit=suit,
                    avoid=avoid,
                )
                return return_text
            else:
                print('获取日历失败:{}'.format(resp.json()['msg']))

        print('获取日历失败。')
    except Exception as exception:
        print(exception)


get_calendar = get_rtcalendar

if __name__ == '__main__':
    date = datetime.now().strftime('%Y%m%d')

    content = get_calendar('20190615')
    print(content)
