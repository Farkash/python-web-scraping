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
from natsort import natsorted

base_url = 'http://www.agrm.org//agrm/Locate_a_Mission.asp'
# post_url = 'http://www.agrm.org/assnfe/CompanyDirectory.asp'
# country_dict = {'clCD_CountryID':181}
# first_page = s.post(post_url, country_dict)

us1 = BeautifulSoup(open("/Users/Steve/Dropbox/programming/Python/web-scraping/AGRM/us1.html"))
us2 = BeautifulSoup(open("/Users/Steve/Dropbox/programming/Python/web-scraping/AGRM/us2.html"))
us3 = BeautifulSoup(open("/Users/Steve/Dropbox/programming/Python/web-scraping/AGRM/us3.html"))
us4 = BeautifulSoup(open("/Users/Steve/Dropbox/programming/Python/web-scraping/AGRM/us4.html"))
us5 = BeautifulSoup(open("/Users/Steve/Dropbox/programming/Python/web-scraping/AGRM/us5.html"))
us6 = BeautifulSoup(open("/Users/Steve/Dropbox/programming/Python/web-scraping/AGRM/us6.html"))
us7 = BeautifulSoup(open("/Users/Steve/Dropbox/programming/Python/web-scraping/AGRM/us7.html"))
us8 = BeautifulSoup(open("/Users/Steve/Dropbox/programming/Python/web-scraping/AGRM/us8.html"))
page_list = [us1, us2, us3, us4, us5, us6, us7, us8]


org = []
city = []
state = []
phone = []
agrm_page_url = []

street_address = []
zip_code = []
website = []
email_address = []


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
    file = open("/Users/Steve/Desktop/agrm-pages/%s%s%s.html" %(k, "-", org[k]), "w")
    file.write(raw_html)
    file.close()
    sleep(random.randint(1,3))

# test_frame = pandas.DataFrame()
# test_frame["name"] = org
# test_frame[""]

# create list of html files to parse through
org_site_list = []
org_site_list = os.listdir("/Users/Steve/Desktop/agrm-pages/")
org_site_list = natsorted(org_site_list)
del org_site_list[272]
for p in range(0, len(org_site_list)):
    org_soup = BeautifulSoup(open("/Users/Steve/Desktop/agrm-pages/%s" %org_site_list[p]))
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
    if(len(pretty_addr_list) > 2):
        del pretty_addr_list[1]
    pretty_addr_inter = pretty_addr_list[1].split(',')
    v_zip = pretty_addr_inter[1].strip().split(' ')[len(pretty_addr_inter[1].strip().split(' ')) -1]
    zip_code.append(v_zip)
    print v_zip
    # website
    div_contact = org_soup.find('div', class_='contact').p
    ugly_contact_list = div_contact.text.strip().split('\n')
    pretty_contact_list = [x.replace(u'\xa0', u'').strip() for x in ugly_contact_list if x.strip() != '']
    v_website = pretty_contact_list[1][pretty_contact_list[1].find(':') +1 :].strip().encode('utf-8')   
    website.append(v_website)
    print v_website
    # email_address
    v_email = pretty_contact_list[4][pretty_contact_list[4].find(':') +1 :].strip().encode('utf-8')
    email_address.append(v_email)
    print v_email












# agrm_page_url[12]

# unsafe method of querying the site directly
s = requests.Session() 
for p in range(0, len(agrm_page_url)):
    org_response = s.get(agrm_page_url[p])
    org_soup = BeautifulSoup(org_response.content, "lxml")
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
    v_website = pretty_contact_list[1][pretty_contact_list[1].find(':') +1 :].strip().encode('utf-8')   
    website.append(v_website)
    print v_website
    # email_address
    v_email = pretty_contact_list[4][pretty_contact_list[4].find(':') +1 :].strip().encode('utf-8')
    email_address.append(v_email)
    print v_email

# agrm_page_url[83]
agrm_page_url[8]


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
# bad_zip_resp = requests.get('http://www.agrm.org/assnfe/CompanyDirectory.asp?MODE=VIEW&SEARCH_TYPE=13&ID=100102')
bad_zip_resp = requests.get('http://www.agrm.org/assnfe/CompanyDirectory.asp?MODE=VIEW&SEARCH_TYPE=13&ID=115946')
bad_zip_soup = BeautifulSoup(bad_zip_resp.content, "lxml")
div_address = bad_zip_soup.find('div', class_='CoAddress').p
ugly_addr_list = div_address.text.strip().split('\n')
pretty_addr_list = [x.strip() for x in ugly_addr_list if x.strip() != '']
v_street = pretty_addr_list[0]
print v_street
# v_city = pretty_addr_list[1].split(',')[0]
# city.append(v_city)
# print v_city
# v_state = pretty_addr_list[1].split(' ')[1]
# state.append(v_state)
# print v_state
pretty_addr_inter = pretty_addr_list[1].split(',')
v_zip = pretty_addr_inter[1].strip().split(' ')[len(pretty_addr_inter[1].strip().split(' ')) -1]
print v_zip
    
len(pretty_addr_inter[1].strip().split(' '))

testset = set(org)

len(testset)    
    
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
i = 0
raw_html = page.content
file = open("/Users/Steve/Desktop/%s%s.html" %(i, org_name), "w")
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


