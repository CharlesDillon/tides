~~~
                             _______     __         
                            /_  __(_)___/ /__  _____
                             / / / / __  / _ \/ ___/
                            / / / / /_/ /  __(__  ) 
                           /_/ /_/\__,_/\___/____/       Brought to you by Lightwave.  And NOAA.  
~~~
# Tides
Scrape the noaa website for tidal hieght and times on a weekly basis to ensure there is enough water for practice.  

Times are in 24 hour format, and height is in feet.  Datum is MLLW.  Both the station and the minimum height are parameters, with defaults set for our location and sport.  

~~~
Foundling:src/tides % ./tide.py -h
usage: tide.py [-h] [-m MINIMUM] [--station STATION] [-s] [-d] [-v]
               beginDate endDate startTime endTime

check the tides weekly between a start and end date, and between a start and
end time, to make sure that the tides are above the required level.

positional arguments:
  beginDate             Beginning date to start checking tides. YYYY-MM-DD
  endDate               Final date to check the height of the tides. YYYY-MM-
                        DD
  startTime             Beginning of time window to check check the tides.
                        HH:MM e.g.: 10:15 AM would be 10:15
  endTime               End of time window to check check the tides. HH:MM
                        e.g.: 2.30 PM would be 14:30

optional arguments:
  -h, --help            show this help message and exit
  -m MINIMUM, --minimum MINIMUM
                        minimum tide height necessary for good boating
                        practice. In feet. default is 1.5
  --station STATION     NOAA measuring station, e.g.: Redwood City is 9414523
                        default is 9414523.
  -s, --suppress        Do not show the times the tide is below the minimum
                        required for practice
  -d, --debug           Print lots of debugging statements
  -v, --verbose         Be verbose

Do not take this, or any piece of software as authoratative over good sense in
boating.
~~~

NOAA resources:
<dl>
<dt>station info
<dd>https://tidesandcurrents.noaa.gov/stationhome.html?id=9414523
<dt>api info
<dd>https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date=20190703&end_date=20190704&datum=MLLW&station=9414523&time_zone=lst_ldt&units=english&interval=hilo&format=json
<dt>api documentation: 
<dd>https://tidesandcurrents.noaa.gov/api/
<dt>noaa Tide Predictions 
<dd>https://tidesandcurrents.noaa.gov/noaatidepredictions.html?id=9414523&units=standard&bdate=20230226&edate=20230226&timezone=LST/LDT&clock=12hour&datum=MLLW&interval=hilo&action=dailychart&thresholdvalue=1.5&threshold=lessThan
</dl>

