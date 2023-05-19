from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
@login_required # Só pode acessar a página se estiver logado
def home():
    return render_template("home.html.j2", user=current_user) # Renderiza a página home.html.j2 com o usuário atual