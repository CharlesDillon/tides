#! /usr/bin/env python3

"""
tide -- go through the tides on weekly iteration and print whether or not the level is above some particular level for a specific noaa station.  station is Redwood City, 9414523 and datum is MLLW, with the levels in feet.  
"""
# station info
# https://tidesandcurrents.noaa.gov/stationhome.html?id=9414523
# api info
# https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date=20190703&end_date=20190704&datum=MLLW&station=9414523&time_zone=lst_ldt&units=english&interval=hilo&format=json
# api documentation: https://tidesandcurrents.noaa.gov/api/
# noaa Tide Predictions 
# https://tidesandcurrents.noaa.gov/noaatidepredictions.html?id=9414523&units=standard&bdate=20230226&edate=20230226&timezone=LST/LDT&clock=12hour&datum=MLLW&interval=hilo&action=dailychart&thresholdvalue=1.5&threshold=lessThan


import json
import urllib.request
from datetime import datetime
from datetime import timedelta
from datetime import time 

import logging
import argparse

# logging.basicConfig(level=logging.DEBUG)
#logging.debug('The log message')
#likewise .info .warn .error .critical
# logging.disable(logging.CRITICAL)

# move to appropiet spot and uncomment if necessary
# import pdb; pdb.set_trace()
# type help

parser = argparse.ArgumentParser(
        description="check the tides weekly between a start and end date, \
        and between a start and end time, to make sure that the tides are \
        above the required level.",
        epilog="Do not take this, or any piece of software as authoratative\
        over good sense in boating.")

parser.add_argument(
        'beginDate',
        help='Beginning date to start checking tides. YYYY-MM-DD',
        type=lambda s: datetime.strptime(s, '%Y-%m-%d'),
)
parser.add_argument(
        'endDate',
        help='Final date to check the height of the tides. YYYY-MM-DD',
        type=lambda s: datetime.strptime(s, '%Y-%m-%d'),
)
parser.add_argument(
        'startTime',
        help='Beginning of time window to check check the tides. HH:MM \
        e.g.: 10:15 AM would be 10:15',
        type=lambda s: datetime.strptime(s, '%H:%M').time(),
)
parser.add_argument(
        'endTime',
        help='End of time window to check check the tides. HH:MM \
        e.g.: 2.30 PM would be 14:30',
        type=lambda s: datetime.strptime(s, '%H:%M').time(),
)
#parser.add_argument('date', type=datetime.date.fromisoformat) supported in 3.7

parser.add_argument(
        '-m', '--minimum',
        help='minimum tide height necessary for good boating practice.  In feet.\
        default is 1.5',
        default=1.5,
        type=float)

# station = "9414523" # Redwoodcity
parser.add_argument(
        '--station',
        help='NOAA measuring station, e.g.: Redwood City is 9414523\
         default is 9414523.',
        default="9414523", type=str)

parser.add_argument(
        '-s', '--suppress',
        help='Do not show the times the tide is below the minimum required for practice',
        action='store_true')

parser.add_argument(
    '-d', '--debug',
    help="Print lots of debugging statements",
    action="store_const", dest="loglevel", const=logging.DEBUG,
    default=logging.WARNING,
)
parser.add_argument(
    '-v', '--verbose',
    help="Be verbose",
    action="store_const", dest="loglevel", const=logging.INFO,
)

args = parser.parse_args()

logging.basicConfig(level=args.loglevel)

# print(args.beginDate, args.endDate, args.startTime, args.endTime) # prints datetime.datetime object
# print(args.minimum, args.station)

# --verbose -v
# logging.info('info message')
# --debug -d
# logging.warning('warning message')
# logging.error('error message')
# logging.critical('critical message')

practiceStart = args.startTime
practiceEnd = args.endTime

seasonStart = args.beginDate
seasonEnd = args.endDate

# minimumPracticeHeight = 1.5
aWeek = timedelta(days=7)
currentDay = seasonStart
# station = "9414523" # Redwoodcity

minimumPracticeHeight = args.minimum
station = args.station

while currentDay <= seasonEnd:

    # datetime.strptime(ted,'%Y-%m-%d %H:%M')
    # tideurl = ("https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date=%s&end_date=%s&datum=MLLW&station=%s&time_zone=lst_ldt&units=english&format=json" % ('{0:%Y%m%d}'.format(currentDay),'{0:%Y%m%d}'.format(currentDay),station))
    tideurl = ("https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date=%s&range=%s&datum=MLLW&station=%s&time_zone=lst_ldt&units=english&format=json" % ('{0:%Y%m%d}'.format(currentDay), practiceEnd.hour+1, station))
    response = urllib.request.urlopen(tideurl)
    tidejson = response.read().decode('utf-8')
    tides = json.loads(tidejson)
    tideevents = tides['predictions']
    
    previousNotChecked = True
    tidesGoodForPractice = True
    print("Tide predictions for %s" % '{0:%A %B %d %Y}'.format(currentDay) ) 
    for event in tideevents:
        eventTime=datetime.strptime(event['t'],'%Y-%m-%d %H:%M').time()
        eventHeight = float(event['v'])
        if eventTime > practiceEnd:
            break
            # and no more should be parsed from the list
         
        if eventTime > practiceStart:
            #compare previous and flag if too low
            if previousNotChecked:
                if previousEventHeight <= minimumPracticeHeight:
                    logging.info("INSUFFICIENT tide %s at level %f" % (previousEventTime, previousEventHeight))
                    tidesGoodForPractice = False
                    if not args.suppress:
                        print("INSUFFICIENT tide %s at level %f" % (previousEventTime, previousEventHeight))
                else:
                    logging.info("tide good %s at level %f" % (previousEventTime, previousEventHeight))
                previousNotChecked = False

            if eventHeight <= minimumPracticeHeight:
                logging.info("INSUFFICIENT tide %s at level %f" % (eventTime, eventHeight))
                tidesGoodForPractice = False
                if not args.suppress:
                        print("INSUFFICIENT tide %s at level %f" % (eventTime, eventHeight))
            else:
                logging.info("tide good %s at level %f" % (eventTime, eventHeight))
    
        if eventTime < practiceStart: 
            previousEventTime = eventTime
            previousEventHeight = eventHeight
            continue

    if tidesGoodForPractice:
        print('Tide is sufficiently high for this date.')        
    else:
        print('tides are INSUFFICIENT for this date at some or all of time specified.')
        lowTideDate = '{0:%Y%m%d}'.format(currentDay)
        print ("Please check\nhttps://tidesandcurrents.noaa.gov/noaatidepredictions.html?id=%s&units=standard&bdate=%s&edate=%s&timezone=LST/LDT&clock=12hour&datum=MLLW&interval=hilo&action=dailychart&thresholdvalue=%f&threshold=lessThan" % ( station, lowTideDate, lowTideDate, minimumPracticeHeight ))
    
    currentDay += aWeek 
    print(" ")



