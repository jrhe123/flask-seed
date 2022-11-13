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
            fields = "id, mobile, nickname, imooc_num, face, sex, birthday, country, province, city, district, description, bg_img, can_imooc_num_be_updated, created_time, updated_time"
            sql = 'INSERT INTO users ({}) VALUES (%s, %s, "roytest", "55555", "www.google.ca", "2", "2022-01-01", "canada", "ontario", "toronto", "markham", "my desc", "www.google.ca", 0, "2021-09-29 23:44:51", "2021-09-29 23:44:51");'.format(
                fields
            )
            # start
            conn.begin()
            # step 1:
            try:
                cursor.execute(sql, ("2001", "1231231288"))
                print("executed 1")
            except Exception as e:
                conn.rollback()
                print("e1: ".format(e))
                print("roll back all in e1")

            # step 2:
            try:
                cursor.execute(sql, ("2001", "1231231288"))
                print("executed 2")
            except Exception as e:
                conn.rollback()
                print("e2: ".format(e))
                print("roll back all in e2")

            # commit
            conn.commit()
except Error as e:
    print("connection error: {}".format(e))
