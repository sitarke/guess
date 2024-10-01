import json
import re
from datetime import datetime

import requests


def convert_chinese_to_number(chinese_num: str) -> int:
    mapping = {
        '一': 1,
        '二': 2,
        '三': 3,
        '四': 4,
        '五': 5,
        '六': 6,
        '七': 7,
    }
    return mapping.get(chinese_num, -1)  # 返回-1表示未找到


def get_rate() -> dict:
    """
    :return: {
        success:处理状态
        data:成功获取到时才有，竞猜的详细信息
        message:附加信息
    }
    """
    url = ("https://inf.ds.163.com/v1/web/feed/basic/getSomeOneFeeds?feedTypes=1,2,3,4,6,7,10,"
           "11&someOneUid=462382f1127b46c5add1185d88f0ea40")
    headers = {
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
    }

    pattern = r'(第(\w+)天)(第(\w+)局)\n(左|右)\(.*?\) (\d+)%'

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        feeds = data.get('result', {}).get('feeds', [])
        if not feeds:
            return {"success": False, "message": "数据获取错误"}

        first_feed = feeds[0]
        update_time_dt = datetime.fromtimestamp(first_feed['updateTime'] / 1000)
        current_hour = datetime.now().hour

        time_slots = {
            0: (10, 12),
            1: (12, 14),
            2: (14, 16),
            3: (16, 18),
            4: (18, 20),
            5: (20, 22),
            6: (22, 24)
        }

        current_slot = next((slot for slot, (start, end) in time_slots.items() if start <= current_hour < end), None)
        if current_slot is None:
            return {"success": False, "message": "当前时间不在定义的档次内"}

        update_hour = update_time_dt.hour
        start, end = time_slots[current_slot]
        if not (start <= update_hour < end):
            return {"success": False, "message": "没有本次竞猜的数据"}

        content = json.loads(first_feed['content'])
        text = content['body']['text']
        media = content.get('body', {}).get('media', [])
        if media:
            image_urls = [image['url'] for image in media if 'url' in image]
        else:
            image_urls = []
        match = re.search(pattern, text)
        if match:
            day = convert_chinese_to_number(match.group(2))  # 将中文天数转换为数字
            round_number = convert_chinese_to_number(match.group(4))  # 将中文局数转换为数字
            return {
                "success": True,
                "data": {
                    "day": day,
                    "round_number": round_number,
                    "prediction_side": match.group(5),
                    "probability": match.group(6),
                    'image_urls': image_urls
                }
            }
        return {"success": False, "message": "未找到匹配内容，可能该条不是竞猜内容"}

    except (ValueError, KeyError) as e:
        return {"success": False, "message": f"请求失败: {str(e)}"}
    except requests.RequestException as e:
        return {"success": False, "message": f"请求失败，状态码: {e.response.status_code if e.response else '未知错误'}"}

def botpush() -> dict:
    """
    :return: {
        success:处理状态
        data:成功获取到时才有，竞猜的详细信息
        message:附加信息
    }
    """
    url = ("https://inf.ds.163.com/v1/web/feed/basic/getSomeOneFeeds?feedTypes=1,2,3,4,6,7,10,"
           "11&someOneUid=462382f1127b46c5add1185d88f0ea40")
    headers = {
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
    }

    pattern = r'(第(\w+)天)(第(\w+)局)\n(左|右)\(.*?\) (\d+)%'

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        feeds = data.get('result', {}).get('feeds', [])
        if not feeds:
            return {"success": False, "message": "数据获取错误"}

        first_feed = feeds[0]
        update_time_dt = datetime.fromtimestamp(first_feed['updateTime'] / 1000)
        current_hour = datetime.now().hour

        time_slots = {
            0: (10, 12),
            1: (12, 14),
            2: (14, 16),
            3: (16, 18),
            4: (18, 20),
            5: (20, 22),
            6: (22, 24)
        }

        current_slot = next((slot for slot, (start, end) in time_slots.items() if start <= current_hour < end), None)
        if current_slot is None:
            return {"success": False, "message": "当前时间不在定义的档次内"}

        update_hour = update_time_dt.hour
        start, end = time_slots[current_slot]

        content = json.loads(first_feed['content'])
        text = content['body']['text']
        media = content.get('body', {}).get('media', [])
        if media:
            image_urls = [image['url'] for image in media if 'url' in image]
        else:
            image_urls = []
        match = re.search(pattern, text)
        
        if match:
            day = convert_chinese_to_number(match.group(2))  # 将中文天数转换为数字
            round_number = convert_chinese_to_number(match.group(4))  # 将中文局数转换为数字
            return {
                "success": True,
                "data": {
                    "day": day,
                    "round_number": round_number,
                    "prediction_side": match.group(5),
                    "probability": match.group(6),
                    "update_time": update_time_dt.strftime('%Y-%m-%d %H:%M:%S'),
                    "text": text,
                    'image_urls': image_urls
                }
            }
        return {"success": False, "message": "未找到匹配内容，可能该条不是竞猜内容"}

    except (ValueError, KeyError) as e:
        return {"success": False, "message": f"请求失败: {str(e)}"}
    except requests.RequestException as e:
        return {"success": False, "message": f"请求失败，状态码: {e.response.status_code if e.response else '未知错误'}"}


# a= get_rate()
# print(a)
