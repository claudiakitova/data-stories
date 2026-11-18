"""Makes the synthetic data for the orders-by-area notebook: monthly successful orders from 11 vendors
across the areas of Bahrain, February to July 2024. The area names are real places; the vendors and
every order count are generated.

Run: python make_data.py  (writes area_orders.csv)
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(9)

areas = ["Madinat Hamad Hamad Town", "Alfateh", "Tubli", "Isa Town", "Muharraq", "Manama Center", "Riffa Alshamali North Riffa",
         "West Riffa", "Saar", "Juffair", "Seef", "Sanabis", "Hidd", "Arad", "Busaiteen", "Galaly", "Amwaj Islands",
         "Salmabad", "Sitra Al Qaryah", "Jid Ali", "Zinj", "Adliya", "Um Al Hassam", "Budaiya", "Diraz", "Barbar",
         "Janabiya", "Hamala", "Jidhafs", "Sanad", "Aali", "Askar", "Zallaq", "Karbabad", "Sehla", "Qudaibiya",
         "Hoora", "Reef Island", "Diyar Al Muharraq", "Salman City", "Bu Ashira", "Karzakkan", "Nuwaidrat", "Maqabah",
         "Jannusan", "Sadad", "Duraz", "Al Markh", "Bilad Al Qadeem", "Mahooz"]
vendors = {  # vendor: (popularity, how much its orders grew per month)
    "Grill House": (3.0, 0.02), "Burger Bay": (2.6, -0.04), "Shawarma Corner": (2.2, 0.06), "Pizza Point": (1.8, 0.00),
    "Karak & Co": (1.5, 0.08), "Biryani Bowl": (1.3, 0.03), "Sushi Tide": (0.9, 0.10), "Salad Studio": (0.8, -0.06),
    "Falafel Street": (0.7, 0.01), "Dessert Lab": (0.6, 0.04), "Noodle Box": (0.5, -0.08),
}
months = pd.date_range("2024-02-01", "2024-07-01", freq="MS")
# Ramadan 2024 ran from about March 11 to April 9: families eat at home at iftar, then order late at night;
# summer heat from June keeps people indoors, and many residents travel abroad in July
month_effect = {"2024-02": 1.0, "2024-03": 1.18, "2024-04": 1.10, "2024-05": 0.98, "2024-06": 1.08, "2024-07": 0.86}

area_size = np.sort(rng.pareto(1.2, len(areas)) + 0.2)[::-1] * 0.35
rows = []
for a, size in zip(areas, area_size):
    reach = rng.random(len(vendors)) < np.clip(0.25 + size / 1.5, 0.25, 0.95)     # not every vendor delivers everywhere
    for (v, (pop, growth)), delivers in zip(vendors.items(), reach):
        if not delivers:
            continue
        for k, m in enumerate(months):
            expected = size * pop * month_effect[m.strftime("%Y-%m")] * (1 + growth) ** k
            rows.append((m.date(), a, v, int(rng.poisson(expected))))
area_orders = pd.DataFrame(rows, columns=["month", "area", "vendor", "successful_orders"])
area_orders.to_csv("area_orders.csv", index=False)
print(f"{area_orders.area.nunique()} areas, {area_orders.vendor.nunique()} vendors, {area_orders.successful_orders.sum():,} orders")
