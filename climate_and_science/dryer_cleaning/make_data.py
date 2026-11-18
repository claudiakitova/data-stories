"""Makes the synthetic sensor data for the dryer cleaning notebook.

A drum granulator-dryer at a fertilizer plant slowly collects deposits on its walls. As they build
up, the exhaust temperature creeps up, the gas flow through the drum drops, and the pressure drop
across it rises, until the drum is stopped and cleaned. Every reading here is generated.

Run: python make_data.py  (writes sensors.csv.gz with hourly readings and cleanings.csv)
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(21)
hours = pd.date_range("2024-01-01", "2025-06-30 23:00", freq="h")
n = len(hours)

fouling = np.zeros(n)          # 0 = clean drum, 1 = must be cleaned now
running = np.ones(n, dtype=bool)
cleanings = []
level, rate = 0.0, rng.uniform(1 / 900, 1 / 500)
i = 0
while i < n:
    level += rate * rng.lognormal(0, 0.5) * (1.6 if level > 0.6 else 1.0)   # deposits grow faster once they start
    fouling[i] = min(level, 1.0)
    if level >= 1.0 or (level > 0.75 and rng.random() < 0.004):              # stop for cleaning
        stop = int(rng.integers(10, 30))
        cleanings.append((hours[i], hours[min(i + stop, n - 1)]))
        running[i:i + stop] = False
        i += stop
        level, rate = 0.0, rng.uniform(1 / 900, 1 / 500)
        continue
    i += 1

load = np.clip(rng.normal(1.0, 0.06, n) + 0.04 * np.sin(np.arange(n) * 2 * np.pi / 24), 0.75, 1.15)  # production rate
f = fouling ** 2                                                              # effects show up late
sensors = pd.DataFrame({
    "time": hours,
    "production_t_h": np.round(55 * load, 1),
    "inlet_gas_temp_c": np.round(560 + 25 * (load - 1) + rng.normal(0, 6, n), 1),
    "exhaust_temp_c": np.round(95 + 18 * (load - 1) + 14 * f + rng.normal(0, 2.5, n), 1),
    "gas_flow_knm3_h": np.round(120 * load * (1 - 0.18 * f) + rng.normal(0, 3, n), 1),
    "pressure_drop_kpa": np.round(2.0 + 0.3 * (load - 1) + 1.4 * f + rng.normal(0, 0.12, n), 2),
    "drum_motor_kw": np.round(410 + 30 * (load - 1) + 45 * f + rng.normal(0, 9, n), 1),
    "product_moisture_pct": np.round(1.1 + 0.25 * (load - 1) + 0.5 * f + rng.normal(0, 0.12, n), 2),
})
sensors.loc[~running, sensors.columns[1:]] = np.nan                           # the drum is stopped
sensors.to_csv("sensors.csv.gz", index=False)
pd.DataFrame(cleanings, columns=["stopped", "restarted"]).to_csv("cleanings.csv", index=False)
print(f"{n:,} hours, {len(cleanings)} cleanings")
