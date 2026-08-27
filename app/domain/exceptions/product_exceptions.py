class ProductDomainException(Exception):
    """Base exception for product domain errors."""
    pass

class ProductNotFoundException(ProductDomainException):
    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"Product with id {product_id} was not found.")

class InvalidProductDataException(ProductDomainException):
    def __init__(self, message: str):
        super().__init__(message)
