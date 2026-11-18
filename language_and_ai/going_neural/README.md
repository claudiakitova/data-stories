# Going Neural: word2vec on Going Postal

What does a small neural network learn about words from a single novel?

**Notebook:** [going_neural.ipynb](going_neural.ipynb) · **Data:** the text of Terry Pratchett's *Going Postal*, not included here because the book is under copyright

## Data

The full text of *Going Postal* (2004), about 117,000 words. Words seen at least 5 times are kept, which leaves a vocabulary of 2,134 words.

## Approach

1. Split the book into words, dropped rare ones and kept very common words such as "the" only part of the time.
2. Built (center word, nearby word) pairs from a window of up to 5 words on each side.
3. Wrote word2vec (skip-gram with negative sampling) from scratch in PyTorch and trained 100-number vectors for 10 passes over the book.
4. Explored the vectors: nearest words, word pairs, analogies, a t-SNE map of the vocabulary, character similarity, a hero vs. villain direction, odd-one-out puzzles, word chains, and text written from the vectors alone.

## Results

- Names and the words around them come out close: "vetinari" is nearest to "lord" (0.78), and "adora" to "belle" (0.94) and "dearheart" (0.66).
- Characters who share scenes or roles are alike: Reacher Gilt and Greenyham (0.53), Vetinari and Drumknott (0.52), Stanley and Groat (0.49).
- One book is too little text for analogies: "man is to woman as he is to ?" does not give "she".

## Running

Put a plain-text copy of the book next to the notebook as `going_postal.txt`.

## Tools

Python, PyTorch, NumPy, scikit-learn (t-SNE), matplotlib, plotly, ipywidgets
