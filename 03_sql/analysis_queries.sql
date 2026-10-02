-- Run after `python 02_scripts/run_pipeline.py build --markets auto`
SELECT * FROM vw_market_summary ORDER BY mean_kes_per_kg DESC;
SELECT * FROM vw_seasonality ORDER BY market, month_number;
SELECT year, market, mean_kes_per_kg, production_tonnes FROM vw_annual_price_production ORDER BY year, market;
-- Market-month price changes
SELECT market,date,price_per_kg,ROUND(100.0*(price_per_kg-LAG(price_per_kg) OVER(PARTITION BY market ORDER BY date))/LAG(price_per_kg) OVER(PARTITION BY market ORDER BY date),2) AS month_change_pct FROM market_prices;
