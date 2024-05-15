# Importando bibliotecas
import os
from flask import Flask, render_template, request, redirect, session, flash, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Criando o app
app = Flask(__name__)

app.secret_key = 'brechosimmodasustentavel'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'admin',
        servidor = 'localhost',
        database = 'dbbrechosim'
    )

db = SQLAlchemy(app)


# Definindo as classes
class Brecho(db.Model):
    cdPedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nk_cdProduto = db.Column(db.Integer, nullable=False)
    nk_cdCliente = db.Column(db.Integer, nullable=False)
    dtAgendamento = db.Column(db.DateTime, nullable=False)
    dtContato = db.Column(db.DateTime, nullable=False)
    qtProduto = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Name %r>' %self.name
    

class Catalogo(db.Model):
    cdProduto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nmProduto = db.Column(db.String(50), nullable=False)
    cdFornecedor = db.Column(db.Integer, nullable=False)
    nmFornecedor = db.Column(db.String(50), nullable=False)
    cdCategoria = db.Column(db.Integer, nullable=False)
    nmCategoria = db.Column(db.String(50), nullable=False)
    cdUnidade = db.Column(db.Integer, nullable=False)
    dsUnidade = db.Column(db.String(50), nullable=False)
    vlUnidade = db.Column(db.Numeric(10, 2), nullable=False)
    idFotoProduto = db.Column(db.String(100), nullable=False)
    dtCadastro = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Name %r>' %self.name


class Cliente(db.Model):
    cdCliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nmCliente = db.Column(db.String(50), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    celular = db.Column(db.String(15), nullable=False)
    dtNascimento = db.Column(db.DateTime, nullable=False)
    endereco = db.Column(db.String(50), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    compEnd = db.Column(db.String(50), nullable=False)
    bairro = db.Column(db.String(50), nullable=False)
    cidade = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    cep = db.Column(db.Integer, nullable=False)
    login = db.Column(db.String(50), nullable=False)
    senha = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Name %r>' %self.name



# Rota para renderizar a página inicial do brecho
@app.route('/')
def iniciarBrecho():
    return render_template('brecho.html', titulo='BrechóSim')


# Rota para renderizar a página da coleção completa
@app.route('/colecao')
def verColecao():
    
    # Consulta todos os itens do catálogo no banco de dados
    catalogo = Catalogo.query.order_by(Catalogo.cdProduto).all()
       
    return render_template('colecao.html', fotos=catalogo)


# Rota para renderizar a página de login
@app.route('/login')
def login():
    return render_template('login.html')


# Rota para autenticar o login
@app.route('/autenticar', methods=['POST'])
def autenticar():
    # Recupera o nome de usuário e senha do formulário
    login = request.form['txtLogin']
    senha = request.form['txtSenha']
    
    # Consulta o banco de dados para encontrar um cliente com o nome de usuário fornecido
    cliente = Cliente.query.filter_by(login=login).first()

    # Verifica se o cliente foi encontrado e se a senha está correta
    if cliente and cliente.senha == senha:
        # Define o usuário logado na sessão
        session['usuario_logado'] = cliente.login
        flash(f"Seja bem-vindo, {cliente.nmCliente}!")
        return redirect(url_for('iniciarBrecho'))
    else:
        flash("Usuário ou senha inválida")
        return redirect(url_for('login'))
    

# Rota para sair
@app.route('/agendar')
def agendar():
    if session.get('usuario_logado') is None:
        return redirect(url_for('login'))
    return render_template('agenda.html')


# Rota para sair
@app.route('/sair')
def sair():
    session['usuario_logado'] = None

    return redirect(url_for('login'))


# Rota para renderizar a página de cadastro e processar o formulário
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():

    if session['usuario_logado'] == None or 'usuario_logado' not in session:
        return redirect(url_for('login'))
      
    if request.method == 'POST':
        # Recupera os dados do formulário
        dtCadastro = datetime.now()
        nmProduto = request.form['nmProduto']
        cdFornecedor = 1  # Defina o valor do fornecedor conforme necessário
        nmFornecedor = request.form['nmFornecedor']
        cdCategoria = 1  # Defina o valor da categoria conforme necessário
        nmCategoria = request.form['nmCategoria']
        cdUnidade = 1  # Defina o valor da unidade conforme necessário
        dsUnidade = request.form['dsUnidade']
        vlUnidade = request.form['vlUnidade']
        idFotoProduto = salvar_imagem(request.files['foto'])
        
            
        # Cria uma nova instância da classe Catalogo com os dados do formulário
        novo_item = Catalogo(
            nmProduto=nmProduto,
            cdFornecedor=cdFornecedor,
            nmFornecedor=nmFornecedor,
            cdCategoria=cdCategoria,
            nmCategoria=nmCategoria,
            cdUnidade=cdUnidade,
            dsUnidade=dsUnidade,
            vlUnidade=vlUnidade,
            idFotoProduto=idFotoProduto,
            dtCadastro=dtCadastro
            )
            
        # Adiciona o novo item ao banco de dados
        db.session.add(novo_item)
        db.session.commit()
            
    # Renderiza a página de cadastro
    return render_template('cadastra_catalogo.html')

# Função para salvar a imagem enviada pelo formulário
def salvar_imagem(foto):
    # Define o diretório onde as imagens serão salvas
    diretorio_destino = 'static/img_colecao/'
    
    # Salva a imagem no diretório de destino com o mesmo nome original do arquivo
    caminho_imagem = diretorio_destino + foto.filename
    foto.save(caminho_imagem)
    
    # Retorna o caminho completo da imagem
    return foto.filename


@app.route('/pagamento', methods=['POST'])
def pagamento():
    # Lógica para processar o pagamento...

    # Gerar um QR code do PIX
    qr = qrcode.make('Dados do pagamento PIX')  # Substitua 'Dados do pagamento PIX' pelos dados reais do PIX

    # Salvar o QR code em um arquivo temporário
    qr_path = 'static/qr_code_pix.png'
    qr.save(qr_path)

    # Renderizar a página de confirmação de pagamento com o QR code do PIX
    return render_template('confirmacao_pagamento.html', qr_code=qr_path)

    # Redirecionar para o WhatsApp
    produto = request.form['nome_produto']  # Supondo que você passe o nome do produto pelo formulário
    mensagem = f'Olá! Gostaria de comprar o produto {produto}.'
    numero_whatsapp = 'seu_numero_whatsapp'  # Substitua pelo número de WhatsApp real
    link_whatsapp = f'https://api.whatsapp.com/send?phone={numero_whatsapp}&text={mensagem}'
    return redirect(link_whatsapp)


if __name__ == '__main__':
    app.run(debug=True)
