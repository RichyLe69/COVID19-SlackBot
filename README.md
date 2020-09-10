# COVID19-SlackBot

![Alpha status](https://img.shields.io/badge/Project%20status-Alpha-red.svg)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PyPI pyversions](https://camo.githubusercontent.com/fd8c489427511a31795637b3168c0d06532f4483/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f77696b6970656469612d6170692e7376673f7374796c653d666c6174)](https://pypi.python.org/pypi/ansicolortags/)


Slack bot designed to provide COVID19 statistics 

Uses API from: https://disease.sh/docs/#/

# Requirements
Python3, Slack Bot API, ngrok localhost webhook.

Use environment variables for API keys:

* SLACK_SIGNING_SECRET
* slack_token
* VERIFICATION_TOKEN

# Bot Uses

Retrieves Data from disease.sh API which is based on Worldometers and John Hopkins University API.

* For particular countries, simply @ the bot followed by the country name (case sensitive).
* For particular states, simply @ the bot followed by the state name (case sensitive).
* For particular counties, simply @ the bot followed by the word 'county' and the county name (case sensitive).

# Example

![Alt Text](https://raw.githubusercontent.com/richardle17/COVID19-SlackBot/master/demo/covid19slackbot-2.jpg)

Todo:

* clean up the code
* possibly change state and country commands to be based on a keyword (e.g state & country)
* Make the visual message slack response more fancy?