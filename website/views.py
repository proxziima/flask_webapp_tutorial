from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from .models import Note
import json
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

@views.route('delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) # Carrega a nota que será deletada
    noteId = note['noteId'] # Pega o id da nota
    note = Note.query.get(noteId) # Pega a nota do banco de dados
    if note:
        if note.user_id == current_user.id: # Verifica se o usuário atual é o dono da nota
            db.session.delete(note) # Deleta a nota do banco de dados
            db.session.commit() # Salva as alterações
    return jsonify({}) # Retorna um json vazio
