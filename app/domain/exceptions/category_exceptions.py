class CategoryNotFoundException(Exception):
    def __init__(self, category_id: int):
        self.category_id = category_id
        super().__init__(f"Category with id {category_id} not found")

class CategoryAlreadyExistsException(Exception):
    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Category with name '{name}' already exists")
