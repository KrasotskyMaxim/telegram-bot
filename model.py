import json
# Ml
from nltk import edit_distance
from numpy import vectorize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


RANDOM_STATE = 42
BOT_CONFIG = {}



with open("BOT_CONFIG.json", 'r', encoding="utf-8") as f:
    BOT_CONFIG = json.load(f)
    #print(BOT_CONFIG["intents"].keys())


# create ML
X = []
y = []

for intent in BOT_CONFIG["intents"].keys():
    try:
        for example in BOT_CONFIG["intents"][intent]["examples"]:
            X.append(example)
            y.append(intent)
    except KeyError:
        pass

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=RANDOM_STATE)


vectorizer = CountVectorizer(ngram_range=(1, 3), analyzer="char")
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)
# print(X_vectorized)

# model = LogisticRegression(random_state=42, C=10)
model = RandomForestClassifier(random_state=RANDOM_STATE, n_estimators=200) 
model.fit(X_train_vectorized, y_train)
#print(model.predict(vectorizer.transform(["say hello"])))


def main():
    # train - 0.8839285714285714
    # test - 0.19212962962962962
    print(model.score(X_train_vectorized, y_train))
    print(model.score(X_test_vectorized, y_test))

    # data table
    y_preds = model.predict(X_test_vectorized)
    print(classification_report(y_preds, y_test))


if __name__ == "__main__":
    main()