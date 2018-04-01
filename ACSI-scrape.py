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
early_education_students = []
elementary_students = []
middle_school_students = []
high_school_students = []
total_students = []
i20_compliant = []
grade_levels_taught = []
year_founded = []
acsi_accreditation_status = []
grades_accredited = []
other_accreditations = []
special_needs = []
 
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



# find the statistics section and parse it
def get_statistics(soup_object):
    div1 = soup_object.find('div', class_='col1-interior')
    div1_h1 = div1.find('h2')
    box = soup_object.find('div', class_='blue-gray-box-content search')
    school_header = box.find('h1')
    div1_h2 = div1_h1.find_next_sibling('h2')
    div1_h3 = div1_h2.find_next_sibling('h2')
    if div1_h2.text == "Statistics":
        address_p = div1_h2.find_next_sibling('p')
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




def get_details(soup_object):
    # narrow it down to the first div of data (1 of 2):
    div1 = soup_object.find('div', class_='col1-interior')
    first_heading = div1.find('h2')
    if first_heading.text == 'Address':
        address_p = first_heading.find_next_sibling('p')
        #get all data from this <p>. Should be ok to just use content list indexes.
        p_list = address_p.contents
        str_addr = p_list[0].strip().encode('utf-8')
        print str_addr
        street_address.append(str_addr)
        v_city = p_list[2][:p_list[2].find(",")].strip().encode('utf-8')
        print v_city
        city.append(v_city)
        zip = p_list[2][p_list[2].find(",") + 5 :].strip().encode('utf-8')
        print zip
        zip_code.append(zip)
        phone = p_list[6][p_list[6].find(':') +2:].strip().encode('utf-8')
        print phone
        phone_number.append(phone)
        fax = p_list[8][p_list[8].find(':') +2:].strip().encode('utf-8')
        print fax
        fax_number.append(fax)
        h_email = p_list[11].text.encode('utf-8')
        print h_email
        primary_contact_email_address.append(h_email)
        school_homepage = p_list[14].text.encode('utf-8')
        print school_homepage
        website_url.append(school_homepage)    
        
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
        elif second_heading.text == 'Statistics':
            # make the accreditation fields blank
            accredit = ''
            print accredit
            acsi_accreditation_status.append(accredit)
            grades_accredit = ''
            print grades_accredit
            grades_accredited.append(grades_accredit)
            # Grab stats data
            stats_raw_p = second_heading.find_next_sibling('p')
            stats_raw_list = stats_raw_p.text.split('\n')
            stats_list = [x.strip() for x in stats_raw_list if x != '']
            # Early Education Enrollment
            early_ed_found = 'N'
            for i in xrange(0, len(stats_list)):
                if 'Early Education Enrollment' in stats_list[i]:
                    early_ed = stats_list[i][stats_list[i].find(':') + 2 :].strip().encode('utf-8')
                    early_education_students.append(early_ed)
                    print early_ed
                    early_ed_found = 'Y'
                    break
            if early_ed_found == 'N':
                early_ed = ''
                early_education_students.append(early_ed)
                print 'Text not found, making this value blank'
            # Elementary Enrollment
            elem_found = 'N'
            for i in xrange(0, len(stats_list)):
                if 'Elementary Enrollment' in stats_list[i]:
                    elem = stats_list[i][stats_list[i].find(':') + 2 :].strip().encode('utf-8')
                    elementary_students.append(elem)
                    print elem
                    elem_found = 'Y'
                    break
            if elem_found == 'N':
                elem = ''
                elementary_students.append(elem)
                print 'Text not found, making this value blank'
            # Middle School Enrollment
            middle_found = 'N'
            for i in xrange(0, len(stats_list)):
                if 'Middle School Enrollment' in stats_list[i]:
                    middle = stats_list[i][stats_list[i].find(':') + 2 :].strip().encode('utf-8')
                    middle_school_students.append(middle)
                    print middle
                    middle_found = 'Y'
                    break
            if middle_found == 'N':
                middle = ''
                middle_school_students.append(middle)
                print 'Text not found, making this value blank'
            # High School Enrollment
            high_found = 'N'
            for i in xrange(0, len(stats_list)):
                if 'High School Enrollment' in stats_list[i]:
                    high = stats_list[i][stats_list[i].find(':') + 2 :].strip().encode('utf-8')
                    high_school_students.append(high)
                    print high
                    high_found = 'Y'
                    break
            if high_found == 'N':
                high = ''
                high_school_students.append(high)
                print 'Text not found, making this value blank'
            # Total Enrollment
            total_s_found = 'N'
            for i in xrange(0, len(stats_list)):
                if 'Total Enrollment' in stats_list[i]:
                    total_s = stats_list[i][stats_list[i].find(':') + 2 :].strip().encode('utf-8')
                    total_students.append(total_s)
                    print total_s
                    total_s_found = 'Y'
                    break
            if total_s_found == 'N':
                total_s = ''
                total_students.append(total_s)
                print 'Text not found, making this value blank'
            # I20
            I20_found = 'N'
            for i in xrange(0, len(stats_list)):
                if 'I20' in stats_list[i]:
                    I20 = stats_list[i][stats_list[i].find(':') + 2 :].strip().encode('utf-8')
                    i20_compliant.append(I20)
                    print I20
                    I20_found = 'Y'
                    break
            if I20_found == 'N':
                I20 = ''
                i20_compliant.append(I20)
                print 'Text not found, making this value blank'
            # Grade Levels
            grade_l_found = 'N'
            for i in xrange(0, len(stats_list)):
                if 'Grade Levels' in stats_list[i]:
                    grade_l = stats_list[i][stats_list[i].find(':') + 2 :].strip().encode('utf-8')
                    grade_levels_taught.append(grade_l)
                    print grade_l
                    grade_l_found = 'Y'
                    break
            if grade_l_found == 'N':
                grade_l= ''
                grade_levels_taught.append(grade_l)
                print 'Text not found, making this value blank'
            # Year Founded
            year_found = 'N'
            for i in xrange(0, len(stats_list)):
                if 'Year Founded' in stats_list[i]:
                    year = stats_list[i][stats_list[i].find(':') + 2 :].strip().encode('utf-8')
                    year_founded.append(year)
                    print year
                    year_found = 'Y'
                    break
            if year_found == 'N':
                year = ''
                year_founded.append(year)
                print 'Text not found, making this value blank'
            # Other Accreditation
            other_a_found = 'N'
            for i in xrange(0, len(stats_list)):
                if 'Other Accreditation' in stats_list[i]:
                    other_a = stats_list[i][stats_list[i].find(':') + 2 :].strip().encode('utf-8')
                    other_accreditations.append(other_a)
                    print other_a
                    other_a_found = 'Y'
                    break
            if other_a_found == 'N':
                other_a = ''
                other_accreditations.append(other_a)
                print 'Text not found, making this value blank'
            # Special Needs
            needs_found = 'N'
            for i in xrange(0, len(stats_list)):
                if 'Special Needs' in stats_list[i]:
                    needs = stats_list[i][stats_list[i].find(':') + 2 :].strip().encode('utf-8')
                    special_needs.append(needs)
                    print needs
                    needs_found = 'Y'
                    break
            if needs_found == 'N':
                needs = ''
                special_needs.append(needs)
                print 'Text not found, making this value blank' 
        else:
            print 'The second heading was not Accreditation or Stats'
        third_heading = second_heading.find_next_sibling('h2')
        if third_heading != None:
            if third_heading.text == 'Statistics':
                # Grab stats data
                stats_raw_p = third_heading.find_next_sibling('p')
                stats_raw_list = stats_raw_p.text.split('\n')
                stats_list = [x.strip() for x in stats_raw_list if x != '']
                # Early Education Enrollment
                early_ed_found = 'N'
                for i in xrange(0, len(stats_list)):
                    if 'Early Education Enrollment' in stats_list[i]:
                        early_ed = stats_list[i][stats_list[i].find(':') + 2 :].strip().encode('utf-8')
                        early_education_students.append(early_ed)
                        print early_ed
                        early_ed_found = 'Y'
                        break
                if early_ed_found == 'N':
                    early_ed = ''
                    early_education_students.append(early_ed)
                    print 'Text not found, making this value blank'
                # Elementary Enrollment
                elem_found = 'N'
                for i in xrange(0, len(stats_list)):
                    if 'Elementary Enrollment' in stats_list[i]:
                        elem = stats_list[i][stats_list[i].find(':') + 2 :].strip().encode('utf-8')
                        elementary_students.append(elem)
                        print elem
                        elem_found = 'Y'
                        break
                if elem_found == 'N':
                    elem = ''
                    elementary_students.append(elem)
                    print 'Text not found, making this value blank'
                # Middle School Enrollment
                middle_found = 'N'
                for i in xrange(0, len(stats_list)):
                    if 'Middle School Enrollment' in stats_list[i]:
                        middle = stats_list[i][stats_list[i].find(':') + 2 :].strip().encode('utf-8')
                        middle_school_students.append(middle)
                        print middle
                        middle_found = 'Y'
                        break
                if middle_found == 'N':
                    middle = ''
                    middle_school_students.append(middle)
                    print 'Text not found, making this value blank'
                # High School Enrollment
                high_found = 'N'
                for i in xrange(0, len(stats_list)):
                    if 'High School Enrollment' in stats_list[i]:
                        high = stats_list[i][stats_list[i].find(':') + 2 :].strip().encode('utf-8')
                        high_school_students.append(high)
                        print high
                        high_found = 'Y'
                        break
                if high_found == 'N':
                    high = ''
                    high_school_students.append(high)
                    print 'Text not found, making this value blank'
                # Total Enrollment
                total_s_found = 'N'
                for i in xrange(0, len(stats_list)):
                    if 'Total Enrollment' in stats_list[i]:
                        total_s = stats_list[i][stats_list[i].find(':') + 2 :].strip().encode('utf-8')
                        total_students.append(total_s)
                        print total_s
                        total_s_found = 'Y'
                        break
                if total_s_found == 'N':
                    total_s = ''
                    total_students.append(total_s)
                    print 'Text not found, making this value blank'
                # I20
                I20_found = 'N'
                for i in xrange(0, len(stats_list)):
                    if 'I20' in stats_list[i]:
                        I20 = stats_list[i][stats_list[i].find(':') + 2 :].strip().encode('utf-8')
                        i20_compliant.append(I20)
                        print I20
                        I20_found = 'Y'
                        break
                if I20_found == 'N':
                    I20 = ''
                    i20_compliant.append(I20)
                    print 'Text not found, making this value blank'
                # Grade Levels
                grade_l_found = 'N'
                for i in xrange(0, len(stats_list)):
                    if 'Grade Levels' in stats_list[i]:
                        grade_l = stats_list[i][stats_list[i].find(':') + 2 :].strip().encode('utf-8')
                        grade_levels_taught.append(grade_l)
                        print grade_l
                        grade_l_found = 'Y'
                        break
                if grade_l_found == 'N':
                    grade_l= ''
                    grade_levels_taught.append(grade_l)
                    print 'Text not found, making this value blank'
                # Year Founded
                year_found = 'N'
                for i in xrange(0, len(stats_list)):
                    if 'Year Founded' in stats_list[i]:
                        year = stats_list[i][stats_list[i].find(':') + 2 :].strip().encode('utf-8')
                        year_founded.append(year)
                        print year
                        year_found = 'Y'
                        break
                if year_found == 'N':
                    year = ''
                    year_founded.append(year)
                    print 'Text not found, making this value blank'
                # Other Accreditation
                other_a_found = 'N'
                for i in xrange(0, len(stats_list)):
                    if 'Other Accreditation' in stats_list[i]:
                        other_a = stats_list[i][stats_list[i].find(':') + 2 :].strip().encode('utf-8')
                        other_accreditations.append(other_a)
                        print other_a
                        other_a_found = 'Y'
                        break
                if other_a_found == 'N':
                    other_a = ''
                    other_accreditations.append(other_a)
                    print 'Text not found, making this value blank'
                # Special Needs
                needs_found = 'N'
                for i in xrange(0, len(stats_list)):
                    if 'Special Needs' in stats_list[i]:
                        needs = stats_list[i][stats_list[i].find(':') + 2 :].strip().encode('utf-8')
                        special_needs.append(needs)
                        print needs
                        needs_found = 'Y'
                        break
                if needs_found == 'N':
                    needs = ''
                    special_needs.append(needs)
                    print 'Text not found, making this value blank' 
            else:
                print "Expected third heading to be Statistics, it wasn't."
    else:
        print 'No h2 heading tag found for Address data.'
    state.append(state_short[st])
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





