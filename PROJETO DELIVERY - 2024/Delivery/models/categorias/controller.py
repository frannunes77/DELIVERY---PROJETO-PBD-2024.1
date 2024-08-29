from flask import Blueprint, request, jsonify
import requests
from models.categorias.dao import DAOCategoria

SECRET_KEY = 'chave_secreta'

categoria_controller = Blueprint('categoria_controller', __name__)
categoriaDao = DAOCategoria()


VALIDATION_URL = 'http://127.0.0.1:5000/ms_authentication/api/v1/authentication/validation/'


@categoria_controller.route('/delivery/api/vi/categories', methods=['GET'])
def get_categorias():

    token_header = request.headers.get('token')
    validade_token = requests.post(VALIDATION_URL, json={'token' : token_header})

    if validade_token.status_code == 200:
        categorias = categoriaDao.get_all()

        return jsonify({'response' : categorias}), 200
    
    else:
        return jsonify({'response' : 'O token liberado não permite tal ação'}), 500
    

