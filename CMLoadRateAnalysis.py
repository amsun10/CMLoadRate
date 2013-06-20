#-------------------------------------------------------------------------------
# Name:        CM Load Rate Analysis
# Purpose:
#
# Author:      Zhang Xiang
#
# Created:     20/06/2013
# Copyright:   (c) Administrator 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import re
import urllib,urllib2,cookielib
import time

TIMER_INTERVAL = 15 # Set the interval that to get CMS LoadRate and save to local CSV file

DEBUG = 0

class CCMLoadRateParser:
    def __init__(self,index):
        self.cj = cookielib.LWPCookieJar()
        self.Parser = None
        self.Opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        self.RequestURL = 'http://wxgemini.eng.wux.chin.seagate.com/cgi-bin/cmLoad.py?location=wx'
        self.Index = index #index that tell us this is the how many time we parse the data

    def RequestSummary(self,):
        Summary = {}
        if DEBUG:
            f = open('Test2.html','r')
            result = f.read()
            f.close()
        else:
            request = urllib2.Request(self.RequestURL, None, {})
            result = self.Opener.open(request).read()
        self.parse(result)
        return Summary
        pass

    def parse(self,result):
        pat_0 = '<A href="[\s\S]*?" TARGET="_top">(?P<MachineName>[\s\S]*?)</A>[\s\S]*?<table border=1 width=100% cellpadding=2 bgcolor=#EEEEFF>(?P<Table><tr>[\s\S]*?)</table>'
        pat_0 = re.compile(pat_0)
        MachineSummaryList = pat_0.findall(result)

        pat_1 = '<td bgcolor=#[A-Z0-9]{6} valign=top align=right>(?P<col%s>[\s\S]*?)</td>\n' * 10 % (0,1,2,3,4,5,6,7,8,9)
        pat_1 = re.compile(pat_1)
        f = open('result.csv','a')
        for item in MachineSummaryList:
            table = pat_1.findall(item[1])
            for row in table:
                newRow = list(row)
                newRow.insert(0,item[0]) #Insert Machine Name In Every Row
                newRow.insert(0,self.Index) #Insert Machine Name In Every Row
                f.write(str(newRow)[1:-1]+'\n') #remove "[" and "]"
        f.close()
        pass

def main():
    i = 0
    while(True):
        print "The %d time Crunching Data, current time: %s " % (i,str(time.strftime('%Y-%d-%d %H:%M:%S') ))
        OCCMLoarRateParser = CCMLoadRateParser(i)
        OCCMLoarRateParser.RequestSummary()
        print "Sleep %d Mins To Start Next Data Crunch " % TIMER_INTERVAL
        time.sleep(TIMER_INTERVAL * 60)
        i += 1
    pass

if __name__ == '__main__':
    main()
