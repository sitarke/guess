from script import Script
from adb import ScreenCapture
from difflib import SequenceMatcher
import time
from colorama import init, Fore, Style
import json
from PIL import ImageGrab
import os
import  re
import threading
import base64
import schedule
import random
from datetime import datetime
from 面灵气喵 import get_rate


# 初始化 colorama
init(autoreset=True)


class Start:
    stop_event = threading.Event()  # 创建一个停止事件
    @staticmethod
    def game_of_chess_and_guessing(pos_list):
        def click_with_random_offset(position, x_offset, y_offset):
            """辅助函数，通过随机偏移点击位置。"""
            x, y = Script.random_offset(position[0], position[1], *x_offset, *y_offset)
            print(f'{Fore.GREEN}点击坐标：[x: {x}, y: {y}]{Style.RESET_ALL}')
            ScreenCapture.click(x, y)

        def check_text_and_click(ocr_area, expected_texts, x_offset, y_offset):
            """辅助函数，检查OCR文本并在匹配时点击。"""
            text, position, _ = Script.OCR(*ocr_area)
            if text and text in expected_texts:
                print(f'{Fore.GREEN}点击：{text} at {position}{Style.RESET_ALL}')
                click_with_random_offset(position, x_offset, y_offset)
                return True
            return False
                # 拒绝悬赏操作
        def reject_reward():
            """拒绝悬赏操作。"""
            text, position, _ = Script.OCR(414,114,532,149)
            if text:
                print(f'{Fore.RED}识别到：{text}{position}{Style.RESET_ALL}')
                if text in ['悬实封印', '悬赏封印']:
                    print(f'{Fore.GREEN}拒绝悬赏，勾协来了都不行{Style.RESET_ALL}')
                    click_with_random_offset((585,94), (0, 10), (0, 10))
                    return True
        # 将图片存为base64编码
        def image_to_base64(image_path):
            """
            将图片文件转换为Base64编码字符串。
            
            :param image_path: 图片文件的路径
            :return: Base64编码后的字符串
            """
            with open(image_path, 'rb') as file:
                # 读取图片的二进制内容
                image_data = file.read()
                # 使用base64标准库进行编码
                base64_str = base64.b64encode(image_data).decode('utf-8')
                return base64_str

        last_bet_result = None

        while not Start.stop_event.is_set():  # 检查停止事件
            # 悬赏
            reject_reward()
            # 获取上一局结果
            text, position, _ = Script.OCR(355, 176, 608, 287)
            if text:
                print(f'{Fore.CYAN}识别到：{text} at {position}{Style.RESET_ALL}')
                if text in ['竞猜失败', '竞精失败']:
                    last_bet_result = text
                    if check_text_and_click((483, 401, 547, 445), ['局'], (-10, 8), (0, 10)):
                        print(f'{Fore.MAGENTA}上一局失败，等待下一局{Style.RESET_ALL}')
                elif text in ['竞猜成功', '竞精成功']:
                    last_bet_result = text
                    if not check_text_and_click((483, 401, 547, 445), ['局'], (-10, 8), (0, 10)):
                        print(f'{Fore.BLUE}领取奖励{Style.RESET_ALL}')
                        click_with_random_offset((452, 312), (0, 59), (0, 29))
                elif text in ['休息中']:
                    print(f'{Fore.YELLOW}休息中，请手动切换一下游戏界面再切回来{Style.RESET_ALL}')
                    # 截图
                    output_file = ScreenCapture.screenshot(x1=0, y1=0, x2=960, y2=540)
                    # 保存为base64编码
                    base64_res = image_to_base64(output_file)
                    return f"休息中，请手动切换一下游戏界面再切回来", "休息中，未押注！",base64_res
            # 识别竞猜结算
            if check_text_and_click((398, 496, 554, 536), ['点击屏幕继续'], (0, 100), (0, 15)):
                continue
            if check_text_and_click(pos_list['guess'], ['竞猜', '竞精'], (10, 45), (10, 50)):
                print(f'{Fore.RED}当前已在竞猜界面{Style.RESET_ALL}')
                break;
            # 识别已竞猜
            text, position, _ = Script.OCR(59,226,178,273)
            if text and text in ['已竞猜', '已竞精']:
                print(f'{Fore.RED}已竞猜{Style.RESET_ALL}')
                # 截图
                output_file = ScreenCapture.screenshot(x1=0, y1=0, x2=960, y2=540)
                # 保存为base64编码
                base64_res = image_to_base64(output_file)
                return f"上一场结果：{last_bet_result}", "上局竞猜还未结束！", base64_res
            text, position, _ = Script.OCR(786,229,898,282)
            if text and text in ['已竞猜', '已竞精']:
                print(f'{Fore.RED}已竞猜{Style.RESET_ALL}')
                # 截图
                output_file = ScreenCapture.screenshot(x1=0, y1=0, x2=960, y2=540)
                # 保存为base64编码
                base64_res = image_to_base64(output_file)
                return f"上一场结果：{last_bet_result}", "上局竞猜还未结束！", base64_res

        is_click_30w = False
        while not Start.stop_event.is_set():  # 检查停止事件
            # 悬赏
            reject_reward()
            if not is_click_30w:
                is_click_30w = check_text_and_click((626, 441, 693, 475), ['30万'], (0, 20), (0, 10))
            else:
                if check_text_and_click((739, 300, 856, 396), ['竞猜', '竞精'], (10, 45), (10, 50)):
                    break

        while not Start.stop_event.is_set():  # 检查停止事件
            # 悬赏
            reject_reward()
            if check_text_and_click((532, 308, 602, 341), ['确定'], (0, 40), (0, 15)):
                continue
            text, position, _ = Script.OCR(*pos_list['guessed'])
            if text and text in ['已竞猜', '已竞精']:
                print(f'{Fore.RED}已竞猜{Style.RESET_ALL}')
                break
        # 截图
        output_file = ScreenCapture.screenshot(x1=0, y1=0, x2=960, y2=540)
        # 保存为base64编码
        base64_res = image_to_base64(output_file)

        return f"上一场结果：{last_bet_result}", "本局押注成功！", base64_res


    @staticmethod
    def main(which_bet):
        # 押左
        left_pos_list = {
            'guess': [41,203,210,346],
            'guessed': [59,226,178,273]
        }
        # 押右
        right_pos_list = {
            'guess': [780,220,893,311],
            'guessed': [786,229,898,282]
        }
        # 启动adb服务
        ScreenCapture.start_mumu_adb_service()
        # 获取设备id
        if not ScreenCapture.get_device_id():
            print("未发现adb设备，请开启adb服务.")
            return False
        print(f'{Fore.YELLOW}一切准备就绪，开始检测{Style.RESET_ALL}')
        if(which_bet == 'left'):
            last_bet_result,current_excute_res, base64_res = Start.game_of_chess_and_guessing(left_pos_list)
        elif(which_bet == 'right'):
            last_bet_result,current_excute_res, base64_res = Start.game_of_chess_and_guessing(right_pos_list)
        elif(which_bet == 'random'):
            last_bet_result,current_excute_res, base64_res = Start.game_of_chess_and_guessing(random.choice([left_pos_list, right_pos_list]))
        print(f'{Fore.YELLOW}押注完成，等待下次押注{Style.RESET_ALL}')
        return last_bet_result,current_excute_res, base64_res

# 随大流/爬虫
def job(mode):
    direction = 'left'
    if(mode == '爬取博主预测数据'):
        # 爬虫
        print(f'{Fore.YELLOW}使用面灵气喵博主预测数据{Style.RESET_ALL}')
        scraper_res = get_rate()
        print(f'{Fore.YELLOW}博主预测数据：{Fore.GREEN}{scraper_res}{Style.RESET_ALL}')
        direction = 'left'
        if(scraper_res['success']):
            if(scraper_res['data']['prediction_side'] == '左'):
                direction = 'left'
            elif(scraper_res['data']['prediction_side'] == '右'):
                direction = 'right'
        else:
            direction = 'left'
    # 随大流
    if(mode == '随大流'):
        from follow import follow_follow
        left_num, right_num = follow_follow()
        if(left_num != 0 and right_num != 0):
            direction = 'left' if left_num > right_num else 'right'
            print(f'{Fore.YELLOW}随大流  左：{Fore.GREEN}{left_num} {Fore.YELLOW}右：{Fore.GREEN}{right_num}{Style.RESET_ALL}')
        else:
            print(f'{Fore.RED}随大流数据异常，使用左押注{Style.RESET_ALL}')
            direction = 'left'

    Start.main(direction)

if __name__ == '__main__':
    # 模式选择
    mode = '爬取博主预测数据'
    # mode = '随大流'
    # 定义每天执行的时间点
    times = ['11:55', '13:55', '15:55', '17:55', '19:55', '21:55', '23:55']
    print(f'{Fore.RED}任务已经开始{Style.RESET_ALL}')
    # 输出执行时间提醒用户
    print(f'{Fore.GREEN}每天{times}执行任务{Style.RESET_ALL}')

    # 遍历所有时间点，并为每个时间点安排任务
    for t in times:
        schedule.every().day.at(t).do(job, mode)
    # 无限循环检查是否有任务需要执行
    while True:
        schedule.run_pending()
        time.sleep(5)  # 每隔1秒检查一次
