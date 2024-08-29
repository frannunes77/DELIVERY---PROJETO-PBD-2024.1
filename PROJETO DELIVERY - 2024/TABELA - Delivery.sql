--------------------------------------------------------------------------
------------------------------- CATEGORIA ---------------------------------
---------------------------------------------------------------------------

create table if not exists Categoria(
	id serial primary key, 
	name varchar(255) not null
);
insert into Categoria(id, name) values(12, 'Cervejas');
insert into Categoria(id, name) values(13, 'Pratos');
insert into Categoria(id, name) values(14, 'Hambusgues');
insert into Categoria(id, name) values(2, 'Café');
select * from Categoria;


--------------------------------------------------------------------------
---------------------------- PRODUTO -------------------------------------
--------------------------------------------------------------------------

create table if not exists Produto(
	id serial primary key,
	name varchar(255) not null, 
	description text,
	category_id integer references Categoria(id)
);
select * from Produto;
insert into Produto(name, description, category_id) values('Café Santa Clara', '', 2);
insert into Produto(name, description, category_id) values('Café Maria', 'O café da família', 2);
insert into Produto(name, description, category_id) values('Café Bom Sabor', 'O café mais gostoso', 2);
select * from Produto where category_id=2;


-----------------------------------------------------------------------
----------------------------- COMPANY ---------------------------------
-----------------------------------------------------------------------

create table if not exists Company(
	id serial primary key, 
	name varchar (255) not null,
	cnpj varchar(14) not null,
	rua varchar(255),
	cep varchar(8),
	estado varchar(2),
	cidade varchar(255)
);	
select * from Company;
insert into Company(name, cnpj, rua, cep, estado, cidade)
	values('Companhia Café com Leite', '12345678901011', 
	'Rua da Tábua Lascada', '58900000', 'PE', 'Ipubi');

insert into Company(name, cnpj, rua, cep, estado, cidade)
	values('Academia dos Alimentos', '12345678900000', 
	'Rua da Indústria', '56930000', 'PE', 'Calumbi');


-----------------------------------------------------------------------------------
--------------------------   PRODUTO CONFIG ---------------------------------------
-----------------------------------------------------------------------------------

create table if not exists Produto_config(
	id serial primary key,
	company_id integer references Company(id) not null,
	product_id integer references Produto(id) not null,
	price decimal(10,2) not null check(price >= 0), -- preço deve ser maior ou igual a 0--
	--deve ter no máx. 10 digitos, e duas casas decimais --
	stock integer not null check(stock >= 0),
	total_sale integer check(total_sale >= 0)
);

select * from Produto_config;

------------------------- INSERTS ----------------------------------------

insert into Produto_config(company_id, product_id, price, stock, total_sale)
values(1, 1, 3, 100, 2); -- ("Companhia Café com Leite", "Café Santa Clara", "R$ 3") 

insert into Produto_config(company_id, product_id, price, stock, total_sale)
values(1, 2, 3.01, 100, 0); --("Companhia Café com Leite", "Café Maria", "R$ 3.01")

insert into Produto_config(company_id, product_id, price, stock, total_sale)
values(1, 3, 3.02, 100, 0); --("Companhia Café com Leite", "Café Bom Sabor", "R$ 3.02")

insert into Produto_config(company_id, product_id, price, stock, total_sale)
values(2, 1, 2.99, 200, 0); -- ("Academia dos Alimentos", "Café Santa Clara", "2.99")


------------------------ Query com Company_ID ----------------------------------

SELECT pc.id, c.id, c.name, c.cnpj, p.id, p.name, pc.price, pc.stock, 
pc.total_sale FROM Produto_config pc INNER JOIN Company c ON pc.company_id = c.id 
INNER JOIN Produto p ON pc.product_id = p.id WHERE pc.company_id = 1;



------------------------ Query com Produto_ID ----------------------------------

SELECT pc.id, c.id, c.name, c.cnpj, p.id, p.name, pc.price, pc.stock, 
pc.total_sale FROM Produto_config pc INNER JOIN Company c ON pc.company_id = c.id 
INNER JOIN Produto p ON pc.product_id = p.id WHERE pc.product_id = 2;



-------------------- Query com Company_ID e Product_ID --------------------------

SELECT pc.id, c.id, c.name, c.cnpj, p.id, p.name, pc.price, pc.stock, 
pc.total_sale FROM Produto_config pc INNER JOIN Company c ON pc.company_id = c.id 
INNER JOIN Produto p ON pc.product_id = p.id WHERE pc.company_id = 2 
AND pc.product_id = 2;