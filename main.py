import json
import requests
import os
import errno
from datetime import datetime
from flask import Flask, Response
from slackeventsapi import SlackEventAdapter
from threading import Thread
from slack import WebClient

# This `app` represents your existing Flask app
app = Flask(__name__)

# greetings = ["hello", "hello there", "hey"]
states = ["alaska", "alabama", "arkansas", "american samoa", "arizona", "california", "colorado", "connecticut",
          "district ", "of columbia", "delaware", "florida", "georgia", "guam", "hawaii", "iowa", "idaho", "illinois",
          "indiana", "kansas", "kentucky", "louisiana", "massachusetts", "maryland", "maine", "michigan", "minnesota",
          "missouri", "mississippi", "montana", "north carolina", "north dakota", "nebraska", "new hampshire",
          "new jersey", "new mexico", "nevada", "new york", "ohio", "oklahoma", "oregon", "pennsylvania", "puerto rico",
          "rhode island", "south carolina", "south dakota", "tennessee", "texas", "utah", "virginia", "virgin islands",
          "vermont", "washington", "wisconsin", "west Virginia", "wyoming"]
countries = ['Germany', 'France', 'China', 'United States']
help_command = ['help']


SLACK_SIGNING_SECRET = ''
slack_token = ''
VERIFICATION_TOKEN = ''

# instantiating slack client
slack_client = WebClient(slack_token)


# An example of one of your Flask app's routes
@app.route("/")
def event_hook(request):
    json_dict = json.loads(request.body.decode("utf-8"))
    if json_dict["token"] != VERIFICATION_TOKEN:
        return {"status": 403}

    if "type" in json_dict:
        if json_dict["type"] == "url_verification":
            response_dict = {"challenge": json_dict["challenge"]}
            return response_dict
    return {"status": 500}
    return


slack_events_adapter = SlackEventAdapter(
    SLACK_SIGNING_SECRET, "/slack/events", app
)


@slack_events_adapter.on("app_mention")
def handle_message(event_data):
    def send_reply(value):
        event_data = value
        message = event_data["event"]
        if message.get("subtype") is None:
            command = message.get("text")
            channel_id = message["channel"]
            if any(item in command.lower() for item in help_command):
                message = "@ me with any country, statefor detailed information. For specific counties, use 'county <county>'."
                slack_client.chat_postMessage(channel=channel_id, text=message)
            elif any(state in command.lower() for state in states):  # US states
                my_state = (command.split('>')[1].lstrip().title())
                response_data = get_state_stats(my_state)
                message = "State: {} --- Cases: {} --- Deaths: {} --- Active: {}" \
                    .format(response_data['state'], response_data['cases'], response_data['deaths'],
                            response_data['active'])
                slack_client.chat_postMessage(channel=channel_id, text=message)
            elif any(country in command for country in countries):
                my_country = (command.split('>')[1].lstrip().title())
                response_data = get_country_stats(my_country)
                message = "Country: {} --- Cases: {} --- Deaths: {} --- Active: {}"\
                    .format(response_data['country'], response_data['cases'], response_data['deaths'], response_data['active'])
                slack_client.chat_postMessage(channel=channel_id, text=message)
            elif command.split('> ')[1].split(' ')[0] == 'county':
                # <> county Santa Clara
                my_county = (command.split('county ')[1])
                print('county command: -{}-'.format(my_county))
                response_data = get_county_stats(my_county)
                print(response_data)
                message = "County: {} --- Cases: {} --- Deaths: {} --- Recovered: {}" \
                    .format(response_data['county'], response_data['cases'], response_data['deaths'], response_data['recovered'])
                slack_client.chat_postMessage(channel=channel_id, text=message)
            else:
                print('unknown command')
                message = 'Unknown command'
                slack_client.chat_postMessage(channel=channel_id, text=message)

    thread = Thread(target=send_reply, kwargs={"value": event_data})
    thread.start()
    return Response(status=200)


def get_state_stats(state):
    query = 'https://disease.sh/v3/covid-19/states?sort=cases&yesterday=false'
    full_data = (requests.get(query))
    if full_data.status_code == 200:
        json_data = json.loads(full_data.text)

        # return (json_data)
        counter = 0
        for num in json_data:
            if num['state'] == state:
                response = json_data[counter]
            counter = counter + 1
        print(response)
        return {'state': state, 'cases': response['cases'], 'deaths': response['deaths'], 'active': response['active']}


def get_country_stats(country):
    query = 'https://disease.sh/v3/covid-19/countries/{}?yesterday=true&strict=true'.format(country)
    full_data = (requests.get(query))
    if full_data.status_code == 200:
        json_data = json.loads(full_data.text)
        return {'country': country, 'cases': json_data['cases'], 'deaths': json_data['deaths'],
                'active': json_data['active']}


def get_county_stats(county):
    query = 'https://disease.sh/v3/covid-19/jhucsse/counties/{}'.format(county)
    full_data = (requests.get(query))
    if full_data.status_code == 200:
        json_data = json.loads(full_data.text)
        return {'county': county, 'cases': json_data[0]['stats']['confirmed'], 'deaths': json_data[0]['stats']['deaths'],
                'recovered': json_data[0]['stats']['recovered']}


# Start the server on port 3000
if __name__ == "__main__":
    app.run(port=3000)

