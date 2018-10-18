from wtforms import Form,StringField,IntegerField
from flask import g
from wtforms.validators import Length,Regexp,EqualTo,ValidationError
from utils.memcached import mc
from .models import UserModel


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
    password=StringField(validators=[Regexp(r'\w{6,16}',message='密码个数输入不正确')])



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
    password = StringField(validators=[Regexp(r'\w{6,16}', message='密码长度为6到16位，只能为数字字母下划线')])
    newpassword = StringField(validators=[Regexp(r'\w{6,16}', message='新密码长度为6到16位，只能为数字字母下划线')])
    newpassword2 = StringField(validators=[EqualTo('newpassword',message='2次密码输入不一致')])



