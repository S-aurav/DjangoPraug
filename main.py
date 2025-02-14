from fastapi import FastAPI, HTTPException, status, Path, Query
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

inventory = {
    1: {
        'name':'milk',
        'price':3.22,
        'brand':'regular',
    }
}

@app.get('/get-item/{item_id}/')
def get_item(item_id: int = Path(description="The id of the item you'd like to view", gt=0)):
    return inventory[item_id]
# http://127.0.0.1:8000/1

@app.get('/get-by-name/{item_id}')
def get_item(*, item_id: int, name: Optional[str] = None, test = int):
    for item_id in inventory:
        if inventory[item_id]['name'] == name:
            return inventory[item_id]
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item name not found")
# http://127.0.0.1:8000/get-by-name/1?test=2&name=milk

@app.post('/create-item/{item_id}')
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail="Item ID already exists")
    
    inventory[item_id] = item
    return inventory[item_id]

@app.put('/update-item/{item_id}')
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID doesn't exists")
    
    if item.name !=None:
        inventory[item_id].name = item.name

    if item.price !=None:
        inventory[item_id].price = item.price

    if item.brand !=None:
        inventory[item_id].brand = item.brand


    return inventory[item_id]

@app.delete('/delete')
def delete_item(item_id: int = Query(..., description="Thid ID of the item that is to be deleted")):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID doesn't exists")
    
    del inventory[item_id]

    raise HTTPException(status_code=status.HTTP_200_OK, detail="Item deleted successfully!")