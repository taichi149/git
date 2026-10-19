# 文件：app.py
# Flask 入口：创建应用、注册蓝图、启动服务

from flask import Flask
import config

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY

# 注册 UI 层蓝图（路由）
from ui.routes import ui_bp

app.register_blueprint(ui_bp)

if __name__ == "__main__":
    app.run(debug=config.DEBUG)