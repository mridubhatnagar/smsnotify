import os
import json
from datetime import date
import requests
from dotenv import load_dotenv
from twilio.rest import Client
load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
RECEIVER_PHONE_NUMBER = os.getenv("RECEIVER_PHONE_NUMBER")
WORDNIK_API_KEY = os.getenv("WORDNIK_API_KEY")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def get_word_of_the_day(current_date):
    """
    Fetch word of the day from Wordnik API
    """
    response_data = {"word": "Sorry, No new word today", "definition": "No definition available"}
    url = f"https://api.wordnik.com/v4/words.json/wordOfTheDay?date={current_date}" \
          f"&api_key={WORDNIK_API_KEY}"
    response = requests.get(url)
    api_response = json.loads(response.text)
    if response.status_code == 200:
        response_data["word"] = api_response["word"]
        for definition in api_response["definitions"]:
            response_data["definition"] = definition
            break
    return response_data


def send_sms(response_data):
    """
    Send SMS notification with New word
    """
    body = str(response_data["word"]) + "\n\n" + str(response_data["definition"]["text"])
    message = client.messages.create(
        body=body,
        from_=TWILIO_PHONE_NUMBER,
        status_callback='https://demo.twilio.com/welcome/voice/',
        to=RECEIVER_PHONE_NUMBER
    )


if __name__ == "__main__":
    current_date = date.today()
    data = get_word_of_the_day(current_date)
    send_sms(data)
