-- Check duplicate product names
SELECT product_name, COUNT(*) 
FROM core.dim_product 
GROUP BY product_name 
HAVING COUNT(*) > 1;

-- Check duplicate store_name + city combos
SELECT store_name, city, COUNT(*) 
FROM core.dim_store 
GROUP BY store_name, city 
HAVING COUNT(*) > 1;

-- Check duplicate dates
SELECT date_sold, COUNT(*) 
FROM core.dim_date 
GROUP BY date_sold 
HAVING COUNT(*) > 1;

--truncate the table before use
TRUNCATE TABLE core.fact_sales;

WITH dedup_product AS (
    SELECT DISTINCT ON (product_name) product_id, product_name
    FROM core.dim_product
),
dedup_store AS (
    SELECT DISTINCT ON (store_name, city) store_id, store_name, city
    FROM core.dim_store
),
dedup_date AS (
    SELECT DISTINCT ON (date_sold) date_sold
    FROM core.dim_date
)
INSERT INTO core.fact_sales (product_id, store_id, date_id, price, discount, quantity)
SELECT 
    dp.product_id,
    ds.store_id,
    dd.date_sold,
    s.price,
    s.discount,
    s.quantity
FROM staging.stg_sales_cleaned s
JOIN dedup_product dp ON s.product_name = dp.product_name
JOIN dedup_store ds ON s.store_name = ds.store_name AND s.region = ds.city
JOIN dedup_date dd ON s.date_sold::DATE = dd.date_sold;

SELECT * FROM core.fact_sales;