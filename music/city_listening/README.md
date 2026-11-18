# Music Listening in Moscow and St. Petersburg

Do the two biggest Russian cities listen to music differently?

**Notebook:** [music_of_big_cities.ipynb](music_of_big_cities.ipynb) · **Data:** [music_of_big_cities.csv](music_of_big_cities.csv)

About 65,000 Yandex.Music plays with the user, track, artist, genre, city, time, and day of the week. Three hypotheses were tested:

1. People in the two cities listen to music on different schedules.
2. The top genres on Monday morning and Friday evening are different.
3. The two cities prefer different genres.

The data was cleaned (missing values, duplicates, and hip-hop spelled four ways), and plays were compared by city, day, and time.

**Results:** The cities are mirror images. Moscow listens most on Monday and Friday and least on Wednesday; St. Petersburg listens most on Wednesday. Pop leads in both cities, and the top 5 genres are the same: pop, dance, rock, electronic, hip-hop. The differences show up lower in the top 10. Rap was expected to be more popular in St. Petersburg, but it wasn't. Of the three hypotheses, only the second was confirmed.

## Tools

Python, pandas
