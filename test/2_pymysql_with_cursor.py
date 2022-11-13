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
            user_id = "1001"
            number = "imooc-test"
            sql = "SELECT * FROM red_book.users WHERE id = %s AND imooc_num = %s;"
            cursor.execute(sql, (user_id, number))
            # 1. print all
            # for item in cursor:
            #     print("item: {}".format(item))
            print("-----------------------")
            print("-----------------------")
            print("-----------------------")
            # 2. fetch one by one
            # first_row = cursor.fetchone()
            # second_row = cursor.fetchone()
            # print(first_row)
            # print(second_row)
            print("-----------------------")
            print("-----------------------")
            print("-----------------------")
            # 3. fetch all
            # all_rows = cursor.fetchall()
            # for item in all_rows:
            #     print(item)
            print("-----------------------")
            print("-----------------------")
            print("-----------------------")
            # 4. fetch spcific number of rows
            data_list = cursor.fetchmany(3)
            for item in data_list:
                print("nickname: {}".format(item["nickname"]))
except Error as e:
    print("connection error: {}".format(e))
