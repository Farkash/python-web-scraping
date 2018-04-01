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

def get_school_name(soup_object):
    print("List of schools for this get response:")
    school_list = soup_object.findAll("a", id="Details_item.cst_key")
    for i in range(0, len(school_list)):
        school_name.append(school_list[i].text)
        print(school_list[i].text.encode('utf-8'))

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

#get a list of all the html files:
file_list = listdir("/Users/Steve/Dropbox/programming/Python/web-scraping/data/acsi/html-files")

# function to open html file, create soup object from it, and close it
def file_to_soup(file_path):
    html = open(file_path, "r")
    soup_to_nuts = BeautifulSoup(html, "lxml")
    html.close()
    return soup_to_nuts

# get the contact info for the school
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
                v_acsi_accreditation_status = accred_dict.get('ACSI Accreditation')
            else:
                v_acsi_accreditation_status = ''
            print(v_acsi_accreditation_status)
            acsi_accreditation_status.append(v_acsi_accreditation_status)
            # Grades Accredited
            if 'Grades Accredited' in accred_dict:
                v_grades_accredited = accred_dict.get('Grades Accredited')
            else:
                v_grades_accredited= ''
            print(v_grades_accredited)
            grades_accredited.append(v_grades_accredited)


# find the primary contact person section in second div, parse it
primary_contact_name = []
def get_primary_contact(soup_object):
    col1_div = soup_object.find('div', class_='col1-interior')
    address_h = col1_div.find('h2', text = 'Address')
    address_p = address_h.find_next_sibling('p')
    address_list = address_p.get_text().split("\n")
    address_list = [x.strip() for x in address_list]
    if address_list[2] == 'UNITED STATES':    
        col2_div = soup_object.find('div', class_='col2-interior')
        main_contact_p = col2_div.find('p')
        if main_contact_p != None:
            main_contact_list = main_contact_p.get_text().split("\n")
            main_contact_list = [x.strip() for x in main_contact_list]   
            contact_person = main_contact_list[0][: main_contact_list[0].find('-') -1].strip()
        else:
            contact_person = ''
        print(contact_person)
        primary_contact_name.append(contact_person)

for i, v in enumerate(file_list):
    soup_to_nuts = file_to_soup(f"{data_dir}html-files/{file_list[i]}")
    get_contact_info(soup_to_nuts) 
    get_statistics(soup_to_nuts)
    get_accreditation(soup_to_nuts) 
    get_primary_contact(soup_to_nuts)


# write all lists to pandas frame to prepare for extract
master_frame = pandas.DataFrame()

master_frame["School Name"] = school_name
master_frame["Street Address"] = street_address
master_frame["City"] = city
master_frame["State"] = state_list
master_frame["Zip Code"] = zip_code
master_frame["Primary Contact Name"] = primary_contact_name
master_frame["Primary Contact Email"] = primary_contact_email_address
master_frame["Phone Number"] = phone_number
master_frame["Fax Number"] = fax_number
master_frame["ACSI Page"] = school_page_url
master_frame["School Website"] = website_url
master_frame["Early Education Students"] = early_education_enrollment
master_frame["Elementary Students"] = elementary_enrollment
master_frame["Middle School Students"] = middle_school_enrollment
master_frame["High School Students"] = high_school_enrollment
master_frame["Total Students"] = total_enrollment
master_frame["I20 Compliant"] = i20
master_frame["Grade Levels Taught"] = grade_levels
master_frame["Year Founded"] = year_founded
master_frame["ACSI Accreditation Status"] = acsi_accreditation_status
master_frame["Grades Accredited"] = grades_accredited
master_frame["Other Accreditations"] = other_accreditation
master_frame["Special Needs"] = special_needs
master_frame["Boarding School"] = boarding_school
master_frame["EFL"] = efl
master_frame["Home School"] = home_school
master_frame["Online"] = online

print(master_frame.head(5))

# write frame to file
master_frame.to_csv("/Users/Steve/Dropbox/programming/Python/web-scraping/data/acsi_new.csv", encoding='utf-8', index=False)   

