# Generate NRF Calendar Data

*National Retail Federation* uses special [4-5-4calendar](https://nrf.com/resources/4-5-4-calendar) for consistent revenue reporting acrosss all retailers. 
The tool here is aimed at generating the mapping from Gregorian Calendar to NRF Calendar.

##Solution Approach##
 Start with Jan 30, 2000 as the Retail Epoch. And generate the 4-5-4 calendar output as per NRF rules.
 Uses custom python module and a python notebook to generate the output.

##Code##
 * [Python Class Library for NRF Calendar](NRFCalendar.py)
 * [Python Notebook to use the Class Library](generateNRFCalendar.ipynb)

The code has more in-line documentation.

##Data Files##
 * [NRF 4-5-4 Calendar for 2001](nrfCalendar2001.csv)
 * [NRF 4-5-4 Calendar for 2000-2021](nrfCalendar2021.csv)

###Wish List###
 * Experience
  * Provide start and end range for generation of calendar
  * Better visual representation of the generated calendar. 

##Contributors##
Murali Krishnan

