from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/abcd', methods=['GET'])
def run_script():
    # 获取 GET 请求的参数（例如，要执行的 Python 脚本和参数）
    arg = request.args.get('s')
    arg=arg+'.py'
    # 执行 Python 脚本
    result = subprocess.run(['python', f'/root/botj/{arg}'], capture_output=True)
    # 返回执行结果
    return result.stdout.decode('utf-8')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
