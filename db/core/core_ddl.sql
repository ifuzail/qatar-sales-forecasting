-- core.fact_sales
CREATE TABLE IF NOT EXISTS core.fact_sales (
    sales_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES core.dim_product(product_id),
    store_id INT REFERENCES core.dim_store(store_id),
    date_id DATE REFERENCES core.dim_date(date),
    price NUMERIC(10, 2),
    discount NUMERIC(5, 2),
    quantity INT
);

-- core.dim_product
CREATE TABLE IF NOT EXISTS core.dim_product (
    product_id SERIAL PRIMARY KEY,
    product_name TEXT,
    category TEXT
);

-- core.dim_store
CREATE TABLE IF NOT EXISTS core.dim_store (
    store_id SERIAL PRIMARY KEY,
    store_name TEXT UNIQUE,
    city TEXT DEFAULT 'Qatar'
);

-- core.dim_date
CREATE TABLE IF NOT EXISTS core.dim_date (
    date DATE PRIMARY KEY,
    day INT,
    month INT,
    year INT,
    quarter INT,
    weekday TEXT
);

