# Service Canada Locations

This is an effort to create a machine-readable dataset of geolocated Service Canada service centres.

Goals
- use python to write a script to scrape service canada locations from the internet
- geolocate all service canada locations using an API or other web service
- maintain this script through github, make publicly available

Service canada locations are here: https://www.servicecanada.gc.ca/tbsc-fsco/sc-hme.jsp?lang=eng

Using Geocoder.ca to lookup latitude and longitude based on postal codes. This isn't ideal, but it's fast and free, and it should serve for a national or regional scale map.

Split the process into 2 main scripts to run.
1. get_addresses.py will generate the list of centers and addresses and export to a CSV file.
2. get_geo_coords.py will add latitude and longitude columns to the previous file and output a new CSV file.

get_center_list.py was my first attempt at just scraping the list of centers from each provincial / territorial page. it has some extra info like languages and the type of center.

postal_code_lookup.py is the module that connects to Geocoder.ca and looks up the lat / long for get_geo_coords.py