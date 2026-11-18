# Data Stories

Real-life questions answered with data, for learning and teaching data science. Each project starts from a question and ends with what the data says, including when a model turns out no better than a simple rule.

## Business analytics

| Project | Question | Tools |
|---|---|---|
| [game_player_value](business_analytics/game_player_value/) | How much will a new player of a mobile game bring in over 120 days, judging by their first week? | pandas, LightGBM |
| [food_delivery](business_analytics/food_delivery/) | Do a few vendors dominate each market, what vendor segments exist, and why does a regression overstate what vouchers do? | scikit-learn (k-means), statsmodels |
| [promo_forecast](business_analytics/promo_forecast/) | How many units will each store sell of a product on promotion? | pandas, LightGBM |
| [car_prices](business_analytics/car_prices/) | What sets a car's price, and how closely can its specifications predict it? | scikit-learn, XGBoost |

## Crypto and finance

| Project | Question | Tools |
|---|---|---|
| [bitcoin_forecast](crypto_and_finance/bitcoin_forecast/) | Can a neural network predict tomorrow's Bitcoin price better than "tomorrow equals today"? | TensorFlow / Keras (LSTM), statsmodels |
| [fintech_app](crypto_and_finance/fintech_app/) | Where do new users of a crypto-finance app drop out, do they come back, and which crypto-backed loans get liquidated? | pandas, matplotlib |

## Language and AI

| Project | Question | Tools |
|---|---|---|
| [company_docs_chatbot](language_and_ai/company_docs_chatbot/) | How well can a chatbot find the right passage in a company's internal documents? | FastEmbed, BM25 |
| [movie_review_sentiment](language_and_ai/movie_review_sentiment/) | Is an IMDB movie review positive or negative? A neural network, plus a function that scores any text | TensorFlow / Keras |

## Climate and science

| Project | Question | Tools |
|---|---|---|
| [starship_life_support](climate_and_science/starship_life_support/) | Can an algae photobioreactor supply a starship crew's oxygen and absorb their carbon dioxide? | pandas, NumPy |
| [dryer_cleaning](climate_and_science/dryer_cleaning/) | Can sensors warn a few days ahead that an industrial dryer needs cleaning? | scikit-learn |
| [temperature_trend](climate_and_science/temperature_trend/) | How fast did the global temperature rise from 1882 to 2014? | NumPy, scikit-learn, seaborn |

## Cities and travel

| Project | Question | Tools |
|---|---|---|
| [krasnodar_neighbourhoods](cities_and_travel/krasnodar_neighbourhoods/) | Which neighborhoods of Krasnodar, Russia, are the most comfortable to live in, judging by the venues around them? | pandas, geopy, scikit-learn (k-means) |
| [flight_delays](cities_and_travel/flight_delays/) | Will a flight arrive on time, given its date, time, and route? | pandas, scikit-learn (random forest) |

## Music

| Project | Question | Tools |
|---|---|---|
| [listening](music/listening/) | How do Moscow and St. Petersburg listen to music, and does a song's sound explain the popularity of top Caucasian songs? | pandas, scikit-learn (PCA, t-SNE), plotly |
| [melody_generation](music/melody_generation/) | Can a small neural network continue a melody the way Bach wrote them? | TensorFlow / Keras (LSTM), music21 |

## Running

Each project folder is self-contained: open the notebook in Jupyter or Google Colab, and the data it needs is next to it. Where the data is synthetic, the script that generated it (`make_data.py`) is in the folder too.
