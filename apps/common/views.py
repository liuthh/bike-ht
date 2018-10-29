from flask import Blueprint,request,jsonify
from .forms import Verify_sendcode,Verify_SendLoginCode
from utils.miaodi import sendIndustrySms
from utils.memcached import mc
import random
bp=Blueprint('common',__name__,url_prefix='/common')

@bp.route('/sendcode/',methods=['POST'])                    #发送短信验证码，注册短信api
def sendcode():
    '''
    :param          mobile
    :return:        (1): code:412       手机号码输入不正确，或者已被注册
                    (2): code:200       发送短信成功
    '''
    form=Verify_sendcode(request.form)                      #验证表单
    if form.validate():
        mobble=form.mobile.data
        code=random.randrange(1000,9999)
        code=str(code)
        print(code)
        smsContent='【爱家社区】您的验证码为{0}，请于5分钟内正确输入，如非本人操作，请忽略此短信。'.format(code)
        sendIndustrySms(mobble,smsContent)
        mc.set(mobble,code,300)             #把短信验证码存放在memcached里面
        print(mc.get(mobble))
        return jsonify({'code':200,'message':'发送成功'})
    else:
        message = form.errors.popitem()[1][0]                 #弹出第一条验证失败错误信息
        print(type(jsonify({'code':406})))
        return jsonify({'code':412,'message':message})


@bp.route('/sendLoginCode/',methods=['POST'])                    #登录短信验证接口api
def sendLoginCode():
    '''
     :param          mobile
     :return:        (1): code:412       手机号码输入不正确，或者未注册
                     (2): code:200       发送短信成功
     '''
    form=Verify_SendLoginCode(request.form)
    if form.validate():
        mobile=form.mobile.data
        code=random.randrange(1000,9999)
        code=str(code)
        smsContent='【爱家社区】登录验证码：{0}，如非本人操作，请忽略此短信。'.format(code)
        sendIndustrySms(mobile,smsContent)
        mc.set(mobile,code)
        return jsonify({'code':200,'message':'获取验证码成功'})
    else:
        message=form.errors.popitem()[1][0]
        return jsonify({'code':412,'message':message})

