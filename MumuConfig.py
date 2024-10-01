import os
import json

def get_mumu_info():
    # 获取 Roaming AppData 目录
    appdata = os.environ['APPDATA']
    mumu_config_path = os.path.join(appdata, "Netease", "MuMuPlayer-12.0",  "install_config.json")
    mumu_share_path = os.path.join(appdata, "Netease", "MuMuPlayer-12.0",  "vm_config.json")

    # 读取配置文件
    with open(mumu_config_path, 'r', encoding='utf-8') as file:
        config_data = json.load(file)
    
    # 提取player部分的version和install_dir
    player_version = config_data['player']['version']
    player_install_dir = config_data['player']['install_dir']
    # adb 路径
    adb_path = os.path.join(player_install_dir, 'adb.exe')

    # 读取共享文件夹JSON文件
    with open(mumu_share_path, 'r', encoding='utf-8') as file:
        share_data = json.load(file)

    # 提取sharefolder部分的user里的path
    sharefolder_user_path = share_data['vm']['sharefolder']['user']['path']

    # 定义图片保存目录
    windows_image_save_dir = os.path.join(sharefolder_user_path, 'Pictures')
    android_image_save_dir = '/sdcard/Pictures'

    # 返回收集的信息
    return {
        "player_version": player_version,
        "player_install_dir": player_install_dir,
        "adb_path": adb_path,
        "sharefolder_user_path": sharefolder_user_path,
        "windows_image_save_dir": windows_image_save_dir,
        "android_image_save_dir": android_image_save_dir
    }

# 调用函数并打印结果
mumu_info = get_mumu_info()
print(f"版本: {mumu_info['player_version']}")
print(f"安装目录: {mumu_info['player_install_dir']}")
print(f"adb路径: {mumu_info['adb_path']}")
print(f"用户共享文件夹路径: {mumu_info['sharefolder_user_path']}")
print(f"Windows本地目录映射: {mumu_info['windows_image_save_dir']}")
print(f"安卓端目录映射: {mumu_info['android_image_save_dir']}")