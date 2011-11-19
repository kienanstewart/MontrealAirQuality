#!/usr/bin
"""
For parsing the xml from http://ville.montreal.qc.ca/rsqa/servlet/makeXmlActuel?date=13/11/11

quick example
<iqa><journee jour="19" mois="11" annee="2011"><station id="7" donnees="oui"><echantillon heure="0"><qualite value="7"/><polluant nom="NO2" value="4"/><polluant nom="PM" value="7"/><polluant nom="SO2" value="1"/></echantillon>
"""
import logging
import os
import lxml

log = logging.getLogger(__name__)

class MontrealIQADay(object):

    def __init__(self, day, month, year, stations = []):
        self.day = day
        self.month = month
        self.year = year
        self.stations = stations


class MontrealIQAStation(object):
    
    def __init__(self, id, name = None, measurements = []):
        self.id = id
        self.name = name
        self.measurements = measurements


class MontrealIQAMeasurement(object):

    def __init__(self, hour, pollutants = {}):
        self.hour = hour
        self.pollutants = pollutants # p1 : value; p2 : value
    
    
    def AddPolutant(name, value):
        self.pollutants[name] = value


class IQAParserError(Exception):
    
    def __init__(self, msg):
        super(type(self), self).__init__(msg)


def ParseFile(filepath):
    """
    opens and parses a file and tries to return an instance of MontrealIQADay
    can raise IQAParserError
    """
    filepath = os.path.abspath(os.path.expanduser(filepath))
    if not os.path.isfile(filepath):
        raise IQAParserError('File %s does not exist' %(filepath))
    
    filecontents = ''
    try:
        filecontents = open(filepath, 'rt').read()
    except OSError, ose:
        raise IQAParserError('Error reading file %s: %s' %(filepath, str(ose)))

    return Parse(filecontents)


def Parse(content):
    """
    parses filecontents as an xml string and tries to return an instance of MontrealIQADay
    can raise IQAParserError
    """
    
    if not isinstance(content, str):
        raise IQAParserError('content is not a string')

    doc = lxml.etree.XML(content)
    
    dayNode = None
    for node in doc:
        if node.tag == 'journee':
            dayNode = node

    if dayNode is None:
        raise IQAParserError('not journee node found')

    day = dayNode.get('jour')
    month = dayNode.get('mois')
    year = dayNode.get('annee')
    
    result = MontrealIQADay(day, month, year)
    stations = []
    for node in dayNode:
        if node.tag == 'station':
            station = ParseStation(node)
            if station is not None:
                stations.append(station)

    result.stations = stations
    return result


def ParseStation(stationnode):
    id = stationnode.get('id')
    if id is None:
        return None

    data = stationnode.get('donnees')
    if data != 'oui':
        log.warning('Station node has no data')
        return None

    samples = []
    for subnode in stationnode:
        
