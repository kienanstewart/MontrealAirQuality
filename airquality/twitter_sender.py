# -*- coding: utf-8 -*-
"""
Here is the module responsible for posting to twitter. It requires a json file called auth.json in the root directory to hold passwords, etc with the following structure:

auth.json:

{
    "username": "kofkofmtl",
    "consumer_key": "...",
    "consumer_secret": "...",
    "access_token_key": "...",
    "access_token_secret": "..."
}

All these values can be found here: https://dev.twitter.com/apps/1400522/show
"""

import json

import twitter as twitter

FR_TEMPLATE = """La station {station} rapporte un niveau élevé de {pollutants} dans la dernière heure. http://bit.ly/sXfDgS"""

def get_login_details():
    with open("auth.json") as auth_file:
        return json.load(auth_file)

def get_api():
    login_details = get_login_details()
    api_details = login_details.copy()
    username = api_details.pop("username")

    return twitter.Api(**api_details)

def concat_pollutants_fr(pollutants):
    if len(pollutants) == 1:
        return pollutants[0]
    elif len(pollutants) == 2:
        return "%s et %s" % (pollutants[0], pollutants[1])
    else:
        return "%s et %s" % (
            ", ".join(pollutants[:-1]),
            pollutants[-1]
        )

def send_air_message(station, pollutants):
    api = get_api()
    text = FR_TEMPLATE.format(
        station=station,
        pollutants=concat_pollutants_fr(pollutants)
    )
    api.PostUpdate(text)
