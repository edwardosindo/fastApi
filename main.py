#You need this to use FastApi, work with statues and be able to end HTTPExceptions
from fastapi import FastAPI, status, HTTPException

#Both used for BaseModel
from pydantic import BaseModel
from typing import Optional



# You need to be able to turn classes into JSONs and return 
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


app = FastAPI()

#create a basemodel how the customer class will look like

class Customer(BaseModel):
    customer_id: str
    country: str
    # city : Optional[str] = None


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

class URLlink(BaseModel):
    #url: str
    url: Optional[str] = None

class Invoice(BaseModel):
    invoice_no : int
    invoice_date : str
    customer: Optional[URLlink] = None

fakeInvoiceTable = dict()



@app.post("/customer")
async def create_customer(item: Customer): #body awaits json with customer:
#This is how to work with and return a item
#   country = item.country
#   return {item.country}

        # You will add here the code for created a customer in the database


        # Encode the created customer item if succesful into a json and return
        json_compatible_item_data = jsonable_encoder(item)
        return JSONResponse(content=json_compatible_item_data, status_code=201)

#Get a customer by customer_id
@app.get("/customer/{customer_id}") # Customer ID will be a path parameter
async def read_customer(customer_id: str):

    # Only succeed if the item is  12345
    if customer_id == "12345" :
        # Create a fake customer (usually you would get this from a database)
        item = Customer(customer_id = "12345", country= "Germany")

        # Encode the customer into json and send it back 
        json_compatible_item_data = jsonable_encoder(item)
        return JSONResponse(content= json_compatible_item_data)

    else: 
        # Raise a 404 exception
        raise HTTPException(status_code=404, detail= "Item not found")

#Create a new invoice for a customer
@app.post("/customer/{customer_id}/invoice")
async def create_invoice(customer_id: str, invoice: Invoice):

    #Add the customer link to the invoice
    invoice.customer.url = "/customer/" + customer_id

    #Turn the invoice instance into a JSON string and store it 
    jsonInvoice = jsonable_encoder(invoice)
    fakeInvoiceTable[invoice.invoice_no] = jsonInvoice

    #Read it from the store and return a stored item
    ex_invoice = fakeInvoiceTable[invoice.invoice_no] 

    return JSONResponse(content= ex_invoice)


@app.get("/invoice/{invoice_no}")
async def read_invoice(invoice_no:int):
    #Option to manually create an invoice
        #ex_inv = invoice(invoice_no = invoice_no, invoice_data ="2021-01-05")
        #json_compatible_item_data = json_encoder(ex_inv)

    #Read invoice from the dictionary
    ex_invoice = fakeInvoiceTable[invoice_no]

    #Return the json that we stored
    return JSONResponse(content=ex_invoice)

#Return all invoices 
@app.get("/customer/ {customer_id}/invoice")
async def get_invoices(customer_id: str):
    #Create links to the actual invoice(get from DB)
    ex_json = {
        "id_123456" : "/invoice/123456",
        "id_789101" : "/invoice/789101",
    }
    return JSONResponse(content=ex_json)





    

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.get("/")
def read_root():
    return {"Hello": "World"}