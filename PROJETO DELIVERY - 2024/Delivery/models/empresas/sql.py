class SQLCompany:
    campos_obrigatorios = ['name', 'cnpj']

    buscar_cnpj_sql = 'select cnpj from Company where cnpj=%s'
    criar_empresa_sql = 'insert into Company(name, cnpj, rua, cep, estado, cidade) values(%s, %s, %s, %s, %s, %s)'

    todas_as_empresas_sql = 'select * from Company'