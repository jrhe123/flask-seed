from pymysql import connect, Error
from pymysql.cursors import DictCursor

conn = None
try:
    conn = connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="red_book",
        cursorclass=DictCursor,  # map it to dictionary
    )
    with conn:
        with conn.cursor() as cursor:
            # 1. insert
            # user_id = "1004"
            # mobile = "1231231237"
            # fields = "id, mobile, nickname, imooc_num, face, sex, birthday, country, province, city, district, description, bg_img, can_imooc_num_be_updated, created_time, updated_time"
            # sql = 'INSERT INTO users ({}) VALUES (%s, %s, "roytest", "55555", "www.google.ca", "2", "2022-01-01", "canada", "ontario", "toronto", "markham", "my desc", "www.google.ca", 0, "2021-09-29 23:44:51", "2021-09-29 23:44:51");'.format(
            #     fields
            # )
            # cursor.execute(sql, (user_id, mobile))
            # conn.commit()
            # print("+++: sql inserted")
            # 1.1 batch insert
            # fields = "id, mobile, nickname, imooc_num, face, sex, birthday, country, province, city, district, description, bg_img, can_imooc_num_be_updated, created_time, updated_time"
            # sql = 'INSERT INTO users ({}) VALUES (%s, %s, "roytest", "55555", "www.google.ca", "2", "2022-01-01", "canada", "ontario", "toronto", "markham", "my desc", "www.google.ca", 0, "2021-09-29 23:44:51", "2021-09-29 23:44:51");'.format(
            #     fields
            # )
            # data_list = (("1005", "1231231238"), ("1006", "1231231239"))
            # cursor.executemany(sql, data_list)
            # conn.commit()
            # print("+++: sql batch inserted")
            # 2. update
            # update_mobile = "13961111111"
            # sql = "UPDATE users SET mobile = %s WHERE id = '1001'"
            # cursor.execute(sql, (update_mobile))
            # conn.commit()
            # print("+++: sql updated")

            pass
except Error as e:
    print("connection error: {}".format(e))
