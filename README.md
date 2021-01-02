# mk-home-automation

`mk-home-automation` is an additional service for the *MK Home* ecosystem. It allows to receives the protocoled Tradfri light information from [mk-home-server](https://github.com/Mo0812/mk-home-server) and trains as model to predict weather a specific light bulb is turned on or off for a specific weekday and daytime.

It uses the tracked data of the `TradfriDataCollection` module of `mk-home-server` to do so. And trains a gradient boost model based on your own behavior of switching your connected lights in your home.

While this service alone only supports the training and prediction of light states for specific weekday/daytime combinations, the `Automator` module of `mh-home-server` enables to automatically control lights based on the prediction of this project in different modes.

To learn more about how `mk-home-automation` works look at section X of this README.

To learn more about how to use the automation functions in combination with `mk-home-server` look at the [specific section]() it the README of that project.