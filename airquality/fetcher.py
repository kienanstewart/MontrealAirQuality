"""
All the code which fetches the data from the api, and parses it with airquality.parser
"""
import datetime
import logging

import requests

from airquality.parser import Parse

FEED_URL = "http://ville.montreal.qc.ca/rsqa/servlet/makeXmlActuel"
LOG = logging.getLogger(__name__)

class FetchException(Exception):
    """Error raised when fetching."""

def fetch_for(day=None):
    """Fetches and parses the xml data for the given day.

        :param day: Datetime object of the day to fetch for. If None, uses today.
    """
    if day is None:
        day = datetime.datetime.today()

    day_string = day.strftime("%y%m%d")
    LOG.debug("Fetching xml for day %r" % day_string)

    answer = requests.get(FEED_URL, params={"date": day_string})

    if answer.status_code != 200:
        raise FetchException(
            "Feed request has status %r with content %r" % (
                answer.status_code,
                answer.content
            )
        )

    return Parse(answer.content.encode("iso-8859-1"))
