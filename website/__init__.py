from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abcdef'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')       # Registra o blueprint views com o prefixo / (raiz)
    app.register_blueprint(auth, url_prefix='/')    # Registra o blueprint auth com o prefixo / (raiz)


    return app
