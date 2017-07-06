import os
from flask import Flask, redirect, url_for
from flask_login import current_user
from flask_principal import identity_loaded, UserNeed, RoleNeed
from sqlalchemy import event
from controllers.blog import blog_blueprint
from controllers.main import main_blueprint
from webapp.extensions import (
    bcrypt,
    oid,
    login_manager,
    principals,
    rest_api,
    celery,
    debug_toolbar,
    cache,
    assets_env,
    main_js,
    main_css,
    admin,
    mail
)
from webapp.tasks import on_reminder_save
from webapp.models import db, Reminder, User, Post, Role, Comment, Tag
from .controllers.rest.post import PostApi
from .controllers.rest.auth import AuthApi
from webapp.controllers.admin import (
    CustomView,
    CustomModelView,
    PostView,
    CustomFileAdmin
)


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    event.listen(Reminder, 'after_insert', on_reminder_save)
    bcrypt.init_app(app)
    oid.init_app(app)
    login_manager.init_app(app)
    principals.init_app(app)
    rest_api.add_resource(
        PostApi,
        '/api/post',
        '/api/post/<int:post_id>',
        endpoint='api'
    )
    rest_api.add_resource(
        AuthApi,
        '/api/auth',
        endpoint='auth'
    )
    rest_api.init_app(app)
    celery.init_app(app)
    debug_toolbar.init_app(app)
    cache.init_app(app)
    assets_env.init_app(app)
    assets_env.register("main_js", main_js)
    assets_env.register("main_css", main_css)
    admin.init_app(app)
    # admin.add_view(CustomView(name="Custom"))
    # models = [User, Role, Post, Comment, Tag, Reminder]
    # for model in models:
    #     if model is not Post:
    #         admin.add_view(
    #             CustomModelView(model, db.session, category="models")
    #         )
    #     else:
    #         admin.add_view(
    #             PostView(Post, db.session, category="models")
    #         )
    admin.add_view(CustomView(name='Custom'))
    admin.add_view(
        CustomModelView(
            User, db.session, category="Models"
        )
    )
    admin.add_view(
        CustomModelView(
            Role, db.session, category="Models"
        )
    )
    #
    # Need to use a special view for Posts to get the CKEditor functionality
    #
    admin.add_view(
        PostView(Post, db.session, category="Models")
    )
    admin.add_view(
        CustomModelView(
            Comment, db.session, category="Models"
        )
    )
    admin.add_view(
        CustomModelView(
            Tag, db.session, category="Models"
        )
    )
    admin.add_view(
        CustomModelView(
            Reminder, db.session, category="Models"
        )
    )
    admin.add_view(
        CustomFileAdmin(
            os.path.join(os.path.dirname(__file__), 'static'),
            '/static/',
            name='Static Files'
        )
    )
    mail.init_app(app)


    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

    #
    # Routes
    #
    @app.route('/')
    def index():
        return redirect(url_for('blog.home'))

    app.register_blueprint(blog_blueprint)
    app.register_blueprint(main_blueprint)

    return app
