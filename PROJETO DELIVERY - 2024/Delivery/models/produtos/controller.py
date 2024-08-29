from flask import Flask, Blueprint, request, jsonify
import requests
from models.produtos.modelo import Produto
from models.produtos.dao import DAOProduto
from models.produtos.sql import SQLProduto
 
produtos_controller = Blueprint('produtos_controller', __name__)
daoProduto = DAOProduto()

    

@produtos_controller.route('/deliveryapi/v1/product/create', methods=['POST'])
def criar_produto():
    data = request.json
    erros = []
    
    Validation_Token_URL = 'http://127.0.0.1:5000/ms_authentication/api/v1/authentication/validation/'
    token_header = request.headers.get('token')
    validade_token = requests.post(Validation_Token_URL, json={'token' : token_header})

    if validade_token.status_code == 200:
        for campos in SQLProduto.campos_obrigatorios:
            if campos not in data.keys() or not data.get(campos, '').strip():
                erros.append(f'O campo {campos} é obrigatório.')
        
        if not erros and daoProduto.get_nameProduto(data.get('name')):
            erros.append('Já existe um produto com esse nome.')
        if erros:
            response = jsonify(erros)
            response.status_code = 401
            return response
        
        produto = Produto(**data)
        daoProduto.create_produto(produto)
        return jsonify({'response' : 'Deu certo'}), 200
    
    else:
        return jsonify({'Error' : 'O token recebido não está liberado'}), 500


@produtos_controller.route('/deliveryapi/v1/product/<product_id>/', methods=['PUT'])
def editar_produto(product_id):
    data = request.json
    erros = []

    Validation_Token_URL = 'http://127.0.0.1:5000/ms_authentication/api/v1/authentication/validation/'
    token_header = request.headers.get('token')
    validade_token = requests.post(Validation_Token_URL, json={'token' : token_header})

    if validade_token.status_code == 200:
        new_name = data['new_name']
        new_description = data['new_description']
        new_category_id = data['new_category_id']

        results_id = daoProduto.get_produto_id(product_id)
        if not results_id:
            erros.append("Não foi encontrado um Produto com esse id!")
            response = jsonify(erros)
            response.status_code = 404
            return response


        if 'new_name' in data and new_name!="":
            daoProduto.update_name(product_id, new_name)

        if 'new_description' in data and new_description!="":
            daoProduto.update_description(product_id, new_description)

        if 'new_category_id' in data and new_category_id!="":
            daoProduto.update_category_id(product_id, new_category_id)

        response = jsonify("Produto atualizado com sucesso")
        response.status_code = 200
        return response
    
    else:
        return jsonify({'Error' : 'O token recebido não está liberado'}), 500



@produtos_controller.route('/delivery/api/v1/product/', methods=['GET'])
def get_produtos_by_categoryID():

    Validation_Token_URL = 'http://127.0.0.1:5000/ms_authentication/api/v1/authentication/validation/'
    token_header = request.headers.get('token')
    validade_token = requests.post(Validation_Token_URL, json={'token' : token_header})

    if validade_token.status_code == 200:
        category_id = request.args.get('category_id')

        if not category_id:
            return jsonify({'error' : 'O parâmetro category_id deve ser fornecido'}), 400
        
        if category_id is int:
            return jsonify({'error' : 'Só são aceitos valores numéricos'}), 400
        
        produtos = daoProduto.get_DAO_produto_by_category_id(category_id)

        if not produtos:
            return jsonify('Sem produto'), 400
        
        return jsonify({'produtos' : produtos}), 200
    
    else:
        return jsonify({'Error' : 'O token recebido não está liberado'}), 500
    