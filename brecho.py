import os
import random

from flask import Flask, render_template, request

# Definição da classe Catalogo para representar os itens do catálogo
class Catalogo:
    def __init__(self, foto, idnome, descricao, preco):
        self.foto = foto
        self.idnome = idnome
        self.descricao = descricao
        self.preco = preco

app = Flask(__name__)

# Lista para armazenar os nomes das imagens do catálogo
catalogo = os.listdir('static/imagens')

# Rota para renderizar a página inicial do catálogo
@app.route('/')
def iniciarBrecho():
    # Seleciona aleatoriamente 10 imagens do catálogo
    fotos_aleatorias = random.sample(catalogo, 10)
    return render_template('brecho.html', titulo='BrechóSim', fotos_aleatorias=fotos_aleatorias)


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
    diretorio_destino = 'static/imagens/'
    
    # Salva a imagem no diretório de destino com o mesmo nome original do arquivo
    caminho_imagem = diretorio_destino + foto.filename
    foto.save(caminho_imagem)
    
    # Retorna o caminho completo da imagem
    return caminho_imagem




app.run(debug=True)
