from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from .database import Base

# Таблица связи между блюдами и фотографиями (для реализации связи многие-ко-многим)
menu_item_photos = Table(
    'menu_item_photos',
    Base.metadata,
    Column('menu_item_id', Integer, ForeignKey('menu_items.id')),
    Column('photo_id', Integer, ForeignKey('photos.id'))
)

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    
    # Отношение к фотографиям (один ко многим)
    photos = relationship("Photo", secondary=menu_item_photos, back_populates="menu_items")
    
    def __repr__(self):
        return f"<MenuItem(id={self.id}, name='{self.name}', category='{self.category}', price={self.price})>"

class Photo(Base):
    __tablename__ = "photos"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    alt_text = Column(String)
    is_main = Column(Integer, default=0)  # 0 - не основное, 1 - основное фото
    
    # Отношение к блюдам меню (многие ко многим)
    menu_items = relationship("MenuItem", secondary=menu_item_photos, back_populates="photos")
    
    def __repr__(self):
        return f"<Photo(id={self.id}, url='{self.url}', is_main={self.is_main})>"

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>" 