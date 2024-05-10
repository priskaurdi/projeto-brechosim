SELECT * FROM dbbrechosim.cliente;

ALTER TABLE cliente
MODIFY COLUMN endereco varchar(50);

INSERT INTO cliente(nmCliente, cpf, celular, dtNascimento, endereco, numero, compEnd, bairro, cidade, estado, cep, login, senha, email)
VALUES('Madalena Caslav', '90177880371', '19932110175', '2003-08-25', 'Avenida Moreira', 200, 'Casa', 'Burle Marx', 'Cotia', 'RJ', '07068868', 'caslav.ilic', 'dickens', 'caslav.ilic@example.com'),
('Daniel Madsen', '15055523089', '1298935395', '2010-01-13', 'Rua Magnolia', 11, 'Ap 03', 'Amelia', 'Santos', 'SP', '96507868', 'daniel.madsen', 'sadfrog185', 'daniel.madsen@example.com'),
('Helena Carvalho', '09512711779', '1196775158', '1979-02-23', 'Travessa Mercurio', 44, 'Casa 04', 'Floresta', 'America', 'SP', '07489680', 'anton.helen', 'libqND2c', 'anton.helen@example.com');

truncate table cliente;

ALTER TABLE cliente
ADD UNIQUE(login);

DELETE FROM cliente WHERE cdCliente = 3


