from models.categorias.sql import SQLCategoria
from service.connect import Connect

class DAOCategoria(SQLCategoria):
    def __init__(self):
        self.connection = Connect().get_instance()


    def get_all(self):
        query = self.todas_as_categorias
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        categorias = []
        for linha in results:
            categoria = {
                'id' : linha[0],
                'name' : linha[1]
            }
            categorias.append(categoria)

        return categorias
    
    