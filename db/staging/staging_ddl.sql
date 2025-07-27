-- Create staging.sales_raw
CREATE TABLE IF NOT EXISTS staging.sales_raw (
    product_code VARCHAR(50),
    store_code VARCHAR(50),
    date_sold DATE,
    price NUMERIC(10, 2),
    discount NUMERIC(5, 2),
    quantity INT
);

-- Create staging.products_raw
CREATE TABLE IF NOT EXISTS staging.products_raw (
    product_code VARCHAR(50),
    product_name VARCHAR(100),
    category VARCHAR(100),
    sub_category VARCHAR(100)
);

-- Create staging.stores_raw
CREATE TABLE IF NOT EXISTS staging.stores_raw (
    store_code VARCHAR(50),
    store_name VARCHAR(100),
    city VARCHAR(100),
    region VARCHAR(100),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    open_date DATE
);
