from wtforms import Form,StringField,IntegerField
from wtforms.validators import Length,Regexp,EqualTo,ValidationError,InputRequired
from utils.memcached import mc
from apps.models import OrderModel
from .models import UserModel
from flask import g


class Verify_regist(Form):                                         #前台用户注册验证
    mobile=StringField(validators=[Regexp(r'^1(3|4|5|7|8)\d{9}$',message='手机号码输入错误')])
    code=StringField(validators=[Regexp(r'\d{4}',message='验证码格式不正确')])
    username=StringField(validators=[Length(2,16,message='用户名长度应为4到16位')])
    password=StringField(validators=[Regexp(r'\w{6,16}',message='密码长度为6到16位，只能为数字字母下划线')])
    repassword=StringField(validators=[EqualTo('password',message='两次密码输入不一致')])

    def validate_code(self,field):                                 #验证验证码是否正确
        mobile=self.mobile.data
        if mobile:
            code=mc.get(mobile)
            if not code or code!=field.data:
                raise ValidationError(message='验证码错误')

    def validate_mobile(self,field):                                #验证手机号码是否已经注册
        mobile=field.data
        user=UserModel.query.filter_by(mobile=mobile).first()
        if user:
            raise ValidationError(message='手机号码已注册过了')



class Verify_login(Form):                                            #前台用户账号密码登录验证
    mobile=StringField(validators=[Regexp(r'^1(3|4|5|7|8)\d{9}$',message='手机号码输入错误')])
    password=StringField(validators=[Regexp(r'\w{6,16}',message='密码输入不正确')])



class Verify_code_login(Form):                                        #前台用户验证码登录验证
    mobile=StringField(validators=[Regexp(r'^1(3|4|5|7|8)\d{9}$',message='手机号码输入错误')])
    code=StringField(validators=[Regexp(r'\d{4}',message='验证码格式不正确')])
    def validate_code(self,field):                                    #验证验证码是否正确
        mobile=self.mobile.data
        if mobile!=None:
            code=mc.get(mobile)
            if not code or code!=field.data:
                raise ValidationError(message='验证码错误')



class Verify_resetpassword(Form):                                   #修改密码验证
    password = StringField(validators=[Regexp(r'[0-9a-zA-Z_]{6,16}', message='密码长度为6到16位，只能为数字字母下划线')])
    newpassword = StringField(validators=[Regexp(r'[0-9a-zA-Z_]{6,16}', message='新密码长度为6到16位，只能为数字字母下划线')])
    newpassword2 = StringField(validators=[EqualTo('newpassword',message='2次密码输入不一致')])



class Verify_GenerateOrder(Form):                                  #生成订单验证
    # 数量（number），商品单价（price）, 商品编号（good_id),
    number=IntegerField(validators=[InputRequired('数量不能为空')])
    price=IntegerField(validators=[InputRequired(message='价格不能为空')])
    good_id=IntegerField(validators=[InputRequired(message='商品ID不能为空')])
    address_id=IntegerField(validators=[InputRequired(message='地址不能为空')])



class Verify_aCart(Form):                                                #添加购物车商品id验证
    goods_id=IntegerField(validators=[InputRequired(message='商品id没传参')]) #商品id

class Verify_dCart(Verify_aCart):                                       #移除购物车商品
    types=IntegerField(validators=[Regexp(r'[10]',message='选择减少商品或者删除商品类型错误（0，1）')])

class Verify_apost(Form):                                                #添加帖子验证
    title=StringField(validators=[InputRequired(message='标题不能为空')])  #标题
    content=StringField(validators=[InputRequired(message='内容不能为空')])#内容
    img_code=IntegerField(validators=[Regexp(r'\d{4}',message='验证码不正确')])#验证码
    def validate_img_code(self,field):
        img_code=field.data
        user_id=g.front_user.id
        code=mc.get(user_id)
        if not code and img_code!=code:
            raise ValidationError(message='验证码输入不正确')

class Verify_refer_Verify(Form):
    order_code=IntegerField(validators=[InputRequired(message='请输入订单编号')])
    passwd=StringField(InputRequired(message='请输入密码'))







