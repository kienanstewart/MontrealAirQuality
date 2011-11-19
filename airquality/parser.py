#!/usr/bin
"""
For parsing the xml from http://ville.montreal.qc.ca/rsqa/servlet/makeXmlActuel?date=13/11/11

quick example
<iqa><journee jour="19" mois="11" annee="2011"><station id="7" donnees="oui"><echantillon heure="0"><qualite value="7"/><polluant nom="NO2" value="4"/><polluant nom="PM" value="7"/><polluant nom="SO2" value="1"/></echantillon>
"""
import logging
import lxml.etree
import os
import unittest

log = logging.getLogger(__name__)

class MontrealIQADay(object):

    def __init__(self, day, month, year, stations = []):
        self.day = day
        self.month = month
        self.year = year
        self.stations = stations

    
    def __str__(self):
        s = repr(self)
        s += '\nDay: %d\nMonth: %d\nYear: %d\n' %(self.day, self.month, self.year)
        if self.stations:
            s += '---- Stations ----\n\t'
            s += '\n\t'.join([str(x) for x in self.stations])
        else:
            s += 'No stations'
        s += '\n'
        return s


class MontrealIQAStation(object):
    
    def __init__(self, id, name = None, measurements = []):
        self.id = id
        self.name = name
        self.measurements = measurements

    
    def __str__(self):
        s = 'Station id %s : name %s' %(self.id, self.name)
        s += '\n\t' + '\n\t'.join([str(x) for x in self.measurements])
        return s


class MontrealIQAMeasurement(object):

    def __init__(self, hour, pollutants = {}):
        self.hour = hour
        self.pollutants = pollutants # p1 : value; p2 : value
    
    
    def AddPolutant(name, value):
        self.pollutants[name] = value

    
    def __str__(self):
        s = 'Sample at hour %d: %s' %(self.hour, repr(self.pollutants))
        return s


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
    
    result = MontrealIQADay(int(day), int(month), int(year)) #this could throw ValueError
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
        log.warning('Station node has no id')
        return None

    data = stationnode.get('donnees')
    if data != 'oui':
        log.warning('Station node has no data. donnees tag contained %s != \'oui\'' %data)
        return None

    samples = []
    for samplenode in stationnode:
        sample = ParseSample(samplenode)
        if sample is not None:
            samples.append(sample)

    #Look up station name from ID???
    return MontrealIQAStation(int(id), None, samples) # this could throw ValueError


def ParseSample(samplenode):
    if samplenode.tag != 'echantillon':
        return None

    pollutants = {}
    hour = samplenode.get('heure')
    if hour is None:
        log.warning('sample node has no tag \'heure\'')
        return None

    for node in samplenode:
        if node.tag != 'polluant':
            continue
        
        pollutant = node.get('nom')
        pollutantvalue = node.get('value')
        if pollutant is not None and pollutantvalue is not None:
            pollutants[pollutant] = int(pollutantvalue) # this could throw ValueError
        else:
            log.warning('polluant node has no tag for either \'nom\' or \'value\'')

    if not pollutants:
        log.warning('no pollutants not found in sample node')
        return None

    return MontrealIQAMeasurement(int(hour), pollutants) # ValueError here


class TestParseExample(unittest.TestCase):
    
    def setUp(self):
        self.examplefilepath = os.path.join(os.path.dirname(__file__), 'test', 'example_day.xml')
        self.examplestring = ''


    def test_fromfile(self):
        d = ParseFile(self.examplefilepath)
        self.assertIsNotNone(d)
        self.assertEqual(d.day, 19)
        self.assertEqual(d.month, 11)
        self.assertEqual(d.year, 2011)
        self.assertIsNotNone(d.stations)
        print str(d)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    testcases = (TestParseExample,)
    for testcase in testcases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testcase))
    unittest.TextTestRunner(verbosity=2).run(suite)
