# Can I hit snooze today?
Estimates the likelihood that there isn't traffic today, and that I can safely hit snooze and not be late for work.

## General idea
For this project, we will get data from [Data.gov.sg](https://data.gov.sg/developer). Namely, we will use their [traffic images API](https://data.gov.sg/dataset/traffic-images). Based on that data set, we will then generate reports on how many cars are at which location, and at what time. In turn, that will allow us to predict how many car there will be for my morning commute. We will be able to estimate whether hitting snooze is safe or not.

## Project pipeline

1. [x] Get and store images from [traffic images API](https://data.gov.sg/dataset/traffic-images) ([script](scripts/get_images.py))
2. [ ] Automatically and periodically get data from [traffic images API](https://data.gov.sg/dataset/traffic-images) for all locations, and all times.
3. [x] Build tool to classify part of an image ([script](scripts/make_selections.py))
4. [x] Go through our image library, classify a lot of examples car/no car
5. [x] Go through classified data, crop and resize selections out of original pictures ([script](scripts/crop_selections.py))
6. [x] Write code to build, train, and test my own deep NNs ([script1](scripts/nn.py)) ([script2](scripts/deep_nn_step_by_step.py))
7. [x] Train CNN to detect whether car/no car ([script](scripts/car_detection.py))
8. [x] Use sliding doors technique to detect the car sections in pictures ([script](scripts/sliding_doors.py))
9. [x] Estimate how many cars in pictures with neighborhood counting ([script](scripts/count_clusters.py))
10. [ ] Use the images from [traffic images API](https://data.gov.sg/dataset/traffic-images) for the times and locations of my commute specifically.
11. [ ] Build time series with how many cars, at what time, and where.
12. [ ] Run LSTM algorithm to estimate whether or not there will be traffic today.
13. [ ] Snooze peacefully 😴😴😴

## Comparison analysis
All the algorithms will be build from scratch. Once the project is finished and running, it would be interesting to compare how our algorithms hold versus the standard libraries'.


## Other approaches to try
* Webcrawler to get traffic data for google maps
* Perform image difference (background extraction) to count how many cars
* Time commute everyday and interpolate from there how long it takes

## Future plans
* Run scripts automatically
* Notification system when the user wakes up
* Parameterizasion for user people to use it in other regions of Singapore
* Plateform where people can sign up, and receive notifications as they wake up
* Mobile app for alarm clock, that will automatically readjust based on traffic
