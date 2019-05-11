import shutil
import configparser
import codecs
from distutils.util import strtobool
from datetime import datetime
import sys, traceback
# libs -------------------------------------------
from libs.logger import writelog  # log出力
from libs.notify_controller import send_notify # 通知 (Line/discord/slack)

# functions ------------------------------------------
# 設定取得
def get_config():
    config = configparser.ConfigParser()
    config.read_file(codecs.open("config.ini", "r", "utf8"))
    return config

# 単位GB変換
def toGB(val):
    return int(val / 1024 ** 3)

# HDDディスク情報取得
def get_disk(disk):
    free = toGB(disk.free)
    total = toGB(disk.total)
    free_per = int(free / total * 100)    
    return free, total, free_per

# HDD容量 通知メッセージ
def get_yabai_msg(free, total, free_per):
    return 'free:' + str(free) + '/' + str(total) + 'GB(' + str(free_per) + '%)'

# process -----------------------------------------
# loopモード処理
def yabai_loop(config):
    writelog('info','yabai_loop','start')
    try:
        hdd_yabai_path = config['HDD']['yabai_path']
        hdd_yabai_gb = int(config['HDD']['yabai_gb'])
        hdd_yabai_loop_intervalmin = int(config['HDD']['yabai_loop_intervalmin'])
        hdd_yabai_log = config['HDD']['yabai_log']

        hdd_yabai_flag = False
        while True:
            if datetime.now().minute % hdd_yabai_loop_intervalmin == 0:
                disk = shutil.disk_usage(hdd_yabai_path)
                free, total, free_per = get_disk(disk)
                msg = get_yabai_msg(free, total, free_per)
                if (free < hdd_yabai_gb) and (hdd_yabai_flag == False):
                    send_notify(msg, config)
                    hdd_yabai_flag = True
                elif free >= hdd_yabai_gb:
                    hdd_yabai_flag = False
                writelog('info' ,hdd_yabai_log, msg, hdd_yabai_log)
    except:
        writelog('error','yabai_loop',traceback.format_exc())
    writelog('info','yabai_loop','end')
    return

# pulseモード処理
def yabai_pulse(config):
    writelog('info','yabai_pulse','start')
    try:
        hdd_yabai_path = config['HDD']['yabai_path'] 
        hdd_yabai_gb = int(config['HDD']['yabai_gb'])
        hdd_yabai_log = config['HDD']['yabai_log']

        disk = shutil.disk_usage(hdd_yabai_path)
        free, total, free_per = get_disk(disk)
        msg = get_yabai_msg(free, total, free_per)
        send_notify(msg, config)
        writelog('info', hdd_yabai_log, msg, hdd_yabai_log)
    except:
        writelog('error','yabai_pulse', traceback.format_exc())
    writelog('info','yabai_pulse','end')
    return

# main---------------------------------------------
def main():
    writelog('info','main','start')
    config = get_config()
    hdd_yabai_loop = strtobool(config['HDD']['yabai_loop'])
    if hdd_yabai_loop:
        yabai_loop(config)
    else:
        yabai_pulse(config)
    writelog('info','main','end')
    return

if __name__ == "__main__":
    main()
    