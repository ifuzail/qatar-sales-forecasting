/* 

Diclaimer: re-running this query will result in deletion of existing data in the table.


*/




DROP TABLE IF EXISTS core.fact_sales;
-- core.fact_sales
CREATE TABLE IF NOT EXISTS core.fact_sales (
    sales_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES core.dim_product(product_id),
    store_id INT REFERENCES core.dim_store(store_id),
    date_id DATE REFERENCES core.dim_date(date_sold),
    price NUMERIC(10, 2),
    discount NUMERIC(5, 2),
    quantity INT
);

DROP TABLE IF EXISTS core.dim_product;
-- core.dim_product
CREATE TABLE IF NOT EXISTS core.dim_product (
    product_id SERIAL PRIMARY KEY,
    product_name TEXT,
    category TEXT
);

DROP TABLE IF EXISTS core.dim_store;
-- core.dim_store
CREATE TABLE IF NOT EXISTS core.dim_store (
    store_id SERIAL PRIMARY KEY,
    store_name TEXT UNIQUE,
    city TEXT DEFAULT 'Qatar'
);


DROP TABLE IF EXISTS core.dim_date;

-- core.dim_date
CREATE TABLE IF NOT EXISTS core.dim_date (
    date_sold DATE PRIMARY KEY,
    day INT,
    month INT,
    year INT,
    quarter INT,
    weekday TEXT
);

CREATE INDEX IF NOT EXISTS idx_product_id ON core.dim_product(product_id);
CREATE INDEX IF NOT EXISTS idx_store_id ON core.dim_store(store_id);
CREATE INDEX IF NOT EXISTS idx_date_id ON core.dim_date(date_sold);

