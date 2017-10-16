import urllib2
from bs4 import BeautifulSoup
import pandas
import requests
base_url = "https://www.privateschoolreview.com"
state_list = ["alabama", "alaska", "arizona", "arkansas", "california", "colorado",
              "connecticut", "delaware", "district-of-columbia", "florida", "georgia", "hawaii",
              "idaho", "illinois", "indiana", "iowa", "kansas", "kentucky", "louisiana",
              "maine", "maryland", "massachusetts", "michigan", "minnesota", "mississippi",
              "missouri", "montana", "nebraska", "nevada", "new-hampshire", "new-jersey",
              "new-mexico", "new-york", "north-carolina", "north-dakota", "ohio", "oklahoma",
              "oregon", "pennsylvania", "rhode-island", "south-carolina", "south-dakota",
              "tennessee", "texas", "utah", "vermont", "virginia", "washington",
              "west-virginia", "wisconsin", "wyoming"
              ]
# declare lists
state_full_final = []
county_final = []
county_short_final = []
school_name_final = []
street_final = []
city_final = []
state_final = []
zip_code_final = []
phone_final = []
website_final = []
psr_webpage_final = []
grades_final = []
total_students_final = []
student_body_final = []
minority_final = []
teachers_final = []
s_t_ratio_final =[]
religion_final = []
year_founded_final = []
faculty_degree_final = []
class_size_final = []
act_final = []
tuition_final = []
acceptance_final = []
sports_final = []
extra_final = []
    
big_frame = pandas.DataFrame(columns=['State Full', 'County', 'School Name', 'Street Address',
'City', 'State', 'Zip Code', 'Phone Number', 'Website', 'Grades Offered', 
'Total Students', 'Student Body Type', 'Students of Color Percentage', 
'Total Classroom Teachers', 'Student-Teacher Ratio', 'Religious Affiliation', 
'Year Founded', 'Faculty with Advanced Degree Percentage', 'Average Class Size',
'Average ACT Score', 'Yearly Tuition Cost', 'Acceptance Rate', 'Total Sports Offered',
'Total Extracurriculars'])

for st in state_list:
    url = base_url + "/" + st
    opened_state = urllib2.urlopen(url)
    soup = BeautifulSoup(opened_state, "lxml")

    target_divs = soup.find_all("div", class_="school-type-list-text")

    county = []
    county_dirs = []
    for div in target_divs:
        county.append(div.find("div", class_="table_cell_county"))
    county = filter(None, county)  # get rid of empty divs
    
    for div in target_divs:
        county_dirs.append(div.find("div", class_="table_cell_county"))
    county_dirs = filter(None, county_dirs)  # get rid of empty divs
    
    for i in range(0, len(county)):  # overwrite county data with just the text
        county[i] = county[i].text.encode('utf-8')
    
    for k in range(0, len(county_dirs)):
        county_dirs[k] = county_dirs[k].find("a", href=True)['href']
        
    for i in range(0, len(county)):
        # county_url = base_url + "/" + st + "/" + county[i].lower().replace(' ', '-')
        county_url = base_url + county_dirs[i]
        print county_url
        opened_county = urllib2.urlopen(county_url)
        county_soup = BeautifulSoup(opened_county, "lxml")
        target_school_text = county_soup.find_all("div", class_="school-type-list-text")
        for d in target_school_text:
            if d.find("a", href=True) != None:
                school_url = base_url + d.find("a", href=True)['href']
                print school_url
                psr_webpage_final.append(school_url)
                state_full_final.append(st.title())
                county_final.append(county[i])
                opened_school = urllib2.urlopen(school_url)
                school_soup = BeautifulSoup(opened_school, "lxml")
                if school_soup.find("h1", id="main-headline") != None:
                    school_name = school_soup.find("h1", id="main-headline").text.encode('utf-8')
                    print school_name
                    school_name_final.append(school_name)
                else:
                    school_name = ''
                    school_name_final.append(school_name)
                if school_soup.find("span", itemprop="streetAddress") != None:
                    street_address = school_soup.find("span", itemprop="streetAddress").text.encode('utf-8')
                    print street_address
                    street_final.append(street_address)
                else:
                    street_address = ''
                    street_final.append(street_address)
                if school_soup.find("span", itemprop="addressLocality") != None:
                    city = school_soup.find("span", itemprop="addressLocality").text.encode('utf-8')
                    print city
                    city_final.append(city)
                else:
                    city = ''
                    city_final.append(city)
                if school_soup.find("span", itemprop="addressRegion") != None:
                    state_short = school_soup.find("span", itemprop="addressRegion").text.encode('utf-8')
                    print state_short
                    state_final.append(state_short)
                else:
                    state_short = ''
                    state_final.append(state_short)
                if school_soup.find("span", itemprop="postalCode") != None:
                    zipcode = school_soup.find("span", itemprop="postalCode").text.encode('utf-8')
                    print zipcode
                    zip_code_final.append(zipcode)
                else:
                    zipcode = ''
                    zip_code_final.append(zipcode)
                if school_soup.find("div", class_="top_card_ctn top_telephone_ctn") != None:
                    phone = school_soup.find("div", class_="top_card_ctn top_telephone_ctn").text.encode('utf-8')
                    phone = phone[(phone.find(' ')+1):len(phone)]
                    print phone
                    phone_final.append(phone)
                else:
                    phone = ''
                    phone_final.append(phone)
                website = school_soup.find("a", class_="website_click")
                if website != None:
                    website = website.text.encode('utf-8')
                    print website
                else:
                    website = ''
                website_final.append(website)
                details_table = school_soup.find("div", id="school_details_table")
                details_list = details_table.find_all("tr", id='school_membership_row')
                detail_list = filter(None, details_list)
                for e in range(0, len(details_list)):
                    details_list[e] = details_list[e].text.encode('utf-8')
                # print details_list
                for f in range(0, len(details_list)):
                    if "Grades Offered" in details_list[f]:
                        grades_raw_list = details_list[f].split('\n')
                        grades_offered = grades_raw_list[2]
                        print grades_offered
                        grades_final.append(grades_offered)
                        break
                    else:
                        if f == (len(detail_list)-1):
                            grades_offered = ''
                            grades_final.append(grades_offered)
                for f in range(0, len(details_list)):
                    if "Total Students" in details_list[f]:
                        students_raw_list = details_list[f].split('\n')
                        total_students = students_raw_list[2][0:students_raw_list[2].find(' ')]
                        print total_students
                        total_students_final.append(total_students)
                        break
                    else:
                        if f == (len(detail_list)-1):
                            total_students = ''
                            total_students_final.append(total_students)
                for f in range(0, len(details_list)):
                    if "Student Body Type" in details_list[f]:
                        body_type_raw_list = details_list[f].split('\n')
                        student_body = body_type_raw_list[2]
                        print student_body
                        student_body_final.append(student_body)
                        break
                    else:
                        if f == (len(detail_list)-1):
                            student_body = ''
                            student_body_final.append(student_body)
                for f in range(0, len(details_list)):
                    if "% Students of Color" in details_list[f]:
                        minority_raw_list = details_list[f].split('\n')
                        minority = minority_raw_list[5]
                        print minority
                        minority_final.append(minority)
                        break
                    else:
                        if f == (len(detail_list)-1):
                            minority = ''
                            minority_final.append(minority)
                for f in range(0, len(details_list)):
                    if "Total Classroom Teachers" in details_list[f]:
                        teachers_raw_list = details_list[f].split('\n')
                        teachers = teachers_raw_list[2][0:teachers_raw_list[2].find(' ')]
                        print teachers
                        teachers_final.append(teachers)
                        break
                    else:
                        if f == (len(detail_list)-1):
                            teachers = ''
                            teachers_final.append(teachers)
                for f in range(0, len(details_list)):
                    if "Student : Teacher Ratio" in details_list[f]:
                        stratio_raw_list = details_list[f].split('\n')
                        stratio = stratio_raw_list[2][0:stratio_raw_list[2].find('N')]
                        print stratio
                        s_t_ratio_final.append(stratio)
                        break
                    else:
                        if f == (len(detail_list)-1):
                            stratio = ''
                            s_t_ratio_final.append(stratio)
                for f in range(0, len(details_list)):
                    if "Religious Affiliation" in details_list[f]:
                        religious_raw_list = details_list[f].split('\n')
                        religious = religious_raw_list[2]
                        print religious
                        religion_final.append(religious)
                        break
                    else:
                        if f == (len(detail_list)-1):
                            religious = ''
                            religion_final.append(religious)
                for f in range(0, len(details_list)):
                    if "Year Founded" in details_list[f]:
                        founded_raw_list = details_list[f].split('\n')
                        founded = founded_raw_list[2]
                        print founded
                        year_founded_final.append(founded)
                        break
                    else:
                        if f == (len(detail_list)-1):
                            founded = ''
                            year_founded_final.append("founded")
                for f in range(0, len(details_list)):
                    if "Faculty w/Advanced Degree" in details_list[f]:
                        degree_raw_list = details_list[f].split('\n')
                        degree = degree_raw_list[5]
                        print degree
                        faculty_degree_final.append(degree)
                        break
                    else:
                        if f == (len(detail_list)-1):
                            degree = ''
                            faculty_degree_final.append(degree)
                for f in range(0, len(details_list)):
                    if "Average Class Size" in details_list[f]:
                        size_raw_list = details_list[f].split('\n')
                        class_size = size_raw_list[2][0:size_raw_list[2].find(' ')]
                        print class_size
                        class_size_final.append(class_size)
                        break
                    else:
                        if f == (len(detail_list)-1):
                            class_size = ''
                            class_size_final.append(class_size)
                for f in range(0, len(details_list)):
                    if "Average ACT score" in details_list[f]:
                        act_raw_list = details_list[f].split('\n')
                        act_score = act_raw_list[2]
                        print act_score
                        act_final.append(act_score)
                        break
                    else:
                        if f == (len(detail_list)-1):
                            act_score = ''
                            act_final.append(act_score)
                for f in range(0, len(details_list)):
                    if "Yearly Tuition Cost" in details_list[f]:
                        tuition_raw_list = details_list[f].split('\n')
                        tuition = tuition_raw_list[2][0:tuition_raw_list[2].find('V')]
                        print tuition
                        tuition_final.append(tuition)
                        break
                    else:
                        if f == (len(detail_list)-1):
                            tuition = ''
                            tuition_final.append(tuition)
                for f in range(0, len(details_list)):
                    if "Acceptance Rate" in details_list[f]:
                        acceptance_raw_list = details_list[f].split('\n')
                        acceptance = acceptance_raw_list[5]
                        print acceptance
                        acceptance_final.append(acceptance)
                        break
                    else:
                        if f == (len(detail_list)-1):
                            acceptance = ''
                            acceptance_final.append(acceptance)
                for f in range(0, len(details_list)):
                    if "Total Sports Offered" in details_list[f]:
                        sports_raw_list = details_list[f].split('\n')
                        sports = sports_raw_list[2][0:sports_raw_list[2].find(' ')]
                        print sports
                        sports_final.append(sports)
                        break
                    else:
                        if f == (len(detail_list)-1):
                            sports = ''
                            sports_final.append(sports)
                for f in range(0, len(details_list)):
                    if "Total Extracurriculars" in details_list[f]:
                        extra_raw_list = details_list[f].split('\n')
                        extracirricular = extra_raw_list[2][0:extra_raw_list[2].find(' ')]
                        print extracirricular
                        extra_final.append(extracirricular)
                        break
                    else:
                        if f == (len(detail_list)-1):
                            extracirricular = ''
                            extra_final.append(extracirricular)


# big_frame['State Full'] = state_full_final
# big_frame['County'] = county_final
# big_frame['School Name'] = school_name_final
# big_frame['Street Address'] = street_final
# big_frame['City'] = city_final
# big_frame['State'] = state_final
# big_frame['Zip Code'] = zip_code_final
# big_frame['Phone Number'] = phone_final
# big_frame['Website'] = website_final
# big_frame['Grades Offered'] = grades_final
# big_frame['Total Students'] = total_students_final
# big_frame['Student Body Type'] = student_body_final
# big_frame['Students of Color Percentage'] = minority_final #
# big_frame['Total Classroom Teachers'] = teachers_final
# big_frame['Student-Teacher Ratio'] = s_t_ratio_final
# big_frame['Religious Affiliation'] = religion_final
# big_frame['Year Founded'] = year_founded_final #
# big_frame['Faculty with Advanced Degree Percentage'] = faculty_degree_final
# big_frame['Average Class Size'] = class_size_final
# big_frame['Average ACT Score'] = act_final
# big_frame['Yearly Tuition Cost'] = tuition_final
# big_frame['Acceptance Rate'] = acceptance_final
# big_frame['Total Sports Offered'] = sports_final
# big_frame['Total Extracurriculars'] = extra_final

# big_frame.to_csv("state_summary.csv",
#                  encoding='utf-8', index=False)

