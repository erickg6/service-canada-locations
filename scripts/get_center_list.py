"""module for getting a simple list of Service Canada Centers

output file is called center_info"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By # Util that helps to select elements with XPath
import csv # CSV library that helps us save our result

#This script only gets links and info from the Service Canada page specific to a province or territory.

options = Options() 
options.add_argument("--headless") # Run selenium under headless mode

driver = webdriver.Firefox(options=options) # Initialize the driver instance

filecsv = open('center_info.csv', 'w', encoding='utf8', newline='') #csv in windows adds an extra newline character, "newline" argument removes it
csv_columns = ['region','center-type', 'center-lang', 'name','link']
writer = csv.DictWriter(filecsv, fieldnames = csv_columns)
writer.writeheader()

regions = ['BC', 'AB', 'SK', 'MB', 'ON', 'QC', 'NB', 'NS', 'PE', 'NL', 'YT', 'NU', 'NT']

for region in regions:
    print(region)

    driver.get(f"https://www.servicecanada.gc.ca/tbsc-fsco/sc-lst.jsp?prov={region}&lang=eng") 
    centers = driver.find_elements(By.XPATH, "/html/body/main/ul//a")

    for center in centers:
        name = center.find_element(By.XPATH, ".").text
        ctype = center.find_element(By.XPATH, "./ancestor::ul[2]/preceding::h2[1]").text
        clang = center.find_element(By.XPATH, "./ancestor::ul[1]/preceding::strong[1]").text
        link = center.find_element(By.XPATH, ".").get_attribute("href")

        writer.writerow({'region': region, 'center-type': ctype, 'center-lang': clang, 'name': name, 'link': link})

filecsv.close()
driver.close()