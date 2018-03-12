from bs4 import BeautifulSoup
import pandas
import requests
import timeit
from time import sleep
import random

base_url = 'https://www.acsi.org'
post_url = 'https://www.acsi.org/member-search/searchresults/SubmitResult?startRow=0&rowsPerPage=3000'

school_name = []
school_page_url = []

def get_school_name(soup_object):
    print("List of schools for this get response:")
    school_list = soup_object.findAll("a", id="Details_item.cst_key")
    for i in range(0, len(school_list)):
        school_name.append(school_list[i].text)
        print(school_list[i].text.encode('utf-8'))


# This one pulls the actual URL from the HREF attribute of the link object
def get_school_page_url(soup_object):
    print("List of school urls for this get response:")
    curr_st_school_page_url = []
    school_urls = soup_object.findAll("a", id="Details_item.cst_key")
    for i in range(0, len(school_urls)):
        school_page_url.append(base_url + school_urls[i]['href'])
        curr_st_school_page_url.append(school_urls[i]['href'])
        print(school_urls[i]['href'])

def find_schools(post_url):
    s = requests.Session()
    response = s.get(post_url)
    response_content = response.content
    soup = BeautifulSoup(response_content, "lxml")
    get_school_name(soup)
    get_school_page_url(soup)
    school_frame = pandas.DataFrame()
    school_frame['school_name'] = school_name
    school_frame['school_page_url'] = school_page_url
    school_frame.to_csv("/Users/Steve/Dropbox/programming/Python/web-scraping/data/acsi_schools.csv", encoding='utf-8', index=False)   
    

find_schools(post_url)

