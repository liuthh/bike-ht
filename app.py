from flask import Flask
from apps.front import bp as front
from apps.common import bp as common
from apps.cms import bp as cms
from exts import db
import config
import flask_cors


app = Flask(__name__)           #主文件
app.register_blueprint(front)   #导入前台蓝图
app.register_blueprint(common)  #导入公共蓝图
app.register_blueprint(cms)     #导入后台蓝图
app.config.from_object(config)
db.init_app(app=app)
flask_cors.CORS(app, supports_credentials=True)




if __name__ == '__main__':
    app.run()
