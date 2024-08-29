from flask import Blueprint, request, jsonify
import requests
from models.empresas.dao import DAOCompany
from models.empresas.sql import SQLCompany
from models.empresas.modelo import Company


empresas_controller = Blueprint('empresas_controller', __name__)
daoCompany = DAOCompany()


@empresas_controller.route('/deliveryapi/v1/company/create', methods=['POST'])
def create_empresa():
    data = request.json
    erros = []

    validation_token_URL = 'http://127.0.0.1:5000/ms_authentication/api/v1/authentication/validation/'
    token_header = request.headers.get('token')
    validate_token = requests.post(validation_token_URL, json={'token' : token_header})

    if validate_token.status_code == 200:
        for campos in SQLCompany.campos_obrigatorios:
            if campos not in data.keys() or not data.get(campos, '').strip():
                erros.append(f'O campo {campos} é obrigatório')
    
        if not erros and daoCompany.procurar_cnpj_dao(data.get('cnpj')):
            erros.append('Já existe um um número de CNPJ como esse')
        if erros:
            response = jsonify(erros)
            response.status_code = 401
            return response
        
        company = Company(**data)
        daoCompany.create_empresa_dao(company)
        return jsonify({'response' : 'Empresa criada com sucesso'}), 200
    
    else:
        return jsonify({'Error' : 'Token não está liberado'}), 500
    

@empresas_controller.route('/deliveryapi/v1/company/companys')
def todas_as_empresas():
    validation_token_URL = 'http://127.0.0.1:5000/ms_authentication/api/v1/authentication/validation/'
    token_header = request.headers.get('token')
    validate_token = requests.post(validation_token_URL, json={'token' : token_header})

    if validate_token.status_code == 200:
        empresas = daoCompany.get_all_dao()
        return jsonify({"response" : empresas}), 200
    else:
        return jsonify({'response' : 'O token liberado não permite tal ação'}), 500
