from exts import db
from datetime import datetime

class ShopModel(db.Model):       #商品表
    __tablename__='shop'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    title=db.Column(db.String(100),nullable=False)                                  #标题
    brand=db.Column(db.String(100),nullable=False)                                  #品牌
    price=db.Column(db.Integer,nullable=False)                                #价格
    create_time=db.Column(db.DateTime,default=datetime.now(),nullable=False)        #价格
    intr=db.Column(db.Text,nullable=False)                                          #商品简介
    color=db.Column(db.String(10),nullable=False)                                   #商品颜色


    def to_dic(self):
        '''将对象转换成字典'''
        d={
            'id':self.id,
            'title':self.title,
            'brand':self.brand,
            'price':self.price,
            'create_time':self.create_time,
            'intr':self.intr,
            'color':self.color
        }
        return d



class ShopImgModel(db.Model):     #商品图片表
    __tablename__='shop_img'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    url_img=db.Column(db.String(200),nullable=False)
    shop_id=db.Column(db.Integer,db.ForeignKey('shop.id'),nullable=False)

    shop=db.relationship('ShopModel',backref='shop_img')