 
### Modelling of COVID-19 epidemiological data in Germany

### run server ###
to run server:

$ export FLASK_APP=FetchController.py
$ export FLASK_ENV=development
$ flask run
-------------------------
  
This programm contains a scraper which downloads all daily report files about the COVID-19 pandamic provided by the Robert-Koch-Institut (RKI) (www.rki.de)
Data is stored in a csv file provided by RKI (https://www.arcgis.com/home/item.html?id=f10774f1c63e40168479a1feb6c7ca74)
Also theprogramm will download data about ICU COVID-19 cases in Germany, provided by the german DIVI institute for intensive care (https://www.divi.de/).  
The programm visualizes  the daily new infections, the daily infections, occupancy od intensiv care untits and daily deaths in line plots. 
  
#### Further improvements ####
- implement comand line interface
- changing minor misscalculations in new infections and new deaths
- creating more plots :) 
  
