from flask import (
    redirect,
    url_for,
    flash,
    session
)
from flask_bcrypt import Bcrypt
from flask_openid import OpenID
from flask_oauth import OAuth
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed
from flask_restful import Api
from flask_celery import Celery
from flask_debugtoolbar import DebugToolbarExtension
from flask_cache import Cache
from flask_assets import Environment, Bundle
from flask_admin import Admin
from flask_mail import Mail
from flask_youtube import Youtube
#
# For inline GZip-compression extension (in progress)
#
from flask import request
from gzip import GzipFile
from io import BytesIO


bcrypt = Bcrypt()
oid = OpenID()
oauth = OAuth()
login_manager = LoginManager()
principals = Principal()
rest_api = Api()
celery = Celery()
debug_toolbar = DebugToolbarExtension()
cache = Cache()
assets_env = Environment()
admin = Admin()
mail = Mail()
youtube_ext = Youtube()

login_manager.login_view = "main.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"

admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))


@login_manager.user_loader
def load_user(userid):
    from models import User
    return User.query.get(userid)


@oid.after_login
def create_or_login(resp):
    from models import db, User
    username = resp.fullname or resp.nickname or resp.email
    if not username:
        flash('Invalid login. Please try again.', category='danger')
        return redirect(url_for('main.login'))
    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username)
        db.session.add(user)
        db.session.commit()
    #
    # Log the user in
    #
    return redirect(url_for('blog.home'))


facebook = oauth.remote_app(
    'facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key='784131115083402',
    consumer_secret='93835302657b088f25c095e811301b40',
    request_token_params={'scope': 'email'}
)

twitter = oauth.remote_app(
    'twitter',
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key='pCctFa1eMT1D8WOMfVPrxfSsZ',
    consumer_secret='a5lC1xmjeGBZAzCque228ifBypAE832E00SsRYdByxe5Zt1qPG'
)


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('facebook_oauth_token')


@twitter.tokengetter
def get_twitter_oauth_token():
    return session.get('twitter_oauth_token')


#
# Assets
#
main_css = Bundle(
    'css/bootstrap.css',
    filters='cssmin',
    output='css/common.css'
)

main_js = Bundle(
    'js/jquery.js',
    'js/bootstrap.js',
    filters='jsmin',
    output='js/common.js'
)


class GZip(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.after_request(self.after_request)

    def after_request(self, response):
        encoding = request.headers.get('Accept-Encoding', '')
        if 'gzip' not in encoding or response.status_code not in (200, 201):
            return response
        response.direct_passthrough = False
        contents = BytesIO()
        with GzipFile(mode='wb',
                      compresslevel=5,
                      fileobj=contents) as gzip_file:
            gzip_file.write(response.get_data())
        response.set_data(bytes(contents.getvalue()))
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = response.content_length
        return response


flask_gzip = GZip()
