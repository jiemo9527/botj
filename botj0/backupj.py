import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver
import time
import threading
import subprocess
import requests
import os
import glob
from tqdm import tqdm
import psutil


# Telegram Bot API密钥
TELEGRAM_BOT_TOKEN = ''
# 你的Telegram群组ID
TELEGRAM_CHAT_ID = ''


class FileDownloadHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)
# 设置文件服务目录
directory = '/srv'



# 开启服务函数
def start_server():
    server_address = ('', 8000)  # 使用空字符串表示监听所有可用的网络接口
    http_server = HTTPServer(server_address, FileDownloadHandler)
    print('Starting server...')
    http_server.serve_forever()

def stop_server():
    print('Stopping server...')
    # 获取所有正在运行的进程
    for proc in psutil.process_iter():
        try:
            # 检查进程是否在监听 8000 端口
            for conn in proc.connections():
                if conn.laddr.port == 8000:
                    # 终止该进程
                    proc.terminate()
                    print('Server stopped successfully.')
                    return
        except psutil.NoSuchProcess:
            pass
    
def backup_files():
    print("开始备份...")
    # 获取匹配指定模式的文件列表
    rmFile = glob.glob('/srv/*.tar')

    # 逐个删除文件
    for file_path in rmFile:
        os.remove(file_path)
    backup_file = "/srv/" + time.strftime("%m%d-%H%M.tar")
    subprocess.run(["tar", "-cvf", backup_file, "/srv/jellyfin/"])
    send_to_telegram(backup_file)
    print("备份完成。")



def send_to_telegram(backup_file):
    print("上传到 rclone...")
    rclone_upload_dir = 'download:'
    rclone_upload_path = 'download:Jellyfin备份/'
    subprocess.run(["rclone", "copy", "--transfers", "16", backup_file, rclone_upload_path])


    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': '今日备份已成功上传至 http://xxxxx '}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("成功发送消息到 Telegram！")
    else:
        print("发送消息到 Telegram 失败！")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ['start', 'stop', 'backup']:
        print("用法: python xxx.py [start|stop|backup]")
        sys.exit(1)

    if sys.argv[1] == 'start':
        start_server()
    elif sys.argv[1] == 'stop':
        stop_server()
    elif sys.argv[1] == 'backup':
        backup_files()
