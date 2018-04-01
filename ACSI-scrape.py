# shebang line to make sure this uses python 3

#!/usr/bin/python3

# Association of Christian Schools International (ACSI)
# https://www.acsi.org/
# this site requires the submission of forms and capture of the search
# results.
# Cannot use explicit URLs to navigate. Furthermore, result sets are returned
# only 10
# at a time, so results will have to be captured with multiple iterations.

from bs4 import BeautifulSoup
import pandas
import requests
import timeit
from time import sleep
import random
from os import listdir
from collections import Counter

base_url = 'https://www.acsi.org'
post_url = 'https://www.acsi.org/member-search/searchresults/SubmitResult?startRow=0&rowsPerPage=3000'
data_dir = "/Users/Steve/Dropbox/programming/Python/web-scraping/data/acsi/"

# declare public lists:
school_name = []
school_page_url = []
street_address = []
city = []
state = []
zip_code = []
primary_contact_name = []
primary_contact_email_address = []
phone_number = []
fax_number = []
website_url = []



 
# since I'll be submitting a form to get results back, I will be using
# the POST HTTP method. Then the GET method to paginate through search result
# pages.

# Analyze the page's post form process and learn details from the post header
# open Chrome developer tools, click "Network," and submit the form.
# In the results, click the first item (SubmitRequest item), and look at the
# headers tab.
# Grab the Request URL there and use it as the URL to send the post request to.
# Scroll down to Form Data at the bottom, and find the name:value pair argument
# needed to pass to the post method. In this case, it is
# SelectedState:<state 2 digit>.
# For example, SelectedState:AL

# starting URL that has the primary form I want to submit searches on (one for
# each state)

# Function to grab every school name and school page url from the list of
# schools, paginating through the subsets of school listings since the 
# site only returns 10 at a time. Make sure to sleep between each call 
# so the site doesn't block me from too many rapid get requests. 
# Maybe a random pause between 5 and 20 seconds. 

# custom functions
# this pulls the text of the school name from the link object
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


# this version is good if I can't control the amount of search results 
# returned by the post request. 
# BUT I can! I can pass the URL query string of ?startRow=0&rowsPerPage=3000
# So, the post URL becomes 
# https://www.acsi.org/member-search/searchresults/SubmitResult?startRow=0&rowsPerPage=3000
# take the post url, return the content, pull out the school name and urls, 
# and create a pandas dataframe. Then write out to file.
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
    school_frame.to_csv("/Users/Steve/Dropbox/programming/Python/web-scraping/data/acsi-schools.csv", encoding='utf-8', index=False)   
   

# Call the functions to write out the school and school URL file
find_schools(post_url)
# Now the file of schools has been created, and is a proxy for querying the
# actual site itself and tempting it to block me. 
schools = pandas.read_csv("/Users/Steve/Dropbox/programming/Python/web-scraping/data/acsi-schools.csv")
url_list = schools['school_page_url']
school_name_list = schools['school_name']
for z in range(0, len(school_name_list)):
    school_name_list[z] = school_name_list[z].replace( "/", "-")   


# Function that takes a list of URLs for which I want to place "get"
# requests, capture HTML content, and write to file for each site.
def curate_html(url_list, school_name_list, data_dir):
    s = requests.Session()
    for i in range(0, len(url_list)):
        response = s.get(url_list[i])
        response_content = response.content
        fh = open(f"{data_dir}html-files/{school_name_list[i]}.html", "wb")
        fh.write(response_content)
        fh.close()
        sleep(random.randint(1, 3))

curate_html(url_list, school_name_list, data_dir)



# now, need to loop over html files in dir and parse through them all.
# Build in extensive testing and error handling. 
# First step to that is probably to split the rest of the work into
# smaller functions and evaluate them separately.





# list declarations:
state_short = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL",
    "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA",
    "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC",
    "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT",
    "VA", "WA", "WV", "WI", "WY"]


#get a list of all the html files:
file_list = listdir("/Users/Steve/Dropbox/programming/Python/web-scraping/data/acsi/html-files")

# function to open html file, create soup object from it, and close it
def file_to_soup(file_path):
    html = open(file_path, "r")
    soup_to_nuts = BeautifulSoup(html, "lxml")
    html.close()
    return soup_to_nuts

# analyze_p_list = [x for x in analyze_p_list if x[2] == 'UNITED STATES']

school_name = []
school_page_url = []
street_address = []
city = []
state_list = []
zip_code = []
primary_contact_email_address = []
phone_number = []
fax_number = []
website_url = []

def get_contact_info(soup_object):
    box = soup_object.find('div', class_='blue-gray-box-content search')
    school_header = box.find('h1')
    col1_div = soup_object.find('div', class_='col1-interior')
    address_h = col1_div.find('h2', text = 'Address')
    address_p = address_h.find_next_sibling('p')
    p_list = address_p.get_text().split("\n")
    p_list = [x.strip() for x in p_list]    
    if p_list[2] == 'UNITED STATES':
        v_school_name = school_header.text
        print(v_school_name)
        school_name.append(v_school_name)
        str_addr = p_list[0]
        print (str_addr)
        street_address.append(p_list[0])
        v_city = p_list[1][:p_list[1].find(",")]
        print (v_city)
        city.append(v_city)
        state = p_list[1][p_list[1].find(",") + 1 : p_list[1].find(",") + 4 ].strip()
        print (state)
        state_list.append(state)
        zip = p_list[1][p_list[1].find(",") + 4 :].strip()
        print (zip)
        zip_code.append(zip)
        phone = p_list[3][p_list[3].find(':') +2:]
        print (phone)
        phone_number.append(phone)
        fax = p_list[4][p_list[4].find(':') +2:]
        print (fax)
        fax_number.append(fax)
        h_email = p_list[5]
        print (h_email)
        primary_contact_email_address.append(h_email)
        school_homepage = p_list[6]
        print (school_homepage)
        website_url.append(school_homepage)


for i in range(0, len(file_list)):
    soup_to_nuts = file_to_soup(f"{data_dir}html-files/{file_list[i]}")
    get_contact_info(soup_to_nuts)        



master_frame = pandas.DataFrame()

master_frame["School Name"] = school_name
master_frame["Street Address"] = street_address
master_frame["City"] = city
master_frame["State"] = state_list
master_frame["Zip Code"] = zip_code
master_frame["Primary Contact Email"] = primary_contact_email_address
master_frame["Phone Number"] = phone_number
master_frame["Fax Number"] = fax_number
master_frame["School Website"] = website_url


# write frame to file
# master_frame.to_csv("/Users/Steve/Dropbox/programming/Python/web-scraping/data/acsi.csv", encoding='utf-8', index=False)   
   

######### PROFILING ##########

# how often is the second heading "Statistics?"
# how often is it "ACSI Accredited?"
# how often is it null?
h2_list = []
def analyze_second_h2(soup_object):
    div1 = soup_object.find('div', class_='col1-interior')
    div1_h1 = div1.find('h2')
    div1_h2 = div1_h1.find_next_sibling('h2')
    div1_h3 = div1_h2.find_next_sibling('h2')
    if div1_h2 != None:
        print(div1_h2.text)
        h2_list.append(div1_h2.text)


for i in range(0, len(file_list)):
    html = open(f"{data_dir}html-files/{file_list[i]}", "r")
    soup_to_nuts = BeautifulSoup(html, "lxml")
    html.close()
    analyze_second_h2(soup_to_nuts)   

Counter(h2_list)
# Counter({'ACSI Accredited': 871, 'Statistics': 1581})

h3_list = []
def analyze_second_h3(soup_object):
    div1 = soup_object.find('div', class_='col1-interior')
    div1_h1 = div1.find('h2')
    div1_h2 = div1_h1.find_next_sibling('h2')
    div1_h3 = div1_h2.find_next_sibling('h2')
    if div1_h3 != None:
        print(div1_h3.text)
        h3_list.append(div1_h3.text)
    else:
        print('None')
        h3_list.append('None')


for i in range(0, len(file_list)):
    html = open(f"{data_dir}html-files/{file_list[i]}", "r")
    soup_to_nuts = BeautifulSoup(html, "lxml")
    html.close()
    analyze_second_h3(soup_to_nuts)   

Counter(h3_list)

# how to find a heading with specific text?
stats_heading_list = []
def find_statistics_h2(soup_object):
    div1 = div1 = soup_object.find('div', class_='col1-interior')
    h2_stats = div1.find('h2', text = 'Statistics')
    print(h2_stats.text)
    stats_heading_list.append(h2_stats.text)

for i in range(0, len(file_list)):
    html = open(f"{data_dir}html-files/{file_list[i]}", "r")
    soup_to_nuts = BeautifulSoup(html, "lxml")
    html.close()
    find_statistics_h2(soup_to_nuts) 


#clean up stats list
soup_object = file_to_soup(f"{data_dir}html-files/{file_list[i]}")
col1_div = soup_object.find('div', class_='col1-interior')
stats_h = col1_div.find('h2', text = 'Statistics')
stats_p = stats_h.find_next_sibling('p')
stats_list = stats_p.get_text().split("\n")
stats_list = [x.strip() for x in stats_list] 
stats_list = [x for x in stats_list if x != '']
stats_list_names = [x[: x.find(':')].strip() for x in stats_list]

stats_dict = {}
#populate the dictionary
for j, v in enumerate(stats_list):
    stats_dict[stats_list[j][: stats_list[j].find(':')].strip()] = stats_list[j][stats_list[j].find(':') +1 :].strip()

if 'Year Founded' in stats_dict:
    print(stats_dict.get('Year Founded'))

# make a list of lists of all the stats labels per file
# then compare them to see what we're dealing with
stats_contents_eval = []
def eval_stats_list(soup_object):
    col1_div = soup_object.find('div', class_='col1-interior')
    address_h = col1_div.find('h2', text = 'Address')
    address_p = address_h.find_next_sibling('p')
    address_list = address_p.get_text().split("\n")
    address_list = [x.strip() for x in address_list]    
    stats_h = col1_div.find('h2', text = 'Statistics')
    stats_p = stats_h.find_next_sibling('p')
    stats_list = stats_p.get_text().split("\n")
    stats_list = [x.strip() for x in stats_list]  
    stats_list = [x for x in stats_list if x != '']
    stats_list_names = [x[: x.find(':')].strip() for x in stats_list]
    if address_list[2] == 'UNITED STATES':
        print(stats_list_names)
        stats_contents_eval.append(stats_list_names)

for i, v in enumerate(file_list):
    soup_to_nuts = file_to_soup(f"{data_dir}html-files/{file_list[i]}")
    eval_stats_list(soup_to_nuts) 

# how many unique orientations of the stats data are there?
unique_data = [list(x) for x in set(tuple(x) for x in stats_contents_eval)]
# there are 51 variants.

# so, find all the possible stats items. Make variables for each.
# Initialize them as empty, but update if you find any. 

# what are all the possible stats items?
"""
'Boarding School'
'Elementary Enrollment'
'Year Founded'
'I20'
'Special Needs'
'EFL'
'Total Enrollment'
'Home School'
'Grade Levels'
'Online'
'Other Accreditation'
'Early Education Enrollment'
'High School Enrollment'
'Middle School Enrollment'
"""

# better order:
"""
'Early Education Enrollment'
'Elementary Enrollment'
'Middle School Enrollment'
'High School Enrollment'
'Total Enrollment'
'Grade Levels'
'Year Founded'
'Boarding School'
'I20'
'Special Needs'
'EFL'
'Home School'
'Online'
'Other Accreditation'
"""

# stats variable names
"""
early_education_enrollment
elementary_enrollment
middle_school_enrollment
high_school_enrollment
total_enrollment
grade_levels
year_founded
boarding_school
i20
special_needs
efl
home_school
online
other_accreditation
"""

########## end PROFILING ##########

# find the statistics section and parse it
early_education_enrollment = []
elementary_enrollment = []
middle_school_enrollment = []
high_school_enrollment = []
total_enrollment = []
grade_levels = []
year_founded = []
boarding_school = []
i20 = []
special_needs = []
efl = []
home_school = []
online = []
other_accreditation = []

def get_statistics(soup_object):
    col1_div = soup_object.find('div', class_='col1-interior')
    address_h = col1_div.find('h2', text = 'Address')
    address_p = address_h.find_next_sibling('p')
    address_list = address_p.get_text().split("\n")
    address_list = [x.strip() for x in address_list]    
    stats_h = col1_div.find('h2', text = 'Statistics')
    stats_p = stats_h.find_next_sibling('p')
    stats_list = stats_p.get_text().split("\n")
    stats_list = [x.strip() for x in stats_list]   
    stats_list = [x for x in stats_list if x != '']
    if address_list[2] == 'UNITED STATES':
        # set up and populate dictionary
        stats_dict = {}
        for j, v in enumerate(stats_list):
            stats_dict[stats_list[j][: stats_list[j].find(':')].strip()] = stats_list[j][stats_list[j].find(':') +1 :].strip()
        # Early Education Enrollment
        if 'Early Education Enrollment' in stats_dict:
            v_early_education_enrollment = stats_dict.get('Early Education Enrollment')
        else:
            v_early_education_enrollment = ''
        print(v_early_education_enrollment)
        early_education_enrollment.append(v_early_education_enrollment)
        # Elementary Enrollment
        if 'Elementary Enrollment' in stats_dict:
            v_elementary_enrollment = stats_dict.get('Elementary Enrollment')
        else:
            v_elementary_enrollment = ''
        print(v_elementary_enrollment)
        elementary_enrollment.append(v_elementary_enrollment)
        # Middle School Enrollment
        if 'Middle School Enrollment' in stats_dict:
            v_middle_school_enrollment = stats_dict.get('Middle School Enrollment')
        else:
            v_middle_school_enrollment = ''
        print(v_middle_school_enrollment)
        middle_school_enrollment.append(v_middle_school_enrollment)
        # High School Enrollment
        if 'High School Enrollment' in stats_dict:
            v_high_school_enrollment = stats_dict.get('High School Enrollment')
        else:
            v_high_school_enrollment = ''
        print(v_high_school_enrollment)
        high_school_enrollment.append(v_high_school_enrollment)
        # Total Enrollment
        if 'Total Enrollment' in stats_dict:
            v_total_enrollment = stats_dict.get('Total Enrollment')
        else:
            v_total_enrollment = ''
        print(v_total_enrollment)
        total_enrollment.append(v_total_enrollment)
        # Grade Levels
        if 'Grade Levels' in stats_dict:
            v_grade_levels = stats_dict.get('Grade Levels')
        else:
            v_grade_levels = ''
        print(v_grade_levels)
        grade_levels.append(v_grade_levels)
        # Year Founded
        if 'Year Founded' in stats_dict:
            v_year_founded = stats_dict.get('Year Founded')
        else:
            v_year_founded = ''
        print(v_year_founded)
        year_founded.append(v_year_founded)
        # Boarding School
        if 'Boarding School' in stats_dict:
            v_boarding_school = stats_dict.get('Boarding School')
        else:
            v_boarding_school = ''
        print(v_boarding_school)
        boarding_school.append(v_boarding_school)
        # I20
        if 'I20' in stats_dict:
            v_i20 = stats_dict.get('I20')
        else:
            v_i20 = ''
        print(v_i20)
        i20.append(v_i20)
        # Special Needs
        if 'Special Needs' in stats_dict:
            v_special_needs = stats_dict.get('Special Needs')
        else:
            v_special_needs = ''
        print(v_special_needs)
        special_needs.append(v_special_needs)
        # EFL
        if 'EFL' in stats_dict:
            v_efl = stats_dict.get('EFL')
        else:
            v_efl = ''
        print(v_efl)
        efl.append(v_efl)
        # Home School
        if 'Home School' in stats_dict:
            v_home_school = stats_dict.get('Home School')
        else:
            v_home_school = ''
        print(v_home_school)
        home_school.append(v_home_school)
        # Online
        if 'Online' in stats_dict:
            v_online = stats_dict.get('Online')
        else:
            v_online = ''
        print(v_online)
        online.append(v_online)
        # Other Accreditation
        if 'Other Accreditation' in stats_dict:
            v_other_accreditation = stats_dict.get('Other Accreditation')
        else:
            v_other_accreditation = ''
        print(v_other_accreditation)
        other_accreditation.append(v_other_accreditation)


for i, v in enumerate(file_list):
    soup_to_nuts = file_to_soup(f"{data_dir}html-files/{file_list[i]}")
    get_statistics(soup_to_nuts) 



"""
'Early Education Enrollment'
'Elementary Enrollment'
'Middle School Enrollment'
'High School Enrollment'
'Total Enrollment'
'Grade Levels'
'Year Founded'
'Boarding School'
'I20'
'Special Needs'
'EFL'
'Home School'
'Online'
'Other Accreditation'
"""

"""
early_education_enrollment
elementary_enrollment
middle_school_enrollment
high_school_enrollment
total_enrollment
grade_levels
year_founded
boarding_school
i20
special_needs
efl
home_school
online
other_accreditation
"""


# find the ACSI accredited section, if exists, and parse it
acsi_accreditation_status = []
grades_accredited = []
def get_accreditation(soup_object):
    col1_div = soup_object.find('div', class_='col1-interior')
    address_h = col1_div.find('h2', text = 'Address')
    address_p = address_h.find_next_sibling('p')
    address_list = address_p.get_text().split("\n")
    address_list = [x.strip() for x in address_list]
    if address_list[2] == 'UNITED STATES':    
        accred_h = col1_div.find('h2', text = 'ACSI Accredited')
        if accred_h == None:
            v_acsi_accreditation_status = ''
            print(v_acsi_accreditation_status)
            acsi_accreditation_status.append(v_acsi_accreditation_status)
            v_grades_accredited = ''
            print(v_grades_accredited)
            grades_accredited.append(v_grades_accredited)
        else:
            accred_p = accred_h.find_next_sibling('p')
            accred_list = accred_p.get_text().split("\n")
            accred_list = [x.strip() for x in accred_list]   
            accred_list = [x for x in accred_list if x != '']
            # set up and populate dictionary
            accred_dict = {}
            for j, v in enumerate(accred_list):
                accred_dict[accred_list[j][: accred_list[j].find(':')].strip()] = accred_list[j][accred_list[j].find(':') +1 :].strip()
            # ACSI Accreditation
            if 'ACSI Accreditation' in accred_dict:
                v_acsi_accreditation_status = stats_dict.get('ACSI Accreditation')
            else:
                v_acsi_accreditation_status = ''
            print(v_acsi_accreditation_status)
            acsi_accreditation_status.append(v_acsi_accreditation_status)
            # Grades Accredited
            if 'Grades Accredited' in accred_dict:
                v_grades_accredited = stats_dict.get('Grades Accredited')
            else:
                v_grades_accredited= ''
            print(v_grades_accredited)
            grades_accredited.append(v_grades_accredited)






# find the primary contact person section in second div, parse it

































def get_details(soup_object):
    # narrow it down to the first div of data (1 of 2):
    div1 = soup_object.find('div', class_='col1-interior')
    first_heading = div1.find('h2')
    
        
        #move on to next section of the first div 
        second_heading = address_p.find_next_sibling('h2')
        if second_heading.text == 'ACSI Accredited':
            accredit_p = second_heading.find_next_sibling('p')
            #grab all the accreditation data
            p_list_accredit = accredit_p.contents
            accredit = p_list_accredit[0][p_list_accredit[0].find(':') + 2 :].strip().encode('utf-8')
            print accredit 
            acsi_accreditation_status.append(accredit)
            grades_accredit = p_list_accredit[2][p_list_accredit[2].find(':') + 2 :].strip().encode('utf-8')
            print grades_accredit
            grades_accredited.append(grades_accredit)
        

    # jump down to the next div
    div2 = soup_object.find('div', class_='col2-interior')
    main_contact_p = div2.find('p')
    if main_contact_p != None:
        contact_person = main_contact_p.text.encode('utf-8')
        primary_contact_name.append(contact_person)
    else:
        contact_person = ''
        primary_contact_name.append(contact_person)
        print 'Text not found, making this value blank'

# start a session to make repeated calls to the server much faster, since
# the underlying TCP connection will be reused. This is what's meant by "HTTP persistent connection."
# This is much more performant than making hundreds of isolated HTTP requests all separately.
s = requests.Session()    

scrape_start_time = timeit.default_timer()
# post field selections (values in the form) must be passed to post request as a dictionary
# make a dictionary (key-value pair associative array) of state to search. 
for st in range(0, len(state_short)):
    # curr_st_school_page_url = []
    state_dict = {'SelectedState':state_short[st]}
    post_response = s.post(post_url, state_dict)
    soup = BeautifulSoup(post_response.content, "lxml")
    get_school_name(soup)
    get_school_page_url(soup)
    # get_curr_st_school_page_url(soup)
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
    # Go to the detail page for each school and grab detailed data
    for i in range(0, len(curr_st_school_page_url)):
        school_page_response = s.get(base_url + school_page_url[i])
        page_soup = BeautifulSoup(school_page_response.content, "lxml")
        get_details(page_soup)
        sleep(30)
    
scrape_time_elapsed = timeit.default_timer() - scrape_start_time    
print "Scrape time elapsed: %d" %scrape_time_elapsed



file_io_start_time = timeit.default_timer()

master_frame = pandas.DataFrame()

master_frame["School Name"] = school_name
master_frame["Street Address"] = street_address
master_frame["City"] = city
master_frame["State"] = state
master_frame["Zip Code"] = zip_code
master_frame["Primary Contact Name"] = primary_contact_name
master_frame["Primary Contact Email"] = primary_contact_email_address
master_frame["Phone Number"] = phone_number
master_frame["Fax Number"] = fax_number
master_frame["ACSI Page"] = school_page_url
master_frame["School Website"] = website_url
master_frame["Early Education Students"] = early_education_students
master_frame["Elementary Students"] = elementary_students
master_frame["Middle School Students"] = middle_school_students
master_frame["High School Students"] = high_school_students
master_frame["Total Students"] = total_students
master_frame["I20 Compliant"] = i20_compliant
master_frame["Grade Levels Taught"] = grade_levels_taught
master_frame["Year Founded"] = year_founded
master_frame["ACSI Accreditation Status"]= acsi_accreditation_status
master_frame["Grades Accredited"] = grades_accredited
master_frame["Other Accreditations"] = other_accreditations
master_frame["Special Needs"] = special_needs


print master_frame.head(5)

# write frame to file
master_frame.to_csv("/Users/Steve/Dropbox/programming/Python/web-scraping/data/acsi.csv", encoding='utf-8', index=False)   
    
file_io_time_elapsed = timeit.default_timer() - file_io_start_time  

print "Scrape time elapsed: %d" %file_io_time_elapsed





