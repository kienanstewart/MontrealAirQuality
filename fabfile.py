# -*- coding: utf-8 -*-

import csv
import datetime
import logging

from fabric.api import task

from airquality.fetcher import fetch_for
from airquality.twitter_sender import send_air_message, get_login_details

logging.basicConfig(level=logging.DEBUG)

@task
def grab_data(days=5):
    """Grabs the data for the last 5 days and outputs to a csv file called data.csv."""

    with open("data.csv", "w") as output_file:
        writer = csv.writer(output_file)
        for n in range(days):
            today = datetime.datetime.today() - datetime.timedelta(n)
            print "Doing %s" % today
            data = fetch_for(today)

            writer.writerow(["Year", "Month", "Day"])
            writer.writerow([data.year, data.month, data.day])
            writer.writerow([])

            writer.writerow(["Station Id", "Station Name", "Hour", "Pollutant", "Value"])
            for station in data.stations:
                for measure in station.measurements:
                    for pollutant, value in measure.pollutants.items():
                        writer.writerow([station.id, station.name, measure.hour, pollutant, value])
            writer.writerow([])

@task
def post_update():
    """Posts an update to the twitter feed."""
    send_air_message("Bienvenue à Kof Kof Montreal!")

@task
def authenticate_w_twitter():
    """Ask twitter for an access key and secret by posting url, asking for PIN."""
    import tweepy

    login_details = get_login_details()
    auth = tweepy.OAuthHandler(
        login_details["consumer_key"],
        login_details["consumer_secret"]
    )
    print "Auth url: ", auth.get_authorization_url()
    print "What is the pin?", 
    pin = int(raw_input())

    auth.get_access_token(pin)

    print "ACCESS_KEY = '%s'" % auth.access_token.key
    print "ACCESS_SECRET = '%s'" % auth.access_token.secret
