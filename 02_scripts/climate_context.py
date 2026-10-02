"""Descriptive climate-price context for five market-location proxy series."""
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
prices=pd.read_csv(ROOT/'06_outputs/tables/tomato_market_prices_with_outlier_flags.csv',parse_dates=['date'])
climate=pd.read_csv(ROOT/'01_data/processed/market_point_climate_monthly.csv')
# Explicit mapping: climate points are market locations, not tomato production zones.
mapping={'eldoret uasin gishu':'eldoret','kangemi nairobi':'nairobi','kibuye kisumu':'kisumu','kathonzweni makueni':None,'wakulima nakuru':'nakuru'}
climate['market']=climate.market_key.map(mapping)
climate=climate[climate.market.notna()].copy()
for col in ['precipitation_mm_month','temperature_c']:
    climate[col+'_anomaly']=climate[col]-climate.groupby(['market_key','month_number'])[col].transform('mean')
monthly=(prices[~prices.outlier_flag].groupby(['market','year','month_number']).price_per_kg.mean().reset_index())
joined=monthly.merge(climate,on=['market','year','month_number'],how='inner')
joined.to_csv(ROOT/'06_outputs/tables/market_price_climate_context.csv',index=False)
rows=[]
for market,g in joined.groupby('market'):
    rows.append({'market':market,'observations':len(g),'price_precipitation_anomaly_correlation':g.price_per_kg.corr(g.precipitation_mm_month_anomaly),'price_temperature_anomaly_correlation':g.price_per_kg.corr(g.temperature_c_anomaly)})
pd.DataFrame(rows).round(3).to_csv(ROOT/'06_outputs/tables/market_price_climate_correlations.csv',index=False)
