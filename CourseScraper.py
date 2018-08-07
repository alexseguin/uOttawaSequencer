#!/usr/bin/env python
# -*- coding: utf-8 -*-

#################################################
#			IMPORT			#
#################################################

from selenium import webdriver 						# launch and initiate browser
from selenium.webdriver.common.by import By 				# parameter searches
from selenium.webdriver.support.ui import WebDriverWait 		# Wait for page load
from selenium.webdriver.support import expected_conditions as EC 	# Specify load condition
from selenium.common.exceptions import TimeoutException			# Look at the name

import psycopg2								# db connector import

#################################################
#			CODE			#
#################################################

# open db connection
conn = psycopg2.connect(database="sequencer", user = "postgres", password = "password", host = "127.0.0.1", port = "5432")
cur = conn.cursor()

# set selenium timeoute for specific element load
timeout = 15

# Set browsing mode to incognito
option = webdriver.ChromeOptions()
option.add_argument(" — incognito")

# Create chrome browser instance using chromedriver
browser = webdriver.Chrome(executable_path='files/chromedriver', chrome_options=option)

# Open browser instance
browser.get("https://web30.uottawa.ca/v3/SITS/timetable/Search.aspx")

# Wait for required input button to be loaded 
# exit if it isn't found
try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//input[@type='submit']")))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()

# loaded page is an ASP.NET search page which returns tables containing all courses
# first step to scraping the information is submitting a search for all courses
# the default search options are to search for this, thus click submit

submit_button = browser.find_element_by_xpath("//input[@type='submit']")
submit_button.click()


counter = 0
# Iterate through all the pages of the website (break condition within loop)
while(1):
	# Find table within HTML contents
	table_body = browser.find_element_by_xpath("//tbody")

	# Iterate throught all the rows of the table
	for row in table_body.find_elements_by_xpath(".//tr")[1:]:
		counter = counter + 1

		#############
		# NEXT STEP #  =======> refactor script into functions and create class object, store all objects into set
		#############			and then will eventually move into other storage once script is completed
		term = row.find_elements_by_xpath(".//td[@class='Term']")[0].text # TERM COLUMN
		code =  row.find_elements_by_xpath(".//a")[0].text # COURSE CODE COLUMN -> will eventually have to navigate to link and scrape that
		title = row.find_elements_by_xpath(".//td[@class='CourseTitle']")[0].text # TITLE COLUMN
		faculty = row.find_elements_by_xpath(".//td[@class='Faculty']")[0].text # FACULTY COLUMN
		department = row.find_elements_by_xpath(".//td[@class='Department']")[0].text # Department COLUMN

		print str(counter) + " - " + str(code)
		
		# Insert new course only if course doesn't exist already
		# Sections are listed as seperate courses 
		cur.execute("\
				INSERT INTO courses (code,title,term,faculty,department)\
				SELECT %(code)s, %(title)s, %(term)s, %(faculty)s, %(department)s\
				WHERE NOT EXISTS (SELECT * FROM courses WHERE code = %(code)s);", 
				{"code": code, "title": title, "term": term, "faculty": faculty, "department": department}
			)
	
	conn.commit()
	# emulating a do while loop
	if(len(browser.find_elements_by_xpath("//*[contains(text(), 'Next')]")) < 1):
		conn.close()
		break

	# next page
	browser.find_elements_by_xpath("//*[contains(text(), 'Next')]")[0].click()


