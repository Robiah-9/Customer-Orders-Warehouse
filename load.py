from sqlalchemy.exc import OperationalError, IntegrityError
from pandas.errors import DatabaseError

def load(df, table_name, engine):
    if df is None:
        print(f"Skipping load for {table_name} — no data to load")
        return None
    try:
        df.to_sql(table_name, con=engine, if_exists="append", index=False)
        print(f'Loaded {len(df)} rows into {table_name}')
    except OperationalError:
        print('Database connection failed')
    except (IntegrityError, DatabaseError):
        print(f"{table_name} rows are duplicated")