from . import db                                     # Importa o banco de dados do arquivo __init__.py
from flask_login import UserMixin                    # Importa a classe UserMixin do flask_login
from sqlalchemy.sql import func               # Importa a função func do sqlalchemy


class Note(db.Model):                                # Cria a classe Note que herda de db.Model
    id = db.Column(db.Integer, primary_key=True)     # Cria a coluna id do tipo inteiro e chave primária
    data = db.Column(db.String(10000))                              # Cria a coluna data do tipo string com tamanho máximo de 100 caracteres
    date = db.Column(db.DateTime(timezone=True), default=func.now())   # Cria a coluna date do tipo datetime com timezone e valor padrão de agora
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))         # Cria a coluna user_id do tipo inteiro e chave estrangeira da coluna id da tabela user

class User(db.Model, UserMixin):                     # Cria a classe User que herda de db.Model e UserMixin
    id = db.Column(db.Integer, primary_key=True)     # Cria a coluna id do tipo inteiro e chave primária
    email = db.Column(db.String(150), unique=True)   # Cria a coluna email do tipo string com tamanho máximo de 150 caracteres e que não pode ser repetida
    password = db.Column(db.String(150))             # Cria a coluna password do tipo string com tamanho máximo de 150 caracteres
    first_name = db.Column(db.String(150))           # Cria a coluna first_name do tipo string com tamanho máximo de 150 caracteres
    notes = db.relationship('Note')                  # Cria a relação entre as tabelas User e Note