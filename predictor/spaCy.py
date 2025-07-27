# bert_model.py (new logic with spaCy)
import spacy

nlp = spacy.load("en_core_web_sm")

GOALS = ["weight loss", "muscle gain", "get fit", "get slim", "build strength", "increase stamina"]

def extract_goal_from_text(text):
    doc = nlp(text.lower())
    for goal in GOALS:
        if goal in doc.text:
            return goal
    return "general fitness"
