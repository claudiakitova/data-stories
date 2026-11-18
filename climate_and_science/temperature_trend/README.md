# Climate Change: Temperature Trend, 1882–2014

Is the average global temperature going up, and how fast?

**Notebook:** [climatechange.ipynb](climatechange.ipynb)

## Data

Two CSV files of five-year mean temperature differences, one value per year:

- [5-year-mean-1882-2014.csv](5-year-mean-1882-2014.csv): the full period, 1882 to 2014
- [5-year-mean-1951-1980.csv](5-year-mean-1951-1980.csv): the 1951–1980 period

## Approach

Plotted the data and fitted the same straight-line trend three different ways, to compare the tools:

1. NumPy (`polyfit`)
2. scikit-learn (`LinearRegression`)
3. seaborn (`regplot`), drawn over the full 1882–2014 data

## Results

NumPy and scikit-learn give the same line: **y = 0.00728 · year − 14.31**. That's a rise of about 0.73 degrees per century, fitted on the 1951–1980 values.

## Tools

Python, NumPy, scikit-learn, matplotlib, seaborn
