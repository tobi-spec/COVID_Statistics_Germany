
## Modelling of COVID-19 ICU patients in Germany  
  
  
### Quick start ####
install requirements.txt  
run COVID_DIVI_crawler.py  
run COVID_DIVI_analyzer.py  
you get a chart with course of COVID-19 ICU Patients in Germany  
  
-------------------------  
  
This repository contains a crawler which downloads all daily report files about COVID-19 cases. Provided by the German DIVI institute for intensive care.  
The data can be visualized by an analyzer to plot the data course as a line chart.  
Unittests for testing the program functionalities are also to find in COVID_unittests.py.  
  
#### Further improvements ####
- Plot dosent show in Bash/ Ubuntu shell
- switching from Beautifulsoup library to scrapy framework  
- adding data analyses for data from RKI (Robert-Koch-Institut)