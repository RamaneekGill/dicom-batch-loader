# Project Title

Batch generator for DICOM and inner contours.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
The following Python packages are used:
- PIL
- Pandas
- Keras
- pydicom


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
