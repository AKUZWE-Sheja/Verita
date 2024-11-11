import json
import random
import re
import spacy
from textblob import TextBlob

class Chatbot:
    def __init__(self, intents_file):
        # Load intents from JSON file
        with open(intents_file, "r") as file:
            self.intents = json.load(file)["intents"]
        # Dictionary to store extracted entities like name and location
        self.entities = {}
        self.nlp = spacy.load("en_core_web_sm")

    def find_intent(self, user_input):
        # Loop through intents and find a match based on keywords in patterns
        for intent in self.intents:
            # Check each pattern in intent patterns
            for pattern in intent["patterns"]:
                # Use regex to detect if the pattern has an entity placeholder
                name_match = re.search(r"\b(?:my name is|I'm|I am|call me)\s+(\w+)", user_input, re.IGNORECASE)
                location_match = re.search(r"\b(?:located in|from|location is)\s+(\w+)", user_input, re.IGNORECASE)
                
                if name_match:
                    self.entities["name"] = name_match.group(1)
                    return intent["tag"]
                elif location_match:
                    self.entities["location"] = location_match.group(1)
                    return intent["tag"]
                elif pattern.lower() in user_input.lower():
                    return intent["tag"]

        return "unknown"
    
    def analyze_sentiment(self, text):
        # Use TextBlob for sentiment score or replace with VADER
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity
        if sentiment_score > 0.1:
            return "positive"
        elif sentiment_score < -0.1:
            return "negative"
        else:
            return "neutral"

    def get_response(self, intent, sentiment):
        # Adjust response based on sentiment
        for intent_obj in self.intents:
            if intent_obj["tag"] == intent:
                if sentiment == "positive":
                    return random.choice(intent_obj.get("positive_responses", intent_obj["responses"]))
                elif sentiment == "negative":
                    return random.choice(intent_obj.get("negative_responses", intent_obj["responses"]))
                return random.choice(intent_obj["responses"])

    def handle_user_input(self, user_input):
        # Detect intent and get response
        intent = self.find_intent(user_input)
        sentiment = self.analyze_sentiment(user_input)
        return self.get_response(intent)
