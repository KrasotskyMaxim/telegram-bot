import random
from string import ascii_letters
from nltk import edit_distance


BOT_CONFIG = {
    "intents": {
        "hello": {
            "examples": ["Hi", "Hello", "Good evening"],
            "responces": ["Hi", "Hello", "Good evening"],
        },
        "thanks": {
            "examples": ["Thank you", "Thanks", "Thank you very much"],
            "responces": ["You are Welcome", "Ok", "Contact again"],
        },
        "goodbuy": {
            "examples": ["Buy", "Goodbuy", "See you"],
            "responces": ["Goodbuy", "Buy", "See you later"],
        },
        "good": {
            "examples": ["Good", "Ok", "Very well"],
            "responces": ["Very well", "Good!", "Well"],
        },
        "bad": {
            "examples": ["Bad", "Very bad", "Poorly"],
            "responces": ["Sorry", "I apologize", "Excuse me"],
        },
    }
}


def clean_text(text):
    output_text = ""
    for ch in text:
        if ch in ascii_letters:
            output_text += ch
    return output_text


def get_intent(input_text):
    for intent in BOT_CONFIG['intents'].keys():
        for example in BOT_CONFIG['intents'][intent]['examples']:
            text1 = input_text.lower()
            text2 = example.lower()
            if edit_distance(text1, text2) / max(len(text1), len(text2)) < 0.3:
                return intent
    return "Not found"


def bot(input_text):
    intent = get_intent(input_text)
    if intent == "Not found":
        return "We don't understand you =( Try again"
    else:
        return random.choice(BOT_CONFIG["intents"][intent]["responces"])


def main():
    input_text = ""
    print("For leaving write a Goodbuy", end=f"\n{'-'*30}\n")

    while True:
        input_text = input("Enter message: ")
        if input_text == "":
            print("You don't text anything!")
        else:
            bot_answer = bot(clean_text(input_text))
            print(bot_answer)
            if bot_answer in BOT_CONFIG["intents"]["goodbuy"]["responces"]:
                break


if __name__ == "__main__":
    main()