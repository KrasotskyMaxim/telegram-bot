from pyexpat.errors import XML_ERROR_TEXT_DECL
import random
# files
import json
from statistics import mode
# alphabet
from string import ascii_letters

# Ml
from nltk import edit_distance
from numpy import vectorize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

RANDOM_STATE = 42
BOT_CONFIG = {}
RUSSIAN_LETTERS = ['ё','й','ц','у','к','е','н','г','ш','щ','з','х','ъ','ф','ы','в','а','п','р','о','л','д','ж','э','я','ч','с','м','и','т','ь','б','ю']


with open("BOT_CONFIG.json", 'r', encoding="utf-8") as f:
    BOT_CONFIG = json.load(f)
    #print(BOT_CONFIG["intents"].keys())

# BOT_CONFIG = {
#     "intents": {
#         "hello": {
#             "examples": ["Hi", "Hello", "Good evening"],
#             "responses": ["Hi", "Hello", "Good evening"],
#         },
#         "thanks": {
#             "examples": ["Thank you", "Thanks", "Thank you very much"],
#             "responses": ["You are Welcome", "Ok", "Contact again"],
#         },
#         "goodbuy": {
#             "examples": ["Buy", "Goodbuy", "See you"],
#             "responses": ["Goodbuy", "Buy", "See you later"],
#         },
#         "good": {
#             "examples": ["Good", "Ok", "Very well"],
#             "responses": ["Very well", "Good!", "Well"],
#         },
#         "bad": {
#             "examples": ["Bad", "Very bad", "Poorly"],
#             "responses": ["Sorry", "I apologize", "Excuse me"],
#         },
#     }
# }


def clean_text(text):
    output_text = ""
    for ch in text:
        if ch in ascii_letters or ch in RUSSIAN_LETTERS:
            output_text += ch
    return output_text

def main():
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

    # LogReg - 1.0
    # LogReg Train - 0.9
    # LogReg Test - 0.6
    #
    # RandFor - 1.0
    # RandFor Train - 1.0
    # RandFor Test - 0.6
    print(model.score(X_train_vectorized, y_train))
    print(model.score(X_test_vectorized, y_test))


    input_text = ""

    while True:
        input_text = input("Enter message: ")
        if input_text == "":
            print("You don't text anything!")
        else:
            bot_answer = bot(clean_text(input_text), model, vectorizer)
            print(bot_answer)
            if leave(bot_answer):
                break

def leave(bot_answer):
    exit_intents = ["bye", "goodbye"]
    for intent in exit_intents:
        if bot_answer in BOT_CONFIG["intents"][intent]["responses"]:
            return True
    return False
        

def get_intent(input_text, model, vectorizer):
    return model.predict(vectorizer.transform([input_text]))[0]


def bot(input_text, model, vectorizer):
    intent = get_intent(input_text, model, vectorizer)
    return random.choice(BOT_CONFIG["intents"][intent]["responses"])


if __name__ == "__main__":
    main()


