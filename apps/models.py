from sqlalchemy.orm import backref

from exts import db
from datetime import datetime
import enum
from apps.front.models import UserModel



class GoodsImgModel(db.Model):      #商品图片表
    __tablename__='goods_img'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    url_img=db.Column(db.String(200),nullable=False)                            #图片的url
    goods_id=db.Column(db.Integer,db.ForeignKey('goods.id'),nullable=False)     #商品的id

    def to_dic(self):
        '''将对象转换成字典'''
        d={
            'id':self.id,
            'url_img':self.url_img,
            'goods_id':self.goods_id
        }
        return d

    goods=db.relationship('GoodsModel',backref='goods_img')


class AddressModel(db.Model):        #收货地址模型
    __tablename__='rcaddress'        #receive address(收货地址)
    user_id=db.Column(db.String(100),db.ForeignKey('user.id'),nullable=False)#用户id外键


    id=db.Column(db.Integer,nullable=False,autoincrement=True,primary_key=True)
    rcMobile=db.Column(db.String(50),nullable=False)                        #手机号码
    rcName=db.Column(db.String(50),nullable=False)                          #收货人名称
    rcAddress=db.Column(db.String(200),nullable=False)                      #收货地址

    user=db.relationship('UserModel',backref='addresses')
    order=db.relationship('OrderModel',uselist=False)                       #和订单模型建立1对1关系

    def to_dic(self):
        d={
            'id':self.id,
            'user_id':self.user_id,
            'rcmobile':self.rcMobile,
            'rcname':self.rcName,
            'rcaddress':self.rcAddress
        }

class StatusEnum(enum.Enum):                                        #订单状态枚举类
    WAIT_PAY=1      #未付款
    PAID=2          #已支付
    WAIT_COMMENT=3  #已评论
    COMPLETE=4      #已完成
    CANCEL=5        #已取消


class OrderModel(db.Model):
    __tablename__='order'
    id=db.Column(db.Integer,primary_key=True,nullable=False)                            #订单编号
    number=db.Column(db.Integer,nullable=False)                                         #商品的数量
    good_price=db.Column(db.Integer,nullable=False)                                     #商品的总价
    status=db.Column(db.Enum(StatusEnum),default=StatusEnum.WAIT_PAY)                   #订单状态
    comment=db.Column(db.Text)                                                          #评论信息，或者拒绝理由
    create_time=db.Column(db.DateTime,default=datetime.now(),nullable=False)            #下单时间
    remark=db.Column(db.Text)                                                           #下单备注

    address_id=db.Column(db.Integer,db.ForeignKey('rcaddress.id'),nullable=False)       #地址id
    user_id = db.Column(db.String(255), db.ForeignKey('user.id'),nullable=False)        #下单客户
    goods_id=db.Column(db.Integer,db.ForeignKey('goods.id'),nullable=False)             #商品ID


    address=db.relationship('AddressModel',backref=backref('indent',uselist=False))
    good=db.relationship('GoodsModel',backref='orders')
    user=db.relationship('UserModel',backref='orders')

class GoodsModel(db.Model):       #商品表
    __tablename__='goods'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    title=db.Column(db.String(100),nullable=False)                                  #标题
    brand=db.Column(db.String(100),nullable=False)                                  #品牌
    price=db.Column(db.Integer,nullable=False)                                      #价格
    create_time=db.Column(db.DateTime,default=datetime.now(),nullable=False)        #价格
    intr=db.Column(db.Text,nullable=False)                                          #商品简介
    color=db.Column(db.String(10),nullable=False)                                   #商品颜色
    Sales=db.Column(db.Integer,default=0)                                           #销量
    stock=db.Column(db.Integer,default=0,nullable=False)                            #库存
    main_img=db.Column(db.Integer)                                                  #主图片



    def to_dic(self):
        '''将对象转换成字典'''
        d={
            'id':self.id,
            'title':self.title,
            'brand':self.brand,
            'price':self.price,
            'create_time':self.create_time,
            'intr':self.intr,
            'color':self.color,
            'sales':self.Sales,
            'stock':self.stock
        }
        return d

