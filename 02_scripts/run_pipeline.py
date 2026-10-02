"""Kenya agricultural market intelligence pipeline.

Run from the project folder:
  python 02_scripts/run_pipeline.py audit
  python 02_scripts/run_pipeline.py build --markets auto
  python 02_scripts/run_pipeline.py all --markets auto

Raw files are read only. Outputs go to 01_data/processed, 03_sql, and 06_outputs.
"""
from __future__ import annotations
import argparse, calendar, re, sqlite3, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
RAW, PROCESSED = ROOT/'01_data/raw', ROOT/'01_data/processed'
TABLES, CHARTS, SQLDIR = ROOT/'06_outputs/tables', ROOT/'06_outputs/charts', ROOT/'03_sql'
for p in (PROCESSED, TABLES, CHARTS, SQLDIR): p.mkdir(parents=True, exist_ok=True)
MONTHS = {m.lower(): i for i, m in enumerate(calendar.month_abbr) if m}
MONTHS.update({m.lower(): i for i, m in enumerate(calendar.month_name) if m})

def kamis():
    p = RAW/'knbs_kamis_monthly_wholesale_prices_2012_2024sep.xlsx'
    d = pd.read_excel(p, sheet_name='Data')
    d.columns = [str(c).strip().lower() for c in d.columns]
    required = {'year','month','county','market','commodity','unit','kg','price'}
    missing = required-set(d.columns)
    if missing: raise ValueError(f'KAMIS columns missing: {missing}')
    d['month_num'] = d.month.astype(str).str.strip().str.lower().map(MONTHS)
    d['year'], d['kg'], d['price'] = (pd.to_numeric(d[c], errors='coerce') for c in ('year','kg','price'))
    d['date'] = pd.to_datetime(dict(year=d.year, month=d.month_num, day=1), errors='coerce')
    for c in ('county','market','commodity','unit'): d[c] = d[c].astype(str).str.strip()
    return d

def audit(d):
    d.to_csv(TABLES/'kamis_raw_profile_sample.csv', index=False)
    q=d[d.commodity.str.casefold().eq('tomatoes')].copy()
    if q.empty: raise ValueError("No exact 'Tomatoes' records. Inspect commodity names in the raw profile.")
    available=q.date.dropna().dt.to_period('M').nunique()
    r=(q.groupby(['market','county'], dropna=False).agg(observations=('price','size'), observed_months=('date',lambda x:x.dt.to_period('M').nunique()), first_month=('date','min'), last_month=('date','max'), units=('unit',lambda x:'; '.join(sorted(set(x)))), kg_values=('kg',lambda x:'; '.join(map(str,sorted(set(x.dropna()))))))
       .reset_index())
    r['coverage_pct']=(100*r.observed_months/available).round(1)
    r.sort_values(['coverage_pct','observations'],ascending=False).to_csv(TABLES/'tomato_market_coverage.csv',index=False)
    c=(d.groupby('commodity').agg(observations=('price','size'),markets=('market','nunique'),months=('date',lambda x:x.dt.to_period('M').nunique()),first_date=('date','min'),last_date=('date','max')).reset_index().sort_values(['markets','observations'],ascending=False))
    c.to_csv(TABLES/'commodity_coverage.csv',index=False)
    print('Audit complete. Read 06_outputs/tables/tomato_market_coverage.csv before accepting auto-selected markets.')
    return q, r

def choose_markets(coverage, spec):
    if spec != 'auto': return [x.strip() for x in spec.split(',') if x.strip()]
    x=coverage.query('coverage_pct >= 70').sort_values(['coverage_pct','observations'],ascending=False).head(8)
    if len(x)<5: x=coverage.sort_values(['coverage_pct','observations'],ascending=False).head(8)
    return x.market.tolist()

def prices(tomatoes, coverage, spec):
    selected=choose_markets(coverage,spec)
    q=tomatoes[tomatoes.market.isin(selected)].copy()
    q=q.dropna(subset=['date','price','kg']).query('kg > 0 and price >= 0').drop_duplicates(['date','market','commodity'])
    q['price_per_kg']=(q.price/q.kg).round(4)
    q['year'],q['month_number']=q.date.dt.year,q.date.dt.month
    q['source']='KNBS/NIPFN KAMIS monthly wholesale price workbook'
    cols=['date','year','month_number','commodity','market','county','unit','kg','price','price_per_kg','source']
    q[cols].sort_values(['market','date']).to_csv(PROCESSED/'tomato_market_prices_clean.csv',index=False)
    pd.DataFrame({'market':selected}).to_csv(TABLES/'selected_markets.csv',index=False)
    return q[cols]

def production():
    z=RAW/'faostat_production_crops_livestock_normalized.zip'
    with zipfile.ZipFile(z) as f:
        name=next(n for n in f.namelist() if n.endswith('.csv') and 'Normalized' in n)
        with f.open(name) as h:
            d=pd.read_csv(h, encoding='latin1')
    d.columns=[str(c).strip() for c in d.columns]
    q=d[(d['Area'].astype(str).str.casefold()=='kenya') & (d['Item'].astype(str).str.casefold()=='tomatoes') & d['Element'].isin(['Production','Area harvested','Yield'])].copy()
    q['Year']=pd.to_numeric(q['Year'],errors='coerce'); q['Value']=pd.to_numeric(q['Value'],errors='coerce')
    out=q.pivot_table(index='Year',columns='Element',values='Value',aggfunc='first').reset_index().rename(columns={'Year':'year','Production':'production_tonnes','Area harvested':'area_harvested_ha','Yield':'yield_kg_per_ha'})
    out.to_csv(PROCESSED/'tomato_production_national.csv',index=False); return out

def climate():
    rows=[]
    for p in (RAW/'nasa_power_market_points').glob('*.csv'):
        lines=p.read_text(encoding='utf-8').splitlines(); start=next(i for i,x in enumerate(lines) if x.startswith('PARAMETER,'))
        d=pd.read_csv(p,skiprows=start); market=re.sub(r'_\d{4}_\d{4}$','',p.stem).replace('_',' ')
        d.columns = [str(c).strip().upper() for c in d.columns]
        for _,r in d.iterrows():
            for m,n in zip([m.upper() for m in calendar.month_abbr[1:]],range(1,13)):
                rows.append({'market_key':market,'year':int(r.YEAR),'month_number':n,'parameter':r.PARAMETER,'value':r[m]})
    long=pd.DataFrame(rows); out=long.pivot_table(index=['market_key','year','month_number'],columns='parameter',values='value').reset_index()
    if 'PRECTOTCORR' in out: out['precipitation_mm_month']=out.PRECTOTCORR*out.apply(lambda x:calendar.monthrange(int(x.year),int(x.month_number))[1],axis=1)
    out=out.rename(columns={'T2M':'temperature_c'}); out.to_csv(PROCESSED/'market_point_climate_monthly.csv',index=False); return out

def database(price, prod, clim):
    db=SQLDIR/'market_intelligence.sqlite'; con=sqlite3.connect(db)
    price.to_sql('market_prices',con,if_exists='replace',index=False); prod.to_sql('tomato_production_national',con,if_exists='replace',index=False); clim.to_sql('market_point_climate',con,if_exists='replace',index=False)
    con.executescript("""DROP VIEW IF EXISTS vw_market_summary; DROP VIEW IF EXISTS vw_seasonality; DROP VIEW IF EXISTS vw_annual_price_production;
CREATE VIEW vw_market_summary AS SELECT market, county, COUNT(*) observations, ROUND(AVG(price_per_kg),2) mean_kes_per_kg, ROUND(MIN(price_per_kg),2) min_kes_per_kg, ROUND(MAX(price_per_kg),2) max_kes_per_kg FROM market_prices GROUP BY market,county;
CREATE VIEW vw_seasonality AS SELECT month_number, market, ROUND(AVG(price_per_kg),2) mean_kes_per_kg, COUNT(*) observations FROM market_prices GROUP BY month_number,market;
CREATE VIEW vw_annual_price_production AS SELECT p.year,p.market,ROUND(AVG(p.price_per_kg),2) mean_kes_per_kg,t.production_tonnes,t.area_harvested_ha,t.yield_kg_per_ha FROM market_prices p LEFT JOIN tomato_production_national t ON p.year=t.year GROUP BY p.year,p.market;""")
    con.commit(); con.close()

def charts(price, prod):
    sns.set_theme(style='whitegrid');
    plt.figure(figsize=(12,6)); sns.lineplot(data=price,x='date',y='price_per_kg',hue='market'); plt.ylabel('KES per kg'); plt.title('Monthly tomato wholesale prices'); plt.tight_layout(); plt.savefig(CHARTS/'tomato_price_trends.png',dpi=180); plt.close()
    plt.figure(figsize=(12,6)); sns.lineplot(data=price,x='month_number',y='price_per_kg',hue='market',estimator='mean',errorbar=None); plt.xticks(range(1,13),calendar.month_abbr[1:]); plt.ylabel('KES per kg'); plt.title('Tomato price seasonality'); plt.tight_layout(); plt.savefig(CHARTS/'tomato_seasonality.png',dpi=180); plt.close()
    v=price.groupby('market').price_per_kg.agg(['mean','std','count']).reset_index(); v['coefficient_of_variation']=v['std']/v['mean']; v.sort_values('coefficient_of_variation',ascending=False).to_csv(TABLES/'tomato_market_volatility.csv',index=False)

def main():
    a=argparse.ArgumentParser(); a.add_argument('stage',choices=['audit','build','all']); a.add_argument('--markets',default='auto'); args=a.parse_args()
    d=kamis(); tomato,coverage=audit(d)
    if args.stage=='audit': return
    p=prices(tomato,coverage,args.markets); prod=production(); clim=climate(); database(p,prod,clim); charts(p,prod)
    print('Build complete. Clean data: 01_data/processed. Database: 03_sql/market_intelligence.sqlite.')
if __name__=='__main__': main()
