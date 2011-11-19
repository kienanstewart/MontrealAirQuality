import csv
import datetime

from fabric.api import task

from airquality.fetcher import fetch_for

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
