from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from models import Product, Base
from db import SessionLocal, engine

app = FastAPI()

# Create all tables
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Message": "Hello From the Route", "Status": "Success"}


@app.get("/products")
def list_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return {"products": [p.__dict__ for p in products], "Status": "Success"}


@app.get("/products/{product_id}")
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product Not Found")
    return {"product": product.__dict__, "Status": "Success"}


@app.post("/products")
def add_product(
    name: str = Body(...),
    description: str = Body(...),
    price: float = Body(...),
    quantity: int = Body(...),
    db: Session = Depends(get_db)
):
    new_product = Product(
        name=name,
        description=description,
        price=price,
        quantity=quantity
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"Message": "Product Added Successfully", "product": new_product.__dict__, "Status": "Success"}


@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    name: str = Body(...),
    description: str = Body(...),
    price: float = Body(...),
    quantity: int = Body(...),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product Not Found")

    product.name = name
    product.description = description
    product.price = price
    product.quantity = quantity

    db.commit()
    db.refresh(product)
    return {"Message": "Product Updated Successfully", "product": product.__dict__, "Status": "Success"}


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product Not Found")

    db.delete(product)
    db.commit()
    return {"Message": "Product Deleted Successfully", "Status": "Success"}
