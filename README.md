# phase_4_project
Timi, Brian, Tim's phase 4 Flatiron Project

# LOCATION FORECASTING USING TIME SERIES FORECASTING

![](Figures/178b9290b3d3016ae511d862d0620987.png)


## STAKEHOLDER AND BUSINESS UNDERSTANDING 
Our firm, BTT Consulting has been hired by a real estate property company, OVATION REAL ESTATE. They are looking to invest in five(5) new locations 
around the country. They want locations that assure them of immediate profitability and return on investment. We are focusing on the average return on investment of properties to arrive at our recommended locations.

## DATA  &  DATA ANALYSIS
We are making use of Zillow Research data sourced from the Zillow website. The dataset encompasses mean monthly property values in close to 15,000 
zip codes spread around the country from April, 1996 up to April, 2018. We aggregated the data by quarter to arrive at the return on investment (ROI) over 
each quarter. Making use of quarterly Returns on Investment, we were able to arrive at first, the state with the highest ROI, then we narrowed it down to 
metro, county and finally the best performing cities.  

## MODELING
We carried out the bulk of our analyses using Time Series forecasting. 

### Baseline Model
Our baseline model was a Naive Forecast, which was merely a carry-over of the current values of property into the next quarter. This model assumes all
conditions remaining constant, the present mean values we had in our dataset will remain unchanged over the next fiscal quarter. Using Root Mean Square error as our metric of choice, we had a value of 0.0103 (1.03%) for this model. This model did not satisfy our questions concerning volatility in the real estate sector.


### First Model
The first model is an ARIMA model(incorporating Walk-forward modelling). Using the most recent ROIs, we ran a forecast to have an idea of the expected ROIs on the zipcodes in our dataset over the next financial quarter. This model takes into consideration the property values in previous lags (times periods) and trends or seasonality effects over the same periods. Of note is the 2008 Housing Bust which could potentially distort the forecast of the best designed model. We arrived at Delaware as the state with the highest ROI, New Castle County and the five best performing cities in the county as potential locations of choice. This model had an RMSE of 0.00725 (~0.73%). While this model is significantly more reliable than the baseline model, we designed a second to overcome any shortcomings we had with this model.
![](Figures/model1_Bear_ROI.png)

### Second Model
Our second model took a different approach from the first, but also incorporates the walk-forward optimization. This time we used a tiered system to pick locations from the first model. This model produced better results than the first model, and is computationally less-intensive. The model predicted Stapleton, Baldwin AL as the best-performing city nationwide with a mean ROI of 4.7% over the next fiscal quarter. However, we could not adopt the results of this model because it came in late.

![](Figures/model2_Stapleton_ROI.png)

## Conclusions:
In conclusion, we are recommending the following:
- With the highest ROI of all the states, we are recommending setting up in Delaware
- Our model forecasted the New Castle county as having the highest sustained ROI over the next fiscal quarter
- We recommend the following 5 cities having the highest ROIs in New Castle county: 
     - Bear (~3.1% ROI)
     - Claymont (~1.0% ROI)
     - Newport (~0.9% ROI)
     - Wilmington (~0.7% ROI), and 
     - New Castle (~0.6% ROI)

## Future Considerations:
Looking forward, we would like to incorporate the following into our model as we feel these can give us some more insight:
- The market volume 
- Operating costs and overheads
