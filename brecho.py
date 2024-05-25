# Importando bibliotecas
import os
from flask import Flask, render_template, request, redirect, session, flash, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Criando o app
app = Flask(__name__)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

# Importando as rotas
from views import *

# Iniciando o projeto
if __name__ == '__main__':
    app.run(debug=True)
