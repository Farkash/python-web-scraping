# Association of Gospel Rescue Missions (AGRM)
# Scraping process required for this site:
# Base URL: http://www.agrm.org//agrm/Locate_a_Mission.asp
# Loop through each state, submitting a search for each.
# For each organization returned from the search, capture the link and navigate to the organization's page.
# From each org's page, gather the following data:

# Rescue Mission Name
# Street Address
# City
# State
# Zip Code
# Phone Number
# Website URL
# Email Address
# Services Provided

import urllib2
from bs4 import BeautifulSoup
import pandas
import requests

base_url = "http://www.agrm.org//agrm/Locate_a_Mission.asp"

# cannot navigate to each state's page in this site, because the URL structure 
# does not use explicit URLs. So, I have to use request to submit a search
# to return the results for each state. 
# So, use request to grab the returned content, then save it to a variable and parse it as usual

# example https://stackoverflow.com/questions/17509607/submitting-to-a-web-form-using-python

data= {
    'q': '[python]'
    }
# r = requests.get('http://stackoverflow.com', params=data)
r = requests.post('https://stackoverflow.com/search', data=data)

print r.text


