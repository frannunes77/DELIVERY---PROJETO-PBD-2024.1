from flask import Flask, Blueprint, request, jsonify
import requests
from models.produtos_config.dao import Produto_configDAO
from models.produtos_config.modelo import Produto_Config
from models.produtos_config.sql import SQLProduto_Config


produtos_config_controller = Blueprint('produtos_config_controller', __name__)
dao_produtos_config = Produto_configDAO()


def response_geral(mensagem, status_code):
    response = jsonify(mensagem)
    response.status_code = status_code
    return response


@produtos_config_controller.route('/deliveryapi/v1/productConfig/create', methods=['POST'])
def create_produto_config():
    data = request.json
    erros = []

    Validate_Token_URL = 'http://127.0.0.1:5000/ms_authentication/api/v1/authentication/validation/'
    token_header = request.headers.get('token')
    validade_token = requests.post(Validate_Token_URL, json={'token' : token_header})

    if validade_token.status_code == 200:
        for campos in SQLProduto_Config.campos_obrigatorios:
            if campos not in data.keys() or not data.get(campos, '').strip():
                erros.append(f'O campo {campos} é obrigatório')

        'DEPOIS DO PESO, PENSAR NA QUESTÃO DE INSERIR O MESMO OS MESMOS DADOS IGUAIS'
        if erros:
            return response_geral(erros, 401)
            
        
        new_produtoConfig = Produto_Config(**data)
        dao_produtos_config.create_ProdutoConfigDAO(new_produtoConfig)
        return jsonify({'response' : 'Criado!'}), 200
    
    else:
        return jsonify({'Error' : 'O token recebido não está liberado'}), 500
    


@produtos_config_controller.route('/deliveryapi/v1/productConfig/editar/<produtoConfig_ID>/', methods=['PUT'])
def editar_produtoConfig(produtoConfig_ID):
    data = request.json
    erros = []

    Validade_Token_URL = 'http://127.0.0.1:5000/ms_authentication/api/v1/authentication/validation/'
    token_header = request.headers.get('token')
    validate_token = requests.post(Validade_Token_URL, json={'token' : token_header})

    if validate_token.status_code == 200:
        result_ProdutoConfig = dao_produtos_config.get_ID_ProdutoConfig_DAO(produtoConfig_ID)
        
        if not result_ProdutoConfig:
            erros.append('Não foi encontrado algum produto com esse ID')
            return response_geral(erros, 404)
            
        
        if "new_companyID" in data:
            new_companyID = data["new_company_id"]
            if new_companyID!="":
                dao_produtos_config.update_PC_CompanyID_DAO(new_companyID, produtoConfig_ID)

        if "new_productID" in data:
            new_productID = data["new_product_id"]
            if new_productID!="":
                dao_produtos_config.update_PC_ProdutoID_DAO(new_productID, produtoConfig_ID)
        
        if "new_price" in data:
            new_price = data["new_price"]
            if new_price!="":
                dao_produtos_config.update_PC_price_DAO(new_price, produtoConfig_ID)


        stock_numeric = dao_produtos_config.get_Stock_ProdutoConfig_DAO(produtoConfig_ID)[0]
        result_totalSale = dao_produtos_config.get_totalSale_ProdutoConfig_DAO(produtoConfig_ID)
        result_totalSale_numeric = int(result_totalSale[0])


        if "new_stock" in data: 
            new_stock = data["new_stock"]
            new_stock_numeric = int(new_stock)
            if new_stock!='':
                if new_stock_numeric >= result_totalSale_numeric:
                    dao_produtos_config.update_PC_stock_DAO(new_stock, produtoConfig_ID)
                elif new_stock_numeric < result_totalSale_numeric:
                    erros.append("Veja a quantidade do novo estoque, menor do que a quantidade vendida.")
                    return response_geral(erros, 400)      
        

        if "new_totalSale" in data:
            new_totalSale = data["new_totalSale"]
            new_totalSale_numeric = int(new_totalSale)

            if new_totalSale!='':
                if new_totalSale_numeric > int(stock_numeric):
                    erros.append('A quantidade de produtos vendidos, é maior do que a de estoque')
                    return response_geral(erros, 400)  
                else:
                    dao_produtos_config.update_PC_totalSale_DAO(new_totalSale, produtoConfig_ID)
        
        return response_geral('Produto atualizado com sucesso!', 200)

    
    
    else:
        erros.append('O token recebido, não está liberado. Tempo expirado ou token incorreto.')
        return response_geral(erros, 400)



@produtos_config_controller.route('/deliveryapi/v1/productConfig/get/', methods=['GET'])
def get_produtoConfig():
    #erros = []

    Validade_Token_URL = 'http://127.0.0.1:5000/ms_authentication/api/v1/authentication/validation/'
    token_header = request.headers.get('token')
    validate_token = requests.post(Validade_Token_URL, json={'token' : token_header})

    if validate_token.status_code==200:
        company_id = request.args.get('company_id')
        product_id = request.args.get('product_id')

        #companys = dao_produtos_config.get_PC_company_by_CompanyID_DAO(company_id)
        #produtos = dao_produtos_config.get_PC_produto_by_ProdutoID_DAO(product_id)

        # Os args do query paremeters voltam como 'str'
        # Caso necessário, ver a questão se colocar uma string no lugar do int

        if product_id is None and company_id is None:
            produtos_config_geral = dao_produtos_config.get_PC_geral_DAO()
            response = jsonify(produtos_config_geral)
            response.status_code = 200
            return response
 
             
        if company_id == None and product_id!=None:
            produtos_config_geral = dao_produtos_config.get_PC_query_produtoID_DAO(product_id)
            response = jsonify(produtos_config_geral)
            response.status_code = 200
            return response

        if company_id != None and product_id == None:
            produtos_config_geral = dao_produtos_config.get_PC_query_companyID_DAO(company_id)
            response = jsonify(produtos_config_geral)
            response.status_code = 200
            return response

        
        if company_id != None and product_id != None:
            produtos_config_geral = dao_produtos_config.get_PC_query_companyID_produtoID_DAO(company_id, product_id)
            response = jsonify(produtos_config_geral)
            response.status_code = 200
            return response

    else:
        response = jsonify('O token expirou ou não é váilido!')
        response.status_code = 404
        return response