"""Audit local market, production, climate, and spatial inputs without altering raw data.

Run from this project directory:
    python 02_scripts/audit_available_data.py
"""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
WORKSPACE = PROJECT.parents[1]
RAW = WORKSPACE / "kenya_food_security_project" / "data" / "raw"
OUTPUT = PROJECT / "04_outputs" / "tables"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as source:
        return list(csv.DictReader(source))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def market_audit(rows: list[dict[str, str]]) -> None:
    wholesale = [row for row in rows if row["pricetype"] == "Wholesale"]
    commodity_groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in wholesale:
        commodity_groups[row["commodity"]].append(row)

    commodity_report = []
    for commodity, group in commodity_groups.items():
        dates = [row["date"] for row in group]
        commodity_report.append(
            {
                "commodity": commodity,
                "observations": len(group),
                "markets": len({row["market"] for row in group}),
                "months": len({date[:7] for date in dates}),
                "first_date": min(dates),
                "last_date": max(dates),
                "units": "; ".join(sorted({row["unit"] for row in group})),
            }
        )
    commodity_report.sort(key=lambda row: (-int(row["markets"]), -int(row["observations"])))
    write_csv(
        OUTPUT / "wholesale_commodity_coverage.csv",
        commodity_report,
        ["commodity", "observations", "markets", "months", "first_date", "last_date", "units"],
    )

    tomatoes = [row for row in wholesale if row["commodity"] == "Tomatoes"]
    tomato_months = {row["date"][:7] for row in tomatoes}
    markets: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in tomatoes:
        markets[row["market"]].append(row)
    tomato_report = []
    for market, group in markets.items():
        months = {row["date"][:7] for row in group}
        tomato_report.append(
            {
                "market": market,
                "county": group[0]["admin2"],
                "latitude": group[0]["latitude"],
                "longitude": group[0]["longitude"],
                "observations": len(group),
                "observed_months": len(months),
                "first_month": min(months),
                "last_month": max(months),
                "coverage_of_available_tomato_months": round(len(months) / len(tomato_months), 4),
                "unit": "; ".join(sorted({row["unit"] for row in group})),
            }
        )
    tomato_report.sort(key=lambda row: (-int(row["observations"]), str(row["market"])))
    write_csv(
        OUTPUT / "tomato_market_coverage.csv",
        tomato_report,
        ["market", "county", "latitude", "longitude", "observations", "observed_months", "first_month", "last_month", "coverage_of_available_tomato_months", "unit"],
    )
    print(f"Market audit: {len(rows):,} records; {len(tomatoes):,} tomato wholesale records across {len(markets)} markets.")


def production_audit(rows: list[dict[str, str]]) -> None:
    tomatoes = [row for row in rows if row["Item"] == "Tomatoes"]
    elements = Counter(row["Element"] for row in tomatoes)
    print("Production audit: tomato elements:", dict(elements))


def climate_audit() -> None:
    climate_files = sorted(RAW.glob("worldbank_kenya_*.csv"))
    for path in climate_files:
        rows = read_csv(path)
        values = [row["value"] for row in rows if row.get("value", "")]
        print(f"Climate audit: {path.name}: {len(values)} non-empty observations, {len(set(values))} distinct values.")


def main() -> None:
    price_rows = read_csv(RAW / "wfp_food_prices_kenya.csv")
    market_audit(price_rows)
    production_audit(read_csv(RAW / "faostat_kenya_crop_livestock.csv"))
    climate_audit()
    print(f"Wrote coverage reports to {OUTPUT}")


if __name__ == "__main__":
    main()
