# Generating Melodies in the Style of Bach

Can a small neural network learn to continue a melody the way Bach wrote them?

**Notebook:** [melody_generation.ipynb](melody_generation.ipynb) · **Data:** [melodies.csv](melodies.csv), extracted by [make_data.py](make_data.py) · **Result:** [generated_melody.mid](generated_melody.mid)

## Data

The soprano melodies of 409 Bach chorales from the corpus that comes with the music21 library, 21,214 notes, transposed to C major or A minor.

## Approach

1. Looked at the notes, note lengths, and the jumps between notes.
2. Trained an LSTM to predict the next note's pitch and length from the 16 notes before it, holding out a fifth of the chorales for testing.
3. Compared it with two rules: repeat the last pitch, and pick the pitch that most often follows the current one.
4. Let the network continue the opening of an unseen chorale for 48 notes and saved the result as a MIDI file.

## Results

- On unseen chorales the LSTM gets the next pitch right 62% of the time (87% within its top 3), against 44% for the best simple rule, and the next length 78% of the time, against 71%.
- Its generated melody moves by small steps as often as Bach's do (83% against 85%), but it has no sense of a phrase's larger shape.

## Tools

Python, TensorFlow / Keras (LSTM), music21, pandas, NumPy, matplotlib
