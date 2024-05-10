import os

from flask import Flask, render_template, request, redirect, session, flash, url_for

# Definição da classe Catalogo para representar os itens do catálogo
class Catalogo:
    def __init__(self, foto, idnome, descricao, preco):
        self.foto = foto
        self.idnome = idnome
        self.descricao = descricao
        self.preco = preco

# Definição da classe Usuário
class Usuario:
    def __init__(self, cdCliente, nmCliente, cpf, celular, endereco, numero, compEnd, 
                 bairro, cidade, estado, cep, login, senha):
        self.cdCliente = cdCliente
        self.nmCliente = nmCliente
        self.cpf = cpf
        self.celular = celular
        self.endereco = endereco
        self.numero = numero
        self.compEnd = compEnd
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep
        self.login = login
        self.senha = senha

usuario01 = Usuario("0001", "Daniel", "12345678900", "11912345678", "Rua Mantua", "15", "Casa", "Lisboa", 
                    "Santos", "CE", "08646780", "dani.dani", "admin")
usuario02 = Usuario("0002", "Patrick", "12345678900", "11912345678", "Rua Mantua", "15", "Casa", "Lisboa", 
                    "Santos", "CE", "08646780", "patrick.sponge", "1234")
usuario03 = Usuario("0003", "Xavier", "12345678900", "11912345678", "Rua Mantua", "15", "Casa", "Lisboa", 
                    "Santos", "CE", "08646780", "xavi.mente", "7968")

usuarios = {
    usuario01.login : usuario01,
    usuario02.login : usuario02,
    usuario03.login : usuario03
}


# Criando o app
app = Flask(__name__)

app.secret_key = 'brechosimmodasustentavel'

# Lista para armazenar os nomes das imagens do catálogo
catalogo = os.listdir('static/img_colecao')

# Rota para renderizar a página inicial do brecho
@app.route('/')
def iniciarBrecho():
    return render_template('brecho.html', titulo='BrechóSim')


# Rota para renderizar a página da coleção completa
@app.route('/colecao')
def verColecao():
    if session['usuario_logado'] == None or 'usuario_logado' not in session:
        return redirect(url_for('login'))
    else:   
        return render_template('colecao.html', fotos=catalogo)


# Rota para renderizar a página de login
@app.route('/login')
def login():
    return render_template('login.html')


# Rota para autenticar o login
@app.route('/autenticar', methods=['POST'])
def autenticar():
    if request.form['txtLogin'] in usuarios:

        usuarioEncontrado = usuarios[request.form['txtLogin']]

        if request.form['txtSenha'] == usuarioEncontrado.senha:
        
            session['usuario_logado'] = request.form['txtLogin']
        
            flash(f"Seja bem-vindo, {usuarioEncontrado.nome}!")

            return redirect(url_for('iniciarBrecho'))
        else:
            flash("Senha inválida!")

            return redirect(url_for('login')) 
    
    else:

        flash("Usuário ou Senha inválida")

        return redirect(url_for('login'))

# Rota para sair
@app.route('/agendar')
def agendar():
    if session['usuario_logado'] == None or 'usuario_logado' not in session:
        return redirect(url_for('login'))
    else:   
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
    else:   
        if request.method == 'POST':
            # Recupera os dados do formulário
            foto = request.files['foto']
            idnome = request.form['idnome']
            descricao = request.form['descricao']
            preco = request.form['preco']
            
            # Salva a imagem no diretório "static/imagens"
            caminho_imagem = salvar_imagem(foto)
            
            # Cria uma nova instância da classe Catalogo com os dados do formulário
            novo_item = Catalogo(caminho_imagem, idnome, descricao, preco)
            
            # Adiciona o novo item à lista de catalogo
            catalogo.append(novo_item)
            
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
    return caminho_imagem


app.run(debug=True)
