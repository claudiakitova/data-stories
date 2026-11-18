"""Extracts the soprano melodies of the Bach chorales that come with the music21 library.

Each melody is transposed to C major or A minor, so the model learns melody shapes rather than keys.
Run: python make_data.py  (writes melodies.csv: one row per note)
"""
import pandas as pd
from music21 import corpus, interval, pitch

rows = []
for path in corpus.getComposer("bach"):
    score = corpus.parse(path)
    soprano = [p for p in score.parts if (p.partName or "").lower().startswith("soprano")]
    if not soprano:
        continue
    key = score.analyze("key")
    target = pitch.Pitch("C") if key.mode == "major" else pitch.Pitch("A")
    shift = interval.Interval(key.tonic, target)
    melody = soprano[0].flatten().notes.stream().transpose(shift)
    name = path.stem
    for i, n in enumerate(melody):
        if not n.isNote:
            continue
        rows.append((name, key.mode, i, n.pitch.midi, n.pitch.nameWithOctave, float(n.quarterLength)))

melodies = pd.DataFrame(rows, columns=["chorale", "mode", "position", "pitch", "note", "duration"])
melodies.to_csv("melodies.csv", index=False)
print(f"{melodies.chorale.nunique()} chorales, {len(melodies):,} notes")
