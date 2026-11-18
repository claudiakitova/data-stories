"""Makes the synthetic data for the promo forecast notebook.

A grocery chain runs weekly promotions. For every product on promotion in a store, the data has the
plan (discount, mechanic, duration, advertising, checkout display) and the units actually sold.
Every store, product and sale here is generated.

Run: python make_data.py  (writes promos.csv.gz)
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(3)

categories = {"dairy": 1.4, "snacks": 1.0, "drinks": 1.2, "coffee and tea": 0.7, "sweets": 0.9, "household": 0.6}
products = []
for cat, base in categories.items():
    for k in range(30):
        products.append((f"{cat[:3].upper()}{k:03d}", cat, round(float(rng.lognormal(np.log(3), 0.5)), 2),
                         base * rng.lognormal(0, 0.5), rng.uniform(1.5, 3.5)))   # id, category, price, popularity, price sensitivity
products = pd.DataFrame(products, columns=["product_id", "category", "regular_price", "popularity", "elasticity"])

stores = pd.DataFrame({"store_id": [f"S{i:03d}" for i in range(120)],
                       "format": rng.choice(["convenience", "supermarket", "hypermarket"], 120, p=[0.5, 0.35, 0.15])})
stores["traffic"] = stores.format.map({"convenience": 400, "supermarket": 900, "hypermarket": 2500}) * rng.lognormal(0, 0.3, 120)
stores["traffic_cluster"] = pd.qcut(stores.traffic, 3, labels=["low", "medium", "high"]).astype(str)
stores["region"] = rng.choice(["North", "Center", "South", "Volga", "Urals"], 120)

weeks = pd.date_range("2019-01-02", "2020-12-30", freq="W-WED")
mechanics = {"price cut": 1.0, "2 for 1": 1.35, "loyalty points": 0.8, "bundle": 0.9}
rows = []
for week in weeks:
    covid = pd.Timestamp("2020-03-11") <= week <= pd.Timestamp("2020-04-01")
    season = 1 + 0.15 * np.sin(2 * np.pi * week.day_of_year / 365)
    on_promo = products.sample(25, random_state=int(week.strftime("%Y%m%d")) % 2**31)
    for p in on_promo.itertuples():
        discount = float(rng.choice([0.1, 0.15, 0.2, 0.25, 0.3, 0.4]))
        mechanic = rng.choice(list(mechanics), p=[0.55, 0.15, 0.2, 0.1])
        duration = int(rng.choice([7, 14]))
        advertised = rng.random() < 0.35
        store_ids = stores.sample(int(rng.integers(30, 90)), random_state=int(rng.integers(1e9)))
        for s in store_ids.itertuples():
            display = rng.random() < 0.25
            expected = (p.popularity * s.traffic / 100 * season
                        * (1 + discount) ** (p.elasticity * 2) * mechanics[mechanic]
                        * (1.3 if advertised else 1.0) * (1.25 if display else 1.0) * duration / 7)
            if covid:                                                       # panic buying, then a slump
                expected *= 1.8 if week < pd.Timestamp("2020-03-25") else 0.7
            units = rng.poisson(expected * rng.lognormal(0, 0.25))
            rows.append((week.date(), p.product_id, p.category, p.regular_price, s.store_id, s.format, s.traffic_cluster,
                         s.region, discount, mechanic, duration, int(advertised), int(display), units))

promos = pd.DataFrame(rows, columns=["week", "product_id", "category", "regular_price", "store_id", "store_format",
                                     "traffic_cluster", "region", "discount", "mechanic", "duration_days", "advertised",
                                     "checkout_display", "units_sold"])
promos.to_csv("promos.csv.gz", index=False)
print(f"{len(promos):,} product-store promotions over {promos.week.nunique()} weeks")
