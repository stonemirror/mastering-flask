from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    session
)
from webapp.forms import LoginForm, RegisterForm, OpenIDForm
from webapp.models import db, User
from webapp.extensions import oid, facebook, twitter
from os import path

main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder=path.join(path.pardir, 'templates', 'main'),
)


@main_blueprint.route('/')
def index():
    return redirect(url_for('blog.home'))


@main_blueprint.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    form = LoginForm()
    openid_form = OpenIDForm()
    if openid_form.validate_on_submit():
        return oid.try_login(
            openid_form.openid.data,
            ask_for=['nickname', 'email'],
            ask_for_optional=['fullname']
        )

    if form.validate_on_submit():
        session['username'] = form.username.data
        flash("You have been logged in.", category="success")
        return redirect(url_for('blog.home'))

    openid_errors = oid.fetch_error()
    if openid_errors:
        flash(openid_errors, category="danger")

    return render_template(
        'login.html',
        form=form,
        openid_form=openid_form
    )


@main_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    flash("You have been logged out.", category="success")
    session.pop('username', None)
    return redirect(url_for('blog.home'))


@main_blueprint.route('/register', methods=['GET', 'POST'])
@oid.loginhandler
def register():
    form = RegisterForm()
    openid_form = OpenIDForm()
    if openid_form.validate_on_submit():
        return oid.try_login(
            openid_form.openid.data,
            ask_for=['nickname', 'email'],
            ask_for_optional=['fullname']
        )

    if form.validate_on_submit():
        new_user = User(form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash(
            "Your user has been created, please log in.",
            category="success"
        )
        return redirect(url_for('.login'))
    openid_errors = oid.fetch_error()
    if openid_errors:
        flash(openid_errors, category="danger")

    return render_template(
        'register.html',
        form=form,
        openid_form=openid_form
    )


@main_blueprint.route('/facebook')
def facebook_login():
    return facebook.authorize(
        callback=url_for(
            '.facebook_authorized',
            next=request.referrer or None,
            _external=True
        )
    )


@main_blueprint.route('/facebook/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['facebook_oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    user = User.query.filter_by(username=me.data['name']).first()
    if not user:
        user = User(me.data['name'])
        db.session.add(user)
        db.session.commit()
    #
    # Login user here
    #
    flash('You have been logged in.', category="success")
    return redirect(
        request.args.get('next') or url_for('blog.home')
    )


@main_blueprint.route('/twitter-login')
def twitter_login():
    response = twitter.authorize(
        callback=url_for(
            '.twitter_authorized',
            next=request.referrer or None,
            _external=True
        )
    )
    return response


@main_blueprint.route('/twitter-login/authorized')
@twitter.authorized_handler
def twitter_authorized(resp):
    if resp is None:
            return 'Access denied: reason=%s error=%s' % (
                request.args['error_reason'],
                request.args['error_description']
            )
    session['twitter_oauth_token'] = resp['oauth_token'] +\
        resp['oauth_token_secret']
    user = User.query.filter_by(
        username=resp['screen_name']
    ).first()
    if not user:
        user = User(resp['screen_name'])
        db.session.add(user)
        db.session.commit()
    #
    # Login user here
    #
    flash('You have been logged in.', category='success')
    return redirect(
        request.args.get('next') or url_for('blog.home')
    )
