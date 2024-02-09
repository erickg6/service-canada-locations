"""Module for getting the address of a Service Canada Center"""

import csv # CSV library that helps us save our result
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By # Util that helps to select elements with XPath

options = Options()
#options.add_argument("--headless") # Run selenium under headless mode

driver = webdriver.Firefox(options=options) # Initialize the driver instance
driver.implicitly_wait(10) #tell the driver to wait if the javascript hasn't loaded yet

filecsv = open('file-pages.csv', 'w', encoding='utf8', newline='')
#csv in windows adds an extra newline character, "newline" argument removes it

csv_columns = ['region', 'page-header', "link", "address"]
writer = csv.DictWriter(filecsv, fieldnames = csv_columns)
writer.writeheader()

center_links = [] #initialize a list for the centers in a region

regions = ['BC', 'AB', 'SK', 'MB', 'ON', 'QC', 'NB', 'NS', 'PE', 'NL', 'YT', 'NU', 'NT']
#regions = ['SK']


for region in regions:
    print(region)

    driver.get("https://www.servicecanada.gc.ca/tbsc-fsco/sc-lst.jsp?prov="+region+"&lang=eng")
    centers = driver.find_elements(By.XPATH, "/html/body/main/ul//a") #note element's' plural generates list of elements

    for center in centers:
        link = center.find_element(By.XPATH, ".").get_attribute("href")
        center_links.append(link)

    for center_page in center_links:
        driver.get(center_page)
        header = driver.find_element(By.XPATH, "//h1[@property='name']").text
        address = driver.find_element(By.XPATH, "/html/body/main//div[@class='row-BI']/div[@class='col-xs-10'][1]").text
        writer.writerow({'region': region, 'page-header': header, 'link': center_page, 'address': address})

    center_links = [] #reinitialize center_links when done with a region

filecsv.close()
driver.close()
