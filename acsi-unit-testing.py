from bs4 import BeautifulSoup
import pandas
import requests
import timeit
from time import sleep
import random

base_url = 'https://www.acsi.org'
post_url = 'https://www.acsi.org/member-search/searchresults/SubmitResult'
hackish_post_url = 'https://www.acsi.org/member-search/searchresults/SubmitResult?startRow=0&rowsPerPage=3000'

def get_school_name(soup_object):
    print("List of schools for this get response:")
    school_name = []
    school_list = soup_object.findAll("a", id="Details_item.cst_key")
    for i in range(0, len(school_list)):
        school_name.append(school_list[i].text.encode('utf-8'))
        print(school_list[i].text.encode('utf-8'))


# This one pulls the actual URL from the HREF attribute of the link object
def get_school_page_url(soup_object):
    print("List of school urls for this get response:")
    school_page_url = []
    curr_st_school_page_url = []
    school_urls = soup_object.findAll("a", id="Details_item.cst_key")
    for i in range(0, len(school_urls)):
        school_page_url.append(base_url + school_urls[i]['href'])
        curr_st_school_page_url.append(school_urls[i]['href'])
        print(school_urls[i]['href'])

def find_schools(post_url):
    s = requests.Session()
    url = post_url
    x = 0
    # while True:
    while x < 3:
        # pull all the data from url
        print(url)
        response = s.get(url)
        print(response)
        response_content = response.content
        soup = BeautifulSoup(response_content, "lxml")
        get_school_name(soup)
        get_school_page_url(soup)
        # find next button url and overwrite url var
        next_page_anchor = soup.find("a", class_="pagerNext pager-next-button")
        if next_page_anchor is None:
            break
        else:
            url = next_page_anchor['href']
            sleep(random.randint(1, 20))
            x = x + 1

find_schools(post_url)

