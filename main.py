from typing import Optional

import uvicorn
from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
