from script import Script
from adb import ScreenCapture
from colorama import init, Fore, Style
from start import Start

def follow_follow():
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
                return 0,0
        # 识别竞猜结算
        if check_text_and_click((398, 496, 554, 536), ['点击屏幕继续'], (0, 100), (0, 15)):
            continue
        text, position, _ = Script.OCR(439,393,521,422) #剩余时间
        if text:
            if text in ['剩余时间']:
                text, position, _ = Script.OCR(94,365,183,395)
                if text:
                    left_num = int(text.replace(" ", ""))
                text, position, _ = Script.OCR(831,368,907,398)
                if text:
                    right_num = int(text.replace(" ", ""))
                return left_num, right_num;


