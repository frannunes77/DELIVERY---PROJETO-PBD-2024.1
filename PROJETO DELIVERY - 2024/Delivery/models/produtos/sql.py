class SQLProduto:
    campos_obrigatorios = ['name', 'category_id']
    
    criar_produto = "insert into Produto(name, description, category_id) values(%s, %s, %s)"
    
    editar_name_produto = "update Produto set name=%s where id=%s"
    editar_description_produto = "update Produto set description=%s where id=%s"
    editar_category_id = "update Produto set category_id=%s where id=%s"

    get_name = "select name from Produto where name=%s"
    get_id = "select id from Produto where id=%s"

    get_produtos_category_id = 'select * from Produto where category_id=%s'
