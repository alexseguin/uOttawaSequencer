#!/usr/bin/env python
# -*- coding: utf-8 -*-

#################################################
#					IMP0RTS					    #
#################################################

from selenium import webdriver 										# launch and initiate browser
from selenium.webdriver.common.by import By 						# parameter searches
from selenium.webdriver.support.ui import WebDriverWait 			# Wait for page load
from selenium.webdriver.support import expected_conditions as EC 	# Specify load condition
from selenium.common.exceptions import TimeoutException				# Look at the name

#################################################
#					IMP0RTS					    #
#################################################

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

# Find table within HTML contents
table_body = browser.find_element_by_xpath("//tbody")

# Iterate throught all the rows of the table
for row in table_body.find_elements_by_xpath(".//tr")[1:]:
	
	#############
	# NEXT STEP #  =======> refactor script into functions and create class object, store all objects into set
	#############			and then will eventually move into other storage once script is completed

		print row.find_elements_by_xpath(".//td[@class='Term']")[0].text # TERM COLUMN
		print row.find_elements_by_xpath(".//a")[0].text # COURSE CODE COLUMN -> will eventually have to navigate to link and scrape that
		print row.find_elements_by_xpath(".//td[@class='CourseTitle']")[0].text # TITLE COLUMN

	#for col in row.find_elements_by_xpath(".//td"):
	#	print col.text