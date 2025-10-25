from sqlalchemy import inspect
from ftc4.data_pipeline.database.connection import engine
from ftc4.data_pipeline.database.init_db import init_db

def test_init_db():
    init_db()

def test_check_tables():
    insp = inspect(engine)
    assert insp.get_table_names() == ['stock_prices']


    