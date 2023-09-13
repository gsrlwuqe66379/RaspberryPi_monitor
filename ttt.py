# -*- coding: UTF-8 -*-
# 导入psycopg2包
import time
import psycopg2
from random import choice, randint


print("wait")

# 连接到一个给定的数据库
conn = psycopg2.connect(
                        database="postgres",
                        user="postgres",
                        password="11111111",
                        host="192.168.1.106",
                        port="5432")
                        
cursor = conn.cursor()


def insert_batch():
    
    t = time.time()
    values = []
    name = "猪腿肉 羊肉 鸡排 牛 骨头肉 付谕葱 孙成好 邓克罂".split(" ")
    for i in range(10):
        values.append("('{}',{},{})".format(choice(name), randint(1, 100), randint(1, 100)))
    sql = "insert into sell (name, weight, unitprice) values " + ",".join(values)
    cursor.execute(sql)
    conn.commit()
    #print("insert batch用时: {}".format(time.time() - t))
    


if __name__ == '__main__':
    try:

        insert_batch()
        print("Finish")
    except Exception as e:
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()
        raise e
    