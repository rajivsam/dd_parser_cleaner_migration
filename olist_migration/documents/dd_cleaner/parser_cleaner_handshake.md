# 📑 Data Dictionary: Provisional Entity Assignment Report
**Generation Timestamp:** `2026-06-18 09:39:13`
**Source Blueprint:** `data_dictionary.csv`

### 🏗️ Structural Assessment
- **Inferred Dataset Type:** `cross-sectional`
> ⚠️ **Note:** This inference is an automated suggestion based on schema patterns and may be incorrect. The `dataset_type` must be explicitly confirmed or defined in `config.yaml` before the Cleaner phase begins.

### 📊 Classification Summary
- **Customers**: 4 fields
- **Orders**: 2 fields
- **OrderItems**: 2 fields
- **Products**: 1 fields

### ⚠️ Orphans in Data Dictionary
> These attributes exist in the dictionary but were **not found** in the raw data file. They have been excluded from the assignments below.

- `freq_cust`
- `freq_purch_prod`
- `year`
- `month`
- `woy`

---

### 📋 Detailed Assignments
| Attribute                  | Assignment   | Logical Type   | Physical Type   | Flag: Geographic   |
|----------------------------|--------------|----------------|-----------------|--------------------|
| `order_id`                 | `Orders`     | `text`         | `str`           | `False`            |
| `customer_id`              | `Customers`  | `text`         | `str`           | `False`            |
| `order_purchase_timestamp` | `Orders`     | `datetime`     | `datetime`      | `False`            |
| `order_item_id`            | `OrderItems` | `numeric`      | `int`           | `False`            |
| `product_id`               | `Products`   | `text`         | `str`           | `False`            |
| `price`                    | `OrderItems` | `numeric`      | `float`         | `False`            |
| `customer_zip_code_prefix` | `Customers`  | `numeric`      | `int`           | `True`             |
| `customer_city`            | `Customers`  | `text`         | `str`           | `True`             |
| `customer_state`           | `Customers`  | `categorical`  | `str`           | `True`             |

---
*Report generated via automated dd-parser post-processing.*