# mk-home-automation

*mk-home-automation* is an additional service for the *MK Home* ecosystem. It allows to receives the protocoled Tradfri light information from [mk-home-server](https://github.com/Mo0812/mk-home-server) and trains as model to predict weather a specific light bulb is turned on or off for a specific weekday and daytime.

It uses the tracked data of the `TradfriDataCollection` module of `mk-home-server` to do so. And trains a gradient boost model based on your own behavior of switching your connected lights in your home.

While this service alone only supports the training and prediction of light states for specific weekday/daytime combinations, the `Automator` module of *mk-home-server* enables to automatically control lights based on the prediction of this project in different modes.

To learn more about how *mk-home-automation* works look at section X of this README.

To learn more about how to use the automation functions in combination with `mk-home-server` look at the [specific section]() it the README of that project.

## Requirements

- Python 3.8
- Rquired pip packages installed on your system (see [Pipfile](Pipfile))

**Optional:**
- pipenv
- pm2
- Docker
- Jupyter

## Run the project

There are different options to run this project. While it is created to work natively with a python environment on raspberry pi, it is also possible to use it with [pm2](https://github.com/Unitech/pm2), Docker or directly on your system in combination with [pipenv](https://github.com/pypa/pipenv).

To discover or enhance the base machine learning model and data aggregation you also can use the attached [jupyter notebook](jupyter/mk-home-automation.ipynb) in this repository. The important data modelation, and feature optimization used in the application code is originated there.

### Production

Because the training and prediction functionality of this project is encapsulated in a REST API (using Flask), it is recommended to use [gunicorn](https://github.com/benoitc/gunicorn) to run it reliable and safe in production. This purpose is already included into the pm2 and Docker setup shown below.

#### pm2

To run *mk-home-automation* with pm2 you need to install pipenv and pm2. After doing so, jump into the root folder of this project and install the required python version and pip packages which are needed with pipenv: 

```
pipenv install
```

After having setup all the requirements you can just start the application and the build-in REST server with:

```
pm2 start ecosystem.config.yml
```

To run this service permanently use: 

```
pm2 save
```

#### Docker

To build the project via Docker run from the root folder:

```
docker build -t mkha .
```

To start it then use:

```
docker run -it -p 9090:9090 mkha:latest
```

If you want to configure the outgoing port or other things, feel free to change it inside the [Dockerfile](Dockerfile). Other project related configuration you can find and change in the [.env.docker](..env.docker) file.

#### Pipenv

If you want to run the project directly via *pipenv* use:

```
pipenv install
```

And to start the project:

```
pipenv run gunicorn --bind 0.0.0.0:9090 --pythonpath 'app' server:app"
```

### Development

When using *mk-home-automation* for development purposes, you can use pipenv and start the application directly with:

```
pipenv run python app/server.py
```

If not all dependencies are installed correctly for the virtual environment remember to use `pipenv install` first.

When having `DEBBUGING` set to `True` in the `.env`file, flask also is doing hot reloading on code changes.

### Jupyter

To explore or modify the steps of creating and optimizing the model used in this project, you can directly use the attached jupyter notebook in this repository.

To run it just go in the related directory with:

```
cd jupyter
```

and start the notebook with:

```
jupyter notebook
```

## Configuration

For now all configuration for the project is maintained in `.env` files. For development and production use the [.env](.env) file, for the docker setup use the [.env.docker](.env.docker) file.

## Use the project

The functionality of training the tracked light interactions from *mk-home-server* or predicting the on/off state of a specific light at a concrete weekday/daytime combination is exposed through an REST API by the application.

To use it there are two routes integrated in the service which are accessible by everyone who can connect to this service.

### Train the model

To train the model use the `/train` route of the API with a *POST* request and an attached csv file with all the light interaction data comes from the *mk-home-server* application.

After training a new model based on the input data, the created model get saved in the file system to reuse it later on.

### Predict a light state

To predict a light state of specific light at a provided weekday/daytime combination use the `/predict` route with a *POST* request.

You also need to provide the needed information through a JSON body attached to the request.
That information must have the following form:

```
{
    "instanceid": 65537,
    "type": 2,
    "weekday": "Thursday",
    "time": "16:23"
}
```

| Option | Value |
| - | - |
| instanceid | *The ID of the light for which the prediction should be made* |
| type | *The internal type of device (2 stands for a light bulb)* |
| weekday | *The weekday for which the prediction should be made. Here the english weekday names are used with a captial letter at the beginning* |
| time | *The time for which the prediction should be made. Here the time is provided in a 24 hour format according to `HH:mm`* |