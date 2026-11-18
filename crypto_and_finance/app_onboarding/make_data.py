"""Makes the synthetic data of a crypto-finance app for this notebook.

Every user, transaction and loan here is made up. Only the Bitcoin prices are real (from ../bitcoin_forecast).

The whole app (users, transactions, loans) is generated, and this folder keeps users.csv.
Run: python make_data.py  (writes users.csv)
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
N_USERS = 12_000
START, END = pd.Timestamp("2024-01-01"), pd.Timestamp("2025-12-31")

# --- users and the identity check (KYC) -----------------------------------------------------------
countries = {  # country: (share of sign-ups, region, chance an applicant is rejected)
    "Spain": (0.16, "EU", 0.08), "Germany": (0.12, "EU", 0.06), "France": (0.10, "EU", 0.07),
    "Italy": (0.09, "EU", 0.09), "Portugal": (0.06, "EU", 0.08), "Poland": (0.06, "EU", 0.10),
    "Netherlands": (0.05, "EU", 0.05), "Romania": (0.04, "EU", 0.14), "Argentina": (0.09, "LATAM", 0.22),
    "Bolivia": (0.06, "LATAM", 0.28), "Colombia": (0.07, "LATAM", 0.20), "Mexico": (0.06, "LATAM", 0.18),
    "Nigeria": (0.04, "Other", 0.35),
}
names = list(countries)
share = np.array([countries[c][0] for c in names]); share /= share.sum()
channels = ["organic", "referral", "paid ads", "partner site"]

days = (END - START).days
growth = np.linspace(0.6, 1.4, days + 1)                       # sign-ups grow over the two years
signup_day = rng.choice(days + 1, size=N_USERS, p=growth / growth.sum())
users = pd.DataFrame({
    "user_id": np.arange(100001, 100001 + N_USERS),
    "signup_date": START + pd.to_timedelta(np.sort(signup_day), unit="D"),
    "country": rng.choice(names, size=N_USERS, p=share),
    "channel": rng.choice(channels, size=N_USERS, p=[0.45, 0.20, 0.25, 0.10]),
    "device": rng.choice(["iOS", "Android", "web"], size=N_USERS, p=[0.38, 0.47, 0.15]),
})
users["region"] = users["country"].map(lambda c: countries[c][1])

# KYC steps: started -> ID document -> selfie -> proof of address -> review
steps = ["started", "id_document", "selfie", "proof_of_address", "review"]
drop = {"id_document": 0.18, "selfie": 0.12, "proof_of_address": 0.15, "review": 0.0}
reached = []
for device in users["device"]:
    last = "started"
    for step in steps[1:]:
        p = drop[step] + (0.08 if step == "selfie" and device == "web" else 0)   # selfies are hard on a laptop
        if rng.random() < p:
            break
        last = step
    reached.append(last)
users["kyc_last_step"] = reached

reasons = ["blurry or cut-off document", "document expired", "selfie doesn't match",
           "unsupported country", "proof of address too old", "suspected fraud"]
status, attempts, reason, approved = [], [], [], []
for _, u in users.iterrows():
    if u.kyc_last_step != "review":
        status.append("abandoned"); attempts.append(int(rng.integers(1, 3))); reason.append(""); approved.append(pd.NaT)
        continue
    reject_p = countries[u.country][2]
    tries = 1
    while rng.random() < reject_p and tries < 4:      # a rejected applicant often tries again
        tries += 1
        if rng.random() < 0.45:                      # ... or gives up after a rejection
            break
    final_reject = rng.random() < reject_p * (0.9 if tries == 1 else 0.5)
    attempts.append(tries)
    if final_reject:
        w = np.array([3, 1, 1.5, 0.3, 1.2, 0.6])
        if u.region == "LATAM": w[0] += 2.5          # photo quality is the big one there
        if u.region == "Other": w[3] += 3; w[5] += 1.5
        status.append("rejected"); reason.append(rng.choice(reasons, p=w / w.sum())); approved.append(pd.NaT)
    else:
        status.append("approved"); reason.append("")
        approved.append(u.signup_date + pd.Timedelta(hours=float(rng.gamma(2, 9 * tries))))
users["kyc_status"], users["kyc_attempts"] = status, attempts
users["reject_reason"], users["approved_at"] = reason, pd.to_datetime(approved)

# products taken after approval
ok = users["kyc_status"] == "approved"
eu = users["region"] == "EU"
users["has_card"] = ok & eu & (rng.random(N_USERS) < 0.34)          # the card is only offered in the EU
users["has_iban"] = ok & (rng.random(N_USERS) < np.where(eu, 0.41, 0.22))

# --- transactions -------------------------------------------------------------------------------
products = {  # product: (relative popularity, median amount in EUR, fee rate)
    "exchange": (0.42, 180, 0.012), "card payment": (0.25, 35, 0.005), "IBAN transfer": (0.15, 420, 0.002),
    "staking": (0.08, 900, 0.0), "loan": (0.04, 2500, 0.0), "renting": (0.06, 1500, 0.0),
}
coins = ["BTC", "ETH", "USDT", "SOL", "XRP", "ADA"]
meme_coins, meme_listed = ["DOGE", "PEPE", "BONK", "FLOKI"], pd.Timestamp("2024-11-12")

rows = []
for u in users[ok].itertuples():
    start = u.approved_at.normalize()
    if start > END:
        continue
    loyal = 1.6 if u.channel == "referral" else 1.0                   # referred friends stick around longer
    lifetime = rng.exponential(140 * loyal)                           # days until the user goes quiet
    activity = rng.gamma(1.5, 2.2) * loyal                            # transactions per week while active
    t = start
    while True:
        t += pd.Timedelta(days=float(rng.exponential(7 / activity)))
        if t > END or (t - start).days > lifetime:
            break
        weights = np.array([p[0] for p in products.values()])
        if not u.has_card: weights[1] = 0
        if not u.has_iban: weights[2] = 0
        product = rng.choice(list(products), p=weights / weights.sum())
        median, fee_rate = products[product][1], products[product][2]
        amount = float(np.round(rng.lognormal(np.log(median), 0.9), 2))
        coin = ""
        if product in ("exchange", "staking", "loan", "renting"):
            coin = rng.choice(coins, p=[0.38, 0.22, 0.2, 0.09, 0.06, 0.05])
            if product == "exchange" and t >= meme_listed:
                hype = 0.35 * np.exp(-(t - meme_listed).days / 60) + 0.04   # a burst after listing, then it fades
                if rng.random() < hype:
                    coin = rng.choice(meme_coins, p=[0.45, 0.3, 0.15, 0.1])
                    amount = float(np.round(amount * 0.4, 2))
        failed = rng.random() < (0.09 if product == "card payment" else 0.03)
        rows.append((u.user_id, t.round("min"), product, coin, amount,
                     "failed" if failed else "completed", 0.0 if failed else round(amount * fee_rate, 2)))
tx = pd.DataFrame(rows, columns=["user_id", "time", "product", "coin", "amount_eur", "status", "fee_eur"])
tx = tx.sort_values("time").reset_index(drop=True)
tx.insert(0, "tx_id", np.arange(1, len(tx) + 1))

# --- crypto-backed loans, against the real Bitcoin price ----------------------------------------
btc = pd.read_csv("../bitcoin_forecast/btc_usdt_daily.csv", parse_dates=["date"], index_col="date")["close"]
LIQUIDATION_LTV = 0.85            # the loan is closed when it's worth 85% of the collateral
loan_rows = []
borrowers = users[ok].sample(900, random_state=3)
for i, u in enumerate(borrowers.itertuples(), 1):
    issued = max(u.approved_at.normalize(), START) + pd.Timedelta(days=int(rng.integers(0, 400)))
    if issued > pd.Timestamp("2025-10-31"):
        continue
    ltv = float(rng.choice([0.3, 0.5, 0.7], p=[0.25, 0.45, 0.30]))
    amount = float(np.round(rng.lognormal(np.log(2500), 0.8), -1))
    collateral_btc = amount / ltv / btc[issued]
    term = int(rng.choice([90, 180, 365]))
    repaid_on = issued + pd.Timedelta(days=int(term * rng.uniform(0.3, 1.0)))
    status, closed, reason = "repaid", repaid_on, ""
    path = btc[issued:min(repaid_on, pd.Timestamp("2025-12-31"))]
    current_ltv = amount / (collateral_btc * path)
    over = current_ltv[current_ltv >= LIQUIDATION_LTV]
    if len(over):
        status, closed, reason = "liquidated", over.index[0], "price drop: LTV reached 85%"
    elif repaid_on > END:
        status, closed = "active", pd.NaT
    loan_rows.append((f"L{i:04d}", u.user_id, issued, amount, "BTC", round(collateral_btc, 6), ltv,
                      round(float(rng.choice([0.069, 0.099, 0.129])), 3), term, status, closed, reason))
loans = pd.DataFrame(loan_rows, columns=["loan_id", "user_id", "issued", "amount_eur", "collateral_coin",
                                          "collateral_amount", "ltv_at_issue", "annual_rate", "term_days",
                                          "status", "closed", "close_reason"])

users.drop(columns=["region"]).to_csv("users.csv", index=False)
print(f"{len(users):,} users, {len(tx):,} transactions, {len(loans):,} loans")
