# Movie Review Sentiment with a Neural Network

Can a small neural network tell whether a movie review is positive or negative?

**Notebook:** [text_analysis_with_neural_network.ipynb](text_analysis_with_neural_network.ipynb)

## Data

The IMDB reviews dataset that comes with Keras: 50,000 reviews labeled positive or negative, split into 25,000 for training and 25,000 for testing. Only the 10,000 most common words are kept, and every review is padded or cut to 500 words.

## Approach

- Decoded a review from numbers back into words to see what the model actually gets
- Built a network with Keras: a word embedding layer, two dense layers of 16 neurons, and a sigmoid output
- Trained it for 5 epochs and plotted training vs. validation loss
- Wrote an `analyze()` function that scores any sentence from 0 (negative) to 1 (positive)

## Results

- **86.9% accuracy** on the 25,000 test reviews
- "Easily the most stellar experience I have ever had." → **0.93**
- "The long lines and poor customer service really turned me off." → **0.02**

## Tools

Python, Keras with TensorFlow, NumPy, matplotlib, seaborn
