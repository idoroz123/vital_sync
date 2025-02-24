import os


class Base(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URL")


class Local(Base):
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DB_URL")
        or "postgresql://postgres:postgres@127.0.0.1:5432/postgres"
    )
    DEBUG = True


class Test(Local):
    USING_TEST_CONFIG = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DB_URL")
        or "postgresql://postgres:postgres@127.0.0.1:5432/postgres_test"
    )
