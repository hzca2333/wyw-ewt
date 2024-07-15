from flask import Flask, request

app = Flask(__name__)

@app.route('/api/info')
def get_info():
    # 读取请求头中的 Cookie
    cookies = request.headers.get('Cookie')

    # 获取请求者的IP地址
    client_ip = request.remote_addr

    # 打印 Cookie 和 IP 信息
    print("Received Cookie:", cookies)
    print("Client IP Address:", client_ip)

    # 返回响应（你可以根据需要返回其他内容）
    return "Hello! Check the console for Cookie and IP information."

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
