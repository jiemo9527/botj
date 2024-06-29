import time
import subprocess
import requests
import os
import glob



# Telegram Bot API密钥
TELEGRAM_BOT_TOKEN = ''
# 你的Telegram群组ID
TELEGRAM_CHAT_ID = ''


    
def backup_files():
    print("开始备份...")
    # 获取匹配指定模式的文件列表
    rmFile = glob.glob('/srv/*.tar')

    # 逐个删除文件
    for file_path in rmFile:
        os.remove(file_path)
    backup_file = "/srv/" + time.strftime("%m%d-%H%M.tar")
    subprocess.run(["tar", "-cvf", backup_file, "/srv/jellyfin/"])
    return backup_file




def send_to_telegram(f):
    print("上传到 rclone...")
    rclone_upload_dir = 'download:'
    rclone_upload_path = 'download:Jellyfin备份/'
    subprocess.run(["rclone", "copy", "--transfers", "16", f, rclone_upload_path])


    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': '今日备份已成功上传至 http://xxxxx '}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("成功发送消息到 Telegram！")
    else:
        print("发送消息到 Telegram 失败！")



send_to_telegram(backup_files())