SELECT * FROM catalogo;

select * from catalogo where nmProduto like '%Bata%';

select * from catalogo where vlUnidade <> 15.00;

select * from catalogo where vlUnidade <= 15.00;

select * from catalogo where vlUnidade >= 20.00;

update catalogo set vlUnidade = 21.00 where cdProduto = 5;

ALTER TABLE catalogo
ADD COLUMN dtCadastro datetime;

update catalogo set dtCadastro = '2025-05-10' where cdProduto in (1, 2, 3, 4, 5);