from sqlalchemy import create_engine

# v1
engine = create_engine(
    "mysql://root:@localhost:3306/flask_seed?charset=utf8",
    echo=True,
)

# v2
engine_future = create_engine(
    "mysql://root:@localhost:3306/flask_seed?charset=utf8",
    echo=True,
    future=True,
)
