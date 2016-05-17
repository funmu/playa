#!/usr/bin/python

# ------------------------------------------------------------------------------------------------
#
#  Module for genearting NRF Calendar
#
#  Author: Murali Krishnan
#  Date: May 2016
#

import datetime;
import csv;
    
class NRFCalendarDay:
    Retail454dayofweek = 1;
    Retail454dayofmonth = 1;
    Retail454month = 1;
    Retail454weekofmonth = 1;
    Retail454weeksinmonth = 4; 
    Retail454weekofyear  = 1;
    Retail454quarter = 1;
    Retail454year = 2000;
    
    def __init__( self):
        print "Initialized NRF Calendar Day";

    def Clone( self):
        cloneFrom = self;
        newNRFC = NRFCalendarDay();
        newNRFC.Retail454dayofweek = cloneFrom.Retail454dayofweek;
        newNRFC.Retail454dayofmonth = cloneFrom.Retail454dayofmonth;
        newNRFC.Retail454month = cloneFrom.Retail454month;
        newNRFC.Retail454weekofmonth = cloneFrom.Retail454weekofmonth;
        newNRFC.Retail454weeksinmonth = cloneFrom.Retail454weeksinmonth; 
        newNRFC.Retail454weekofyear  = cloneFrom.Retail454weekofyear;
        newNRFC.Retail454year = cloneFrom.Retail454year;
        newNRFC.Retail454quarter = cloneFrom.Retail454quarter;
        return newNRFC;


    #  calculate number of weeks in 454 month
    def NumWeeksInMonth( self, givenMonth):
        numWeeks = 4;
        if ( ( self.Retail454month == 2) or ( self.Retail454month == 5) or ( self.Retail454month == 8) or ( self.Retail454month == 11)):
            numWeeks = 5;
        elif ( self.Retail454month == 12) :
            if ( givenMonth == 12):
                numWeeks = 5;

        return numWeeks;

    #  calculate Week of Year given other data
    def calcWeekOfYear( self):
        weekOfYear = self.Retail454weekofyear;
        # check if there is a rollover. if so, reset week of year.
        # ToDo: How do i distinguish between years with 52 weeks and 53 weeks?
        if ( self.Retail454dayofweek == 1):
            weekOfYear = self.Retail454weekofyear + 1;
            if ((self.Retail454month == 1) and (self.Retail454weekofyear >= 50)):
                weekOfYear = 1;

        return weekOfYear;


    def IncrementRetail454( self, givenMonth):
        # NRFCalendarDay newDay = NRFCalendarDay;

        # 1. Calculate the day of the week
        self.Retail454dayofweek = (self.Retail454dayofweek % 7) + 1;

        # 2. Calculate day of the month
        if ( ( self.Retail454weeksinmonth == 4) and (self.Retail454dayofmonth == 28) or ( self.Retail454weeksinmonth == 5) and (self.Retail454dayofmonth == 35)):
            # roll forward the month
            self.Retail454month = ((self.Retail454month % 12) + 1);
            self.Retail454dayofmonth = 1;
        else:
            self.Retail454dayofmonth += 1;

        # 3. set the week of month number
        if (self.Retail454dayofweek == 1):
            if (self.Retail454weekofmonth == self.Retail454weeksinmonth):
                # reset the week to be the starting week of a month
                self.Retail454weekofmonth = 1;
            else:
                # roll forward the week to next week
                self.Retail454weekofmonth += 1;

        # 4. Calculate number of weeks in month if it is a new month
        if ( self.Retail454dayofmonth == 1):
            self.Retail454weeksinmonth = self.NumWeeksInMonth( givenMonth);
            self.Retail454quarter = self.Retail454month / 3 + 1;

        # 5. Calculate week of year and udpate accordingly
        self.Retail454weekofyear = self.calcWeekOfYear();

        # 6. Update year only if there is a roll over. 
        #   i.e. only if day == 1 and week of year == 1;
        if ((self.Retail454dayofweek == 1) and (self.Retail454weekofyear == 1)):
            self.Retail454year += 1;

        return self;

    def Print(self):
        formatString = "Retail Day of Week: {0}, Day Of Month {1}, Month {2}, Week Of Month {3}, Weeks In Month {4}, Week Of Year {5}, Quarter {6}, Year {7}";
        print formatString.format( self.Retail454dayofweek, self.Retail454dayofmonth, self.Retail454month, self.Retail454weekofmonth, self.Retail454weeksinmonth, self.Retail454weekofyear, self.Retail454quarter, self.Retail454year);

# - local helper function
def writeCalendarForDate( csvWriter, dtCur, rc):
    rowToWrite = [  dtCur.year, dtCur.month, dtCur.day, 
                    rc.Retail454dayofweek, rc.Retail454dayofmonth, rc.Retail454month, 
                    rc.Retail454weekofmonth, rc.Retail454weeksinmonth, 
                    rc.Retail454weekofyear, rc.Retail454quarter, rc.Retail454year];
    csvWriter.writerow( rowToWrite);


class NRFGenerator:
    retailEpocStart = None;
    outputFormat = [ "GregorianYear", "GregorianMonth", "GregorianDay",
                    "Retail454dayofweek", "Retail454dayofmonth", "Retail454month",
                    "Retail454weekofmonth", "Retail454weeksinmonth", 
                    "Retail454weekofyear", "Retail454quarter", "Retail454year" ];

    def __init__(self):
        self.retailEpocStart = datetime.datetime( 2000, 1, 30);
        print "Initialized NRF Generator";

    def NumDaysFromRetailEpoch( self, dtStart):
        tdStart = dtStart - self.retailEpocStart; # gives the time delta between the new start date and epoch
        print "Number of days from epoch for start date: {0}".format( tdStart.days);
        return tdStart.days;

    def RunTillNumDays( self, dtFrom, dtTill, nrfCalendarDay, csvWriter):
        tdStart = dtTill - dtFrom; # gives the time delta between the new start date and epoch
        numDaysTill = tdStart.days;
        dtIter = dtFrom;
        r = nrfCalendarDay;
        if ( csvWriter != None):
            writeCalendarForDate( csvWriter, dtIter, r);

        for i in range(0, numDaysTill):
            dtIter = dtIter + datetime.timedelta( days = 1);
            if ( i %100 == 0):
                print " ... Iterating for date: {0}".format( dtIter);
            r = r.IncrementRetail454( dtIter.month);
            if ( csvWriter != None):
                writeCalendarForDate( csvWriter, dtIter, r);
        return r;

    def SetupStartDatesTill( self, dtStart, csvWriter):
        numDaysFromEpoch = self.NumDaysFromRetailEpoch( dtStart);

        # setup a dictionary with Gregorian Calendar Year # and equivalent Retail454CalendarDay
        dictForYearStart = {}; # dict.fromkeys( range( 2000, dtStart.year + 1));
        yearsList = range( 2001, dtStart.year + 1);

        dtFrom = self.retailEpocStart;
        nrfcFrom = NRFCalendarDay();

        if (csvWriter != None):
            csvWriter.writerow( self.outputFormat);

        for i in yearsList:

            dtNextYear = datetime.datetime( i, 1, 1);
            nrfCalendarForNextYear = self.RunTillNumDays( dtFrom, dtNextYear, nrfcFrom, csvWriter);
            dictForYearStart[ dtNextYear] = nrfCalendarForNextYear;

            dtFrom = dtNextYear;
            nrfcFrom = nrfCalendarForNextYear.Clone();
        return dictForYearStart;


    def Print( self):
        print "NRF Generator Ready to go. Epoch Set to: {0}".format( self.retailEpocStart);


# -------------- TESTING CODE
def GenerateNRFCalendarTill( tillYear, csvOutputFile):
    csvWriter = None;
    outputFileHandle  = None;
    ng = NRFGenerator();
    ng.Print();

    if (csvOutputFile != None):
        outputFileHandle = open( csvOutputFile, "wb");
        csvWriter = csv.writer( outputFileHandle, delimiter=',');

    dy = ng.SetupStartDatesTill( datetime.datetime( tillYear, 1, 1), csvWriter);

    print "\n\nFinished generating the Retail Calendar. Writing summary output."
    keys = sorted(dy.keys());
    vals = dy.values();
    for k in keys:
        print "\nFor Date: {0}".format(k);
        dy[k].Print();

    if (outputFileHandle != None):
        outputFileHandle.close();

# TEST with 
# TestGeneration(2001, None);
# TestGeneration(2003, "test2003.csv");
# TestGeneration(2018);
