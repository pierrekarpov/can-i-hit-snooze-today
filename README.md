# Can I hit snooze today?
Estimates the likelihood that there isn't traffic today, and that I can safely hit snooze and not be late for work.

## General idea
For this project, we will get data from [Data.gov.sg](https://data.gov.sg/developer). Namely, we will use their [traffic images API](https://data.gov.sg/dataset/traffic-images). Based on that data set, we will then generate reports on how many cars are at which location, and at what time. In turn, that will allow us to predict how many car there will be for my morning commute. We will be able to estimate whether hitting snooze is safe or not.

## Project pipeline

1. Get and store images from [traffic images API](https://data.gov.sg/dataset/traffic-images) [DONE]
2. Automatically and periodically get data from [traffic images API](https://data.gov.sg/dataset/traffic-images) for all locations, and all times.
3. Build tool to classify part of an image [DONE]
4. Go through our image library, classify a lot of examples car/no car
5. Train CNN to detect whether car/no car
6. Go through our image library, label how many cars in each picture.
7. Test CNN detect the correct number of cars
8. Use the images from [traffic images API](https://data.gov.sg/dataset/traffic-images) for the times and locations of my commute specifically.
9. Build time series with how many cars, at what time, and where.
10. Run LSTM algorithm to estimate whether or not there will be traffic today.
11. Snooze peacefully 😴😴😴

## Comparison analysis
All the algorithms will be build from scratch. Once the project is finished and running, it would be interesting to compare how our algorithms hold versus the standard libraries'.
