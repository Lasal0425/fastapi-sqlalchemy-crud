from fastapi import FastAPI
from models import Product

api = FastAPI()

@api.get("/")
def index():
    return {"message": "Hello World"}
 
products = [
    Product(id=1, name="phone", description="budget phone", price=1000, quantity=10),
    Product(id=2, name="laptop", description="gaming laptop", price=2000, quantity=20),
    Product(id=5, name="mouse", description="gaming mouse", price=200, quantity=30),
    Product(id=4, name="keyboard", description="gaming keyboard", price=300, quantity=40),
]

@api.get("/products")
def get_all_products():
    
    return products

@api.get("/product/{id}")
def get_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product
    
    return "Product not found"

@api.post("/product")
def add_product(product: Product):
    products.append(product)
    return product

@api.put("/product")
def update_product(id : int, product : Product):
    for i in range (len(products)):
        if products[i].id == id:
            products[i] = product
            return "product updated"
    
    return "Product not found"

@api.delete("/product")
def delete_product(id : int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "product deleted"

    return "Product not found"