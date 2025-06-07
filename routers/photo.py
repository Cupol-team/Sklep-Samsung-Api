from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from db.database import get_db
from db import crud, models
from schemas.menu_item import Photo, PhotoCreate

router = APIRouter(
    prefix="/photos",
    tags=["photos"],
    responses={404: {"description": "Не найдено"}}
)

@router.get("/", response_model=List[Photo])
def get_photos(
    skip: int = 0, 
    limit: int = 100, 
    is_main: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Photo)
    if is_main is not None:
        query = query.filter(models.Photo.is_main == is_main)
    photos = query.offset(skip).limit(limit).all()
    return photos

@router.get("/{photo_id}", response_model=Photo)
def get_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = crud.get_photo(db, photo_id=photo_id)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Фотография с ID {photo_id} не найдена")
    return photo

@router.put("/{photo_id}", response_model=Photo)
def update_photo(photo_id: int, photo_data: PhotoCreate, db: Session = Depends(get_db)):
    db_photo = crud.get_photo(db, photo_id=photo_id)
    if db_photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Фотография с ID {photo_id} не найдена")
    
    if photo_data.is_main == 1:
        for menu_item in db_photo.menu_items:
            for item_photo in menu_item.photos:
                if item_photo.id != db_photo.id and item_photo.is_main == 1:
                    setattr(item_photo, "is_main", 0)
        db.commit()
    
    updated_photo = crud.update_photo(db, photo_id=photo_id, photo=photo_data)
    if updated_photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Не удалось обновить фотографию с ID {photo_id}")
    
    return updated_photo

@router.delete("/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_photo(photo_id: int, db: Session = Depends(get_db)):
    success = crud.delete_photo(db, photo_id=photo_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Фотография с ID {photo_id} не найдена")
    
    return None
