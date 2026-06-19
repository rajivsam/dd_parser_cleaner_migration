# Modeling Results Observations

## Summary
The spectral co-clustering analysis of Olist SP 2017 reveals clear temporal affinity structures between specific weeks of the year and product activity profiles. Different times of the year are associated with different groups of products, which supports using a temporal-product joint view rather than a flat product ranking alone.

## Key Observations

- The clustering produced a small number of large week clusters and many smaller, more specific clusters.
- One dominant week cluster contains 21 of the 52 weeks, suggesting a broad baseline demand regime.
- Another significant week cluster contains 11 weeks, and a handful of smaller clusters capture more specialized seasonal patterns.
- Product cluster sizes are highly imbalanced: one cluster includes 8,661 products, which likely corresponds to the baseline set of commonly purchased or evergreen items.
- A second large product cluster contains 420 products, while another cluster contains 150 products, indicating two additional mid-sized affinity groups.
- Several very small product clusters (with 1–14 products) are present, which likely represent highly specialized or seasonal item sets.

## Interpretation

- The largest product cluster appears to represent the store’s baseline inventory — the core products that are purchased regularly across many weeks.
- Smaller product clusters are likely driven by temporal spikes or niche seasonal demand, such as holiday items, promotional bundles, or product-specific campaigns.
- The week clusters align with different demand regimes: a majority of weeks share a common baseline affinity, while a few weeks form distinct clusters with unique product preferences.

## Business Implications

- Baseline inventory planning should be driven by the largest product cluster, as it reflects the core buy-list for São Paulo shoppers.
- Staffing and logistics planning can lean on the largest week cluster for normal operating capacity, while reserving additional flexibility for the weeks in smaller clusters.
- Promotional planning should focus on the small, specialized clusters — these are candidate windows for targeted campaigns or product-specific offers.
- Budget forecasts can differentiate baseline demand from seasonal deviation by viewing the large cluster as the steady-state baseline and the smaller clusters as variance contributors.

## Practical Takeaways

- Use the large product cluster as the default assortment for the SP weekly inventory model.
- Treat the smaller week/product clusters as signal for event-driven or seasonal adjustments.
- This analysis supports a two-tier operational plan: baseline operations plus cluster-triggered surge planning.
- Future work can map these clusters to calendar events, holidays, and promotional periods for sharper planning.

## Conclusion

The Olist SP 2017 clustering results highlight that week-of-year and product affinity are not uniform. A large baseline cluster captures the typical shopping basket, while smaller clusters expose distinct temporal demand patterns. These observations can directly inform inventory, staffing, and budgeting decisions for São Paulo operations.
