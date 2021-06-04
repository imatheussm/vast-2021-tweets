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

# Loading the appropriate stemmer
stemmer = snowball.SnowballStemmer(language="english")

# Loading and preprocessing the data sets.
#
# Time periods:
#  - Period one: 1700-1830
#  - Period two: 1831-2000
#  - Period three: 2001-2131

periods = ("1700-1830", "1831-2000", "2001-2131")
data_frames = [pd.read_csv(f"csv-{period}.csv") for period in periods]
stop_words = stopwords.words("english")

for index, data_frame in enumerate(data_frames):
    print(f"[{index + 1}/{len(data_frames)}] Processing data-frames...")
    data_frame_length = data_frame.shape[0]

    for row in range(data_frame_length):
        print(f" |_ [{row + 1}/{data_frame_length}] Processing row...", end="\r")

        message = data_frame.loc[row, "message"]
        document = nlp(message)
        tokens = [stemmer.stem(token.text) for token in document if token.text not in stop_words]

        data_frame.loc[row, "message"] = " ".join(tokens)

    print(f" |_ [{data_frame_length}/{data_frame_length}] Processing completed.")

for index, data_frame in enumerate(data_frames):
    data_frame.to_csv(f"new-csv-{periods[index]}.csv")
