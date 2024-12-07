from fastapi import APIRouter, HTTPException
from database import database, tubeteikas, operations
from models import Tubeteika, Operation

router = APIRouter()

@router.post("/tubeteikas/")
async def create_tubeteika(tubeteika: Tubeteika):
    query = tubeteikas.insert().values(
        name=tubeteika.name,
        produced=tubeteika.produced,
        sold=tubeteika.sold,
        price=tubeteika.price,
    )
    last_record_id = await database.execute(query)
    return {"id": last_record_id, **tubeteika.model_dump()}

@router.get("/tubeteikas/")
async def read_tubeteikas():
    query = tubeteikas.select()
    return await database.fetch_all(query)

@router.get("/tubeteikas/{tubeteika_id}")
async def read_tubeteika(tubeteika_id: int):
    query = tubeteikas.select().where(tubeteikas.c.id == tubeteika_id)
    tubeteika = await database.fetch_one(query)
    if not tubeteika:
        raise HTTPException(status_code=404, detail="Tubeteika not found")
    return tubeteika

@router.put("/tubeteikas/{tubeteika_id}")
async def update_tubeteika(tubeteika_id: int, tubeteika: Tubeteika):
    query = (
        tubeteikas.update()
        .where(tubeteikas.c.id == tubeteika_id)
        .values(
            name=tubeteika.name,
            produced=tubeteika.produced,
            sold=tubeteika.sold,
            price=tubeteika.price,
        )
    )
    result = await database.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="Tubeteika not found")
    return {"id": tubeteika_id, **tubeteika.model_dump()}

@router.delete("/tubeteikas/{tubeteika_id}")
async def delete_tubeteika(tubeteika_id: int):
    query = tubeteikas.delete().where(tubeteikas.c.id == tubeteika_id)
    result = await database.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="Tubeteika not found")
    return {"message": f"Tubeteika with id {tubeteika_id} deleted successfully"}

@router.post("/operations/")
async def create_operation(operation: Operation):
    query = operations.insert().values(name=operation.name)
    last_record_id = await database.execute(query)
    return {"id": last_record_id, **operation.model_dump()}

@router.get("/operations/")
async def read_operations():
    query = operations.select()
    return await database.fetch_all(query)

@router.put("/operations/{operation_id}")
async def update_operation(operation_id: int, operation: Operation):
    query = operations.update().where(operations.c.id == operation_id).values(name=operation.name)
    result = await database.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="Operation not found")
    return {"id": operation_id, **operation.model_dump()}

@router.delete("/operations/{operation_id}")
async def delete_operation(operation_id: int):
    query = operations.delete().where(operations.c.id == operation_id)
    result = await database.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="Operation not found")
    return {"message": f"Operation with id {operation_id} deleted successfully"}
