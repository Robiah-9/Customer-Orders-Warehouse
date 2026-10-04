import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from extract import extract
from clean import clean
from load import load
from sqlalchemy import create_engine, text

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

customers_df, orders_df = extract(r'C:\Users\HP\Downloads\customers.csv', r'C:\Users\HP\Downloads\orders.csv')
customers_df, orders_df, orphaned_orders_df = clean(customers_df, orders_df)

with engine.connect() as conn:
    conn.execute(text("TRUNCATE TABLE orders, customers RESTART IDENTITY CASCADE"))
    conn.commit()
load(customers_df, "customers", engine)
load(orders_df, "orders", engine)

