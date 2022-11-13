reset python version:

1. brew install pyenv
2. pyenv install 3.11.0
3. pyenv global 3.11.0
4. pyenv version
5. echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
6. exec $0
7. which python
8. python -V
9. pip -V


create tables:
# from db_engine import engine
# from user_models import Base
# Base.metadata.create_all(engine)
# Base.metadata.drop_all(engine)

many-to-many:
https://stackoverflow.com/questions/63298753/sqlalchemy-many-to-many-dynamic-lazyload-not-returning-appenderquery

docs:
https://docs.sqlalchemy.org/en/14/orm/collections.html