## Fast and Curious

![alt text](https://github.com/clementlefevre/Fast_and_Curious/blob/master/SpeedCamFlowChart.png "Logo Title Text 1")


### Concept
- Using a Raspberry Pi + webcam, record the speed of the vehicles driving in my street.
- Label the training set using my own tool (**Mechanical French**)
- Then, apply an image classifier (Tensorflow convnet) to generate stats per vehicle category.
- Finally, implement a Dashboard for the processed data & Look for correlation with other data (weather, time slot, events)


### Tools
- For speed calculation, on the shelf library [**speedcam**](https://github.com/pageauc/speed-camera), using opencv **mean_shift** method.
- For vehicles classification : standard keras wrapper on tensorflow with image augmentation, applying standard CNN layers layout.


### As of 2018_04_06

- 30000 vehicle's speeds recorded, 18000 manually classified.
- Validation accuracy on a binary classifier (_car vs bike_) : 97%

### Some visualizations [here](https://github.com/clementlefevre/Fast_and_Curious/blob/master/speedcam.md)
