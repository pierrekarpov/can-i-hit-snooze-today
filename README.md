# Can I hit snooze today?
Estimates the likelihood that there isn't traffic today, and that I can safely hit snooze and not be late for work.

## General idea
For this project, we will get data from [Data.gov.sg](https://data.gov.sg/developer). Namely, we will use their [traffic images API](https://data.gov.sg/dataset/traffic-images). Based on that data set, we will then generate reports on how many cars are at which location, and at what time. In turn, that will allow us to predict how many car there will be for my morning commute. We will be able to estimate whether hitting snooze is safe or not.

## Project pipeline

1. [x] Get and store images from [traffic images API](https://data.gov.sg/dataset/traffic-images) ([script](scripts/get_images.py))
2. [x] Build tool to classify part of an image ([script](scripts/make_selections.py))
3. [x] Go through our image library, classify a lot of examples car/no car
4. [x] Go through classified data, crop and resize selections out of original pictures ([script](scripts/crop_selections.py))
5. [x] Write code to build, train, and test my own deep NNs ([script1](scripts/nn.py)) ([script2](scripts/deep_nn_step_by_step.py))
6. [x] Train CNN to detect whether car/no car ([script](scripts/car_detection.py))
7. [x] Use sliding doors technique to detect the car sections in pictures ([script](scripts/sliding_doors.py))
8. [x] Estimate how many cars in pictures with neighborhood counting ([script](scripts/count_clusters.py))
9. [x] Use the images from [traffic images API](https://data.gov.sg/dataset/traffic-images) for the times and locations of my commute specifically. ([script](scripts/location_time_series.py))
10. [x] Build time series with how many cars, at what time, and where. ([script](scripts/location_time_series.py))
11. [x] Run ARIMA algorithm to estimate whether or not there will be traffic today. ([script](scripts/time_series_prediction.py))
12. [ ] (WIP) Snooze peacefully 😴😴😴

## Comparison analysis
A lot of these algorithms will be build from scratch. Once the project is finished and running, it would be interesting to compare how they hold versus the standard libraries'.


## Other approaches to try
* Webcrawler to get traffic data for google maps
* Perform image difference (background extraction) to count how many cars
* Time commute everyday and interpolate from there how long it takes
* LTSM vs ARIMA (LTSM requires a lot of data to perform well, but handles trends and seasons better)

## Future plans
* Run scripts automatically
* Notification system when the user wakes up
* Parameterizasion for user people to use it in other regions of Singapore
* Plateform where people can sign up, and receive notifications as they wake up
* Mobile app for alarm clock, that will automatically readjust based on traffic
