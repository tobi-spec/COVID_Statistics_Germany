
## Modelling of COVID-19 ICU patients in Germany  
  
  
### Quick start ####
install requirements.txt  
run COVID_scraper.py  
run COVID_analyzer.py  
A chart with the courses of daily infections, occupancy of intensiv care units and daily deaths will occure.
All data refers to the COVID-19 pandemic in germany
  
-------------------------  
  
This repository contains a scraper which downloads all daily report files about the COVID-19 pandemic provided by the Robert-Koch-Institut (RKI) (www.rki.de).
Data is stored in a csv file provided by RKI (https://www.arcgis.com/home/item.html?id=f10774f1c63e40168479a1feb6c7ca74) (.
Also the repository contains data about ICU COVID-19 cases in Germany, provided by the german DIVI institute for intensive care (https://www.divi.de/) (https://www.divi.de/divi-intensivregister-tagesreport-archiv-csv?layout=table).  
The program visualizes the daily infections, occupancy of intensiv care untits and daily deaths in line plots. 
Unittests for testing the program functionalities are also to find in COVID_unittests.py, but it is to mention that in current state of the project all unittests have to be redesigned because of major changes in programm architecture   
  
#### Further improvements ####
- implement unitests again
- change minor misscalculations in new infections and new deaths
- implement input() function to create console commands 
- create more plots :) 
- switche from Beautifulsoup library to scrapy framework for faster scrape  
