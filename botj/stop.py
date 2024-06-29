import psutil


# Telegram Bot API密钥
TELEGRAM_BOT_TOKEN = ''
# 你的Telegram群组ID
TELEGRAM_CHAT_ID = ''


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
    

stop_server()
