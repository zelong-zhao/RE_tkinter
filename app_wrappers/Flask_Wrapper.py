import os,sys
import threading
from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime
from RE_Wrangler.bs4_goofish_goods_wrangle import goodfish_wrangle_auto

# 创建 Flask 应用
def create_flask_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/process', methods=['POST'])
    def process_data():
        data = request.get_json()
        data['base_path'] = app.config["RE_BOT_word_dir"]
        print(type(data),data.keys())
        print(f"{data['base_path']=}")
        goodfish_wrangle_auto(data)

        print("RE Bot: Received data.",datetime.datetime.now())
        # Your data processing logic here
        return jsonify({'status': 'success'}),200

    # 添加关闭服务器的路由
    @app.route('/shutdown', methods=['GET'])
    def shutdown():
        shutdown_server()
        return 'Server shutting down...'

    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is not None:
            func()
        else:
            print("Could not shut down server.")

    return app

# Flask 服务器控制器
class FlaskServerController:
    def __init__(self):
        self.app = create_flask_app()
        self.server_thread = None

    def start_server(self, RE_BOT_word_dir, host='localhost', port=4444):
        self.app.config["RE_BOT_word_dir"]=RE_BOT_word_dir

        if self.server_thread and self.server_thread.is_alive():
            print("Server is already running.")
            return

        def run_app():
            print(f"Starting Flask server on {host}:{port}...")
            self.app.run(host=host, port=port)

        self.server_thread = threading.Thread(target=run_app, daemon=True)
        self.server_thread.start()

    def stop_server(self,host='localhost',port=4444):
        import requests
        try:
            requests.get(f'http://{host}:{str(port)}/shutdown')
        except requests.exceptions.RequestException:
            pass
        print("Server stopped.")

if __name__ == '__main__':
    controller = FlaskServerController()

    # 启动服务器
    controller.start_server(host='localhost', port=4444,RE_BOT_word_dir='./tmp')

    import time
    time.sleep(50)  # 运行 5 秒

    # 停止服务器
    controller.stop_server(host='localhost', port=4444)