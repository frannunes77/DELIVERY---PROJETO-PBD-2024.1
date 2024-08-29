from models.produtos_config.sql import SQLProduto_Config
from models.produtos_config.modelo import Produto_Config
from service.connect import Connect

class Produto_configDAO(SQLProduto_Config):

    def __init__(self):
        self.connection = Connect().get_instance()


    def execute_query_one_fetchall(self, query, parametro):
        cursor = self.connection.cursor()
        cursor.execute(query, (parametro,))
        results = cursor.fetchall()
        self.connection.commit()
        return results
    

    def formatar_dados(self, results):
        dados_formatados = []
        
        for linha in results:
            new_stock = int(linha[7]) - int(linha[8])
            dados = {
                "id": linha[0],
                "Company": {
                    "id": linha[1],
                    "name": linha[2],
                    "cnpj": linha[3]
                },
                "price": linha[6],
                "stock": new_stock,
                #"stock": linha[7],
                #"total_sale": linha[8],
                "Produto": {
                    "id": linha[4],
                    "name": linha[5]
                }
            }
            dados_formatados.append(dados)

        return dados_formatados

# ------------------------------------------------------------------------------------------------------ #
# ---------------------------------------- CREATE ------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------ #


    def create_ProdutoConfigDAO(self, produto_config : Produto_Config):
        if not isinstance(produto_config, Produto_Config):
            raise Exception('Tipo Inválido!')
        
        query = self.criar_Produto_Config_SQL
        cursor = self.connection.cursor()
        cursor.execute(query, (produto_config.company_id, produto_config.product_id, produto_config.price, produto_config.stock, produto_config.total_sale))
        self.connection.commit()
        return produto_config


# ------------------------------------------------------------------------------------------------------
# ---------------------------------------- UPDATES -----------------------------------------------------
# ------------------------------------------------------------------------------------------------------


    def update_PC_CompanyID_DAO(self, new_CompanyID, produtoConfig_ID):
        query = self.editar_companyID_SQL
        cursor = self.connection.cursor()
        cursor.execute(query, (new_CompanyID, produtoConfig_ID))
        self.connection.commit()


    def update_PC_ProdutoID_DAO(self, new_ProdutoID, produtoConfig_ID):
        query = self.editar_productID_SQL
        cursor = self.connection.cursor()
        cursor.execute(query, (new_ProdutoID, produtoConfig_ID))
        self.connection.commit()

    
    def update_PC_price_DAO(self, new_price, produtoConfig_ID):
        query = self.editar_price_SQL
        cursor = self.connection.cursor()
        cursor.execute(query, (new_price, produtoConfig_ID))
        self.connection.commit()

    
    def update_PC_stock_DAO(self, new_stock, produtoConfigID):
        query = self.editar_stock_SQL
        cursor = self.connection.cursor()
        cursor.execute(query, (new_stock, produtoConfigID))
        self.connection.commit()

    def update_PC_totalSale_DAO(self, new_totalSale, produtoConfigID):
        query = self.editar_totalSale_SQL
        cursor = self.connection.cursor()
        cursor.execute(query, (new_totalSale, produtoConfigID))
        self.connection.commit()



# ------------------------------------------------------------------------------------------------ #
# ----------------------------------- GET GERAL -------------------------------------------------- #
# ------------------------------------------------------------------------------------------------ #
    
    def get_PC_geral_DAO(self):
        query = self.listar_PC_geral_SQL
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        produtos_config_list = []
        for linha in results:
            new_stock = int(linha[4]) - int(linha[5])
            produtos_config_dict = {
                'id' : linha[0],
                'company_id' : linha[1],
                'product_id' : linha[2],
                'price' : linha[3],
                'stock' : new_stock
            }
            produtos_config_list.append(produtos_config_dict)
        self.connection.commit()
        return produtos_config_list
    
    

# ------------------------------------------------------------------------------------------------ #
# ------------------------- GETs PRODUTO_CONFIG por COMPANY_ID ----------------------------------- #
# ------------------------------------------------------------------------------------------------ #

    def get_PC_query_companyID_DAO(self, company_id):
        query = self.listar_PC_QP_by_companyID_SQL
        results = self.execute_query_one_fetchall(query, company_id)
        return self.formatar_dados(results)
    
        
# ------------------------------------------------------------------------------------------------
# -------------------------------  GET by QUERY PRODUCT ID ---------------------------------------
# ------------------------------------------------------------------------------------------------

    def get_PC_query_produtoID_DAO(self, produto_ID):
        query = self.listar_PC_QP_by_produtoID_SQL
        results = self.execute_query_one_fetchall(query, produto_ID)
        return self.formatar_dados(results)



# ------------------------------------------------------------------------------------------------ #
# ------------------- GETs PRODUTO_CONFIG por COMPANY_ID e PRODUCT_ID ---------------------------- #
# ------------------------------------------------------------------------------------------------ #

    def get_PC_query_companyID_produtoID_DAO(self, company_id, product_id):
        query = self.listar_PC_QP_by_companyID_and_productID_SQL
        cursor = self.connection.cursor()
        cursor.execute(query, (company_id, product_id,))
        results = cursor.fetchall()
        self.connection.commit()
        return self.formatar_dados(results)



# ------------------------------------------------------------------------------------------------
# ------------------------ GETs por ID do PRODUTO_CONFIG -----------------------------------------
# ------------------------------------------------------------------------------------------------    

    def get_ID_ProdutoConfig_DAO(self, id):
        query = self.listar_ProductConfig_ID
        cursor = self.connection.cursor()
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        self.connection.commit()
        return result
    

    def get_Price_ProdutoConfig_DAO(self, id):
        query = self.listar_ProductConfig_Price
        cursor = self.connection.cursor()
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        return result
    

    def get_Stock_ProdutoConfig_DAO(self, id):
        query = self.listar_ProductConfig_Stock
        cursor = self.connection.cursor()
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        return result
    

    def get_totalSale_ProdutoConfig_DAO(self, id):
        query = self.listar_ProdutoConfig_TS
        cursor = self.connection.cursor()
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        self.connection.commit()
        return result

