# Popular Caucasian Songs: Does the Sound Explain the Hit?

**Notebook:** [popular_songs.ipynb](popular_songs.ipynb) · **Data:** [caucasus_music.csv](caucasus_music.csv)

Yandex.Music's "Caucasian music" genre has about 500 tracks, and some of them become hits far beyond the Caucasus. 477 of them were matched with their Spotify audio features (danceability, energy, mood, tempo, and others) and popularity, to see whether a song's sound explains its popularity.

Mood is charted against danceability, then PCA and t-SNE map the songs by how similar they sound, colored by popularity. Hover over a point in the interactive charts to see the artist and song.

## Tools

Python, pandas, NumPy, scikit-learn (PCA, t-SNE), matplotlib, plotly
