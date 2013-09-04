#!/usr/bin/env python
import requests
import pandas as pd
 
# IMPORTANT NOTE to get an API key, go to this website: http://co.opencampaigndata.org/keys/new
# Then place your key here instead of 'None'
API_KEY = '3KDOKC5XE46VALX'
 
# The fields we would like to include
fields = ['lastName','firstName','city','state','zip','amount']
 
# Create the query string
qstr = '&zip=80303' + '&fields='+ ','.join(str(f) for f in fields)
request_str = 'http://co.opencampaigndata.org/expenditures?apiKey='+ API_KEY + qstr 
 
print request_str
r = requests.get(request_str)
data = r.json()
pdata = pd.DataFrame(data[u'expenditures'])
 
# Grab up to the next 5 pages
for i in xrange(5):
    if data[u'meta']['next-href'] is None:
        break
    r = requests.get(data[u'meta']['next-href'])
    data = r.json()
    temp = pd.DataFrame(data[u'expenditures'])
    pdata = pd.concat([pdata,temp])
 
print 'There are {numrows} rows in the dataset.'.format(numrows=len(pdata))
 
#example
print pdata.groupby('lastName')['amount'].sum().order()
