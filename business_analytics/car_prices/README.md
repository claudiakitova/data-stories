# What Sets a Car's Price?

Clean a dealership's records of 245 car sales, find what drives the price, and price a car from its specifications.

**Notebook:** [car_prices.ipynb](car_prices.ipynb) · **Data:** [cars.csv](cars.csv), a sample dataset of car sales, with the owners' personal columns removed

## Data

Car model, sale date, fuel type, aspiration, doors, body, drive wheels, engine location, dimensions, weight, cylinders, engine size, compression ratio, horsepower, peak rpm, fuel economy, and price.

## Approach

1. Dropped rows without a car identity, fixed misspelled brands, and filled the remaining gaps.
2. Looked at price by brand and its correlation with each specification, and built combined features: power to weight, combined fuel economy, and a luxury-brand flag.
3. Compared linear regression, ridge, random forest, XGBoost, and a ridge + XGBoost blend with 5-fold cross-validation.

## Results

- XGBoost prices a car within $1,250 on average (R² 0.94); linear models miss by about $1,560–1,590.
- The luxury-brand flag and engine size matter most.
- The largest errors are on luxury models, whose price depends on more than their specifications.

## Tools

Python, pandas, NumPy, scikit-learn, XGBoost, matplotlib
