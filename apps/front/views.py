import json
import random
import config
import math
from .pymysql_ import *
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
                    Verify_resetpassword,
                    Verify_GenerateOrder,
                    Verify_aCart,
                    Verify_dCart,
                    Verify_apost,
                    Verify_refer_Verify,
                    Verify_aAddress
                    )
from apps.models import (
                         GoodsModel,
                         AddressModel,
                         OrderModel,
                         CartModel,
                         PostModel,
                         cart_goods_middle,
                         OrderModel,
                         StatusEnum,
                         GoodsT_Model,
                         )
from exts import db
from .models import UserModel
from .decorators import RequestLogin
from config import User


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
                    session[User] = user.id
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




@bp.route('/searchShop/',methods=['GET'])                      #搜索商品
def searchShop():
    '''
    ：param:   content(搜索内容)    String
               PAGE               String
               Sort               string
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
    page=int(page)
    start = (page - 1) * 8
    end = start + 8
    sort=int(sort)
    if content:
        content='%'+content+'%'
        if sort==1:
            shops=GoodsModel.query.order_by(GoodsModel.create_time.desc()).filter(GoodsModel.title.like(content)).slice(start,end).all()
            if shops:
                count=GoodsModel.query.filter(GoodsModel.title.like(content)).count()
                page=math.ceil(count/8.0)
                count={'page':page}
                shops_dic=[]
                for shop in shops:
                    shops_dic.append(shop.to_dic())
                return jsonify({'code':200,'message':shops_dic,'page':count})
            else:
                return jsonify({'code':201,'message':'没有找到您搜索的商品'})
        elif sort==2:
            shops=GoodsModel.query.order_by(GoodsModel.price.desc()).filter(GoodsModel.title.like(content)).slice(start,end).all()
            if shops:
                count = GoodsModel.query.filter(GoodsModel.title.like(content)).count()
                page = math.ceil(count / 8.0)
                count = {'page': page}
                shops_dic=[]
                for shop in shops:
                    shops_dic.append(shop.to_dic())
                return jsonify({'code':200,'message':shops_dic,'page':count})

            else:
                return jsonify({'code':201,'message':'没有找到您搜索的商品'})
        elif sort==3:
            shops = GoodsModel.query.order_by(GoodsModel.sales.asc()).filter(GoodsModel.title.like(content)).slice(start,end).all()
            if shops:
                count = GoodsModel.query.filter(GoodsModel.title.like(content)).count()
                page = math.ceil(count / 8.0)
                count = {'page': page}
                shops_dic = []
                for shop in shops:
                    shops_dic.append(shop.to_dic())
                return jsonify({'code':200,'message':shops_dic,'page':count})
            else:
                return jsonify({'code': 201, 'message': '没有找到您搜索的商品'})

    else:                                                                   #没有接受搜索条件
        count = GoodsModel.query.count()
        page = math.ceil(count / 8.0)
        print(page)
        count = {'page': page}
        if sort==1:
            shops=GoodsModel.query.order_by(GoodsModel.create_time.desc()).slice(start,end).all()
            shops_dic=[]
            for shop in shops:
                shops_dic.append(shop.to_dic())
            return jsonify({'code':202,'message':shops_dic,'page':count})
        elif sort==2:
            shops=GoodsModel.query.order_by(GoodsModel.price.desc()).slice(start,end).all()
            shops_dic = []
            for shop in shops:
                shops_dic.append(shop.to_dic())
            return jsonify({'code': 202, 'message': shops_dic,'page':count})
        elif sort==3:
            shops = GoodsModel.query.order_by(GoodsModel.Sales.asc()).slice(start,end).all()
            shops_dic = []
            for shop in shops:
                shops_dic.append(shop.to_dic())
            return jsonify({'code': 202, 'message': shops_dic,'page':count})



@bp.route('/getSpDetial/',methods=['GET'])                       #进入商品详情页
def getSpDetial():
    '''
    :param      商品id(spId)          string
    :return:    412:  接受商品
                404:  该商品已经删除或者不存在
                200:  成功返回该商品（good）,商品图片(good_imgs)
    '''
    spId=request.args.get('spId')
    spId=int(spId)
    if spId:
        Goods=GoodsModel.query.filter_by(id=spId).first()
        if Goods:
            good=Goods.to_dic()
            good_imgs=good.goods_img
            good_imgs_dic=[]
            for good_img in good_imgs:
                good_imgs_dic.append(good_img.to_dic())
            return jsonify({'code':200,'good':good,'good_imgs':good_imgs_dic})
        else:
            return jsonify({'code':404,'message':'不存在该商品'})
    else:
        return jsonify({'code':412,'message':'接受参数错误'})


@bp.route('/genarateOrder/',methods=['POST','GET'])             #生成订单
@RequestLogin
def genarateOrder():
    '''
    :param:    商品的id(good_id)
    :return:   code  305   必须登录
               code  412   表单验证失败，返回具体错误信息
               code  200   返回该商品信息(set)    返回当前用户的所有地址(list)
    '''
    if request.method=='GET':
        good_id=request.args.get('good_id')
        if good_id:
            good=GoodsModel.query.get(good_id)
            good_dic=good.to_dic()
            user=g.front_user
            addresses=user.addresses
            addresses_dic=[]                        #用户的所有地址
            for address in addresses:
                addresses_dic.append(address.to_dic())
            return jsonify({'code':200,'good_dic':good_dic,'addresses_dic':addresses_dic})
        else:
            return jsonify({'code':404,'message':'不存在该商品'})
    else:                                            #post方法
        '''
        :param: 数量（number），商品总价（price）,商品编号（good_id）,收货地址编号（address_id）
        :return:   code  305   必须登录
                   code  412   表单验证有错误
                   code  411   没有数据库未找到
                   code  200   返回该商品信息(set)    返回当前用户的所有地址(list)
        '''
        form=Verify_GenerateOrder(request.form)
        if form.validate():
            number=form.number.data                 #商品数量
            price=form.price.data                   #商品价格
            good_id=form.good_id.data               #商品id
            address=form.address_id.data            #订单地址
            user=g.front_user                       #用户
            good=GoodsModel.query.filter_by(id=good_id).first()     #商品对象
            if good:
                address=AddressModel.query.filter_by(id=address).first()
                if address:
                    id=random.randrange(100000000,999999999)  #随机生成12位订单号
                    print(id)
                    order=OrderModel(id=id,number=number,good_price=price)
                    order.address=address
                    order.good=good
                    order.user=user
                    db.session.add(order)
                    db.session.commit()
                    order=order.to_dic()
                    return jsonify({'code':'200','message':'生成订单成功','order':order})
                else:
                    return jsonify({'code':411,'message':'地址传参错误'})
            else:
                return jsonify({'code':411,'message':'没有找到该商品'})
        else:
            message=form.errors.popitem()[0][1]                     #弹出表单验证第一条出错信息
            return jsonify({'code':412,'message':message})

@bp.route('/personal/',methods=['GET'])                             #个人信息                                     #个人中心
@RequestLogin
def personal():
    '''
    :return: code 305   用户未登陆
            code 200    返回用户信息
    '''
    user=g.front_user
    user=user.to_dic()
    return jsonify({'code':200,'message':user})




@bp.route('/delogin/')                              #注销登录                                                           #注销登录
@RequestLogin
def delogin():
    del session[config.User]
    return jsonify({'code':200,'message':'注销成功'})


@bp.route('/reSetPasswd/',methods=['POST'])         #修改密码                                      #修改密码
@RequestLogin
def reSetPasswd():
    '''
    :param:  null
    :return: code 412： 表单验证有问题
             code 401:  密码错误
             code 200:  修改密码成功
             code 305:   用户未登陆
    '''
    form=Verify_resetpassword(request.form)
    if form.validate():
        password=form.password.data
        newpassword=form.newpassword.data
        user=g.front_user
        if user.check_passwd(password):
            user.passwd=newpassword
            db.session.commit()
            return jsonify({'code':200,'message':'修改密码成功'})
        else:
            return jsonify({'code':401,'message':'密码错误'})
    else:
        message=form.errors.popitem()[0][1]                         #弹出表单验证失败第一条错误信息
        return jsonify({'code':412,'message':message})


@bp.route('/aCart/',methods=['POST'])                                #添加购物车
@RequestLogin
def aCart():
    '''
    :param:  goods_id(商品id),number(商品数量)
    :return: code  200    加入购物车成功
             code  411    该商品不存在或者已经下架
             code  412    表单验证失败
             code  305    用户未登陆
    '''
    form=Verify_aCart(request.form)
    if form:
        goods_id=form.goods_id.data
        number=form.number.data
        user=g.front_user
        goods=GoodsModel.query.filter_by(id=goods_id).first()          #查询是否有这件商品
        if goods:
            cart1=CartModel.query.filter_by(user_id=user.id).first()   #查询用户是否有购物车
            if cart1:
                if CartModel.query.filter_by(user_id=user.id,goods_id=goods.id).first():
                    sql = "UPDATE cart_goods_middle SET number =number+{} WHERE cart_id ={} and goods_id={}".format(number,cart1.id,goods.id)
                    res = cur.execute(sql)  # 执行sql语句
                    dbMy.commit()
                    return jsonify({'code':200,'message':'商品数量加1'})
                else:
                    cart1.goods.append(goods)
                    db.session.commit()
                    return jsonify({'code':201,'message':'添加购物车成功'})
            else:
                cart = CartModel()
                cart.user=user
                cart.user_id=user.id
                cart.goods_id = goods.id
                cart.goods.append(goods)
                db.session.add(cart)
                db.session.commit()
                return jsonify({'code': 200, 'message': '加入购物车成功'})
    else:
        message=form.errors.popitem()[0][1]                         #弹出表单验证失败第一条错误信息
        return jsonify({'code':412,'message':message})



@bp.route('/delGoods/',methods=['POST'])                                             #移除购物车商品
@RequestLogin
def delGoods():
    '''
    :param: 商品id(good_id)    0表示删除商品 1表示商品减1（types）
    :return:
            code 201    商品数量只剩下1
            code 202    商品-1成功
            code 200    删除商品成功
            code 411    购物车中不存在该商品
            code 412    表单验证失败
    '''
    form=Verify_dCart(request.form)
    if form.validate():
        goods_id=form.goods_id.data
        types=form.types.data
        user_id=g.front_user.id
        cart=CartModel.query.filter_by(user_id=user_id).first()
        gods = db.session.query(cart_goods_middle).filter_by(cart_id=cart.id, goods_id=goods_id).first()
        if types==1:
            count=gods.number
            if count<=1:
                return jsonify({'code':201,'message':'购物车商品只剩下1'})
            else:
                sql = "UPDATE cart_goods_middle SET number =number-1 WHERE cart_id ={} and goods_id={}".format(cart.id,goods_id)  # 查询购物车的这个商品
                res = cur.execute(sql)  # 执行sql语句
                dbMy.commit()
                return jsonify({'code':202,'message':'商品减1成功'})
        elif types==0:
            del cart
            db.session.commit()
            return jsonify({'code':200,'message':'删除商品成功'})
    else:
        message = form.errors.popitem()[0][1]                       # 弹出表单验证失败第一条错误信息
        return jsonify({'code': 412, 'message': message})



@bp.route('/postlist/',methods=['GET'])                               # 帖子列表接口（所有）
def postlist():
    posts1=PostModel.query.all()
    posts=[]
    for post in posts1:
        posts.append(post.to_dic())
    return jsonify({'code':200,'message':posts})


@bp.route('/apost/',methods=['POST'])                                 #发布帖子功能
@RequestLogin
def apost():
    '''

    :return:
    '''
    form=Verify_apost(request.form)
    if form.validate():
        title=form.title.data
        content=form.content.data
        user=g.front_user
        post=PostModel(title=title,content=content)
        post.author=user
        db.session.add(post)
        db.session.commit()
        return jsonify({'code':200,'message':'发布成功'})

    else:
        message = form.errors.popitem()[0][1]  # 弹出表单验证失败第一条错误信息
        return jsonify({'code': 412, 'message': message})



@bp.route('/catCart/',methods=['GET'])                                          # 查看购物车
@RequestLogin
def catCart():
    '''
    :return: 305 未登录
             200 成功
    '''
    user=g.front_user                           #获取当前登录用户
    cart=CartModel.query.filter_by(user_id=user.id).first()
    if cart:
        cart=user.cart                              #取到当前的购物车
        goods=cart.goods                            #获取购物车的所有商品
        goods_list=[]
        for good in goods:
            gods = db.session.query(cart_goods_middle).filter_by(cart_id=cart.id, goods_id=good.id).first()
            d={'number':gods.number}
            a=good.to_dic()
            a.update(d)
            goods_list.append(a)
        print(goods_list)
        return jsonify({'code':200,'message':goods_list})
    else:
        cart=CartModel(user_id=user.id)
        db.session.add(cart)
        db.session.commit()
        return jsonify({'code':201,'message':'购物车空'})
    
    
    

@bp.route('/referOrder/',methods=['POST'])                  # 支付订单
@RequestLogin
def referOrder():
    '''
    :param: passwd(用户密码)，order_code(订单编号)
    :return:
             200 成功
             414 余额不足
             413 密码错误
             412 表单验证错误
    '''
    form=Verify_refer_Verify(request.form)
    if form.validate():
        passwd=form.passwd.data
        order_code=form.order_code.data
        user=g.front_user
        if user.check_passwd(passwd=passwd):
            order=OrderModel.query.get(order_code)
            price=order.good_price*order.number
            if user.money>=price:
                user.money-=price
                order.status=StatusEnum.PAID
                db.session.commit()
                return jsonify({'code':200,'message':'支付成功'})
            else:
                return jsonify({'code':414,'message':'余额不足'})
        else:
            return jsonify({'code':413,'message':'密码错误'})
    else:
        message=form.errors.popitem()[1][0]
        return jsonify({'code':412,'message':message})



@bp.route('/myOrder/',methods=['GET'])                      # 我的订单
@RequestLogin                                               # 必须登录
def myOrder():
    user=g.front_user                                       #获取当前用户
    orders=OrderModel.query.filter_by(user_id=user.id).all()#查找当前用户所有订单
    order_dic=[]
    for order in orders:                                    #转换成字典返回给前端
        d=order.to_dic()
        print(d)
        order_dic.append(d)
    print(order_dic)
    return jsonify({'code':200,'message':order_dic})



@bp.route('/getTypeGoods/',methods=['GET'])                                             #获取指定类型商品
def getTypeGoods():
    '''
    :param:  type_id
    :return:
    '''
    type_id=request.args.get('type_id')
    type=GoodsT_Model.query.filter_by(id=type_id).first()
    if type:
        goods=type.goods
        goods_dic=[]
        for shop in goods:
            goods_dic.append(shop.to_dic())
        return jsonify({'code':200,'message':goods_dic})
    else:
        return jsonify({'code':412,'message':'不存在该类型商品'})



@bp.route('/MyAddress/',methods=['GET'])                                                                #我的地址
@RequestLogin
def MyAddress():
    user=g.front_user
    addresses=user.addresses
    addresses_dic=[]
    for address in addresses:
        addresses_dic.append(address.to_dic())
    return jsonify({'code':200,'message':addresses_dic})

@bp.route('/delAddress/',methods=['POST'])                                                                             #删除地址
@RequestLogin
def delAddress():
    address_id=request.form.get('rcAddress_id')
    user=g.front_user
    addresses=user.addresses
    for address in addresses:
        if address.id==address_id:
            address=AddressModel.query.get(address.id)
            del address
            db.session.commit()
            return jsonify({'code':200,'message':'删除成功'})
    return jsonify({'code':404,'message':'该地址不存在或者已经被删除'})

@bp.route('/aAddress/',methods=['POST'])                                                               #添加地址
@RequestLogin
def aAddress():
    '''
    :param:  mobile(手机号), name（收货人姓名），address 收货地址
    :return:
    '''
    form =Verify_aAddress(request.form)
    if form.validate():
        mobile=form.mobile.data
        name=form.name.data
        address=form.address.data
        user = g.front_user
        newaddress=AddressModel(user_id=user.id,rcMobile=mobile,rcName=name,rcAddress=address)
        db.session.add(newaddress)
        db.session.commit()
        return jsonify({'code':200,'message':'添加新地址成功'})
    else:
        message = form.errors.popitem()[1][0]
        return jsonify({'code': 412, 'message': message})












