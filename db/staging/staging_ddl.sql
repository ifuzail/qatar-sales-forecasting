/* 

Diclaimer: re-running this query will result in deletion of existing data in the table.


*/


CREATE TABLE IF NOT EXISTS staging.stg_sales (
    product_name TEXT,
    category TEXT,
    price NUMERIC(10, 2),
    date_sold DATE,
    discount NUMERIC(5, 2),
    quantity INTEGER,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


