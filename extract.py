import pandas as pd

def extract(customers_path, orders_path):
    try:
        customers_df = pd.read_csv(customers_path)
    except FileNotFoundError:
        print('Customers file not found')
        customers_df = None
    try:   
            orders_df = pd.read_csv(orders_path)
    except FileNotFoundError:
            print('Orders file not found')
            orders_df = None
    return customers_df, orders_df