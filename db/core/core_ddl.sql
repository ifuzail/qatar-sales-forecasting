-- Create core.dim_product
CREATE TABLE IF NOT EXISTS core.dim_product (
    product_id SERIAL PRIMARY KEY,
    product_code VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(100),
    category VARCHAR(100),
    sub_category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create core.dim_store
CREATE TABLE IF NOT EXISTS core.dim_store (
    store_id SERIAL PRIMARY KEY,
    store_code VARCHAR(50) UNIQUE NOT NULL,
    store_name VARCHAR(100),
    city VARCHAR(100),
    region VARCHAR(100),
    country VARCHAR(100) DEFAULT 'Qatar',
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    open_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create core.dim_date
CREATE TABLE IF NOT EXISTS core.dim_date (
    date_id DATE PRIMARY KEY,
    day INT,
    month INT,
    year INT,
    quarter INT,
    weekday_name VARCHAR(10),
    is_weekend BOOLEAN
);

-- Create core.fact_sales
CREATE TABLE IF NOT EXISTS core.fact_sales (
    sale_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES core.dim_product(product_id),
    store_id INT REFERENCES core.dim_store(store_id),
    date_id DATE REFERENCES core.dim_date(date_id),
    price NUMERIC(10, 2),
    discount NUMERIC(5, 2),
    quantity INT,
    total_amount NUMERIC(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create core.forecast
CREATE TABLE IF NOT EXISTS core.forecast (
    forecast_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES core.dim_product(product_id),
    store_id INT REFERENCES core.dim_store(store_id),
    date_id DATE REFERENCES core.dim_date(date_id),
    predicted_quantity INT,
    predicted_revenue NUMERIC(10, 2),
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
