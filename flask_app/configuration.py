class BaseConfig(object):
    'Base configuracion'
    USER_APP_NAME = 'FlaskMalcen'
    SECRET_KEY = 'Key'
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:PepeLePew7@localhost:3306/pyalmacen"
    RECAPTCHA_PUBLIC_KEY='6LffHtEUAAAAAI_KcKj6Au3R-bwhqRhPGe-WhHq_'
    RECAPTCHA_PRIVATE_KEY='6LffHtEUAAAAAJdHhV9e8yLOSB12rm8WW8CMxN7X'
    BABEL_TRANSLATION_DIRECTORIES='/Users/andrescruz/Desktop/flask/4_flask_app/flask_app/translations'
    USER_ENABLE_EMAIL=True
    #WTF_CSRF_TIME_LIMIT = 10
class ProductionConfig(BaseConfig):
    'Produccion configuracion'
    DEBUG = False
class DevelopmentConfig(BaseConfig):
    'Desarrollo configuracion'
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'as54556ad4a56sd454d5gf56sd74f/8f56sd4f541ad45as4d4a5sd45a4sd6a'
    MAIL_SUPPRESS_SEND = False
    MAIL_SERVER = "smtp.mailtrap.io"
    MAIL_PORT = 2525
    MAIL_USERNAME="ec5cbede982042"
    MAIL_PASSWORD="08243f07fb0be7"
    #MAIL_DEFAULT_SENDER=('andres de DL',"andres@gmail.com")
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False
    USER_EMAIL_SENDER_EMAIL="andres@gmail.com"
    CACHE_TYPE = "simple"
    FACEBOOK_OAUTH_CLIENT_ID = 202215285023005
    FACEBOOK_OAUTH_CLIENT_SECRET = "bd5d15fdfe0a7f0ed791232b2267f426"