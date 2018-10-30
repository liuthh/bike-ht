from exts import db
import shortuuid
from datetime import datetime
import enum
from werkzeug.security import generate_password_hash,check_password_hash

# python manage.py db migrate              upgrade   映射数据库



class GenderEnum(enum.Enum):   #构造性别枚举类
    man=1
    woman=2
    secret=3
    unknow=4

class UserModel(db.Model):                      #用户表
    __tablename__='user'
    id=db.Column(db.String(200),primary_key=True,default=shortuuid.uuid)     #用户id
    username=db.Column(db.String(50),nullable=False)                    #用户名
    __passwd=db.Column(db.String(255),nullable=False)                   #用户密码
    mobile = db.Column(db.String(11), nullable=False, unique=True)      #手机号码
    is_delete=db.Column(db.String(255),nullable=True)                   #是否拉黑
    avatar = db.Column(db.String(200))                                  #头像
    personal_introduction = db.Column(db.String(150))                   #个人介绍
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.unknow)  #性别
    create_time=db.Column(db.DateTime,default=datetime.now())           #创建时间
    money=db.Column(db.Integer,default=0)                               #金钱

    def __init__(self,*args,**kwargs):
        if 'passwd' in kwargs:      #对接受过来的密码进行一段处理
            passwd=kwargs.get('passwd')
            self.passwd=passwd
            kwargs.pop('passwd')  #删除这个passwd
        super(UserModel, self).__init__(*args,**kwargs)    #剩下的内容交个父类处理


    def to_dic(self):
        d={
            'id':self.id,
            'username':self.username,
            'mobile':self.mobile,
            'avatar':self.avatar,
            'personal_introduction':self.personal_introduction,
            'gender':self.gender,
            'create_time':self.create_time,
            'money':self.money
        }
        return d



    @property                                               #对密码进行加密
    def passwd(self):
        return self.__passwd
    @passwd.setter
    def passwd(self,passwd):
        self.__passwd=generate_password_hash(passwd)

    def check_passwd(self,passwd):                          #查看用户输入的密码是否正确
        return check_password_hash(self.passwd,passwd)