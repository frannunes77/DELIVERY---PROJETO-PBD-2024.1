class SQLProduto_Config:
    campos_obrigatorios = ['company_id', 'product_id', 'price', 'stock']

    criar_Produto_Config_SQL = '''INSERT INTO Produto_config(company_id, product_id, price, stock, 
    total_sale) VALUES(%s, %s, %s, %s, %s);'''
    

# -------------------------------- EDIÇOES / UPDATES -----------------------------------------------------

    editar_companyID_SQL = "UPDATE Produto_config SET company_id=%s WHERE id=%s"
    editar_productID_SQL = "UPDATE Produto_config SET product_id=%s WHERE id=%s"
    editar_price_SQL = "UPDATE Produto_config SET price=%s WHERE id=%s"
    editar_stock_SQL = "UPDATE Produto_config SET stock=%s WHERE id=%s"
    editar_totalSale_SQL = "UPDATE Produto_config SET total_sale=%s WHERE id=%s"


# ------------------------------ LISTAGEM / GETs NORMAIS -------------------------------------------------

    listar_PC_geral_SQL = "SELECT * FROM Produto_config;"
    listar_ProductConfig_ID = 'SELECT id FROM Produto_config WHERE id=%s;'
    listar_ProductConfig_Price = 'SELECT price FROM Produto_config WHERE id=%s;'
    listar_ProductConfig_Stock = 'SELECT stock from Produto_config WHERE id=%s;'
    listar_ProdutoConfig_TS = 'SELECT total_sale from Produto_config where id=%s'


#  ------------------------------ LISTAGEM / GETs - QUERY PARAMETERS ---------------------------------------

    listar_PC_QP_by_companyID_and_productID_SQL = '''SELECT pc.id, c.id, c.name, c.cnpj, 
    p.id, p.name, pc.price, pc.stock, pc.total_sale FROM Produto_config pc INNER JOIN Company c ON 
    pc.company_id = c.id INNER JOIN Produto p ON pc.product_id = p.id WHERE pc.company_id=%s 
    AND pc.product_id=%s ORDER BY pc.id;'''
    
    listar_PC_QP_by_companyID_SQL = '''SELECT pc.id, c.id, c.name, c.cnpj, p.id, p.name, pc.price, pc.stock, 
    pc.total_sale FROM Produto_config pc INNER JOIN Company c ON pc.company_id = c.id 
    INNER JOIN Produto p ON pc.product_id = p.id WHERE pc.company_id=%s;'''

    listar_PC_QP_by_produtoID_SQL = '''SELECT pc.id, c.id, c.name, c.cnpj, p.id, p.name, pc.price, pc.stock, 
    pc.total_sale FROM Produto_config pc INNER JOIN Company c ON pc.company_id = c.id 
    INNER JOIN Produto p ON pc.product_id = p.id WHERE pc.product_id=%s ORDER BY pc.id;'''