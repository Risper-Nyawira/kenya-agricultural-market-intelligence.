# Kenya Agricultural Market Intelligence

## Purpose

This project investigates how agricultural market, production, climate, and spatial data can be integrated to produce practical market intelligence for smallholder agricultural decision-making in Kenya.

The aim is not simply to report prices. It is to convert observed patterns into carefully qualified, usable evidence about where prices differ, when they change, how variable they are, and what supply and climate context accompanies those changes.

## Research questions

1. How do agricultural commodity prices vary across markets and seasons?
2. What relationships exist between production levels and market prices?
3. How are climate conditions associated with production and market-price variability?
4. How can these patterns be translated into accessible market intelligence for agricultural decision-makers?

## First analytical slice

The reproducible first version uses the tomato value chain. It is deliberately narrow: one commodity, monthly wholesale prices, and the markets with sufficient observations. The value chain can be expanded only after its data coverage passes the audit.

### Essential data now downloaded or available

| Layer | Local source | Geographic / time grain | Intended use | Important limitation |
| --- | --- | --- | --- | --- |
| Market prices | KNBS/NIPFN KAMIS monthly wholesale-price workbook; WFP Kenya food-price extract for pilot cross-checking | KAMIS: 2012–September 2024; WFP: market-month, 2006–2026 | Price comparison, seasonality, volatility | KAMIS fields and coverage still require a raw-sheet audit; WFP tomato observations begin in 2021 |
| Market locations | WFP Kenya markets extract and price-record coordinates | Market | Market mapping and market comparisons | Not a production-area or road-access layer |
| Production | FAOSTAT crops and livestock production bulk file | Kenya-year | National tomato production, area, and yield context | Not county-level; cannot identify a market's supplying area |
| Climate | NASA POWER monthly precipitation and temperature at five selected market points | Point-month, 2012–2024 | Pilot climate context | Market-point proxies are not production-zone climate data |
| County boundaries | geoBoundaries Kenya ADM1 GeoJSON | County geometry, 2020 representation | Mapping and future county-level integration | Boundaries do not establish supply flows |

## What this version can and cannot claim

It can describe tomato wholesale-price differences, price seasonality, variability, and the relationship between annual national production and annualised market prices. It can map observed markets.

It cannot claim that climate caused a price movement, or that county production caused a specific market price, until the project adds county-level production and sub-national, varying climate data linked to plausible production areas. Associations must not be presented as causation.

## Folder guide

- `01_data/` — source register and processed analysis tables.
- `02_scripts/` — reproducible audit and preparation scripts.
- `03_analysis/` — notebooks or analysis scripts.
- `04_outputs/` — generated tables, figures, and decision-support briefs.
- `05_docs/` — methodology, data requirements, and interpretation notes.

## Immediate workflow

1. Run the data audit: `python 02_scripts/audit_available_data.py`.
2. Use the resulting market and commodity coverage reports to select the final price-panel markets.
3. Acquire the KNBS/MoA historical wholesale-price file and rerun the same audit against it.
4. Add county-year tomato production and a sub-national monthly rainfall/temperature dataset before answering questions 2–3 at local level.
5. Produce decision-support outputs only after documenting coverage, unit conversions, and uncertainty.
