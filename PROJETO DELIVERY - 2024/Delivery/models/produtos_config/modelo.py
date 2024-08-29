class Produto_Config:
    def __init__(self, company_id, product_id, price, stock, total_sale, id=None):
        self.id = id
        self.company_id = company_id
        self.product_id = product_id
        self.price = price
        self.stock = stock
        self.total_sale = total_sale