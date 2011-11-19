"""
All the code which fetches the data from the api, and parses it with airquality.parser
"""
import datetime

import requests

from airquality.parser import Parse

FEED_URL = "http://ville.montreal.qc.ca/rsqa/servlet/makeXmlActuel?%s"

class FetchException(Exception):
    """Error raised when fetching."""

def fetch_for(day=None):
    """Fetches and parses the xml data for the given day.

        :param day: Datetime object of the day to fetch for. If None, uses today.
    """
    if day is None:
        day = datetime.datetime.today()

    day_string = day.strftime("%d/%m/%y")

    answer = requests.get(FEED_URL % day_string)

    if answer.status_code != 200:
        raise FetchException(
            "Feed request has status %r with content %r" % (
                answer.status_code,
                answer.content
            )
        )

    #with open("data.xml") as data_file:
    #    return Parse(data_file.read())
    return Parse(str(answer.content))
