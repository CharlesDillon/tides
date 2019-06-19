#! /usr/bin/env python3

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

tidejson = """
{ "predictions" : [ {"t":"2019-01-29 00:00", "v":"2.728"},{"t":"2019-01-29 01:00", "v":"2.402"},{"t":"2019-01-29 02:00", "v":"2.812"},{"t":"2019-01-29 03:00", "v":"3.883"},{"t":"2019-01-29 04:00", "v":"5.279"},{"t":"2019-01-29 05:00", "v":"6.672"},{"t":"2019-01-29 06:00", "v":"7.804"},{"t":"2019-01-29 07:00", "v":"8.399"},{"t":"2019-01-29 08:00", "v":"8.228"},{"t":"2019-01-29 09:00", "v":"7.328"},{"t":"2019-01-29 10:00", "v":"5.971"},{"t":"2019-01-29 11:00", "v":"4.419"},{"t":"2019-01-29 12:00", "v":"2.849"},{"t":"2019-01-29 13:00", "v":"1.517"},{"t":"2019-01-29 14:00", "v":"0.764"},{"t":"2019-01-29 15:00", "v":"0.779"},{"t":"2019-01-29 16:00", "v":"1.464"},{"t":"2019-01-29 17:00", "v":"2.602"},{"t":"2019-01-29 18:00", "v":"3.977"},{"t":"2019-01-29 19:00", "v":"5.284"},{"t":"2019-01-29 20:00", "v":"6.128"},{"t":"2019-01-29 21:00", "v":"6.270"},{"t":"2019-01-29 22:00", "v":"5.798"},{"t":"2019-01-29 23:00", "v":"4.964"},{"t":"2019-01-30 00:00", "v":"3.996"},{"t":"2019-01-30 01:00", "v":"3.156"},{"t":"2019-01-30 02:00", "v":"2.801"},{"t":"2019-01-30 03:00", "v":"3.181"},{"t":"2019-01-30 04:00", "v":"4.208"},{"t":"2019-01-30 05:00", "v":"5.553"},{"t":"2019-01-30 06:00", "v":"6.895"},{"t":"2019-01-30 07:00", "v":"7.962"},{"t":"2019-01-30 08:00", "v":"8.455"},{"t":"2019-01-30 09:00", "v":"8.167"},{"t":"2019-01-30 10:00", "v":"7.176"},{"t":"2019-01-30 11:00", "v":"5.758"},{"t":"2019-01-30 12:00", "v":"4.140"},{"t":"2019-01-30 13:00", "v":"2.486"},{"t":"2019-01-30 14:00", "v":"1.082"},{"t":"2019-01-30 15:00", "v":"0.299"},{"t":"2019-01-30 16:00", "v":"0.329"},{"t":"2019-01-30 17:00", "v":"1.082"},{"t":"2019-01-30 18:00", "v":"2.353"},{"t":"2019-01-30 19:00", "v":"3.905"},{"t":"2019-01-30 20:00", "v":"5.377"},{"t":"2019-01-30 21:00", "v":"6.335"},{"t":"2019-01-30 22:00", "v":"6.548"},{"t":"2019-01-30 23:00", "v":"6.114"} ]} """ # with be with interval=h see api doc for details

# tidejson = """
# { "predictions" : [ {"t":"2019-07-03 00:44", "v":"9.060", "type":"H"},{"t":"2019-07-03 08:09", "v":"-1.609", "type":"L"},{"t":"2019-07-03 14:57", "v":"7.295", "type":"H"},{"t":"2019-07-03 20:05", "v":"3.062", "type":"L"},{"t":"2019-07-04 01:34", "v":"9.069", "type":"H"},{"t":"2019-07-04 08:53", "v":"-1.669", "type":"L"},{"t":"2019-07-04 15:42", "v":"7.494", "type":"H"},{"t":"2019-07-04 20:56", "v":"2.911", "type":"L"} ]}
# """ #this be with interval=hilo

#pst = "9:45" # Time the boat should be ready to leave the doc.  Keep in mind, 9:30 should be a reasonable time to start a practice
pst = "17:45" # Time the boat should be ready to leave the doc.  Keep in mind, 9:30 should be a reasonable time to start a practice
#eop = "12:00"   #end of practice, time for lunch
eop = "20:00"   #end of practice, time for lunch
practiceStart = datetime.strptime(pst, '%H:%M').time()
practiceEnd = datetime.strptime(eop, '%H:%M').time()

#ssd = "2/17/2019"
ssd = "3/20/2019"
sadSadDay = "11/7/2019"
seasonStart = datetime.strptime(ssd,'%m/%d/%Y')
seasonEnd = datetime.strptime(sadSadDay,'%m/%d/%Y')
minimumPracticeHeight = 1.5
aWeek = timedelta(days=7)
currentDay = seasonStart
station = "9414523" # Redwoodcity

while currentDay <= seasonEnd:

    # datetime.strptime(ted,'%Y-%m-%d %H:%M')
    tideurl = ("https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date=%s&end_date=%s&datum=MLLW&station=%s&time_zone=lst_ldt&units=english&interval=h&format=json" % ('{0:%Y%m%d}'.format(currentDay),'{0:%Y%m%d}'.format(currentDay),station))
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



