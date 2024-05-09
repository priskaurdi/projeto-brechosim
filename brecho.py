import os

from flask import Flask, render_template, request, redirect, session

# Definição da classe Catalogo para representar os itens do catálogo
class Catalogo:
    def __init__(self, foto, idnome, descricao, preco):
        self.foto = foto
        self.idnome = idnome
        self.descricao = descricao
        self.preco = preco

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
    return render_template('colecao.html', fotos=catalogo)


# Rota para renderizar a página de login
@app.route('/login')
def login():
    return render_template('login.html')


# Rota para autenticar o login
@app.route('/autenticar', methods=['POST'])
def autenticar():
    if request.form['txtSenha'] == 'admin':
        
        session['usuario_logado'] = request.form['txtLogin']
        
        return redirect('/')
    else:
        return redirect('/login')

# Rota para sair
@app.route('/agendar')
def agendar():
    return render_template('agenda.html')


# Rota para sair
@app.route('/sair')
def sair():
    session['usuario_logado'] = None

    return redirect('/')


# Rota para renderizar a página de cadastro e processar o formulário
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
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
