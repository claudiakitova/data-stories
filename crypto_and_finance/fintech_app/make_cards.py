"""Makes the synthetic card data for the card users notebook.

Every card holder, card, and payment here is generated.
Run: python make_cards.py  (writes cards.csv and card_payments.csv.gz)
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(17)

countries = {  # country: (cards ordered, chance a delivered card gets activated, money level, decline rate)
    "Poland": (2800, 0.62, 1.0, 0.10), "Bolivia": (850, 0.40, 0.35, 0.22), "Hungary": (600, 0.58, 0.9, 0.11),
    "Italy": (460, 0.60, 1.3, 0.09), "Argentina": (440, 0.38, 0.4, 0.24), "Mexico": (280, 0.42, 0.5, 0.20),
    "Lithuania": (275, 0.65, 1.0, 0.08), "Romania": (265, 0.55, 0.7, 0.12), "Spain": (230, 0.61, 1.4, 0.09),
    "France": (210, 0.63, 1.5, 0.08), "Serbia": (150, 0.50, 0.6, 0.14), "Peru": (125, 0.39, 0.4, 0.23),
    "Colombia": (100, 0.41, 0.45, 0.21), "Germany": (92, 0.66, 1.8, 0.07), "Portugal": (55, 0.60, 1.1, 0.09),
    "Ecuador": (53, 0.37, 0.4, 0.22), "Chile": (40, 0.45, 0.7, 0.17), "Cyprus": (38, 0.64, 2.2, 0.08),
    "Belgium": (38, 0.63, 1.6, 0.08), "Netherlands": (33, 0.66, 1.9, 0.07),
}
region = {c: ("Latin America" if c in {"Bolivia", "Argentina", "Mexico", "Peru", "Colombia", "Ecuador", "Chile"}
              else "European Union" if c != "Serbia" else "Europe, outside the EU") for c in countries}

cards, payments = [], []
card_id = 0
for country, (n, activate, money, decline) in countries.items():
    for _ in range(n):
        card_id += 1
        ordered = pd.Timestamp("2024-01-01") + pd.Timedelta(days=int(rng.integers(0, 290)))
        if rng.random() < 0.08:
            status = "not processed"                                      # failed checks, never sent
        elif (pd.Timestamp("2024-10-31") - ordered).days < rng.integers(10, 40):
            status = "in delivery"
        elif rng.random() < activate:
            status = rng.choice(["active", "blocked", "closed"], p=[0.86, 0.04, 0.10])
        else:
            status = "delivered, never activated"
        whale = rng.random() < 0.01
        deposits = float(np.round(rng.lognormal(np.log(400 * money), 1.3) * (60 if whale else 1), 2)) if status in ("active", "blocked", "closed") else 0.0
        cards.append((card_id, country, region[country], ordered.date(), status, deposits))
        if status in ("active", "blocked", "closed"):
            for _ in range(int(rng.poisson(14 * money ** 0.5))):
                when = ordered + pd.Timedelta(days=int(rng.integers(15, 300)))
                if when > pd.Timestamp("2024-10-31"):
                    continue
                kind = rng.choice(["groceries", "restaurants", "online shopping", "travel", "cash withdrawal"], p=[0.35, 0.2, 0.25, 0.1, 0.1])
                amount = float(np.round(rng.lognormal(np.log({"groceries": 25, "restaurants": 30, "online shopping": 45,
                                                              "travel": 180, "cash withdrawal": 100}[kind] * money ** 0.5), 0.8), 2))
                reason = ""
                if rng.random() < decline:
                    reason = rng.choice(["insufficient funds", "blocked by issuer", "wrong PIN", "merchant not supported"],
                                        p=[0.5, 0.25, 0.15, 0.1] if region[country] != "Latin America" else [0.35, 0.45, 0.1, 0.1])
                payments.append((card_id, when.date(), kind, amount, "declined" if reason else "approved", reason))

pd.DataFrame(cards, columns=["card_id", "country", "region", "ordered", "status", "deposits_eur"]).to_csv("cards.csv", index=False)
pd.DataFrame(payments, columns=["card_id", "date", "category", "amount_eur", "result", "decline_reason"]).to_csv("card_payments.csv.gz", index=False)
print(f"{len(cards):,} cards, {len(payments):,} card payments")
