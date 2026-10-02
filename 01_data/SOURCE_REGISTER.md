# Source register

Downloaded 1 October 2026. Raw files are preserved unchanged in `raw/`; processing will write separate derived tables.

| Data layer | File / location | Source and coverage | Why it is essential | Use rule |
| --- | --- | --- | --- | --- |
| Historical prices | `raw/knbs_kamis_monthly_wholesale_prices_2012_2024sep.xlsx` | KNBS National Information Platform for Food Security and Nutrition; Ministry of Agriculture / KAMIS; monthly wholesale prices, 2012–September 2024 | Core evidence for price, market, seasonality, and volatility analysis | Use the `Data` worksheet as the record-level source; verify unit, commodity, market, county, and missingness before analysis. |
| Production | `raw/faostat_production_crops_livestock_normalized.zip` | FAOSTAT Crops and livestock products bulk download | Provides annual Kenyan tomato production, area harvested, and yield | It is national-level; it provides supply context, not county supply attribution. |
| County boundaries | `raw/geoboundaries_kenya_adm1.geojson` | geoBoundaries gbOpen; Kenya ADM1 Counties, 2020 representation; 47 units | Provides county geometry for maps and county-level inputs added later | Use with attribution; names must be reconciled to production and market source spellings. |
| Market locations and pilot price extract | `raw/wfp_markets_kenya.csv` and `raw/wfp_food_prices_kenya.csv` | WFP Kenya extract, copied into this project's raw-data folder from the earlier workspace dataset | Supplies coordinates and an independently structured pilot price panel | Retain as a pilot / location source. The KNBS/KAMIS workbook is the preferred long-history price source. |
| Climate at selected market points | `raw/nasa_power_market_points/*.csv` | NASA POWER monthly point API; MERRA-2 corrected precipitation and 2 m temperature; 2012–2024 | Enables a small, geographically explicit climate pilot for five selected market locations | These are market-location weather proxies, not county average or farm-level conditions. Do not make production-causality claims from them. |
| County-production reference | `raw/knbs_national_agriculture_production_report_2025.pdf` | KNBS National Agriculture Production Report, 2025 | An official reference for county production information and definitions | This PDF is not yet a clean data table. We must extract or obtain its underlying county tomato table before using it in a data join. |

## Download locations

- KNBS/NIPFN: <https://nipfn.knbs.or.ke/download/monthly-wholesale-commodity-prices-ministry-of-agriculture-2012-2024sep/>
- FAOSTAT bulk production: <https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_All_Data_(Normalized).zip>
- geoBoundaries API metadata: <https://www.geoboundaries.org/api/current/gbOpen/KEN/ADM1/>
- NASA POWER monthly point service: <https://power.larc.nasa.gov/docs/services/api/temporal/>

## Still required before answering the full local integrated question

1. **A machine-readable county-year tomato production, area harvested, and yield table**, from KNBS, AFA, or the Ministry of Agriculture. FAOSTAT alone is not spatially granular enough. The AFA public download links located during this session returned a file-path error and were therefore not retained as data.
2. **County or production-zone monthly rainfall and temperature**, preferably linked to known tomato-producing counties, not merely markets.
3. **A documented market-to-production-area linkage** (for example, source counties reported by market operators or an appropriately documented transport/supply-flow dataset).

The project can begin Questions 1 and 4 now. Questions 2 and 3 can begin at national/context level but require these additions for defensible county-market analysis.
