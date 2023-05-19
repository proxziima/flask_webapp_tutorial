from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager   # Gerencia o login do usuário

db = SQLAlchemy()           # Instancia o banco de dados
DB_NAME = "database.db "    # Nome do banco de dados

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abcdef'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'   # Configura o banco de dados. /// = caminho relativo ao arquivo atual
    db.init_app(app)        # Inicializa o banco de dados

    

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')       # Registra o blueprint views com o prefixo / (raiz)
    app.register_blueprint(auth, url_prefix='/')    # Registra o blueprint auth com o prefixo / (raiz)

    from .models import User, Note

    with app.app_context():
        db.create_all()     # Cria o banco de dados

    login_manager = LoginManager() # Instancia o gerenciador de login
    login_manager.login_view = 'auth.login' # Define a página de login
    login_manager.init_app(app) # Inicializa o gerenciador de login

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  # Retorna o usuário com o id especificado

    return app

