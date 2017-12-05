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
import timeit
from time import sleep
import random
import os

base_url = 'http://www.agrm.org//agrm/Locate_a_Mission.asp'
# post_url = 'http://www.agrm.org/assnfe/CompanyDirectory.asp'
# country_dict = {'clCD_CountryID':181}
# first_page = s.post(post_url, country_dict)

first_page = BeautifulSoup(open("/Users/Steve/Dropbox/programming/Python/web-scraping/AGRM/agrm-first-200.html"))
second_page = BeautifulSoup(open("/Users/Steve/Dropbox/programming/Python/web-scraping/AGRM/agrm-rest.html"))
page_list = [first_page, second_page]

scrape_start_time = timeit.default_timer()

org = []
street_address = []
city = []
state = []
zip_code = []
phone = []
website = []
email_address = []
agrm_page_url = []

# pull first chunks of data, including urls for each organization's page where more data can be found
for i in range(0, len(page_list)):
    table = page_list[i].find("table")
    rows = table.findAll('tr')
    for j in range(2, len(rows)):
        name = rows[j].find('td', class_="MDSNameTD").text
        org.append(name)
        print name
        page_url = 'http://www.agrm.org/assnfe/' + rows[j].find('td', class_="MDSNameTD").a['href']
        agrm_page_url.append(page_url)
        print page_url
        v_city = rows[j].find('td', class_="MDSCityTD").text
        city.append(v_city)
        print v_city
        v_state = rows[j].find('td', class_="MDSStateTypeTD").text
        state.append(v_state)
        print v_state
        v_phone = rows[j].find('td', class_="MDSPhoneTD").text
        phone.append(v_phone)
        print v_phone
        
# now pull data from each organization's page
# make an html file for every org's page just to be safe
s = requests.Session() 
for k in range(0, len(agrm_page_url)):
    org_response = s.get(agrm_page_url[k])
    # save entire HTML doc to file in case I get blocked by the server with subsequent requests
    raw_html = org_response.content
    file = open("/Users/Steve/Desktop/agrm-pages/%s.html" %org[k], "w")
    file.write(raw_html)
    file.close()
    sleep(random.randint(5, 20))
        
        
# create list of html files to parse through
org_site_list = os.listdir("/Users/Steve/Desktop/agrm-pages/)
for p in range(0, len(org_site_list)):
    org_soup = BeautifulSoup(open(org_site_list[p]))
    div_address = org_soup.find('div', class_='CoAddress').p
    ugly_addr_list = div_address.text.strip().split('\n')
    pretty_addr_list = [x.strip() for x in ugly_addr_list if x.strip() != '']
    v_street = pretty_addr_list[0]
    street_address.append(v_street)
    print v_street
    # v_city = pretty_addr_list[1].split(',')[0]
    # city.append(v_city)
    # print v_city
    # v_state = pretty_addr_list[1].split(' ')[1]
    # state.append(v_state)
    # print v_state
    v_zip = pretty_addr_list[1].split(' ')[2]    
    zip_code.append(z_vip)
    print v_zip
    # website
    div_contact = org_soup.find('div', class_='contact').p
    ugly_contact_list = div_contact.text.strip().split('\n')
    pretty_contact_list = [x.replace(u'\xa0', u'').strip() for x in ugly_contact_list if x.strip() != '']
    v_website = pretty_contact_list[1][pretty_contact_list[i].find(':') +1 :].strip().encode('utf-8')   
    website.append(v_website)
    print v_website
    # email_address
    v_email = pretty_contact_list[4][pretty_contact_list[4].find(':') +1 :].strip().encode('utf-8')
    email_address.append(v_email)
    print v_email

# write data to frame
master_frame = pandas.DataFrame()
master_frame["Organization"] = org
master_frame["Street Address"] = street_address
master_frame["City"] = city
master_frame["State"] = state
master_frame["Zip Code"] = zip_code
master_frame["Phone Number"] = phone
master_frame["Website"] = website
master_frame["Email Address"] = email_address

print master_frame.head(5)

# write frame to file
master_frame.to_csv("/Users/Steve/Dropbox/programming/Python/web-scraping/data/agrm.csv", encoding='utf-8', index=False)   
    
    

    
    
    
########################### TESTING ############
    
test_org_page = BeautifulSoup(open("/Users/Steve/Dropbox/programming/Python/web-scraping/AGRM/test_org_page.html"))
div_address = test_org_page.find('div', class_='CoAddress').p

test = div_address.text.strip().split('\n')
clean = [x.strip() for x in test if x.strip() != '']
clean[0]
clean[1].split(',')[0]
clean[1].split(' ')[1]
clean[1].split(' ')[2]


div_contact = test_org_page.find('div', class_='contact').p
ugly_contact_list = div_contact.text.strip().split('\n')
pretty_contact_list = [x.replace(u'\xa0', u'').strip() for x in ugly_contact_list if x.strip() != '']
v_website = pretty_contact_list[1][pretty_contact_list[i].find(':') +1 :].strip().encode('utf-8')

v_email = pretty_contact_list[4][pretty_contact_list[4].find(':') +1 :].strip().encode('utf-8')


scrape_time_elapsed = timeit.default_timer() - scrape_start_time    
print "Scrape time elapsed: %d" %scrape_time_elapsed




######################### detail test
page = requests.get('http://www.agrm.org/assnfe/CompanyDirectory.asp?MODE=VIEW&SEARCH_TYPE=13&ID=100025')
org_name = "The Foundry Ministries"

raw_html = page.content
file = open("/Users/Steve/Desktop/%s.html" %org_name, "w")
file.write(raw_html)
file.close()
org_soup = BeautifulSoup(raw_html)
div_address = org_soup.find('div', class_='CoAddress').p
ugly_addr_list = div_address.text.strip().split('\n')
pretty_addr_list = [x.strip() for x in ugly_addr_list if x.strip() != '']
v_street = pretty_addr_list[0]
street_address.append(v_street)
print v_street
# v_city = pretty_addr_list[1].split(',')[0]
# city.append(v_city)
# print v_city
# v_state = pretty_addr_list[1].split(' ')[1]
# state.append(v_state)
# print v_state
v_zip = pretty_addr_list[1].split(' ')[2]    
zip_code.append(v_zip)
print v_zip
# website
div_contact = org_soup.find('div', class_='contact').p
ugly_contact_list = div_contact.text.strip().split('\n')
pretty_contact_list = [x.replace(u'\xa0', u'').strip() for x in ugly_contact_list if x.strip() != '']
v_website = pretty_contact_list[1][pretty_contact_list[i].find(':') +1 :].strip()   
website.append(v_website)
print v_website
# email_address
v_email = pretty_contact_list[4][pretty_contact_list[4].find(':') +1 :].strip()
email_address.append(v_email)
print v_email




