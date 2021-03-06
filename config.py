class Config():
    DEBUG = False
    TESTING = False

    DB_NAME = "logistics_company"
    DB_USERNAME = "root"
    DB_PASSWORD = "1234"
    DB_HOST = "localhost"
    DB_PORT = 3306

    SQLALCHEMY_DATABASE_URI = f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = "0bc71b528deccf5539be21de6be4d3de241c593cd5caa7403082d7fc72fcbce4"

    PRICE_PER_KG = 2
    PRICE_SHIPMENT_FROM_ADDRESS = 2
    PRICE_SHIPMENT_TO_ADDRESS = 5
    PRICE_EXPRESS_OFFICE = 10
    PRICE_EXPRESS_ADDRESS = 15

    REDIRECT_QUERY_PARAM = "redirect_handler"

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True
    TEST_DATABASE_PREFIX = "sqlite:///"


env_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}