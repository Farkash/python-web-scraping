import urllib2
from bs4 import BeautifulSoup
import pandas
import requests

base_url = "http://www.ecfa.org"
search_url = "/MemberSearch.aspx"

state_short = [
    "AL", "AK", "AZ", "AR"
, 
"CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL"
, 
"IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV"
, 
"NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX"
, 
"UT", "VT", "VA", "WA", "WV", "WI", "WY"
			]

state_url_query_string = "?State="

# instantiate an empty list to house all the tables, one for each state
soup_cauldron = []

for st in state_short:
    url = base_url + search_url + state_url_query_string + st
    opened_state = urllib2.urlopen(url)
    soup = BeautifulSoup(opened_state, "lxml")
    # find_all makes a list, I don't want a list, I just want the table to be stored temporarily
    # I want to append the table found on each state page into a list of all state pages
    target_table = soup.find("table", id="BaseContent_Content_GridViewData")
    # push target_table to a big list
    soup_cauldron.append(target_table)

# in order to be able to precisely extract each data point, you need 
# to make lists of the <td> table data tags first

# make a control structure that loops through and assigns findings 
# to global lists, don't try to actually make complex list structure that 
# may be hard to index later.
# so say for each table in soup_cauldron, make a list of the rows
# then for each row in that list, make a list of the table data items (cells)
# then index each item of that small list and write it to global lists for each type
# that can be strung together later as columns in a pandas frame

# initialize the global lists
ministry = []
type = []
city = []
state = []
ministry_url_suffix = []

for table in soup_cauldron:
    row_list = table.find_all("tr")
    del row_list[0] # kill the header row for each table, don't want it
    for row in row_list:
        cell_list = row.find_all("td")
        ministry_url_suffix.append(cell_list[0].find("a", href=True)['href'])
        for f in range(0, len(cell_list)):
            cell_list[f] = cell_list[f].text.encode('utf-8').replace("\n", "").replace("\t", "").replace("\r", "")        
        ministry.append(cell_list[0])
        type.append(cell_list[1])
        city.append(cell_list[2])
        state.append(cell_list[3])

# now, add in all the nice detailed data about each organization
# not all orgs will have all the same data, so find all the possible fields,
# and parse through the soup for them. Then check to see if they're null (nonetype)
# before pushing them to the global lists, and change them to "" if they are.

phone = []
fax = []
website = []
top_leader = []
donor_contact = []
total_revenue = []
total_expenses = []
total_assets = []
total_liabilities = []
net_assets = []
reporting_period = []
year_founded = []
membership_start_date = []

for m in range(0, len(ministry_url_suffix)):
    if m != 844:
        ministry_page_url = base_url + "/" + ministry_url_suffix[m]
        opened_profile = urllib2.urlopen(ministry_page_url)
        profile_html = BeautifulSoup(opened_profile, "lxml")
        print ministry_page_url
        print m
        if profile_html.find("span", id="BaseContent_Content_lblContactInfoPhone") != None:
            t_phone = profile_html.find("span", id="BaseContent_Content_lblContactInfoPhone").text.encode("utf-8")
            phone.append(t_phone)
        else:
            phone.append("")
        if profile_html.find("span", id="BaseContent_Content_lblContactInfoFax") != None:
            t_fax = profile_html.find("span", id="BaseContent_Content_lblContactInfoFax").text.encode("utf-8")
            fax.append(t_fax)
        else:
            fax.append("")
        if profile_html.find("span", id="BaseContent_Content_lblContactInfoWebsite") != None:
            t_website = profile_html.find("span", id="BaseContent_Content_lblContactInfoWebsite").find("a", href=True)['href'] 
            website.append(t_website)
        else:
            website.append("")
        if profile_html.find("span", id="BaseContent_Content_lblContact") != None:
            t_top_leader = profile_html.find("span", id="BaseContent_Content_lblContact").text.encode("utf-8")
            top_leader.append(t_top_leader)
        else:
            top_leader.append("")
        if profile_html.find("span", id="BaseContent_Content_lblContact") != None:
            t_donor_contact = profile_html.find("span", id="BaseContent_Content_lblContact").text.encode("utf-8")
            donor_contact.append(t_donor_contact)
        else:
            donor_contact.append("")
        if profile_html.find("span", id="BaseContent_Content_lblTotalRevenue") != None:
            t_total_revenue = profile_html.find("span", id="BaseContent_Content_lblTotalRevenue").text.encode("utf-8")
            total_revenue.append(t_total_revenue)
        else:
            total_revenue.append("")
        if profile_html.find("span", id="BaseContent_Content_lblTotalExpenses") != None:
            t_total_expenses = profile_html.find("span", id="BaseContent_Content_lblTotalExpenses").text.encode("utf-8")
            total_expenses.append(t_total_expenses)
        else:
            total_expenses.append("")
        if profile_html.find("span", id="BaseContent_Content_lblTotalAssets") != None:
            t_total_assets = profile_html.find("span", id="BaseContent_Content_lblTotalAssets").text.encode("utf-8")
            total_assets.append(t_total_assets)
        else:
            total_assets.append("")
        if profile_html.find("span", id="BaseContent_Content_lblTotalLiabilities") != None:
            t_total_liabilities = profile_html.find("span", id="BaseContent_Content_lblTotalLiabilities").text.encode("utf-8")
            total_liabilities.append(t_total_liabilities)
        else:
            total_liabilities.append("")
        if profile_html.find("span", id="BaseContent_Content_lblNetAssets") != None:
            t_net_assets = profile_html.find("span", id="BaseContent_Content_lblNetAssets").text.encode("utf-8")
            net_assets.append(t_net_assets)
        else:
            net_assets.append("")
        if profile_html.find("span", id="BaseContent_Content_lblDataForYearEnded") != None:
            t_reporting_period = profile_html.find("span", id="BaseContent_Content_lblDataForYearEnded").text.encode("utf-8")
            reporting_period.append(t_reporting_period)
        else:
            reporting_period.append("")
        if profile_html.find("span", id="BaseContent_Content_lblHeadingFounded") != None:
            t_year_founded = profile_html.find("span", id="BaseContent_Content_lblHeadingFounded").text.encode("utf-8")
            year_founded.append(t_year_founded)
        else:
            year_founded.append("")
        if profile_html.find("span", id="BaseContent_Content_lblMemberSince") != None:
            t_membership_start_date = profile_html.find("span", id="BaseContent_Content_lblMemberSince").text.encode("utf-8")
            membership_start_date.append(t_membership_start_date)
        else:
            membership_start_date.append("")



print len(phone)
print len(fax)
print len(website)
print len(top_leader)
print len(donor_contact)
print len(total_revenue)
print len(total_expenses)
print len(total_assets)
print len(total_liabilities)
print len(net_assets)
print len(reporting_period)
print len(year_founded)
print len(membership_start_date)



master_frame = pandas.DataFrame()

master_frame['Name of Organization'] = ministry
master_frame["City"] = city
master_frame["State"] = state
master_frame["Phone Number"] = phone
master_frame["Fax Number"] = fax
master_frame["Website"] = website
master_frame["Top Leader"] = top_leader
master_frame["Donor Contact"] = donor_contact
master_frame["Membership Type"] = type
master_frame["Total Revenue"] = total_revenue
master_frame["Total Expenses"] = total_expenses
master_frame["Total Assets"] = total_assets
master_frame["Total Liabilities"] = total_liabilities
master_frame["Net Assets"] = net_assets
master_frame["Reporting Period"] = reporting_period
master_frame["Year Founded"] = year_founded
master_frame["Membership Start Date"] = membership_start_date


print master_frame


# ---------de-bugging-------------
for m in range(0, len(ministry_url_suffix)):
    ministry_page_url = base_url + "/" + ministry_url_suffix[m]
    r = requests.get(ministry_page_url)
    print r
    print ministry_page_url

print len(ministry_url_suffix)

print ministry_url_suffix[844]

