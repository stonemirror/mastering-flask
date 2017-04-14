class Config(object):
    SECRET_KEY = '03c06f3217375956eda2f9075923ac88'
    RECAPTCHA_PUBLIC_KEY = '6LfOcBsUAAAAACkJQTraRQ3zamopYQxIljoNCKvV'
    RECAPTCHA_PRIVATE_KEY = '6LfOcBsUAAAAAKFO3YdVkjkBLJvyOXYLps4L_24y'


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://mflaskUser:i@T4GG&IBWW3x^@localhost/mflaskDB"
