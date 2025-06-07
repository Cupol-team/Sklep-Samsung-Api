from sqlalchemy.orm import Session
from . import models, database, crud
from schemas.menu_item import MenuItemCreate, PhotoCreate

def init_db():
    """Инициализация базы данных и заполнение тестовыми данными"""
    # Создание таблиц
    models.Base.metadata.create_all(bind=database.engine)
    
    # Получение сессии базы данных
    db = database.SessionLocal()
    
    # Проверка, есть ли уже данные в базе
    menu_items = db.query(models.MenuItem).all()
    if menu_items:
        print("База данных уже инициализирована")
        db.close()
        return
    
    # Добавление тестовых данных
    test_menu_items = [
        MenuItemCreate(
            name="Борщ",
            description="Традиционный суп со свеклой, капустой и говядиной",
            price=320.0,
            category="Супы"
        ),
        MenuItemCreate(
            name="Салат Цезарь",
            description="Классический салат с курицей, сыром пармезан и соусом Цезарь",
            price=420.0,
            category="Салаты"
        ),
        MenuItemCreate(
            name="Паста Карбонара",
            description="Итальянская паста с соусом из бекона, яиц и сыра пармезан",
            price=480.0,
            category="Основные блюда"
        ),
        MenuItemCreate(
            name="Стейк Рибай",
            description="Сочный стейк из мраморной говядины с гарниром",
            price=890.0,
            category="Основные блюда"
        ),
        MenuItemCreate(
            name="Тирамису",
            description="Классический итальянский десерт с маскарпоне и кофе",
            price=350.0,
            category="Десерты"
        ),
        MenuItemCreate(
            name="Пицца Маргарита",
            description="Классическая пицца с томатным соусом, моцареллой и базиликом",
            price=450.0,
            category="Пицца"
        ),
        MenuItemCreate(
            name="Чизкейк",
            description="Нежный чизкейк с ягодным соусом",
            price=320.0,
            category="Десерты"
        ),
        MenuItemCreate(
            name="Лимонад",
            description="Освежающий домашний лимонад",
            price=190.0,
            category="Напитки"
        ),
        MenuItemCreate(
            name="Суши-сет",
            description="Набор из 20 суши и роллов с соевым соусом и имбирем",
            price=1200.0,
            category="Суши"
        ),
        MenuItemCreate(
            name="Греческий салат",
            description="Салат с огурцами, помидорами, сыром фета и оливками",
            price=380.0,
            category="Салаты"
        )
    ]
    
    # Добавляем блюда меню
    db_menu_items = []
    for item in test_menu_items:
        db_item = crud.create_menu_item(db, item)
        db_menu_items.append(db_item)
    
    # Добавляем тестовые фотографии для блюд
    test_photos = [
        {"url": "https://example.com/photos/borsch.jpg", "menu_item_id": 1, "is_main": 1},
        {"url": "https://example.com/photos/borsch2.jpg", "menu_item_id": 1, "is_main": 0},
        {"url": "https://example.com/photos/caesar.jpg", "menu_item_id": 2, "is_main": 1},
        {"url": "https://example.com/photos/carbonara.jpg", "menu_item_id": 3, "is_main": 1},
        {"url": "https://example.com/photos/steak.jpg", "menu_item_id": 4, "is_main": 1},
        {"url": "https://example.com/photos/tiramisu.jpg", "menu_item_id": 5, "is_main": 1},
        {"url": "https://example.com/photos/pizza.jpg", "menu_item_id": 6, "is_main": 1},
        {"url": "https://example.com/photos/cheesecake.jpg", "menu_item_id": 7, "is_main": 1},
        {"url": "https://example.com/photos/lemonade.jpg", "menu_item_id": 8, "is_main": 1},
        {"url": "https://example.com/photos/sushi.jpg", "menu_item_id": 9, "is_main": 1},
        {"url": "https://example.com/photos/greek_salad.jpg", "menu_item_id": 10, "is_main": 1},
    ]
    
    for photo_data in test_photos:
        photo = PhotoCreate(
            url=photo_data["url"],
            alt_text=None,
            is_main=photo_data["is_main"]
        )
        crud.create_photo(db, photo, photo_data["menu_item_id"])
    
    print("База данных успешно инициализирована")
    db.close()

if __name__ == "__main__":
    init_db() 