from http.server import HTTPServer, SimpleHTTPRequestHandler



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
    

start_server()
        
