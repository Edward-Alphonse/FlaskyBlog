from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# 解决js fetch请求跨域问题
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type,Access-Token"
    return resp



def create_app(config_name):
    app = Flask(__name__)
    app.after_request(after_request)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint, url_prefix='/profile')

    from .blog import blog as blog_blueprint
    app.register_blueprint(blog_blueprint, url_prefix='/blog')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
