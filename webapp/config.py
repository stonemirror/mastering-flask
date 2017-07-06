from celery.schedules import crontab


class Config(object):
    SECRET_KEY = '03c06f3217375956eda2f9075923ac88'
    RECAPTCHA_PUBLIC_KEY = '6LfOcBsUAAAAACkJQTraRQ3zamopYQxIljoNCKvV'
    RECAPTCHA_PRIVATE_KEY = '6LfOcBsUAAAAAKFO3YdVkjkBLJvyOXYLps4L_24y'


class ProdConfig(Config):
    CACHE_TYPE = 'simple'


class DevConfig(Config):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://mflaskUser:i@T4GG&IBWW3x^@localhost/mflaskDB"
    CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"
    CELERY_BACKEND_URL = "amqp://guest:guest@localhost:5672//"
    CELERY_RESULT_BACKEND = "amqp://"
    CELERYBEAT_SCHEDULE = {
        'weekly-digest': {
            'task': 'webapp.tasks.digest',
            'schedule': crontab(day_of_week=6, hour='10')
        }
    }
    CACHE_TYPE = 'null'
    ASSETS_DEBUG = True
    MAIL_SERVER = 'mail.mcfate.us'
    MAIL_USERNAME = 'mcfate@mcfate.us'
    MAIL_PASSWORD = '8zLlaD&2OLMy3%'
