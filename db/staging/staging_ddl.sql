-- staging.stg_sales
CREATE TABLE IF NOT EXISTS staging.stg_sales (
    product_name TEXT,
    category TEXT,
    price NUMERIC(10, 2),
    date_sold DATE,
    discount NUMERIC(5, 2),
    quantity INTEGER,
    source_store TEXT, -- from file name or manual tagging
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
