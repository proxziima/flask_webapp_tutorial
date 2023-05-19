from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required # Só pode acessar a página se estiver logado
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note) # Adiciona a nota ao banco de dados
            db.session.commit() # Salva as alterações
            flash('Note added!', category='success')
    return render_template("home.html.j2", user=current_user) # Renderiza a página home.html.j2 com o usuário atual