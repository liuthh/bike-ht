from wtforms import Form,StringField,ValidationError
from wtforms.validators import Length,Regexp
from apps.front.models import UserModel


class Verify_sendcode(Form):                    #发送注册验证码验证
    mobile = StringField(validators=[Regexp(r'^1(3|4|5|7|8)\d{9}$', message='手机号码输入错误')])
    def validate_mobile(self,field):
        mobile=field.data
        user=UserModel.query.filter_by(mobile=mobile).first()
        if user:
            raise ValidationError(message='您已经注册过了！')

class Verify_SendLoginCode(Form):                    #发送登录验证码验证
    mobile = StringField(validators=[Regexp(r'^1(3|4|5|7|8)\d{9}$', message='手机号码输入错误')])
    def validate_mobile(self, field):
        mobile = field.data
        user = UserModel.query.filter_by(mobile=mobile).first()
        print(user)
        if not user:
            raise ValidationError(message='您还没有注册哦！')