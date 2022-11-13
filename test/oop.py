from pymysql import connect, Error
from pymysql.cursors import DictCursor


class PyMySQL(object):
    def __init__(self):
        self.conn = self.get_connection()

    def get_one_data(self):
        with self.conn.cursor() as cursor:
            user_id = "1001"
            number = "imooc-test"
            sql = "SELECT * FROM users WHERE id = %s AND imooc_num = %s;"
            cursor.execute(sql, (user_id, number))
            result = cursor.fetchone()
        return result

    def delete_one_data(self, id):
        with self.conn.cursor() as cursor:
            sql = "DELETE FROM users where id = %s"
            cursor.execute(sql, (id))
            self.conn.commit()
            print("deleted")

    def get_connection(self):
        try:
            conn = connect(
                host="localhost",
                port=3306,
                user="root",
                password="",
                database="red_book",
                cursorclass=DictCursor,  # map it to dictionary
            )
            return conn
        except Error as e:
            print("build connection error: {}".format(e))
            return None

    def close_connection(self):
        try:
            if self.conn is not None:
                self.conn.close()
        except Exception as e:
            print("close connection error: {}".format(e))
            return None


def main():
    obj = PyMySQL()
    # result = obj.get_one_data()
    # print(result)

    obj.delete_one_data("1002")

    obj.close_connection()


if __name__ == "__main__":
    main()
