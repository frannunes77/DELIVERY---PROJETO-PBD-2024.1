from models.produtos.modelo import Produto
from models.produtos.sql import SQLProduto
from service.connect import Connect


class DAOProduto(SQLProduto):
    def __init__(self):
        self.connection = Connect().get_instance()
    

    def create_produto(self, produto : Produto):
        if not isinstance(produto, Produto):
            raise Exception('Tipo inválido')
        
        query = self.criar_produto
        cursor = self.connection.cursor()
        cursor.execute(query, (produto.name, produto.description, produto.category_id))
        self.connection.commit()
        return produto
    

    def get_DAO_produto_by_category_id(self, category_id):
        consulta = self.get_produtos_category_id
        cursor = self.connection.cursor()
        cursor.execute(consulta, (category_id,))
        resultado = cursor.fetchall()
        
        produtos = []
        for linha in resultado:
            produto = {
                'id' : linha[0],
                'name' : linha[1],
                'description' : linha[2],
                'category_id' : linha[3],
            }
            produtos.append(produto)

        return produtos


    def get_nameProduto(self, name):
        consulta = self.get_name
        cursor = self.connection.cursor()
        cursor.execute(consulta, (name,))
        resultado = cursor.fetchone()
        return resultado
    
    def get_produto_id(self, id):
        consulta = self.get_id
        cursor = self.connection.cursor()
        cursor.execute(consulta, (id,))
        resultado = cursor.fetchone()
        self.connection.commit()
        return resultado

# Os updates foram separados, pois, em determinadas vezes
# , o cliente não modificará todos os dados, precisando que, 
# o valor antigo permança

    def update_name(self, produto_id, novo_name):
        query = self.editar_name_produto
        cursor = self.connection.cursor()
        cursor.execute(query, (novo_name, produto_id))
        self.connection.commit()
    
    def update_description(self, produto_id, novo_description):
        query = self.editar_description_produto
        cursor = self.connection.cursor()
        cursor.execute(query, (novo_description, produto_id))
        self.connection.commit()

    def update_category_id(self, produto_id, novo_category_id):
        query = self.editar_category_id
        cursor = self.connection.cursor()
        cursor.execute(query, (novo_category_id, produto_id))
        self.connection.commit()
