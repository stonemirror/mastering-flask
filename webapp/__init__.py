from flask import Flask, redirect, url_for
from controllers.blog import blog_blueprint
from controllers.main import main_blueprint
from webapp.extensions import bcrypt
from models import db


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    bcrypt.init_app(app)

    #
    # Routes
    #
    @app.route('/')
    def index():
        return redirect(url_for('blog.home'))

    app.register_blueprint(blog_blueprint)
    app.register_blueprint(main_blueprint)

    return app