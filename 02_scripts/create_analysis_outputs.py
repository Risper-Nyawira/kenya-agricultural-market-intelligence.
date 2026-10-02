"""Create transparent market summaries and a sensitivity check for flagged price outliers."""
from pathlib import Path
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'01_data/processed/tomato_market_prices_clean.csv'
OUT=ROOT/'06_outputs/tables'; OUT.mkdir(parents=True,exist_ok=True)

prices=pd.read_csv(P,parse_dates=['date'])
# Flag - do not delete - values above each market's Q3 + 3 x IQR.
limits=prices.groupby('market').price_per_kg.agg(q1=lambda x:x.quantile(.25),q3=lambda x:x.quantile(.75)).reset_index()
limits['upper_outlier_limit']=limits.q3+3*(limits.q3-limits.q1)
prices=prices.merge(limits[['market','upper_outlier_limit']],on='market',how='left')
prices['outlier_flag']=prices.price_per_kg>prices.upper_outlier_limit
prices.to_csv(OUT/'tomato_market_prices_with_outlier_flags.csv',index=False)

def summary(d,label):
    s=d.groupby(['market','county']).price_per_kg.agg(observations='size',mean_kes_per_kg='mean',median_kes_per_kg='median',min_kes_per_kg='min',max_kes_per_kg='max',standard_deviation='std').reset_index()
    s['coefficient_of_variation']=s.standard_deviation/s.mean_kes_per_kg
    s['summary_version']=label
    return s

all_summary=summary(prices,'all_observations')
screened_summary=summary(prices[~prices.outlier_flag],'excludes_flagged_outliers')
pd.concat([all_summary,screened_summary]).round(4).to_csv(OUT/'tomato_market_summary_sensitivity.csv',index=False)

annual=(prices[~prices.outlier_flag].groupby('year').price_per_kg.mean().rename('selected_market_mean_kes_per_kg').reset_index())
prod=pd.read_csv(ROOT/'01_data/processed/tomato_production_national.csv')
joined=annual.merge(prod,on='year',how='inner')
joined.to_csv(OUT/'annual_price_production_context.csv',index=False)
corr=joined[['selected_market_mean_kes_per_kg','production_tonnes','area_harvested_ha','yield_kg_per_ha']].corr().round(3)
corr.to_csv(OUT/'annual_price_production_correlations.csv')

sns.set_theme(style='whitegrid')
plt.figure(figsize=(12,6))
sns.lineplot(data=prices[~prices.outlier_flag],x='date',y='price_per_kg',hue='market')
plt.ylabel('KES per kg'); plt.title('Monthly tomato wholesale prices (flagged extremes excluded)')
plt.tight_layout(); plt.savefig(ROOT/'06_outputs/charts/tomato_price_trends_screened.png',dpi=180); plt.close()
print('Flagged records:',int(prices.outlier_flag.sum()))
print(prices.loc[prices.outlier_flag,['date','market','price_per_kg','upper_outlier_limit']].to_string(index=False))
print('Production-price correlation:',corr.loc['selected_market_mean_kes_per_kg','production_tonnes'])
