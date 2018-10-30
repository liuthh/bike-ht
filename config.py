# '''数据库连接配置'''
# host='127.0.0.1'
# username='root'
# passwd=''
# db='bike'
# port=3307
'''数据库连接配置'''
host='127.0.0.1'
username='root'
passwd='12345678'
db='bike'
port=3306


DB_URI='mysql+pymysql://{username}:{passwd}@{host}:{port}/{db}?charset=utf8' \
       ''.format(username=username,passwd=passwd,host=host,port=port,db=db)
SQLALCHEMY_DATABASE_URI=DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS=False

import os
SECRET_KEY='fhdsfdhsfdksfjkdasjfldkas'     #加盐



# 用来存放前台用户的session
User='fsjflksdfjakdjfksdf'