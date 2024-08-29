from models.empresas.sql import SQLCompany
from service.connect import Connect
from models.empresas.modelo import Company

class DAOCompany(SQLCompany):
    def __init__(self):
        self.connection = Connect().get_instance()

    def procurar_cnpj_dao(self, cnpj):
        consulta = self.buscar_cnpj_sql
        cursor = self.connection.cursor()
        cursor.execute(consulta, (cnpj,))
        resultado = cursor.fetchone()
        return resultado

    def create_empresa_dao(self, company : Company):
        if not isinstance(company, Company):
            raise Exception('Tipo inválido')
        
        consulta = self.criar_empresa_sql
        cursor = self.connection.cursor()
        cursor.execute(consulta, (company.name, company.cnpj, company.rua, company.cep, company.estado, company.cidade))
        self.connection.commit()
        return company

    def get_all_dao(self):
        consulta = self.todas_as_empresas_sql
        cursor = self.connection.cursor()
        cursor.execute(consulta)
        resultado = cursor.fetchall()

        empresas = []
        for linha in resultado:
            empresa = {
                'id' : linha[0],
                'name' : linha[1],
                'cnpj' : linha[2],
                'rua' : linha[3],
                'cep' : linha[4],
                'estado' : linha[5],
                'cidade' : linha[6]
            }
            empresas.append(empresa)
        return empresas