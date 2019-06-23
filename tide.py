#! /usr/bin/env python3

"""
tide -- go through the tides on weekly iteration and print whether or not the level is above some particular level for a specific noaa station.  station is Redwood City, 9414523 and datum is MLLW, with the levels in feet.  
"""

# https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date=20190703&end_date=20190704&datum=MLLW&station=9414523&time_zone=lst_ldt&units=english&interval=hilo&format=json
# api documentation: https://tidesandcurrents.noaa.gov/api/

import json
import urllib.request
from datetime import datetime
from datetime import timedelta
from datetime import time 

import logging
logging.basicConfig(level=logging.DEBUG)
#logging.debug('The log message')
#likewise .info .warn .error .critical
logging.disable(logging.CRITICAL)

# move to appropiet spot and uncomment if necessary
# import pdb; pdb.set_trace()
# type help

pst = "8:45" # Time the boat should be ready to leave the doc.  Keep in mind, 9:30 should be a reasonable time to start a practice
#pst = "18:15" # Time the boat should be ready to leave the doc.  Keep in mind, 9:30 should be a reasonable time to start a practice
eop = "11:00"   #end of practice, time for lunch
#eop = "20:00"   #end of practice, time for lunch
practiceStart = datetime.strptime(pst, '%H:%M').time()
practiceEnd = datetime.strptime(eop, '%H:%M').time()

#ssd = "2/17/2019"
ssd = "6/23/2019"
sadSadDay = "6/30/2019"
seasonStart = datetime.strptime(ssd,'%m/%d/%Y')
seasonEnd = datetime.strptime(sadSadDay,'%m/%d/%Y')

minimumPracticeHeight = 1.5
aWeek = timedelta(days=7)
currentDay = seasonStart
station = "9414523" # Redwoodcity

while currentDay <= seasonEnd:

    # datetime.strptime(ted,'%Y-%m-%d %H:%M')
    # tideurl = ("https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date=%s&end_date=%s&datum=MLLW&station=%s&time_zone=lst_ldt&units=english&format=json" % ('{0:%Y%m%d}'.format(currentDay),'{0:%Y%m%d}'.format(currentDay),station))
    tideurl = ("https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date=%s&range=%s&datum=MLLW&station=%s&time_zone=lst_ldt&units=english&format=json" % ('{0:%Y%m%d}'.format(currentDay), practiceEnd.hour+1, station))
    response = urllib.request.urlopen(tideurl)
    tidejson = response.read().decode('utf-8')
    tides = json.loads(tidejson)
    tideevents = tides['predictions']
    
    previousNotChecked = True
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
                    print("INSUFFICENT tide %s at level %f" % (previousEventTime, previousEventHeight))
                else:
                    print("tide good %s at level %f" % (previousEventTime, previousEventHeight))
                previousNotChecked = False

            if eventHeight <= minimumPracticeHeight:
                print("INSUFFICENT tide %s at level %f" % (eventTime, eventHeight))
            else:
                print("tide good %s at level %f" % (eventTime, eventHeight))
    
        if eventTime < practiceStart: 
            previousEventTime = eventTime
            previousEventHeight = eventHeight
            continue

    currentDay += aWeek 
    print(" ")



