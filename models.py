
from brecho import db

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

