from flask import redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from flask_openid import OpenID
from flask_oauth import OAuth

bcrypt = Bcrypt()
oid = OpenID()
oauth = OAuth()


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
