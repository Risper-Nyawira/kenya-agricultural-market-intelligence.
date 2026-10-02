# Analysis procedure and first findings

## Scope

This first analysis studies monthly **wholesale tomato prices** in eight Kenyan markets: Eldoret, Busia, Nairobi, Nakuru, Embu, Kisumu, Mombasa, and Kisii. The objective is to establish a reproducible market-intelligence baseline, not to produce causal forecasts.

## Procedure performed

1. **Preserved source data.** The KNBS/NIPFN KAMIS workbook, FAOSTAT production bulk file, NASA POWER climate files, WFP reference files, and county boundaries were stored as raw inputs and never overwritten.
2. **Inspected KAMIS structure.** The record-level `Data` worksheet contains year, month, county, market, commodity, unit, kilogram quantity, and price.
3. **Audited commodity coverage.** Tomatoes have 5,625 observations, 300 markets, and 135 observed months from January 2012 through September 2024. Tomato therefore passed the initial availability test.
4. **Selected markets by completeness.** The eight chosen markets have 87–127 monthly observations each. Reporting is intermittent, so all estimates report the observed-data period rather than assuming a complete monthly panel.
5. **Cleaned the price panel.** The pipeline retained exact `tomatoes` records for selected markets, required valid date/price/kilogram values, removed exact commodity-market-date duplicates, and retained original unit and price. All selected values used `kg = 1`, so `price_per_kg = price / kg` is KES per kg.
6. **Extracted national production context.** FAOSTAT annual Kenya tomato production, harvested area, and yield were reshaped into a year-level table.
7. **Reshaped climate context.** NASA POWER corrected precipitation and 2m temperature were converted to market-location month-year rows. Four selected markets could be matched to the downloaded point series: Eldoret, Nairobi, Kisumu, and Nakuru.
8. **Created a SQLite database.** Clean price, production, and climate tables were loaded into `03_sql/market_intelligence.sqlite`, with reusable market-summary, seasonality, and annual context views.
9. **Generated outputs.** Trend and seasonality charts, coverage tables, volatility summaries, production-price context, and climate-price context were saved in `06_outputs`.
10. **Performed outlier sensitivity checks.** Three records exceed their market-specific Q3 + 3×IQR thresholds. They remain in the flagged dataset, but a sensitivity summary excludes them so one unusually large value does not dominate a market comparison.

## Data-quality results

- Clean selected-market panel: 783 price records, eight markets, January 2012–September 2024.
- Missing values in required cleaned fields: zero.
- Duplicate commodity-market-date records after cleaning: zero.
- Price unit: kilogram for every selected record; no cross-unit conversion was required.
- Flagged records: Busia, April 2024 (KES 583.33/kg); Embu, February 2023 (KES 379.65/kg); Embu, March 2023 (KES 188.38/kg).

## Findings: price variation across markets

The sensitivity summary excluding flagged observations gives the following mean wholesale prices:

| Market | Observations | Mean KES/kg | Median KES/kg | Coefficient of variation |
| --- | ---: | ---: | ---: | ---: |
| Kisii | 87 | 85.55 | 82.03 | 0.324 |
| Mombasa | 89 | 79.48 | 82.47 | 0.343 |
| Kisumu | 90 | 77.31 | 73.05 | 0.297 |
| Nairobi | 96 | 74.98 | 76.86 | 0.239 |
| Eldoret | 127 | 74.66 | 74.38 | 0.309 |
| Busia | 109 | 59.69 | 55.12 | 0.250 |
| Nakuru | 94 | 59.62 | 57.97 | 0.308 |
| Embu | 88 | 41.29 | 40.82 | 0.464 |

Kisii and Mombasa have the highest observed average prices in this selected panel. Embu has the lowest mean price but the highest post-screening variability, so its average should not be interpreted as a stable price opportunity. These are historical observed-price comparisons, not transport-adjusted profit comparisons.

## Findings: production and climate context

- The correlation between annual national tomato production and the selected-market annual mean price is **-0.012**. In this dataset it does not indicate a meaningful linear relationship.
- This is not evidence that production has no effect on prices. National production is a poor proxy for the supply reaching a particular market, reporting differs by market, and prices are affected by many unobserved factors.
- Market-location precipitation-anomaly correlations with price range from -0.076 (Nairobi) to 0.203 (Eldoret); temperature-anomaly correlations range from 0.005 to 0.165. They are descriptive and small.
- Market-location weather must not be interpreted as the climate of tomato-producing farms. It is not valid evidence that rainfall or temperature caused price changes.

## Decision-support interpretation

The current evidence can support a tomato market brief that reports historical price level, seasonality, volatility, and data coverage. It cannot yet prescribe where a farmer should sell, predict future prices, or attribute price changes to production or climate.

## Next data requirement

Obtain a machine-readable county-year tomato production, harvested-area, and yield table, then pair it with county/production-zone climate and a documented market-to-supply-area relationship. That will allow the production and climate questions to move beyond national and market-location context.

