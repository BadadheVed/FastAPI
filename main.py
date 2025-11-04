
from fastapi import FastAPI
from models import Product
app = FastAPI()
@app.get("/")
def read_root():
    return {"Message": "Hello From the Route", "Status": "Success"}


products = [
    Product(id=1, name="Laptop", description="A high-performance laptop", price=999.99, quantity=10),
    Product(id=2, name="Smartphone", description="A latest model smartphone", price=699.99, quantity=25),
    Product(id=3, name="Headphones", description="Noise-cancelling headphones", price=199.99, quantity=15)
]

@app.get("/products")
def listProducts():
    return {"products": products , "Status":"Success"}

@app.get("/products/{product_id}")
def getProductById(product_id: int):
    for product in products:
        if product.id == product_id:
            return {"product": product , "Status":"Success"}
    return {"Message": "Product Not Found", "Status": "Failed"}

@app.post("/products")
def addProduct(product: Product):
    products.append(product)
    return {"Message": "Product Added Successfully", "Status": "Success"}

@app.put("/products/{product_id}")
def updateProduct(product_id: int, updated_product: Product):
    for index, product in enumerate(products):
        if product.id == product_id:
            products[index] = updated_product
            return {"Message": "Product Updated Successfully", "Status": "Success"}
    return {"Message": "Product Not Found", "Status": "Failed"}

@app.delete("/products/{product_id}")
def deleteProduct(product_id: int):
    for index, product in enumerate(products):
        if product.id == product_id:
            del products[index]
            return {"Message": "Product Deleted Successfully", "Status": "Success"}
    return {"Message": "Product Not Found", "Status": "Failed"}


