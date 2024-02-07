from selenium import webdriver 
from selenium.webdriver.firefox.options import Options 
from selenium.webdriver.common.by import By # Util that helps to select elements with XPath
import csv # CSV library that helps us save our result

options = Options() 
options.add_argument("--headless") # Run selenium under headless mode
 
driver = webdriver.Firefox(options=options) # Initialize the driver instance

filecsv = open('file.csv', 'w', encoding='utf8', newline='') #csv in windows adds an extra newline character, "newline" argument removes it
csv_columns = ['name', 'price', 'img', 'link']
writer = csv.DictWriter(filecsv, fieldnames = csv_columns)
writer.writeheader()

driver.get("https://scrapeme.live/shop/") 
pokemons = driver.find_elements(By.XPATH, "//*[@id='main']/ul/li")

for pokemon in pokemons:
    name = pokemon.find_element(By.XPATH, ".//h2").text
    price = pokemon.find_element(By.XPATH, ".//span").text
    img = pokemon.find_element(By.XPATH, ".//img").get_attribute("src")
    link = pokemon.find_element(By.XPATH, ".//a").get_attribute("href")

    writer.writerow({'name': name, 'price': price, 'img': img, 'link': link})

filecsv.close()
driver.close()
