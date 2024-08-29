class Company:
    def __init__(self, name, cnpj, rua, cep, estado, cidade, id=None):
        self.id = id
        self.name = name
        self.cnpj = cnpj
        self.rua = rua
        self.cep = cep
        self.estado = estado
        self.cidade = cidade