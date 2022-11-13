from pymysql import connect, Error

conn = None
try:
    conn = connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="red_book",
    )
    cursor = conn.cursor()
    # crud
    cursor.close()
except Error as e:
    print("connection error: {}".format(e))
finally:
    try:
        conn.close()
        print("connection closed")
    except Exception as e:
        print("connection close error: {}".format(e))
