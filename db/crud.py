from sqlalchemy.orm import Session
from typing import List, Optional
from . import models
from schemas import menu_item as schemas

def get_menu_item(db: Session, item_id: int):
    return db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()

def get_menu_items(db: Session, skip: int = 0, limit: int = 100, category: Optional[str] = None):
    query = db.query(models.MenuItem)
    if category:
        query = query.filter(models.MenuItem.category == category)
    return query.offset(skip).limit(limit).all()

def create_menu_item(db: Session, item: schemas.MenuItemCreate):
    db_item = models.MenuItem(
        name=item.name,
        description=item.description,
        price=item.price,
        category=item.category
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_menu_item(db: Session, item_id: int, item: schemas.MenuItemCreate):
    db_item = get_menu_item(db, item_id)
    if db_item:
        update_data = {
            "name": item.name,
            "description": item.description,
            "price": item.price,
            "category": item.category
        }
        for key, value in update_data.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_menu_item(db: Session, item_id: int):
    db_item = get_menu_item(db, item_id)
    if db_item:
        for photo in db_item.photos:
            delete_photo(db, photo.id)
        db.delete(db_item)
        db.commit()
        return True
    return False

def get_photo(db: Session, photo_id: int):
    return db.query(models.Photo).filter(models.Photo.id == photo_id).first()

def create_photo(db: Session, photo: schemas.PhotoCreate, menu_item_id: int):
    db_photo = models.Photo(
        url=photo.url,
        alt_text=photo.alt_text,
        is_main=photo.is_main
    )
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    
    menu_item = get_menu_item(db, menu_item_id)
    if menu_item:
        menu_item.photos.append(db_photo)
        db.commit()
    
    return db_photo

def update_photo(db: Session, photo_id: int, photo: schemas.PhotoCreate):
    db_photo = get_photo(db, photo_id)
    if db_photo:
        update_data = {
            "url": photo.url,
            "alt_text": photo.alt_text,
            "is_main": photo.is_main
        }
        for key, value in update_data.items():
            setattr(db_photo, key, value)
        db.commit()
        db.refresh(db_photo)
    return db_photo

def delete_photo(db: Session, photo_id: int):
    db_photo = get_photo(db, photo_id)
    if db_photo:
        db.delete(db_photo)
        db.commit()
        return True
    return False

def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_category_by_name(db: Session, name: str):
    return db.query(models.Category).filter(models.Category.name == name).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(
        name=category.name,
        description=category.description
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category: schemas.CategoryCreate):
    db_category = get_category(db, category_id)
    if db_category:
        update_data = {
            "name": category.name,
            "description": category.description
        }
        for key, value in update_data.items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False 