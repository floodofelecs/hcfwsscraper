# Harris County Flood Warning System (HCFWS) Web Scraper 
A web scraper created using Python, selenium, pandas, and beautifulsoup. 

The scraper currently scrapes the 5-minute interval data every day from 12pm of the day it is the running back to 12pm the day before. It then appends the data. The data is arranged where each sheet name is the sensor number, and the file name is the bayou the sensor belongs to. Thus, there will be a number of files, each corrresponding to a bayou, and within each file there are sheets corresponding to sensors in that bayou. 
