from fastapi import FastAPI, Depends
from models import Product
from database import SessionLocal, engine
from database_models import Base, Product as DBProduct
from sqlalchemy.orm import Session

api = FastAPI()

Base.metadata.create_all(bind=engine)

@api.get("/")
def index():
    return {"message": "Hello World"}
 
products = [  #Table Name
    Product(id=1, name="phone", description="budget phone", price=1000, quantity=10),
    Product(id=2, name="laptop", description="gaming laptop", price=2000, quantity=20),
    Product(id=5, name="mouse", description="gaming mouse", price=200, quantity=30),
    Product(id=4, name="keyboard", description="gaming keyboard", price=300, quantity=40),
]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = SessionLocal()
    count = db.query(DBProduct).count

    if count == 0:
       for product in products:
        db.add(DBProduct(**product.model_dump()))
    
    db.commit()

init_db()
    

@api.get("/products")
def get_all_products(db : SessionLocal = Depends(get_db)):

    db_products = db.query(DBProduct).all()
    return db_products

@api.get("/product/{id}")
def get_product_by_id(id: int, db : SessionLocal = Depends(get_db)): 
   db_product = db.query(DBProduct).filter(DBProduct.id == id).first()
   if db_product:
     return db_product
   return "Product not found"
  

@api.post("/product")
def add_product(product: Product, db : SessionLocal = Depends(get_db)):
    db.add(DBProduct(**product.model_dump()))
    db.commit()
    return product

@api.put("/product")
def update_product(id : int, product : Product, db : SessionLocal = Depends(get_db)):
   db_product = db.query(DBProduct).filter(DBProduct.id == id).first()
   if db_product:
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity
    db.commit()
    return "Product Updated"
   else: 
    return "Product not found"

@api.delete("/product")
def delete_product(id : int, db : SessionLocal = Depends(get_db)):
    db_product = db.query(DBProduct).filter(DBProduct.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted"
    else:
        return "Product not found"