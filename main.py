import os
import requests
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# -----------------------------
# Environment Variables
# -----------------------------
API_KEY = os.environ.get("OWM_API_KEY")
TWILIO_ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")

# -----------------------------
# OpenWeather API
# -----------------------------
ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"

weather_params = {
    "lat": 54.1930633,
    "lon": -2.9094791,
    "appid": API_KEY,
    "cnt": 4,      # Next 12 hours (4 forecasts)
}

# -----------------------------
# Get Weather Data
# -----------------------------
response = requests.get(ENDPOINT, params=weather_params)
response.raise_for_status()

weather_data = response.json()

will_rain = False

# -----------------------------
# Check the next 12 hours
# -----------------------------
for forecast in weather_data["list"]:
    weather_id = forecast["weather"][0]["id"]

    # Weather IDs below 700 indicate rain, snow, etc.
    if weather_id < 700:
        will_rain = True
        break

# -----------------------------
# Message to send
# -----------------------------
if will_rain:
    sms_body = "☔ It's going to rain today. Don't forget to take an umbrella!"
else:
    sms_body = "☀ No rain expected today. Have a great day!"

# -----------------------------
# Send SMS
# -----------------------------
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

try:
    message = client.messages.create(
        body=sms_body,
        from_=TWILIO_PHONE_NUMBER,
        to="+918943098094"     # Replace with your verified phone number
    )

    print("Message sent successfully!")
    print("Message SID:", message.sid)

except TwilioRestException as e:
    print("Twilio Error Code:", e.code)
    print("Twilio Error Message:", e.msg)
