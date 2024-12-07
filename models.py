from pydantic import BaseModel

class Tubeteika(BaseModel):
    name: str
    produced: int
    sold: int
    price: float

class Operation(BaseModel):
    name: str

class Worker(BaseModel):
    name: str
    work_place: str
    id_telegram: str