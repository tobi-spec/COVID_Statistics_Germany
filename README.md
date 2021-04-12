
## Modelling of COVID-19 ICU patients in Germany  
  
  
### Quick start ####
install requirements.txt  
run COVID_DIVI_scraper.py  
run COVID_DIVI_analyzer.py  
A chart with course of COVID-19 ICU Patients in Germany will be saved in the folder  
  
-------------------------  
  
This repository contains a scraper which downloads all daily report files about ICU COVID-19 cases in Germany. 
Provided by the german DIVI institute for intensive care (https://www.divi.de/).  
The data can be visualized by an analyzer to plot the data course as a line chart.  
Unittests for testing the program functionalities are also to find in COVID_unittests.py.  
  
#### Further improvements ####
- switching from Beautifulsoup library to scrapy framework  
- adding data analyses for data from RKI (Robert-Koch-Institut)