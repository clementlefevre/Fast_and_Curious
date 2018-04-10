## Fast and Curious


### Concept
- Using a Raspberry Pi + webcam, record the speed of the vehicles driving in my street.
- Label the training set using my own tool (**Mechanical French**)
- Then, apply an image classifier (Tensforflow convnet) to generate stats per vehicle category.
- Finally, implement a Dashboard for the processed data & Look for correlation with other data (weather, time slot, events)


### Tools
- For speed calculation, on the shelf library (**speedcam**)[https://github.com/pageauc/speed-camera], using opencv **mean_shift** method.
- For vehicles classification : standard keras wrapper on tensorflow with image augmentation.


### As of 2018_04_06

- 20000 vehicle's speeds recorded
- Validation accuracy on a binary classifier (_car vs bike_) : 95%
