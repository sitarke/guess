import subprocess
import re
import os
import json
from PIL import Image

from colorama import init, Fore, Style
from MumuConfig import get_mumu_info

init(autoreset=True)


mumu_info = get_mumu_info()
if not mumu_info:
    print("未找到模拟器配置文件，请检查模拟器是否为mumu12最新版且已启动")
    exit()

class ScreenCapture:
    """
    设备管理器类，用于处理与设备相关的操作，如获取设备ID和截图。
    """
    @staticmethod
    def start_mumu_adb_service():
        current_dir = os.getcwd()
        try:

            # 切换工作目录
            os.chdir(mumu_info['player_install_dir'])
             # 执行连接命令
            result = subprocess.run(['adb.exe', 'connect', '127.0.0.1:16384'], check=True, capture_output=True, text=True)
            # 输出adb命令的结果
            print("ADB连接结果:", result.stdout.strip())
            # 切回原目录
            os.chdir(current_dir)
            return result.stdout.strip()
        except Exception as e:
            print(f"启动adb失败，请手动打开: {e}")
             # 切回原目录
            os.chdir(current_dir)
            return []
    
    @staticmethod
    def get_device_id():
        """
        获取连接的模拟器的设备 ID 列表。
        
        :return: 设备 ID 列表
        """
        current_dir = os.getcwd()
        try:

            # 切换工作目录
            os.chdir(mumu_info['player_install_dir'])
            result = subprocess.run(['adb.exe', 'devices'], capture_output=True, text=True).stdout
            device_ids = [line.split('\t')[0] for line in result.split('\n') if '\tdevice' in line]
            # 切回原目录
            os.chdir(current_dir)
            return device_ids
        except Exception as e:
            print(f"获取设备ID失败: {e}")
             # 切回原目录
            os.chdir(current_dir)
            return []

    @staticmethod
    def take_screenshot(device_id, output_file, x1=None, y1=None, x2=None, y2=None):
        """
        使用 adb 工具对指定设备 ID 的模拟器进行截图，并保存到本地文件。
        如果提供了坐标，则只截取该区域的图片。
        
        :param device_id: 模拟器的设备 ID
        :param output_file: 截图保存的本地文件路径
        :param x1, y1: 截图区域的左上角坐标 (可选)
        :param x2, y2: 截图区域的右下角坐标 (可选)
        """
        current_dir = os.getcwd()
        try:
            # 切换工作目录
            os.chdir(mumu_info['player_install_dir'])
            tmp_file = f'{mumu_info["android_image_save_dir"]}/screenshot_tmp.png'
            cmd_capture = f'adb.exe -s {device_id} shell screencap -p {tmp_file}'
            cmd_pull = f'adb.exe -s {device_id} pull {tmp_file} {output_file}'
            cmd_rm = f'adb.exe -s {device_id} shell rm {tmp_file}'
            
            # print(f'正在截取模拟器 {device_id} 的屏幕{Fore.GREEN }[{x1},{y1},{x2},{y2}]{Style.RESET_ALL}')
            subprocess.run(cmd_capture, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            
            try:
                subprocess.run(cmd_pull, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                subprocess.run(cmd_rm, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError:
                print("复制失败" )
                exit(0)
            
            # 如果提供了坐标，则裁剪图片
            if x1 is not None and y1 is not None and x2 is not None and y2 is not None:
                with Image.open(output_file) as img:
                    cropped_img = img.crop((x1, y1, x2, y2))
                    cropped_img.save(output_file)
             # 切回原目录
            os.chdir(current_dir)
        except Exception as e:
            print(f"截图错误: {e}")
             # 切回原目录
            os.chdir(current_dir)
            exit(0)
    @staticmethod
    def screenshot(x1=None, y1=None, x2=None, y2=None):
        """
        截取设备屏幕并返回截图文件路径。
        
        :param x1, y1, x2, y2: 截图区域的坐标 (可选)
        :return: 截图文件路径或 False
        """
        try:
            device_ids = ScreenCapture.get_device_id()
            if not device_ids:
                print("未发现adb设备，请开启adb服务.")
                return False
            
            output_file = f'{mumu_info["windows_image_save_dir"]}/screenshot.png'
            ScreenCapture.take_screenshot(device_ids[0], output_file, x1, y1, x2, y2)
            return output_file
        except Exception as e:
            print(f"截图错误: {e}")
            return False

    @staticmethod
    def click(x, y):
        """
        模拟在设备上指定坐标点击。
        
        :param x: 点击的 x 坐标
        :param y: 点击的 y 坐标
        """
        current_dir = os.getcwd()
        try:
            # 切换工作目录
            os.chdir(mumu_info['player_install_dir'])
            device_ids = ScreenCapture.get_device_id()
            if not device_ids:
                print("未发现adb设备，请开启adb服务.")
                return False
            
            cmd = f'adb.exe -s {device_ids[0]} shell input tap {x} {y}'
            subprocess.run(cmd, shell=True, check=True)
             # 切回原目录
            os.chdir(current_dir)
            return True
        except subprocess.CalledProcessError as e:
            print(f"执行命令失败: {e}")
        except Exception as e:
            print(f"发生错误: {e}")
        return False
