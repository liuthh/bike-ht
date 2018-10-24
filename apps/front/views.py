import json
import random
import config
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
                    Verify_apost
                    )
from apps.models import (
                         GoodsModel,
                         AddressModel,
                         OrderModel,
                         CartModel,
                         PostModel
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
                shops_dic=[]
                for shop in shops:
                    shops_dic.append(shop.to_dic())
                return jsonify(code=200,message=shops_dic)
            else:
                return jsonify({'code':201,'message':'没有找到您搜索的商品'})
        elif sort==2:
            shops=GoodsModel.query.order_by(GoodsModel.price.desc()).filter(GoodsModel.title.like(content)).slice(start,end).all()
            if shops:
                shops_dic=[]
                for shop in shops:
                    shops_dic.append(shop.to_dic())
                return jsonify(code=200,message=shops_dic)
            else:
                return jsonify({'code':201,'message':'没有找到您搜索的商品'})
        elif sort==3:
            shops = GoodsModel.query.order_by(GoodsModel.sales.asc()).filter(GoodsModel.title.like(content)).slice(start,end).all()
            if shops:
                shops_dic = []
                for shop in shops:
                    shops_dic.append(shop.to_dic())
                return jsonify(code=200, message=shops_dic)
            else:
                return jsonify({'code': 201, 'message': '没有找到您搜索的商品'})

    else:                                                                   #没有接受搜索条件
        if sort==1:
            shops=GoodsModel.query.order_by(GoodsModel.create_time.desc()).slice(start,end).all()
            shops_dic=[]
            for shop in shops:
                shops_dic.append(shop.to_dic())
            return jsonify({'code':202,'message':shops_dic})
        elif sort==2:
            shops=GoodsModel.query.order_by(GoodsModel.price.desc()).slice(start,end).all()
            shops_dic = []
            for shop in shops:
                shops_dic.append(shop.to_dic())
            return jsonify({'code': 202, 'message': shops_dic})
        elif sort==3:
            shops = GoodsModel.query.order_by(GoodsModel.Sales.asc()).slice(start,end).all()
            shops_dic = []
            for shop in shops:
                shops_dic.append(shop.to_dic())
            return jsonify({'code': 202, 'message': shops_dic})



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
            # user=UserModel.query.get(1)                  #测试数据
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
        print('ok')
        form=Verify_GenerateOrder(request.form)
        if form.validate():
            print('123')
            number=form.number.data
            price=form.price.data
            good_id=form.good_id.data
            address=form.address_id.data
            # user=g.front_user
            user=UserModel.query.get(1)                  #测试数据
            print(1)
            good=GoodsModel.query.filter_by(id=good_id).first()     #商品对象
            if good:
                address=AddressModel.query.filter_by(id=address).first()
                if address:
                    id=random.randrange(100000000000,999999999999)  #随机生成12位订单号
                    order=OrderModel(id=id,number=number,good_price=price)
                    print(1)
                    order.address=address
                    order.good=good
                    order.user=user
                    print(2)
                    db.session.add(order)
                    print(order)
                    db.session.commit()
                    return jsonify({'code':'200','message':'生成订单成功','id':id})
                else:
                    return jsonify({'code':411,'message':'地址传参错误'})
            else:
                return jsonify({'code':411,'message':'没有找到该商品'})
        else:
            message=form.errors.popitem()[0][1]                     #弹出表单验证第一条出错信息
            return jsonify({'code':412,'message':message})

@bp.route('/personal/',methods=['GET'])                                           #个人中心
@RequestLogin
def personal():
    '''
    :return: code 305   用户未登陆
            code 200    注销成功
    '''
    user=g.front_user
    user=user.to_dic()
    return jsonify({'code':200,'message':user})




@bp.route('/delogin/')                                                              #注销登录
@RequestLogin
def delogin():
    del session[config.User]
    return jsonify({'code':200,'message':'注销成功'})


@bp.route('/reSetPasswd/',methods=['POST'])                                          #修改密码
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
    :param:  goods_id(商品id)
    :return: code  200    加入购物车成功
             code  411    该商品不存在或者已经下架
             code  412    表单验证失败
             code  305    用户未登陆
    '''
    form=Verify_aCart(request.form)
    if form:
        number=1                                                        #默认加入购物车商品1件
        goods_id=form.goods_id.data
        user=g.front_user
        goods=GoodsModel.query.filter_by(id=goods_id).first()          #查询是否有这件商品
        if goods:
            cart1=CartModel.query.filter_by(goods_id=goods_id).first()#判断这件商品用户的购物车中是否已存在
            if cart1:
                cart1.number+=1
                db.session.commit()
                return jsonify({'code':200,'message':'商品数量加1'})
            else:
                cart = CartModel(number=number)
                cart.user = user
                cart.goods = goods
                db.session.add(cart)
                db.session.commit()
                return jsonify({'code': 200, 'message': '加入购物车成功'})
        else:
            return jsonify({'code':411,'message':'该商品已下架，或者不存在'})
    else:
        message=form.errors.popitem()[0][1]                         #弹出表单验证失败第一条错误信息
        return jsonify({'code':412,'message':message})



@bp.route('/delGoods/',methods=['POST'])                                             #移除购物车商品
@RequestLogin
def delGoods():
    '''
    :param: 商品id(good_id)    1表示删除商品 0表示商品减1（types）
    :return:
            code 201    商品数量只剩下1
            code 202    商品-1成功
            code 200    删除商品成功
            code 411    购物车中不存在该商品
            code 412    表单验证失败
    '''
    form=Verify_dCart(request.form)
    if form:
        goods_id=form.goods_id.data
        types=form.types.data
        user_id=g.front_user.id
        cart=CartModel.query.filter_by(goods_id=goods_id,user_id=user_id).first() #查询购物车的这个商品
        if cart:
            if types==1:
                count=cart.number
                if count<=1:
                    return jsonify({'code':201,'message':'购物车商品只剩下1'})
                else:
                    cart.number-=1
                    db.session.commit()
                    return jsonify({'code':202,'message':'商品减1成功'})
            else:
                del cart
                db.session.commit()
                return jsonify({'code':200,'message':'删除商品成功'})
        else:
            return jsonify({'code':411,'message':'购物车中不存在该商品'})
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


@bp.route('/apost/')                                                   #发布帖子功能
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













