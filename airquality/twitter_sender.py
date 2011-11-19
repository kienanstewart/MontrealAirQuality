"""
Here is the module responsible for posting to twitter. It requires a json file called auth.json in the root directory to hold passwords, etc with the following structure:

auth.json:

{
    "username": "kofkofmtl",
    "oauth_token": "...",
    "oauth_token_secret": "..."
}
"""

import json

import twitter as twitter

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
        return "%s et %s" % pollutants
    else:
        return pollutants
    
def send_air_message(station, pollutants):
    api = get_api()
    api.PostUpdate(msg)
