import pymysql  # 导入 pymysql

# 打开数据库连接
dbMy = pymysql.connect(host="localhost", user="root",
                     password="", db="bike", port=3307)

# 使用cursor()方法获取操作游标
cur = dbMy.cursor()

# 1.查询操作
# 编写sql 查询语句  user 对应我的表名
# sql = "UPDATE cart_goods_middle SET number =number+1 WHERE cart_id =8 and goods_id=3"
# try:
#     res=cur.execute(sql)  # 执行sql语句
#     print(res)
#     dbMy.commit()
#     # results = cur.fetchall()  # 获取查询的所有记录
#     # print(results)
#     # 遍历结果
#     # for row in results:
#     #     id = row[0]
#     #     name = row[1]
#     #     password = row[2]
#     #     print(id, name, password)
# except Exception as e:
#     raise e
# finally:
#     db.close()  # 关闭连接