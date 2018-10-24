from exts import db
from datetime import datetime
from werkzeug.security import check_password_hash,generate_password_hash



class Cms_User(db.Model):
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    username=db.Column(db.String(50),nullable=False)
    __password=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(200),nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now(),nullable=False)

    def __init__(self, *args, **kwargs):
        if 'password' in kwargs:  # 对接受过来的密码进行一段处理
            passwd = kwargs.get('password')
            self.passwd = passwd
            kwargs.pop('passwd')  # 删除这个passwd
        super(Cms_User, self).__init__(*args,**kwargs)  # 剩下的内容交个父类处理

    @property
    def password(self):
        return self.__password

    @password.setter        # 对密码进行加密
    def password(self, password):
        self.__password = generate_password_hash(password)

    def check_password(self, password):  # 查看用户输入的密码是否正确
        return check_password_hash(self.password, password)

