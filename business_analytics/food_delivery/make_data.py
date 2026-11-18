"""Makes the synthetic data for the food delivery notebook.

Every vendor, customer and order here is made up. Run: python make_data.py
Writes orders.csv.gz (one row per order) and users.csv (one row per customer, for the voucher question).
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(5)

markets = {  # market: (orders, number of vendors, how much the biggest chains dominate)
    "UAE": (30_000, 1400, 1.0), "Kuwait": (34_000, 1200, 1.0), "Qatar": (13_000, 600, 1.2),
    "Bahrain": (12_000, 650, 0.9), "Oman": (8_000, 450, 1.1), "Egypt": (15_000, 900, 1.3),
    "Jordan": (2_500, 250, 1.0), "Saudi Arabia": (1_500, 120, 1.8),
}
cuisines = ["burgers", "pizza", "shawarma", "chicken", "coffee", "desserts", "healthy", "Asian", "Indian", "grill"]
# a few chains operate in every market and take a big share of orders
big_chains = [("Burger Bros", "burgers"), ("Pizza Palace", "pizza"), ("Cluck House", "chicken"),
              ("Shawarma Street", "shawarma"), ("Bean There", "coffee")]

rows = []
order_id = 0
for market, (n_orders, n_vendors, dominance) in markets.items():
    names = [b[0] for b in big_chains] + [f"{market[:3].upper()}-{i:04d}" for i in range(n_vendors - len(big_chains))]
    kinds = [b[1] for b in big_chains] + list(rng.choice(cuisines, size=n_vendors - len(big_chains)))
    popularity = rng.pareto(1.8, size=n_vendors) + 0.1
    popularity[: len(big_chains)] = np.sort(popularity)[-len(big_chains):][::-1] * 1.3 * dominance
    popularity /= popularity.sum()
    # each vendor's own price level, delivery fee and promotion habits
    price = rng.lognormal(np.log(15), 0.45, size=n_vendors)
    price[np.isin(kinds, ["coffee", "desserts"])] *= 0.55
    fee = np.clip(rng.normal(1.2, 0.5, size=n_vendors), 0, None)
    promo = rng.beta(1.2, 6, size=n_vendors)
    vendor = rng.choice(n_vendors, size=n_orders, p=popularity)
    customers = rng.integers(0, int(n_orders / 3), size=n_orders)
    for v, c in zip(vendor, customers):
        order_id += 1
        discount = rng.random() < promo[v]
        voucher = rng.random() < promo[v] * 0.25
        basket = price[v] * rng.lognormal(0, 0.35) * (0.85 if discount else 1)
        rows.append((order_id, market, names[v], kinds[v], f"{market[:2].upper()}{c:06d}", round(basket, 2),
                     round(fee[v] * (0 if voucher else 1), 2), discount, voucher))

orders = pd.DataFrame(rows, columns=["order_id", "market", "vendor", "cuisine", "customer_id", "basket_eur",
                                     "delivery_fee_eur", "is_discount", "is_voucher"])
orders.to_csv("orders.csv.gz", index=False)

# --- the voucher question: who got a voucher on their first visit, and how much they ordered later ---
n = 20_000
engagement = rng.gamma(2, 1.5, size=n)                    # how much the customer likes ordering in
# vouchers were sent mostly to customers who already looked engaged (opened the app often, browsed menus)
p_voucher = 1 / (1 + np.exp(-(engagement - 3)))
voucher = rng.random(n) < p_voucher
true_effect = 1.5                                         # what a voucher really adds, in lifetime orders
total_orders = rng.poisson(1 + 2.2 * engagement + true_effect * voucher)
users = pd.DataFrame({"user_id": np.arange(1, n + 1), "app_opens_first_week": rng.poisson(engagement * 3),
                      "got_voucher": voucher.astype(int), "lifetime_orders": total_orders})
# a later experiment: vouchers given at random to new customers
m = 6_000
eng_exp = rng.gamma(2, 1.5, size=m)
voucher_exp = rng.random(m) < 0.5
experiment = pd.DataFrame({"user_id": np.arange(1, m + 1), "got_voucher": voucher_exp.astype(int),
                           "lifetime_orders": rng.poisson(1 + 2.2 * eng_exp + true_effect * voucher_exp)})
users.to_csv("users.csv", index=False)
experiment.to_csv("voucher_experiment.csv", index=False)
print(f"{len(orders):,} orders, {orders.vendor.nunique():,} vendor names; {len(users):,} users; {len(experiment):,} in the experiment")
