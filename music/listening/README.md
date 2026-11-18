# Music Listening Studies

Two studies of how people listen to music in Russia.

## 1. Moscow vs. St. Petersburg

**Notebook:** [music_of_big_cities.ipynb](music_of_big_cities.ipynb) · **Data:** [music_of_big_cities.csv](music_of_big_cities.csv)

About 65,000 Yandex.Music plays with the user, track, artist, genre, city, time, and day of the week. Three hypotheses were tested:

1. People in the two cities listen to music on different schedules.
2. The top genres on Monday morning and Friday evening are different.
3. The two cities prefer different genres.

The data was cleaned (missing values, duplicates, and hip-hop spelled four ways), and plays were compared by city, day, and time.

**Results:** The cities are mirror images. Moscow listens most on Monday and Friday and least on Wednesday; St. Petersburg listens most on Wednesday. Pop leads in both cities, and the top 5 genres are the same: pop, dance, rock, electronic, hip-hop. The differences show up lower in the top 10. Rap was expected to be more popular in St. Petersburg, but it wasn't. Of the three hypotheses, only the second was confirmed.

## 2. Popular Caucasian Songs

**Notebook:** [caucasus_spotify_analytics.ipynb](caucasus_spotify_analytics.ipynb) · **Data:** [caucasus_music.csv](caucasus_music.csv)

Yandex.Music's "Caucasian music" genre has about 500 tracks, and some of them become hits far beyond the Caucasus. 477 of them were matched with their Spotify audio features (danceability, energy, mood, tempo, and others) and popularity, to see whether a song's sound explains its popularity.

Mood is charted against danceability, then PCA and t-SNE map the songs by how similar they sound, colored by popularity. Hover over a point in the interactive charts to see the artist and song.

## Tools

Python, pandas, scikit-learn (PCA, t-SNE), matplotlib, plotly
