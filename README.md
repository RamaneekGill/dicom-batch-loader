# DICOM Batch Generator

Batch generator for DICOM and inner contours.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
We use Python, 3.5 to be precise.

The following Python packages are used and their motivation behind them.
- pillow
 - For image boolean mask creation
- pandas
 - For reading a CSV and basic data wrangling
- pydicom
 - For parsing DICOM images
- numpy
 - For use of numpy arrays
- keras
 - For reusing the ImageDataGenerator

TODO `pip freeze > requirements.txr` for exact reproduction of the Python environment.

### Compute Environment

Docker was not used due to time considerations.
Instead a virtual environment was preferred.

We use Python 3.5

Build your environment by running the following in your project directory:

```
virtualenv env -p 3.5
source env/bin/activate
pip install -r requirements.txt
```

Ensure the project works by doing in the Python shell `import DataGenerator`

## Running the tests

This is how you run the tests: `TODO`

# Design Considerations
This is designed to be a batch loader for dicom image data.

The data is loaded via a Python Generator. This is to handle situations where a large dataset cannot fit in memory.
- Note that I have used Keras' ImageDataGenerator
- The work was already done, it has tests around it (here)[https://github.com/fchollet/keras/blob/7f58b6fbe702c1936e88a878002ee6e9c469bc77/tests/keras/preprocessing/image_test.py]
- Also includes useful features such as realtime data augmentation


# Code Reuse
The project is setup to be reused by any other Python project. It is pip installable.

Refer to pip documentation on how to install from a GitHub URL.

# How to Deploy
This project had deployment in mind with CloudFoundry. However Heroku can
be used as well based on their documentation. The server configurations
are in the `manifest.yml` file and runs the `Procfile` when the buildpack
successfully builds the Python project.

Install this project as a Python package.

Create a simple server with a GET route using Flask or an alternative library.

Wrap the following code into a GET route `TODO`

To deploy run `cf push` in the root directory of the project.

# How to use
There are two ways to use the batch generator, through direct usage or through
an API.

For direct usage:
- pip install the project
- `include DataGenerator`
- `DataGenerator.generate(TODO)`

For API:
- TODO

# Questions!

## Part 1

### How did you verify that you are parsing the contours correctly?

TODO

### What changes did you make to the code, if any, in order to integrate it into our production code base?

TODO

## Part 2

### Did you change anything from the pipelines built in Parts 1 to better streamline the pipeline built in Part 2? If so, what? If not, is there anything that you can imagine changing in the future?

TODO

### How do you/did you verify that the pipeline was working correctly?

TODO

### Given the pipeline you have built, can you see any deficiencies that you would change if you had more time? If not, can you think of any improvements/enhancements to the pipeline that you could build in?

TODO 