"""Module for getting the address of all Service Canada Centers"""

import csv # CSV library that helps us save our result
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By # Util that helps to select elements with XPath
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException

options = Options()
options.add_argument("--headless") # Run selenium under headless mode

driver = webdriver.Firefox(options=options) # Initialize the driver instance
driver.implicitly_wait(10) #tell the driver to wait if the javascript hasn't loaded yet

filecsv = open('center_locations.csv', 'w', encoding='utf8', newline='')
#csv in windows adds an extra newline character, "newline" argument removes it

csv_columns = [
    'region', #province or territory
    'center_code', #string found in url that uniquely identifies center
    'page_header', #name of center
    'link', #link to center's page
    'address', #address from the center's page
    'postal_code' #center postal code
    ] 
writer = csv.DictWriter(filecsv, fieldnames = csv_columns)
writer.writeheader()

center_links = [] #initialize a list for the centers in a region

#these are the province & territory (region) 2 letter codes in Canada
regions = ['BC', 'AB', 'SK', 'MB', 'ON', 'QC', 'NB', 'NS', 'PE', 'NL', 'YT', 'NU', 'NT']

#Single region test:
#regions = ['SK']

max_attempts = 3 #maximum number of attempts in case page doesn't load


for region in regions:
    print(region) #keep track of which region is being processed

    driver.get(f"https://www.servicecanada.gc.ca/tbsc-fsco/sc-lst.jsp?prov={region}&lang=eng")
    centers = driver.find_elements(By.XPATH, "/html/body/main/ul//a") 
    #note element's' plural generates list of elements

    #get the link for each center on that region's main page, then add to a list
    for center in centers:
        link = center.find_element(By.XPATH, ".").get_attribute("href")
        center_links.append(link)

    #access the page from the list of links and get information from it   
    for center_page in center_links:
        attempt = 0

        while attempt < max_attempts:
            attempt += 1
            try:
                start_index = center_page.index("rc=") + 3
                end_index = center_page.index("&lang")
                center_code = center_page[start_index:end_index]
                
                driver.get(center_page) #navigate to page

                header = driver.find_element(By.XPATH, "//h1[@property='name']").text
                
                address = driver.find_element(By.XPATH, "/html/body/main//div[@class='row-BI']/div[@class='col-xs-10'][1]").text
                trim_address = address.replace('\n', ', ')
                postal_code = address[-6:]
                
                print(f'{header} ok')
                writer.writerow({'region': region, 
                                 'center_code': center_code,
                                 'page_header': header, 
                                 'link': center_page, 
                                 'address': trim_address,
                                 'postal_code':postal_code})
                
                break #get out of attempt 'while' loop if everything works to here

            except NoSuchElementException:
                print(f"Element not found in {center_page}, refreshing the page and retrying...")
                driver.refresh()  # Refresh the page
                continue  # Retry the operation

    center_links = [] #reinitialize center_links when done with a region

filecsv.close()
driver.quit()
