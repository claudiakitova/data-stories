"""Makes the event log for the Bee Quest notebook, in the format of the original test task.

The players and events are generated; their overall shape follows the original task data (a few
players bring most of the money, the US brings most of the revenue, most players leave on day 1).

Run: python make_data.py  (writes task.csv.gz)

Columns:
  id          - player
  cc          - registration country
  eventId     - 1 login, 2 purchase, 3 new level, 4 tutorial finished, 5 ad watched
  eventSar    - seconds since the player first launched the game
  eventValue  - 0 for a login; money paid for a purchase; the new farm level; 1 for the tutorial;
                money earned from the ad
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(11)
N = 20_000
DAY = 86_400
HORIZON = 120 * DAY
LOGIN, PURCHASE, LEVEL, TUTORIAL, AD = 1, 2, 3, 4, 5

countries = {"US": (0.36, 4.5), "GB": (0.06, 1.3), "DE": (0.05, 1.2), "CA": (0.05, 1.3), "AU": (0.04, 1.3),
             "FR": (0.05, 0.9), "JP": (0.03, 1.4), "BR": (0.10, 0.3), "IN": (0.11, 0.12), "MX": (0.07, 0.35),
             "PH": (0.08, 0.2)}            # country: (share of players, spending multiplier)
codes = list(countries)
share = np.array([countries[c][0] for c in codes]); share /= share.sum()

rows = []
for pid in range(1, N + 1):
    cc = rng.choice(codes, p=share)
    spend_mult = countries[cc][1]
    engagement = rng.lognormal(0, 1.0)                          # how much this player likes the game
    if rng.random() < 0.56:
        lifetime = rng.exponential(9000)                        # leaves within the first hours
    else:
        lifetime = min(HORIZON, rng.exponential(DAY * 22 * engagement ** 0.6))
    t, level = 0.0, 1
    rows.append((pid, cc, LOGIN, 0, 0.0))
    if rng.random() < min(0.95, 0.4 + 0.25 * engagement):
        rows.append((pid, cc, TUTORIAL, int(rng.uniform(300, 1500)), 1.0))
    payer = rng.random() < min(0.5, 0.16 * engagement ** 0.5 * spend_mult)
    big = payer and rng.random() < 0.01
    while True:
        t += rng.exponential(DAY / (0.6 + 0.5 * engagement))   # time to the next session
        if t > lifetime:
            break
        rows.append((pid, cc, LOGIN, int(t), 0.0))
        if rng.random() < 0.5 / level ** 0.3:
            level += 1
            rows.append((pid, cc, LEVEL, int(t + 60), float(level)))
        if rng.random() < 0.45:
            rows.append((pid, cc, AD, int(t + 120), round(float(rng.uniform(0.01, 0.06)), 4)))
        if payer and rng.random() < (0.06 if big else 0.025):
            price = rng.choice([0.99, 1.99, 4.99, 9.99, 19.99],
                               p=[0.1, 0.2, 0.3, 0.25, 0.15] if big else [0.5, 0.28, 0.17, 0.05, 0.0])
            rows.append((pid, cc, PURCHASE, int(t + 300), float(price)))

events = pd.DataFrame(rows, columns=["id", "cc", "eventId", "eventSar", "eventValue"])
events = events[events.eventSar <= HORIZON].sort_values(["id", "eventSar"])
events.to_csv("task.csv.gz", index=False)
print(f"{events.id.nunique():,} players, {len(events):,} events")
