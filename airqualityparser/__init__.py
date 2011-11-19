#!/usr/bin
"""
For parsing the xml from http://ville.montreal.qc.ca/rsqa/servlet/makeXmlActuel?date=13/11/11

quick example
<iqa><journee jour="19" mois="11" annee="2011"><station id="7" donnees="oui"><echantillon heure="0"><qualite value="7"/><polluant nom="NO2" value="4"/><polluant nom="PM" value="7"/><polluant nom="SO2" value="1"/></echantillon>
"""

class MontrealIQADay(object):

    def __init__(self):
        self.day = None
        self.month = None
        self.year = None
        self.stations = []


class MontrealIQAStation(object):
    
    def __init__(self):
        self.id = None
        self.name = None
        self.measurements = []


class MontrealIQAMeasurement(object):

    def __init__(self, hour, pollutants):
        self.hour = None
        self.pollutants = {}


def ParseFile(filepath):
    """
    Parses the given file as xml and returns a dictionary indexed by location name
    which has a 
