# Clustering the Neighborhoods of Krasnodar

Which neighborhoods of Krasnodar, Russia, are the most comfortable to live in, judging by what's around them?

**Notebook:** [city_neighbourhoods.ipynb](city_neighbourhoods.ipynb)

## Data

- [neigh_kras.csv](neigh_kras.csv): 46 Krasnodar neighborhoods with their coordinates (names are in Russian)
- Venues near each neighborhood from the Foursquare API: 364 venues in 132 categories, within 500 meters

## Approach

- Mapped all neighborhoods with folium
- Pulled nearby venues for each neighborhood from Foursquare
- Listed the 10 most common venue types in each neighborhood (cafés, shopping malls, hotels, parks, and so on)
- Grouped the neighborhoods into 5 clusters with k-means and showed them on a map

## Results

Most neighborhoods ended up in one large cluster led by cafés, shopping malls, and stores. A second group is led by hotels, a third by light rail stations, and two outskirts neighborhoods each formed a cluster of their own. The notebook ends with the clusters and doesn't rank the neighborhoods.

## Tools

Python, pandas, geopy, Foursquare API, scikit-learn (k-means), folium
