from flask import Flask
from models.categorias.controller import categoria_controller
from models.produtos.controller import produtos_controller
from models.empresas.controller import empresas_controller
from models.produtos_config.controller import produtos_config_controller

app = Flask(__name__)

app.register_blueprint(categoria_controller)
app.register_blueprint(produtos_controller)
app.register_blueprint(empresas_controller)
app.register_blueprint(produtos_config_controller)

app.run(host='127.0.0.1', port=5001, debug=True)