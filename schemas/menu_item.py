from typing import List, Optional
from pydantic import BaseModel, HttpUrl

class PhotoBase(BaseModel):
    url: str
    alt_text: Optional[str] = None
    is_main: int = 0

class PhotoCreate(PhotoBase):
    pass

class Photo(PhotoBase):
    id: int
    
    class Config:
        orm_mode = True

class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str

class MenuItemCreate(MenuItemBase):
    pass

class MenuItem(MenuItemBase):
    id: int
    photos: List[Photo] = []
    
    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    
    class Config:
        orm_mode = True 