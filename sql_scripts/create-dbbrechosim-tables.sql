create database dbBrechoSim;

use dbbrechosim;

create table brecho(
	cdPedido int primary key auto_increment not null,
    nk_cdProduto int,
    nk_cdCliente int,
    dtAgendamento datetime,
    dtContato datetime,
    qtProduto int
);

create table catalogo(
	cdProduto int primary key auto_increment not null,
    nmProduto varchar(50) not null,
    cdFornecedor int,
    nmFornecedor varchar(50),
    cdCategoria int,
    nmCategoria varchar(50),
    cdUnidade int,
    dsUnidade varchar(50),
    vlUnidade int,
    idFotoProduto int
);

ALTER TABLE catalogo
MODIFY COLUMN vlUnidade decimal(10,2),
MODIFY COLUMN idFotoProduto varchar(100);


create table cliente(
	cdCliente int primary key auto_increment not null,
    nmCliente varchar(50),
    cpf int,
    celular int,
    dtNascimento datetime,
    endereco int,
    numero int,
    compEnd varchar(50),
    bairro varchar(50),
    cidade varchar(50),
    estado varchar(50),
    cep int
);

select * from catalogo;

select nmProduto, cdFornecedor, nmFornecedor, cdCategoria, nmCategoria, cdUnidade, dsUnidade, vlUnidade, idFotoProduto;

insert into catalogo(nmProduto, cdFornecedor, nmFornecedor, cdCategoria, nmCategoria, cdUnidade, dsUnidade, vlUnidade, idFotoProduto)
values('Blusa Bata Amarela', 1, 'Socia', 1, 'Roupa', 1, 'Peça', 15.00, 'blusabatamarela.jpeg');



    

