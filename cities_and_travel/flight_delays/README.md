# Predicting On-Time Flight Arrivals

Given the date, time, origin, and destination, will a flight arrive on time?

**Notebook:** [on_time_flight_arrivals.ipynb](on_time_flight_arrivals.ipynb)

## Data

[flightdata.csv](flightdata.csv): 11,231 US flights from 2016 between five airports (ATL, DTW, JFK, MSP, SEA), with 26 columns. The notebook has a table describing every column.

## Approach

- Cleaned the data: dropped an empty column, kept the 7 columns that matter, and filled 188 missing arrival-delay values
- Turned departure times into hours and airports into one-hot columns
- Trained a random forest classifier on 80% of the flights and tested it on the other 20%
- Wrote a `predict_delay()` function that returns the chance a flight arrives on time, and charted it for one route (JFK → ATL) across a week

## Results

- **86% accuracy** on the test flights
- **ROC AUC 0.67**: most flights arrive on time, so accuracy looks better than the model really is. Of 311 delayed flights in the test set, it caught 51.

## Tools

Python, pandas, scikit-learn (random forest), matplotlib, seaborn
