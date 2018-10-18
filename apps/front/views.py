import json

from flask import (
                    Blueprint,
                    request,
                    render_template,
                    jsonify,
                    views,
                    session,
                    g
                    )
from .forms import (
                    Verify_regist,
                    Verify_login,
                    Verify_code_login,
                    Verify_resetpassword
                    )
from apps.models import ShopModel,ShopImgModel
from exts import db
from .models import UserModel
from config import User
from flask import Response
bp=Blueprint('front',__name__)


class View_Login(views.MethodView):                                #前台登录功能api
    '''
    param:      mobile password
    return:     code: 200   登录成功[跳转到来的页面，如果直接登录，跳转到首页]
                code: 401   用户名或者密码错误
                code: 412   登录格式输入不正确
    '''
    def post(self):
        form=Verify_login(request.form)
        # print(request.form)
        if form.validate():
            mobile=form.mobile.data
            password=form.password.data
            user=UserModel.query.filter_by(mobile=mobile).first()
            if user:
                if user.check_passwd(passwd=password):
                    session[User]=user.id
                    return jsonify({'code':200,'message':'登录成功'})
                else:
                    return jsonify({'code': 401, 'message': '用户名或者密码错误'})
            else:
                return jsonify({'code':401,'message':'用户名或者密码错误'})
        else:
            message=form.errors.popitem()[1][0]                         #返回验证出错的第一条错误信息
            return jsonify({'code':412,'message':message})
bp.add_url_rule('/login/',view_func=View_Login.as_view('login'))




@bp.route('/regist/',methods=['POST'])                            #前台注册功能api
def regist():
    '''
    param:      mobile,code,username,password,repassword
    return:     (1):code:200      注册成功
                (2):code:412      用户输入信息错误
    '''

    if request.method=='POST':
        form=Verify_regist(request.form)
        if form.validate():
            mobile=form.mobile.data
            username=form.username.data
            password=form.password.data
            user=UserModel(mobile=mobile,username=username,passwd=password)
            db.session.add(user)
            db.session.commit()
            return  jsonify({'code':200,'message':'恭喜你！注册成功。'})
        else:
            message = form.errors.popitem()[1][0]                   #弹出第一条出错信息
            return jsonify({'code':412,'message':message})




@bp.route('/getspDetial/',methods=['GET'])                                                   #搜索商品
def getspDetial():
    '''
    ：param:   content(搜索内容)    String
                1: 按最新发布排序
                2：按价格排序(降序)
                3：按销量排序（降序）
    :return:   code  200           请求数据成功
               code  201           仓库没有此商品
               code  202           用户没有输入商品内容,返回全部商品



    '''
    content=request.args.get('content')                        #搜索内容
    page=request.args.get('page',default=1)                    #当前页数
    sort=request.args.get('sort',default=1)                    #排序方式
    start = (page - 1) * 8
    end = start + 8
    sort=int(sort)
    if content:
        content='%'+content+'%'
        if sort==1:
            shops=ShopModel.query.order_by(ShopModel.create_time.desc()).filter(ShopModel.title.like(content)).slice(start,end).all()
            if shops:
                shops_dic=[]
                for shop in shops:
                    shops_dic.append(shop.to_dic())
                return jsonify(code=200,message=shops_dic)
            else:
                return jsonify({'code':201,'message':'没有找到您搜索的商品'})
        elif sort==2:
            shops=ShopModel.query.order_by(ShopModel.price.desc()).filter(ShopModel.title.like(content)).slice(start,end).all()
            if shops:
                shops_dic=[]
                for shop in shops:
                    shops_dic.append(shop.to_dic())
                return jsonify(code=200,message=shops_dic)
            else:
                return jsonify({'code':201,'message':'没有找到您搜索的商品'})
        elif sort==3:
            shops = ShopModel.query.order_by(ShopModel.sales.asc()).filter(ShopModel.title.like(content)).slice(start,end).all()
            if shops:
                shops_dic = []
                for shop in shops:
                    shops_dic.append(shop.to_dic())
                return jsonify(code=200, message=shops_dic)
            else:
                return jsonify({'code': 201, 'message': '没有找到您搜索的商品'})

    else:                                                                   #没有接受搜索条件
        if sort==3:
            shops=ShopModel.query.order_by(ShopModel.create_time.desc()).slice(start,end).all()
            shops_dic=[]
            for shop in shops:
                shops_dic.append(shop.to_dic())
            return jsonify({'code':202,'message':shops_dic})
        elif sort==2:
            shops=ShopModel.query.order_by(ShopModel.price.desc()).slice(start,end).all()
            shops_dic = []
            for shop in shops:
                shops_dic.append(shop.to_dic())
            return jsonify({'code': 202, 'message': shops_dic})
        elif sort==3:
            shops = ShopModel.query.order_by(ShopModel.Sales.asc()).slice(start,end).all()
            shops_dic = []
            for shop in shops:
                shops_dic.append(shop.to_dic())
            return jsonify({'code': 202, 'message': shops_dic})




