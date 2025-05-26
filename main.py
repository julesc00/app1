import json
from typing import Dict, Optional

import uvicorn
from fastapi import Body, FastAPI, Form, Path, Query, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl, EmailStr, SecretStr, Json, FileUrl, field_validator
from starlette.responses import HTMLResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

template = Jinja2Templates(directory="templates")


class Employee(BaseModel):
    ID: str
    pwd: SecretStr
    details: Json
    FBProfile: HttpUrl

    @field_validator("ID")
    def is_alphanumeric(cls, v):
        if v.isalnum() is False:
            raise (ValueError("ID must be alphanumeric"))


class Supplier(BaseModel):
    ID: int
    name: str


class Product(BaseModel):
    ID: int
    name: str
    price: float
    supplier: list[Supplier]


class Customer(BaseModel):
    ID: int
    name: str
    products: list[Product]


class Item(BaseModel):
    prod_id: int
    name: str
    price: float
    stock: int


class Student(BaseModel):
    student_id: int
    name: str
    subjects: Dict[str, int]

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "student_id": 20,
                "subject": {"Math": 90, "English": 80}
            }
        }


@app.get("/testjs/{name}", response_class=HTMLResponse)
async def jsdemo(request: Request, name: str):
    """
    This endpoint serves a JavaScript demo page.
    """
    data = {"name": name}
    return template.TemplateResponse("static-js.html", {"request": request, "data": data})


@app.get("/hi")
async def hi():
    body = '''
<html>
<body>
<h2>Hello World!</h2>
</body>
</html>
'''
    return Response(content=body, media_type="text/html")


@app.post("/student")
async def add_student(student: Student):
    return student


@app.get("/{name}", response_class=HTMLResponse)
async def root(request: Request, name: str):
    return template.TemplateResponse("hello.html", {"request": request, "name": name})


@app.get("/password/{password}")
async def get_password(password: SecretStr):
    return {"password": json.dumps(password.get_secret_value())}



@app.post("/items/")
async def create_item(item: Item):
    dct = item.model_dump()
    dct["price"] = item.price * 1.2
    return item

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/employee")
async def add_employee(employee: Employee):
    return employee


@app.get("/employee/{name}/branch/{branch_id}")
async def get_employee(
        branch_id:int = Path(..., ge=1),
        name:str=Path(
            ...,
            regex="^[A-Za-z]+$",
            title="Employee Name",
            description="Employee Name",
            alias="employee_name"
        ),
        br_name:str=Query(None, min_length=5, max_length=10),
        age:Optional[int] = None
):
    """Use ... (the Ellipsis) as the default inside Path(...) to mark it as required"""
    return {"name": name, "branch": br_name, "branch_id": branch_id, "age": age}


@app.post("/product")
async def add_product(
        request: Request,
        prod_id: int = Body(),
        price: float = Body(..., gt=0),
        stock: str = Body(),
):
    """
    Use ... (the Ellipsis) as the default inside Body(...) to mark it as required
    """
    product = {
        "id": prod_id,
        "price": price,
        "stock": stock
    }
    return product


@app.post("/customer")
async def get_customer(customer: Customer):
    """
    """
    return customer


@app.get("/profile/", response_class=HTMLResponse)
async def info(request: Request):
    data = {
        "name": "Catherine",
        "languages": ["Python", "Go"]
    }
    return template.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "data": data
        }
    )


@app.get("/img/", response_class=HTMLResponse)
async def showing_image(request: Request):
    """
    This endpoint serves an image.
    """
    return template.TemplateResponse("static-img.html", {"request": request})


@app.post("/form/")
async def get_form(
        name: str = Form(...),
        address: str = Form(...),
        post: str = Form(...),
):
    return {
        "name": name,
        "address": address,
        "post": post
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
