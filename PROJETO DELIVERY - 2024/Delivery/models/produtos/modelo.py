class Produto:
    def __init__(self, name, description, category_id, id=None):
        self.id = id
        self.name = name
        self.description = description
        self.category_id = category_id

