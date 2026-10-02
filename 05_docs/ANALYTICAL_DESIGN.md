# Analytical design and evidence boundaries

## Unit of analysis

The core panel is **commodity × market × month**. Each record should have a date, commodity, market identifier, county, coordinates, price type, unit, currency, and price. The analysis must standardise a price only when its unit is known.

For tomato, the local WFP source reports wholesale prices per 64 kg. A normalised `kes_per_kg` value is calculated as `price / 64`; the original value and unit must always remain in the processed data.

## Integration design

```text
market-month prices + market coordinates  -> seasonal patterns, volatility, market comparison
national/county-year production           -> annual supply context
county/month climate                      -> growing-condition context
                                          -> evidence-qualified decision support
```

The final integrated panel should link production and climate to a market only through a documented production-area-to-market relationship. If that relationship is unknown, retain the levels separately and describe the analysis as national or county context rather than local supply effects.

## Measures

| Question | Primary measures | Interpretation rule |
| --- | --- | --- |
| Price variation | market median price, monthly seasonal index, price range | Compare like-for-like wholesale prices and units only. |
| Volatility | coefficient of variation and month-to-month percentage change | Report observation count and missing months alongside every estimate. |
| Production-price relationship | annual national/county production versus annual mean price; correlation | Descriptive association only; do not infer causality. |
| Climate association | rainfall/temperature anomalies, production/yield, annual price measures | Requires varying, geographically matched climate data and adequate observations. |
| Decision support | seasonal price calendar, market comparison, risk flag, data-quality flag | A flag is an advisory prompt, never a price forecast or recommendation guarantee. |

## Required data quality checks

- Deduplicate commodity-market-date records.
- Record raw price units and convert only with an explicit conversion factor.
- Quantify missing months per market before calculating seasonality or volatility.
- Separate nominal price trends from seasonal patterns; nominal price rises can reflect inflation.
- Preserve source, download date, and filtering rules in every processed table.
- Do not mix wholesale and retail prices in the same comparison.

## Minimum acquisition requirements for the integrated version

| Layer | Minimum requirement |
| --- | --- |
| Prices | Monthly wholesale tomato prices with market identifiers for at least five consistently observed markets. |
| Production | Tomato production, area harvested, and yield by county-year for counties plausibly supplying selected markets. |
| Climate | County-level or production-zone monthly rainfall and temperature, with enough variation to calculate anomalies. |
| Spatial | Selected market coordinates plus county boundaries; a documented market-to-production-area linkage. |

## Decision-support prototype

The first accessible output should be a one-page tomato market brief containing: the latest observed price, a 12-month seasonal position, a selected-market comparison, a volatility indicator, coverage warnings, and a plain-language interpretation. It should say “observed pattern” rather than imply a guaranteed selling recommendation.

