# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/addresses/", response_model=schemas.Address)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    return crud.create_address(db=db, address=address)

@app.get("/addresses/{address_id}", response_model=schemas.Address)
def read_address(address_id: int, db: Session = Depends(get_db)):
    db_address = crud.get_address(db, address_id=address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.get("/addresses/", response_model=list[schemas.Address])
def read_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    addresses = crud.get_addresses(db, skip=skip, limit=limit)
    return addresses

@app.delete("/addresses/{address_id}", response_model=schemas.Address)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    db_address = crud.delete_address(db, address_id=address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.put("/addresses/{address_id}", response_model=schemas.Address)
def update_address(address_id: int, address: schemas.AddressUpdate, db: Session = Depends(get_db)):
    db_address = crud.update_address(db, address_id=address_id, address=address)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.get("/addresses/nearby/", response_model=list[schemas.Address])
def read_nearby_addresses(latitude: float, longitude: float, distance: float, db: Session = Depends(get_db)):
    addresses = crud.get_addresses_within_distance(db, latitude, longitude, distance)
    return addresses
