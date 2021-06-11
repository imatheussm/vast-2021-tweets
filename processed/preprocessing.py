import pandas as pd
import spacy as sp

from nltk.stem import snowball
from nltk.corpus import stopwords


# Loading the appropriate model
#
# Before doing so, they need to be installed. Choose one (or both, for safe measure) of them:
#  - Bigger, slower, but more accurate: python -m spacy download en_core_web_trf
#  - Small, faster, but less accurate: python -m spacy download en_core_web_sm
nlp = sp.load("en_core_web_trf")

# Loading and preprocessing the data sets.
#
# Time periods:
#  - Period one: 1700-1830
#  - Period two: 1831-2000
#  - Period three: 2001-2131

periods = ("1700-1830", "1831-2000", "2001-2131")

data_frames = [pd.read_csv(f"original_csv/csv-{period}.csv") for period in periods]

# Merge files
combined_csv = pd.concat(data_frames)
combined_csv.to_csv("processed/full.csv", index=False)


stop_words = stopwords.words("english")

data = pd.read_csv("processed/full.csv")

for row in range(data.shape[0]):
    print(f" |_ [{row + 1}/{data.shape[0]}] Processing row...", end="\r")

    message = data.loc[row, "message"]
    document = nlp(message)
    tokens = [
        token.lemma_ for token in document
        if token.text not in stop_words  # Remove stop words
        and token.is_punct is False      # Remove punctuation
    ]

    data.loc[row, "message"] = " ".join(tokens)

data.to_csv(f"processed/new-csv-full.csv", index=False)

# Extract CC (reports) and Posts
data = pd.read_csv("processed/new-csv-full.csv")

reports = data[data['type'] == 'ccdata']

posts = data[data['type'] == 'mbdata']
posts.to_csv("processed/posts.csv")

reports = reports.drop(['author', 'longitude', 'latitude'], axis='columns')\
    .rename(columns={' location' : 'location'})

reports.to_csv("processed/reports.csv")