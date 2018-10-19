from functools import wraps
import config
from flask import session,jsonify


def RequestLogin(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if config.User in session:
            return func(*args,**kwargs)
        else:
            return jsonify({'code':305,'message':'必须登录'})
    return inner