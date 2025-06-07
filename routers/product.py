from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from db.database import get_db
from db import crud
from schemas.menu_item import MenuItem, MenuItemCreate, Photo, PhotoCreate

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Не найдено"}}
)

@router.get("/", response_model=List[MenuItem])
def get_products(
    skip: int = 0, 
    limit: int = 100, 
    category: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    products = crud.get_menu_items(db, skip=skip, limit=limit, category=category)
    return products

@router.get("/{product_id}", response_model=MenuItem)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_menu_item(db, item_id=product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Товар с ID {product_id} не найден")
    return product

@router.post("/", response_model=MenuItem, status_code=status.HTTP_201_CREATED)
def create_product(product: MenuItemCreate, db: Session = Depends(get_db)):
    return crud.create_menu_item(db=db, item=product)

@router.put("/{product_id}", response_model=MenuItem)
def update_product(product_id: int, product: MenuItemCreate, db: Session = Depends(get_db)):
    db_product = crud.update_menu_item(db, item_id=product_id, item=product)
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Товар с ID {product_id} не найден")
    return db_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    success = crud.delete_menu_item(db, item_id=product_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Товар с ID {product_id} не найден")
    return None

@router.get("/{product_id}/photos", response_model=List[Photo])
def get_product_photos(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_menu_item(db, item_id=product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Товар с ID {product_id} не найден")
    return product.photos

@router.post("/{product_id}/photos", response_model=Photo, status_code=status.HTTP_201_CREATED)
def add_product_photo(product_id: int, photo: PhotoCreate, db: Session = Depends(get_db)):
    product = crud.get_menu_item(db, item_id=product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Товар с ID {product_id} не найден")
    
    if photo.is_main == 1:
        for existing_photo in product.photos:
            if existing_photo.is_main == 1:
                existing_photo.is_main = 0
        db.commit()
    
    return crud.create_photo(db=db, photo=photo, menu_item_id=product_id)

@router.delete("/{product_id}/photos/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_photo(product_id: int, photo_id: int, db: Session = Depends(get_db)):
    product = crud.get_menu_item(db, item_id=product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Товар с ID {product_id} не найден")
    
    photo = crud.get_photo(db, photo_id=photo_id)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Фотография с ID {photo_id} не найдена")
    
    if product not in photo.menu_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Фотография с ID {photo_id} не принадлежит товару с ID {product_id}"
        )
    
    success = crud.delete_photo(db, photo_id=photo_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Фотография с ID {photo_id} не найдена")
    
    return None
