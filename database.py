from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
)
from databases import Database

DATABASE_URL = "sqlite:///./test.db"  # Путь к SQLite базе данных

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()

tubeteikas = Table(
    "tubeteikas",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),  # Название
    Column("produced", Integer, default=0),  # Количество произведенных
    Column("sold", Integer, default=0),  # Количество проданных
    Column("price", Float),  # Цена за штуку
)

operations = Table(
    "operations",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100)),  # Название операции
)

# Таблица для учета выполненных операций
operation_logs = Table(
    "operation_logs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("worker_id", Integer, ForeignKey("workers.id")),  # ID работника
    Column("operation_id", Integer, ForeignKey("operations.id")),  # ID операции
    Column("quantity", Integer),  # Количество выполнений
)

# Таблица для учета работников
workers = Table(
    "workers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("work_place", String(50))  # Имя работника
)

metadata.create_all(engine)  # Создаем таблицы в базе данных
