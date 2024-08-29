from flask import Blueprint, request, jsonify
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
from service.connect import Connect
from sql import verificar_usuario_sql, verificar_username_sql


SECRET_KEY = 'chave_secreta'

app_views = Blueprint('views', __name__)


@app_views.route('/ms_authentication/api/vi/authentication/token/', methods=['POST'])
def get_token():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    connection = Connect().get_instance()
    cursor = connection.cursor()

    cursor.execute(verificar_usuario_sql, (username, password,))
    user = cursor.fetchone()

    connection.close()
    cursor.close()
    

    if user:
        # tempo do token será de 10 minutos
        tempo_token = datetime.now() + timedelta(minutes=10)
        payload = {
            'username': username,
            'tempo_token': tempo_token.strftime('%Y-%m-%d %H:%M:%S')
            # .strftiem tem a função de transformar o objeto Datetime em String
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256') #codificar
        return jsonify({"token" : token}), 200
    
    else:
        return jsonify({"error" : "Usuário não encontrado"}), 400 



@app_views.route('/ms_authentication/api/v1/authentication/validation/', methods=['POST'])
def validate_token():
    token = request.get_json().get('token')

    connection = Connect().get_instance()
    cursor = connection.cursor()

    decode_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256']) # decodificar
    username_token = decode_token.get('username')

    cursor.execute(verificar_username_sql, (username_token,))
    username_token = cursor.fetchone()
    print(username_token)

    connection.close()
    cursor.close()

    if token and username_token:
        try:
            tempo_token = decode_token.get('tempo_token')
            if tempo_token:
                tempo_token = datetime.fromisoformat(tempo_token) # transforma o tempo_token de string para datetime
                if tempo_token < datetime.now():
                    return jsonify({'error': 'Token expirado'}), 401
                # O token é válido
                return jsonify({}), 200
        
        except ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
    else:
        return jsonify({'error': 'Token não fornecido'}), 401