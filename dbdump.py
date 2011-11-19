#!/usr/bin/python

# Built-ins
import datetime
import logging
import optparse
import os
import sys
import sqlite3

# Local
import airquality.fetcher as fetcher

# Vars
log = logging.info(__name__)

pollutantToColumn = {
    'no2' : 'no2',
    'pm' : 'pm2_5f',
    'so2' : 'so2',
    'co' : 'co',
    'o3' : 'o3',
    'no' : 'no',
    'h2s' : 'h2s',
    }

def dbdump_sqlite(dbfile, tablename, days = 5, valuetranslatefunc = None):
    if not os.path.isdir(os.path.dirname(dbfile)):
        log.error('DB file %s\' directory does not exist.' %(dbfile))
        return False
    
    conn = sqlite3.connect(dbfile)
    log.info('Connected to mysql db at %s' %(dbfile))
    c = conn.cursor()
    query = 'create table if not exists %s(' \
        'id integer primary key, sampledate ts, stationid int, ' \
        'co int, h2s int, no int, no2 int, pm2_5 int, pm2_5f int, pm10 int, o3 int, so2 int );' %(tablename)              
    log.info('Executing sql query: """%s"""' %(query))
    c.execute(query)
    conn.commit()

    log.info('Starting dump for %d days' %(days))
    for n in range(days):
        today = datetime.datetime.today() - datetime.timedelta(n)
        try:
            data = fetcher.fetch_for(today)
        except Exception, e:
            log.error('Exception when parsing data for %r: %s' %(today, str(e)))
            continue
        
        for station in data.stations:
            for measure in station.measurements:
                datestamp = datetime.datetime(data.year, data.month, data.day, measure.hour)
                query = 'insert into %s ( sampledate, stationid, ' %(tablename)
                pols = ', '.join([pollutantToColumn[x.lower()] for x in measure.pollutants.keys()])
                query += pols + ') VALUES ( ?, %d, ' %(station.id)
                query += ', '.join([str(x) for x in measure.pollutants.values()])
                query += ");"
                log.info('Executing query: %s' %(query))
                c.execute(query, (datestamp,))
        conn.commit()
    c.close()
    return True

if __name__ == '__main__':
    log = logging.getLogger()
    logging.basicConfig()
    log.setLevel(logging.DEBUG)
    parser = optparse.OptionParser()
    parser.add_option('-d', '--days', action = 'store', default = None, dest = 'daycount',
                      help = 'The number of days to fetch for (working back from today)')
    parser.add_option('-f', '--file', action = 'store', default = None, dest = 'dbfile',
                      help = 'The database file for sqlite')
    parser.add_option('-t', '--table', action = 'store', default = None, dest = 'tablename',
                      help = 'The table to use in the database')
    options, args = parser.parse_args(sys.argv[1:])
    
    if options.dbfile is None:
        parser.error('-f/--file is required')
    options.dbfile = os.path.abspath(os.path.expanduser(options.dbfile))

    if options.tablename is None:
        parser.error('-t/--table is required')

    if options.daycount is not None:
        try:
            options.daycount = int(options.daycount)
        except ValueError:
            parser.error('-d/--days must be an integer')

    if options.daycount is not None:
        dbdump_sqlite(options.dbfile, options.tablename, options.daycount)
    else:
        dbdump_sqlite(options.dbfile, options.tablename)
