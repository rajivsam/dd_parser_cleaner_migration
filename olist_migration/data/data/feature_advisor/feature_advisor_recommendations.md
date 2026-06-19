# Feature Advisor Recommendations

## order_id
- Recommended method: low_count_cat_var_encoding + target_encoding
- Rationale: Use low-count categorical grouping on train data followed by target encoding to produce numeric model-ready features while avoiding unseen categories during validation/active scoring.

## customer_id
- Recommended method: low_count_cat_var_encoding + target_encoding
- Rationale: Use low-count categorical grouping on train data followed by target encoding to produce numeric model-ready features while avoiding unseen categories during validation/active scoring.

## order_purchase_timestamp
- Recommended method: low_count_cat_var_encoding + target_encoding
- Rationale: Use low-count categorical grouping on train data followed by target encoding to produce numeric model-ready features while avoiding unseen categories during validation/active scoring.

## order_item_id
- Recommended method: No encoding required
- Rationale: Numeric feature should be passed through the numeric pipeline without additional categorical encoding, preserving train/validation artifact separation.

## product_id
- Recommended method: low_count_cat_var_encoding + target_encoding
- Rationale: Use low-count categorical grouping on train data followed by target encoding to produce numeric model-ready features while avoiding unseen categories during validation/active scoring.

## price
- Recommended method: No encoding required
- Rationale: Numeric feature should be passed through the numeric pipeline without additional categorical encoding, preserving train/validation artifact separation.

## customer_zip_code_prefix
- Recommended method: No encoding required
- Rationale: Numeric feature should be passed through the numeric pipeline without additional categorical encoding, preserving train/validation artifact separation.

## customer_city
- Recommended method: low_count_cat_var_encoding + target_encoding
- Rationale: Use low-count categorical grouping on train data followed by target encoding to produce numeric model-ready features while avoiding unseen categories during validation/active scoring.

## customer_state
- Recommended method: low_count_cat_var_encoding + target_encoding
- Rationale: Use low-count categorical grouping on train data followed by target encoding to produce numeric model-ready features while avoiding unseen categories during validation/active scoring.

## freq_cust
- Recommended method: No encoding required
- Rationale: Numeric feature should be passed through the numeric pipeline without additional categorical encoding, preserving train/validation artifact separation.

## freq_purch_prod
- Recommended method: No encoding required
- Rationale: Numeric feature should be passed through the numeric pipeline without additional categorical encoding, preserving train/validation artifact separation.

## year
- Recommended method: Review metadata
- Rationale: The field does not match a recognized categorical, numeric, or text featurization pattern. Validate whether it should be treated as a specialized text or hierarchical categorical field.

## month
- Recommended method: Review metadata
- Rationale: The field does not match a recognized categorical, numeric, or text featurization pattern. Validate whether it should be treated as a specialized text or hierarchical categorical field.

## woy
- Recommended method: Review metadata
- Rationale: The field does not match a recognized categorical, numeric, or text featurization pattern. Validate whether it should be treated as a specialized text or hierarchical categorical field.
