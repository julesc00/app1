from typing import Dict, Optional

import uvicorn
from fastapi import Body, FastAPI, Path, Query, Request
from pydantic import BaseModel

app = FastAPI()


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


@app.post("/student")
async def add_student(student: Student):
    return student


@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.post("/items/")
async def create_item(item: Item):
    dct = item.model_dump()
    dct["price"] = item.price * 1.2
    return item

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
