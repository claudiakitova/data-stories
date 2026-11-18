"""Makes the synthetic data for the review sentiment notebook.

An invoicing app for small businesses (estimates, invoices, card payments) collects reviews from the
App Store, Google Play and Trustpilot, and ships app releases every few weeks. Every review, author,
version and release here is generated.

Run: python make_data.py  (writes reviews.csv and releases.csv)
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
START, END = pd.Timestamp("2016-10-01"), pd.Timestamp("2026-11-04")

# ---------- releases: a new version every few weeks on each store ----------
items_pool = ["Faster estimate loading", "New invoice templates", "Fix crash when adding photos",
              "Card payments on invoices", "Deposits on estimates", "Tax rate settings", "New home screen",
              "Subscription plans screen", "Fix sync between phone and web", "Offline mode improvements",
              "Customer list search", "PDF layout fixes", "Tap to pay", "Faster payouts", "Login with Google",
              "Upgrade prompts", "Reports screen", "Fix password reset", "Bulk printing", "Recurring invoices"]
releases = []
for store, prefix, gap in [("App Store", 3, 27), ("Google Play", 2, 24)]:
    day, minor = START - pd.Timedelta(days=20), 0
    while day < END:
        hotfix = minor > 0 and rng.random() < 0.15
        releases.append((store, f"{prefix}.{minor - 1}.1" if hotfix else f"{prefix}.{minor}.0", day,
                         int(rng.integers(1, 4)) if hotfix else int(rng.integers(4, 30)), "yes" if hotfix else "no",
                         "\n".join(rng.choice(items_pool, int(rng.integers(1, 5)), replace=False))))
        day += pd.Timedelta(days=int(rng.integers(gap - 8, gap + 9)))
        minor += 0 if hotfix else 1
releases = pd.DataFrame(releases, columns=["store", "version", "released_at", "tickets", "is_hotfix", "items"])

def version_at(store, when):
    r = releases[(releases.store == store) & (releases.released_at <= when)]
    if len(r) == 0:
        return None
    lag = min(int(rng.geometric(0.6)) - 1, len(r) - 1)   # most people have the latest version, some lag behind
    return r.iloc[-1 - lag].version

# ---------- what reviews say ----------
POS_TITLES = ["Love it", "Great app", "Easy to use", "Best invoicing app", "Works great", "Saves me time",
              "Very professional", "Simple and fast", "Highly recommend", "Excellent", "Five stars", "Must have"]
POS = ["I can send an estimate from the job site in a few minutes.", "My customers love the professional invoices.",
       "Getting paid is so much faster now.", "Turning an estimate into an invoice takes one tap.",
       "I use it every day for my {trade} business.", "Works the same on my phone and my laptop.",
       "Worth every penny.", "Printing and emailing invoices is easy.", "Highly recommend to any small business.",
       "Support answered in an hour and fixed my problem.", "Saves me hours of paperwork every week.",
       "Clean and simple, does exactly what I need.", "My customers can pay by card right from the invoice.",
       "Best app I have found for estimates.", "Great app.", "Love it!", "Easy to use.", "Very helpful app.",
       "Looks professional and my clients notice.", "Keeps all my customers and jobs in one place."]
TRADES = ["painting", "plumbing", "landscaping", "cleaning", "handyman", "roofing", "electrical", "flooring"]
NEG_TITLES = ["Disappointed", "Terrible", "Not worth it", "Used to love it", "Do not download", "Waste of time",
              "Frustrating", "Very bad", "Getting worse", "Avoid"]
THEMES = {
    "pricing": ["It used to be free and now they want a monthly subscription.", "Way too expensive for a small business.",
                "The price went up again with no warning.", "They charge a fee on every payment on top of the subscription.",
                "I cancelled my subscription and still got charged.", "Basic features are now behind a paywall.",
                "Greedy. Not worth the money anymore.", "Can't send an invoice without upgrading to premium.",
                "The monthly price doubled this year.", "Bait and switch: free to start, then they make you pay."],
    "crashes": ["The app keeps crashing when I open an estimate.", "Crashes every time I add a photo.",
                "Full of bugs since the last update.", "Freezes on the loading screen.", "It stopped working after the update."],
    "speed": ["Very slow to load.", "Sync takes forever and my invoices don't show on the laptop.",
              "Useless on a job site with no internet connection."],
    "payments": ["Payments take a week to reach my bank.", "My customer paid by credit card and the funds are on hold.",
                 "The payment processing fees are too high.", "A deposit never showed up in my bank account.",
                 "Customers can't pay with PayPal anymore."],
    "support": ["Support never responds.", "Nobody answers the chat.", "I sent three emails to customer service and got no reply."],
    "login": ["Locked out of my account and the password reset doesn't work.", "It keeps logging me out."],
    "lost data": ["I lost my whole customer list after the update.", "Two of my estimates disappeared."],
    "sending": ["Can't print more than one invoice at a time.", "The PDF my customer gets looks different from the app.",
                "Emails to my customers go to spam."],
    "features": ["The new layout is confusing.", "I wish I could set my own tax rates.", "Too many pop ups asking me to upgrade.",
                 "The update changed everything and now it's hard to find anything."],
}
GENERIC_NEG = ["Terrible.", "Waste of time.", "Garbage app.", "Not good at all.", "Do not download.",
               "It was great until the last update.", "Very disappointed.", "Uninstalling.", "Bad.", "Doesn't work.",
               "Too expensive.", "Meh."]
PAST_GOOD = ["I used to love this app.", "It was easy to use at first.", "I have used it for years for my {trade} business.",
             "This used to be the best app for estimates.", "Great idea, poor execution."]
MILD = ["Wish it had more templates.", "Would be nice to add my logo in color.", "A dark mode would be nice.",
        "Takes a minute to learn.", "A bit pricey but worth it.", "Had one small glitch but support fixed it."]
FILLER = ["I do {trade} work.", "Downloaded it last month.", "Been using it since {year}.", "My wife does the books with it.",
          "I run a small crew.", "Tried a few other apps first."]
BUT = ["Great app, but", "Love the app but", "Works well, but", "Good app overall, however", "Good app.", "Still my favorite.", ""]
VAGUE = ["Ok.", "It's fine.", "Does the job.", "Not bad.", "Could be better.", "It works I guess.", "Needs work.",
         "Pretty good.", "Not sure yet.", "Alright."]
NEUTRAL_TITLES = ["Invoicing app", "Review", "My experience", "Update", "Estimates", "Small business", "Ok"]

def fill(text, t):
    return text.replace("{trade}", rng.choice(TRADES)).replace("{year}", str(int(rng.integers(2014, t.year + 1))))

def theme_weights(t):
    y, ym = t.year, (t.year, t.month)
    w = {"pricing": 0.15, "crashes": 0.08, "speed": 0.1, "payments": 0.2, "support": 0.15,
         "login": 0.05, "lost data": 0.06, "sending": 0.15, "features": 0.3}
    if y == 2017: w["crashes"] = 0.2
    if y in (2018, 2021): w["payments"] = 0.5
    if y >= 2019: w["pricing"] = 0.6
    if y == 2021: w["pricing"] = 0.35
    if y >= 2023: w["pricing"], w["payments"] = 0.65, max(0.08, 0.2 - 0.04 * (y - 2023))
    if (2019, 4) <= ym <= (2019, 7) or (2024, 6) <= ym <= (2024, 7): w["pricing"] = 0.8
    return w

def share_negative(t):
    base = {2016: 0.08, 2017: 0.1, 2018: 0.15, 2019: 0.32, 2020: 0.25, 2021: 0.25,
            2022: 0.3, 2023: 0.34, 2024: 0.38, 2025: 0.33, 2026: 0.3}[t.year]
    if (2019, 4) <= (t.year, t.month) <= (2019, 7): base = 0.62
    if (2024, 6) <= (t.year, t.month) <= (2024, 7): base = 0.78
    return base

def complaint(t):
    w = theme_weights(t)
    picked = [k for k, p in w.items() if rng.random() < p * 0.7] or [rng.choice(list(w), p=np.array(list(w.values())) / sum(w.values()))]
    return [rng.choice(THEMES[k]) for k in picked[:2]]

def negative_text(t):
    if rng.random() < 0.12:
        return rng.choice(GENERIC_NEG)                                           # short, no theme
    parts = complaint(t)
    if rng.random() < 0.3: parts.insert(0, rng.choice(GENERIC_NEG))
    if rng.random() < 0.25: parts.insert(0, rng.choice(PAST_GOOD))              # praise for the past
    if rng.random() < 0.15: parts.insert(int(rng.integers(0, len(parts) + 1)), rng.choice(FILLER))
    return fill(" ".join(parts), t)

def positive_text(t):
    parts = list(rng.choice(POS, int(rng.choice([1, 1, 2, 2, 3])), replace=False))
    if rng.random() < 0.15: parts.append(rng.choice(MILD))
    if rng.random() < 0.15: parts.insert(0, rng.choice(FILLER))
    return fill(" ".join(parts), t)

def soften(text):
    """people write carelessly: lowercase, no final period, a typo now and then"""
    if rng.random() < 0.25: text = text.lower()
    if rng.random() < 0.3: text = text.rstrip(".")
    if rng.random() < 0.08: text = text.replace("the ", "teh ", 1).replace("you", "u", 1)
    return text

FIRST = ["Mike", "Sarah", "John", "Lisa", "Carlos", "Anna", "David", "Maria", "Chris", "Linda", "James", "Kim",
         "Robert", "Jessica", "Tony", "Emily", "Steve", "Laura", "Brian", "Nicole", "Jose", "Amy", "Kevin", "Rachel"]

def author(store):
    if store == "Google Play" and rng.random() < 0.1:
        return "A Google user"
    return f"{rng.choice(FIRST)} {chr(int(rng.integers(65, 91)))}."

def make_review(t, store):
    r = rng.random()
    if r < 0.05:                                                                 # 3 stars: some good, some bad
        c = " ".join(complaint(t))
        rating, text = 3, fill(f"{rng.choice(BUT)} {c[0].lower()}{c[1:]}".strip(), t)
    elif r < 0.05 + 0.95 * share_negative(t):
        rating, text = int(rng.choice([1, 1, 1, 2])), negative_text(t)
        if rng.random() < 0.08: text = positive_text(t)                         # wrong stars
        elif rng.random() < 0.05: text = rng.choice(VAGUE)
    else:
        rating, text = int(rng.choice([4, 5, 5, 5])), positive_text(t)
        if rng.random() < 0.04: text = rng.choice(VAGUE)
        elif rng.random() < 0.1:                                                 # good stars, but a complaint
            c = " ".join(complaint(t))
            text = fill(f"{rng.choice(BUT)} {c[0].lower() if rng.random() < 0.5 else c[0]}{c[1:]}".strip(), t)
    text = soften(text)
    if store == "Google Play" or rng.random() < 0.3:
        title = ""
    elif rng.random() < 0.4:
        title = rng.choice(NEUTRAL_TITLES)
    else:
        title = rng.choice(NEG_TITLES) if rating <= 2 else rng.choice(POS_TITLES) if rating >= 4 else "Mixed feelings"
    version = version_at(store, t) if store != "Trustpilot" and rng.random() < 0.85 else None
    return dict(posted_at=t, store=store, rating=rating, title=title, review_text=text, author=author(store), app_version=version)

rows = []
for month in pd.date_range(START, END, freq="MS"):
    years_in = (month - START).days / 365
    n = int(rng.poisson(95 * np.exp(-0.12 * years_in) + 20))
    for _ in range(n):
        t = month + pd.Timedelta(seconds=int(rng.integers(0, 30 * 86400)))
        if t > END: continue
        rows.append(make_review(t, rng.choice(["App Store", "Google Play"], p=[0.55, 0.45])))
# Trustpilot: a batch imported at once in November 2025 (dated on import), then a few a month
for _ in range(320):
    rows.append(make_review(pd.Timestamp("2025-11-10") + pd.Timedelta(seconds=int(rng.integers(0, 3 * 86400))), "Trustpilot"))
for month in pd.date_range("2025-12-01", END, freq="MS"):
    for _ in range(int(rng.poisson(14))):
        t = month + pd.Timedelta(seconds=int(rng.integers(0, 28 * 86400)))
        if t <= END: rows.append(make_review(t, "Trustpilot"))

reviews = pd.DataFrame(rows)
# edited reviews: about 1% come in again later with the same text and new stars
named = reviews[reviews.author != "A Google user"].sample(frac=0.011, random_state=1).copy()
named["posted_at"] += pd.to_timedelta(rng.integers(1, 60, len(named)), unit="D")
named["rating"] = np.clip(named.rating + rng.choice([-2, -1, 1], len(named)), 1, 5)
reviews = pd.concat([reviews, named[named.posted_at <= END]]).sort_values("posted_at").reset_index(drop=True)
reviews["posted_at"] = reviews.posted_at.dt.floor("s")

# some releases were never written down
releases = releases.drop(releases.sample(frac=0.15, random_state=2).index).sort_values(["store", "released_at"])
reviews.to_csv("reviews.csv", index=False)
releases.to_csv("releases.csv", index=False)
print(len(reviews), "reviews,", len(releases), "releases")
