"""Writes the made-up internal documents of a fictional company into docs/, and the test questions.

Run: python make_docs.py
"""
import json
from pathlib import Path

DOCS = {
"it_vpn.md": """# Connecting to the office network from home (VPN)

To work from home, connect to the company VPN before opening internal sites.

1. Install the VPN client from the Software Center on your laptop.
2. Sign in with your work email and password.
3. Approve the sign-in on your phone in the authenticator app.

If the VPN disconnects every few minutes, switch from Wi-Fi to a cable or restart your router. If it still fails, open a ticket with the IT service desk and attach a screenshot of the error.
""",
"it_password.md": """# Resetting a forgotten password

Passwords expire every 90 days. You get a reminder email 10 days before.

To reset a forgotten password, go to the self-service portal from any browser, enter your work email, and confirm with the code sent to your phone. The new password must be at least 12 characters and differ from your last five passwords.

If your account is locked after five wrong attempts, it unlocks by itself after 30 minutes, or the IT service desk can unlock it right away.
""",
"it_email_archive.md": """# Archiving old email

Mailboxes are limited to 50 GB. When yours is 90% full, move older messages to an archive file.

In the mail app, choose File, then Export, and save the messages older than a year to a local archive file. Keep the file on your laptop's encrypted drive, not on a USB stick. Archived messages stay searchable when you open the archive file in the mail app.
""",
"it_service_desk.md": """# The IT service desk

The IT service desk handles hardware problems, access requests, and software installation.

Open a ticket on the service desk portal or call extension 4357. Urgent problems that stop your work, such as a laptop that won't start, are answered within 2 hours; other requests within 2 working days. New software must be approved by your manager before IT installs it.
""",
"hr_business_trip.md": """# Business trips

A business trip needs approval before any tickets are booked.

Submit a trip request in the HR portal at least 10 working days before departure, with the purpose, dates, and estimated cost. Your direct manager approves trips within the country; trips abroad also need the department head's approval. Once approved, the travel team books flights and hotels.

The daily allowance for meals is 50 euros within the country and 70 euros abroad.
""",
"hr_vacation.md": """# Vacation

Employees have 25 working days of paid vacation a year, plus public holidays.

Request vacation in the HR portal at least two weeks in advance; your manager approves it. At least one vacation period each year must be 10 working days or longer. Up to 5 unused days can be carried over to the next year and must be used by March 31.
""",
"hr_sick_leave.md": """# Sick leave

If you are ill, tell your manager before the start of your working day.

For an absence of up to 3 days, no medical certificate is needed. From the fourth day, upload a doctor's certificate to the HR portal. Sick days don't count against your vacation days.
""",
"hr_onboarding.md": """# The first week for new employees

On your first day, collect your laptop and access badge at reception at 9:00. Your manager and an assigned buddy will show you around.

During the first week, complete the mandatory courses in the learning portal: information security, data protection, and workplace safety. Your probation period is 3 months, with a review meeting at the end.
""",
"fin_expenses.md": """# Expense reimbursement

Work expenses paid with your own money are reimbursed within 15 working days.

Submit an expense report in the finance portal within 30 days of the expense, with a photo of every receipt. Expenses over 200 euros need your manager's approval before the purchase. Taxi rides are reimbursed only after 21:00 or with heavy luggage on a business trip.
""",
"fin_corporate_card.md": """# The corporate card

Employees who travel often can get a corporate card. Ask your manager to request it in the finance portal.

Use the card only for business expenses: travel, hotels, and client meals. Upload the receipts for every card payment by the 5th of the following month. Personal purchases on the card are not allowed, even if you pay them back.
""",
"office_badge.md": """# Access badges and visitors

Wear your access badge at all times in the office. A lost badge must be reported to reception the same day so it can be blocked; a replacement costs 15 euros.

Visitors are registered in the reception system by the employee who invites them, at least one day ahead. The host meets the visitor at reception and accompanies them during the visit.
""",
"office_parking.md": """# Parking

The office garage has 120 spaces, assigned for a month at a time. Apply for a space in the facilities portal by the 20th of the month before.

Spaces for electric cars have chargers and are assigned first to employees who drive electric cars. Bicycles can be left in the secure bike room on level -1 at any time without registering.
""",
}

QUESTIONS = [
    ("Who approves a business trip?", "hr_business_trip.md"),
    ("How far ahead do I need to request a trip abroad?", "hr_business_trip.md"),
    ("What is the meal allowance when traveling?", "hr_business_trip.md"),
    ("My VPN keeps dropping, what should I do?", "it_vpn.md"),
    ("How do I work from home on internal sites?", "it_vpn.md"),
    ("I forgot my password", "it_password.md"),
    ("My account got locked after wrong attempts", "it_password.md"),
    ("My mailbox is almost full", "it_email_archive.md"),
    ("How fast does IT answer an urgent problem?", "it_service_desk.md"),
    ("Can IT install new software for me?", "it_service_desk.md"),
    ("How many vacation days do I get?", "hr_vacation.md"),
    ("Can I carry unused vacation over to next year?", "hr_vacation.md"),
    ("Do I need a doctor's note if I'm sick for two days?", "hr_sick_leave.md"),
    ("What do I do on my first day?", "hr_onboarding.md"),
    ("How long is probation?", "hr_onboarding.md"),
    ("How do I get my money back for a work purchase?", "fin_expenses.md"),
    ("Is a taxi reimbursed?", "fin_expenses.md"),
    ("Can I buy something personal with the company card?", "fin_corporate_card.md"),
    ("I lost my badge", "office_badge.md"),
    ("Where can I leave my bike?", "office_parking.md"),
]

# the same needs, worded without the documents' own vocabulary
PARAPHRASED = [
    ("Can I keep some days off for next year?", "hr_vacation.md"),
    ("Who signs off on flying to a conference in another country?", "hr_business_trip.md"),
    ("How much can I spend on lunch per day when I'm away for work?", "hr_business_trip.md"),
    ("The connection to the intranet keeps cutting out when I'm at home", "it_vpn.md"),
    ("I typed the wrong login too many times and now I can't get in", "it_password.md"),
    ("Outlook says I'm running out of space", "it_email_archive.md"),
    ("Who do I call when my computer won't turn on?", "it_service_desk.md"),
    ("I have the flu, do I need paperwork from a clinic?", "hr_sick_leave.md"),
    ("I paid for a client dinner myself, how do I get it back?", "fin_expenses.md"),
    ("Can I put a personal holiday on the company Visa?", "fin_corporate_card.md"),
    ("A friend is coming to see me at work tomorrow", "office_badge.md"),
    ("Is there a charger for my Tesla at the office?", "office_parking.md"),
]

Path("docs").mkdir(exist_ok=True)
for name, text in DOCS.items():
    Path("docs", name).write_text(text, encoding="utf-8")
Path("test_questions.json").write_text(json.dumps([{"question": q, "document": d, "kind": "uses the documents' words"} for q, d in QUESTIONS]
                                                    + [{"question": q, "document": d, "kind": "paraphrased"} for q, d in PARAPHRASED], indent=1), encoding="utf-8")
print(f"{len(DOCS)} documents, {len(QUESTIONS) + len(PARAPHRASED)} test questions")
