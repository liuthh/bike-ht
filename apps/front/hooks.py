from . import  bp
from flask import session,g
from apps.front.models import UserModel
import config

@bp.before_request                  #钩子函数
def beforerequest():
    if config.User in session:
        user_id=session.get(config.User)
        front_user=UserModel.query.get(user_id)
        if front_user:
            g.front_user=front_user

