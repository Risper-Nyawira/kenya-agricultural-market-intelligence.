# Power BI code and steps

Import the processed CSV files, not raw files:

- `tomato_market_prices_clean.csv`
- `tomato_production_national.csv`
- `market_point_climate_monthly.csv`

Set `date` to Date, `year` and `month_number` to Whole Number, and prices to Decimal Number. Create this measure:

```DAX
Average price (KES/kg) = AVERAGE(tomato_market_prices_clean[price_per_kg])
Latest observed price (KES/kg) =
VAR LatestDate = MAX(tomato_market_prices_clean[date])
RETURN CALCULATE([Average price (KES/kg)], tomato_market_prices_clean[date] = LatestDate)
Price volatility (CV) =
DIVIDE(STDEV.P(tomato_market_prices_clean[price_per_kg]), [Average price (KES/kg)])
```

Create pages: Overview, Price trends, Seasonality and volatility, Production and climate context, Map. Add slicers for market, county, year, and month. Label production and climate associations as descriptive, not causal.
