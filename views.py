from flask import render_template, request, redirect, session, flash, url_for, send_file
from models import Catalogo, Cliente, FormBrecho
from brecho import db, app
from datetime import datetime
from flask_wtf import FlaskForm
from functools import wraps
from werkzeug.utils import secure_filename
import os


# Funcao para centralizar a validacao
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_logado' not in session or session['usuario_logado'] is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function






# Rota para renderizar a página inicial do brecho
@app.route('/')
def iniciarBrecho():
    return render_template('brecho.html', titulo='BrechóSim')


# Rota para editar o catalogo
@app.route('/editar') #/<int:idFotoProduto
@login_required
def editar(idFotoProduto): 
    
    pecaBuscada = Catalogo.query.filter_by(idFotoProduto=idFotoProduto).first()

    return render_template('editar_catalogo.html', 
                           titulo = 'Editar Catálogo',
                           peca = pecaBuscada)


# Rota para atualizar o catalogo
@app.route('/atualizar', methods=['POST'])
def atualizar():
    
    peca = Catalogo.query.filter_by(idFotoProduto=request.form['idFotoProduto']).first()

    peca.dtCadastro = request.form['dtCadastro']
    peca.nmProduto = request.form['nmProduto']
    peca.nmFornecedor = request.form['nmFornecedor']
    peca.nmCategoria = request.form['nmCategoria']
    peca.dsUnidade = request.form['dsUnidade']
    peca.vlUnidade = request.form['vlUnidade']

    db.session.add(peca)
    db.session.commit()

    return redirect(url_for('verColecao'))


# Rota para excluir item do catalogo
@app.route('/excluir/<int:id>')
@login_required
def excluir(id):
    
    Catalogo.query.filter_by(idFotoProduto=id).delete()

    db.session.commit()

    flash("Peça excluída!")

    return redirect(url_for('verColecao'))


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
@login_required
def cadastrar():

    form = FormBrecho()

    if request.method == 'POST' and form.validate_on_submit():
        # Recupera os dados do formulário
        dtCadastro = datetime.now()
        nmProduto = form.nome.data
        cdFornecedor = 1
        nmFornecedor = form.nmFornecedor.data
        cdCategoria = 1
        nmCategoria = form.categoria.data
        cdUnidade = 1
        dsUnidade = form.dsUnidade.data
        vlUnidade = form.vlUnidade.data
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
        return redirect(url_for('verColecao'))
            
    # Renderiza a página de cadastro
    return render_template('cadastra_catalogo.html', 
                           form = form)

# Função para salvar a imagem enviada pelo formulário
def salvar_imagem(foto):
    # Define o diretório onde as imagens serão salvas
    diretorio_destino = 'static/img_colecao/'
    
    # Salva a imagem no diretório de destino com o mesmo nome original do arquivo
    if not os.path.exists(diretorio_destino):
        os.makedirs(diretorio_destino)
    filename = secure_filename(foto.filename)
    caminho_imagem = os.path.join(diretorio_destino, filename)
    foto.save(caminho_imagem)

    # Retorna o caminho completo da imagem
    return filename


@app.route('/pagamento', methods=['POST'])
def pagamento():
    # Lógica para processar o pagamento...

    # Gerar um QR code do PIX
    qr = qrcode.make('Dados do pagamento PIX')  # Substitua 'Dados do pagamento PIX' pelos dados reais do PIX

    # Salvar o QR code em um arquivo temporário
    qr_path = 'static/qr_code_pix.png'
    qr.save(qr_path)

    # Redirecionar para o WhatsApp
    produto = request.form['nome_produto']  # Supondo que você passe o nome do produto pelo formulário
    mensagem = f'Olá! Gostaria de comprar o produto {produto}.'
    numero_whatsapp = 'seu_numero_whatsapp'  # Substitua pelo número de WhatsApp real
    link_whatsapp = f'https://api.whatsapp.com/send?phone={numero_whatsapp}&text={mensagem}'

    # Renderizar a página de confirmação de pagamento com o QR code do PIX
    return render_template('confirmacao_pagamento.html', qr_code=qr_path, whatsapp_link=link_whatsapp)
