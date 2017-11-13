# Association of Christian Schools International (ACSI)
# https://www.acsi.org/
# this site requires the submission of forms and capture of the search results. 
# Cannot use explicit URLs to navigate. Furthermore, result sets are returned only 10
# at a time, so results will have to be captured with multiple iterations. 

import urllib2
from bs4 import BeautifulSoup
import pandas
import requests

# since I'll be submitting a form to get results back, I will be using
# the POST HTTP method. Then the GET method to paginate through search result pages.

# Analyze the page's post form process and learn details from the post header
# open Chrome developer tools, click "Network," and submit the form. 
# In the results, click the first item (SubmitRequest item), and look at the headers tab.
# Grab the Request URL there and use it as the URL to send the post request to.
# Scroll down to Form Data at the bottom, and find the name:value pair parameter
# needed to pass to the post method. In this case, it is SelectedState:<state 2 digit>.
# For example, SelectedState:AL



# starting URL that has the primary form I want to submit searches on (one for each state)
base_url = 'https://www.acsi.org'
post_url = 'https://www.acsi.org/member-search/searchresults/SubmitResult'

# list declarations:
state_short = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", 
"IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", 
"NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", 
"UT", "VT", "VA", "WA", "WV", "WI", "WY"
			]
			
# ','.join(state_short)
			
			
school_name = []
school_page_url = []
street_address = []
city = []
state = []
zip_code = []
headmaster_name = []
headmaster_email_address = []
phone_number = []
fax_number = []
website_url = []
amount_of_early_childhood_students = []
amount_of_elementary_students = []
amount_of_middle_school_students = []
amount_of_high_school_students = []
total_students = []
i20_compliant = []
grade_levels_taught = []
year_founded = []
other_accreditations = []			
			
# custom functions
def get_school_name(soup_object):
    school_list = soup_object.findAll("a", id="Details_item.cst_key")
    for i in range(0, len(school_list)):
        school_name.append(school_list[i].text.encode('utf-8'))

def get_school_page_url(soup_object):
    school_urls = soup_object.findAll("a", id="Details_item.cst_key")
    for i in range(0,len(school_urls)):
        school_page_url.append(school_urls[i]['href'])

def get_details(soup_object):
    # narrow it down to the first div of data (1 of 2):
    div1 = soup_object.find('div', class_='col1-interior')
    div1_paras = div1.findAll('p')
    # p_list = div1.p.contents
    p_list = div1_paras[0].contents
    str_addr = p_list[0].strip().encode('utf-8')
    print str_addr
    street_address.append(str_addr)
    v_city = p_list[2][:p_list[2].rfind(",")].strip().encode('utf-8')
    print v_city
    city.append(v_city)
    zip = p_list[2][-10:].strip().encode('utf-8')
    print zip
    zip_code.append(zip)
    phone = p_list[6].strip().encode('utf-8')
    print phone
    phone_number.append(phone)
    fax = p_list[8].strip().encode('utf-8')
    print fax
    fax_number.append(fax)
    h_email = p_list[11].text.encode('utf-8')
    print h_email
    headmaster_email_address.append(h_email)
    school_homepage = p_list[14].text.encode('utf-8')
    print school_homepage
    website_url.append(school_homepage)
    
    
    
    #skip down to the next div
    div2 = soup_object.find('div', class_='col2-interior')
    p_list3 = div1_paras[1].contents



    # div1 = soup_object.find('div', class_='col1-interior')
    # para_group_1 = div1.findAll('p') 
    # detail_list = []
    # for i in range(0, len(para_group_1)):
    #     line = para_group_1[1].text.encode('utf-8')
    #     print line
    
        



# post field selections (values in the form) must be passed to post request as a dictionary
# make a dictionary (key-value pair associative array) of state to search. 
# for i in range(0,len(state_short)):
#     state_dict = {'SelectedState':state_short[i]}

state_dict = {'SelectedState':'AL'}

# start a session to make repeated calls to the server much faster, since
# the underlying TCP connection will be reused. This is what's meant by "HTTP persistent connection."
# This is much more performant than making hundreds of isolated HTTP requests all separately.
s = requests.Session()

post_response = s.post(post_url, state_dict)
# how to parse through html returned from http POST response?

soup = BeautifulSoup(post_response.content, "lxml")
get_school_name(soup)
get_school_page_url(soup)

# paginate through until the results are all found and recorded
while True: # hack for a do-while loop that Python doesn't explicitly have
    next_page_anchor = soup.find("a", class_="pagerNext pager-next-button")
    if(next_page_anchor == None):
        break
    else:
        next_url = next_page_anchor['href']
        get_response = s.get(next_url)
        soup = BeautifulSoup(get_response.content, "lxml")
        # with open(next_url) as next_html:
        #     soup = BeautifulSoup(next_url)
        get_school_name(soup)
        get_school_page_url(soup)

# here's the part where I go to the detail page for each school and grab detailed data
for i in range(0, len(school_page_url)):
    school_page_response = s.get(base_url + school_page_url[i])
    page_soup = BeautifulSoup(school_page_response.content, "lxml")
    get_details(page_soup)
    
    
# working out how to get the details. The below will go into the get_details function later:
    
# testing
test = s.get('https://www.acsi.org/member-search/searchdetails/SubmitDetail?SchoolKey=d8e31366-f67c-40c5-a4bd-2d7643c5bd33&saccredited=&sgradelevel=&sspecialprogram=&state=AL&accredited=')
test_soup = BeautifulSoup(test.content, "lxml")
div1 = test_soup.find('div', class_='col1-interior')
test_div_paras = div1.findAll('p')
test_p_list = test_div_paras[0].contents
str_addr = p_list[0].strip().encode('utf-8')
print str_addr

test_p_list2 = test_div_paras[1].contents


# just give me the content of the <p> tag in the first target div
# find a good way to parse through the blob
# the .contents list is automatically created for each part of the tree. Call on it. 
p_list = div1.p.contents
p_list
len(p_list)
#clean junk out of the contents list
# for p in range(0, len(p_list)):
    str_addr = p_list[p].strip().encode('utf-8')
    # print str_addr
    
print div1.p.contents[1]
city_state_zip = div1.p.contents[2].encode('utf-8')
print city_state_zip

div1.p.text # will show me where the special chars are, like "\r" and "\n"

for child in div1.p.children:
    print child

p_list[0]
p_list[0].strip().encode('utf-8')


[x for x in p_list if x != ' <br/>']

[x for x in p_list if x is not None]


div2 = test_soup.find('div', class_='col2-interior')
head_name = div2.find('p').text.encode('utf-8')
if(head_name.endswith(' - Headmaster')):
    head_name = head_name[:-13]
if(head_name.startswith('Mr ')):
    head_name = head_name[3:]



headmaster_name.append()

# detail_list = []


    # for i in range(0, len(para_group_1)):
    #     line = para_group_1[1].text.encode('utf-8')
    #     print line

# easier way? Can I just turn the results returned limit in the post request to unlimited?
# Or actually, I think I just make a post request with no parameters (form selections) by just
# navigating to the post url!
# https://www.acsi.org/member-search/searchresults/SubmitResult
# and then just paginate through the search results until the nextpage val is null?
