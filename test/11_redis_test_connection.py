import redis


def get_connection():
    connection = redis.Redis(
        host="localhost",
        password="",
        port=6379,
        db=0,
    )
    return connection


def get_connection_by_pool():
    """auto close connection, release back to pool"""
    pool = redis.ConnectionPool(
        host="localhost",
        password="",
        port=6379,
        db=0,
        max_connections=20,
    )
    connection = redis.Redis(
        connection_pool=pool,
    )
    return connection


def close_connection(connection):
    connection.close()


def main():
    connection = get_connection_by_pool()
    connection.set("roytest2", 666666)
    close_connection(connection)


if __name__ == "__main__":
    main()
