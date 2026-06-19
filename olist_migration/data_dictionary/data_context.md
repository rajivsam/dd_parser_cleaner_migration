# Data Context

## Dataset overview

This project uses a subset of the Kaggle dataset "Brazilian E-Commerce Public Dataset by Olist" (`olistbr/brazilian-ecommerce`). The original dataset contains approximately 100,000 anonymized orders from the Olist marketplace spanning 2016 to 2018. It includes multi-dimensional information across orders, customers, products, payments, geolocation, and reviews.

## Subset used in this example

We are using the raw Olist files from the Kaggle dataset and preparing them into a cleaned order-level dataset. The focus is on the São Paulo (SP) region for the year 2017. The subset includes:

- Olist raw orders from `olist_orders_dataset.csv`
- Olist raw order items from `olist_order_items_dataset.csv`
- Olist raw customer records from `olist_customers_dataset.csv`

From these, the notebook builds `olist_daily_orders_prepared.csv` and then filters to the SP subset, producing:

- `SP_2017_orders_filtered_prepared.csv`
- `SP_2017_weekly_revenue_prepared.csv`
- `SP_2017_freq_prod_weekly_sales_prepared.csv`

## What this subset represents

This subset represents order-level activity for customers located in São Paulo state during 2017. Each row is a single order item with product, customer, and timestamp details. The dataset is suitable for:

- temporal revenue analysis by week
- customer geography-based segmentation for SP
- product purchase frequency analysis in the SP 2017 window

## References for the larger dataset

- Kaggle dataset landing page: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- Original dataset title: Brazilian E-Commerce Public Dataset by Olist
- Dataset description: 100,000 Orders with product, customer and reviews info
- Related dataset: Marketing Funnel Dataset by Olist (`olistbr/marketing-funnel-olist`)

## Notes on data preparation

- The raw dataset is downloaded from Kaggle into `data/`.
- The notebook merges order, order item, and customer files to create the prepared dataset.
- Additional derived fields are added for year, month, and ISO week of year.
- The final SP 2017 subset uses `customer_state == 'SP'` and `year == 2017`.

## Data lineage

1. Download and unzip raw Kaggle files into `data/`.
2. Merge raw orders and raw order items on `order_id`.
3. Enrich with customer geography from raw customers.
4. Save the merged output to `data/olist_daily_orders_prepared.csv`.
5. Filter to SP customers and the year 2017.
6. Produce analysis artifacts in `data/`.
