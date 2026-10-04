def clean(customers_df, orders_df):
    if customers_df is None or orders_df is None:
        return None, None, None
    else:
        customers_df['city'] = customers_df['city'].str.strip().str.title()
        customers_df['city'] = customers_df['city'].replace({"Ph": "Port Harcourt"})
        customers_df['customer_name'] = customers_df['customer_name'].str.strip().str.title()
        customers_df = customers_df.drop_duplicates()
        customers_df['email_missing'] = customers_df['email'].isnull()
        orders_df['unit_price'] = orders_df.groupby('product')['unit_price'].transform(lambda x: x.fillna(x.mean()))
        orphaned_orders = ~(orders_df['customer_id'].isin(customers_df['customer_id']))
        orphaned_orders_df = orders_df[orphaned_orders]
        print(f"{len(orphaned_orders_df)} orphaned orders rejected")
        orders_df = orders_df[~orphaned_orders]
        return customers_df, orders_df, orphaned_orders_df