
from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def read_root():
    return {"Message": "Hello From the Route", "Status": "Success"}


@app.get("/products")
def listProducts():
    return {"message":"Hello From the Products Route", "Status": "Success"}



