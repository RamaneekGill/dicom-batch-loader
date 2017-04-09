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

TODO `pip freeze > requirements.txt` for exact reproduction of the Python environment.

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

Ran out of time: `python tests/test_parsing.py`

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
an API when deployed. Here we discuss direct usage.

For direct usage:
```
import wrangler
import generator

data_dir = '.../final_data/'
dicoms, masks = wrangler.wrangle(data_dir, data_dir + 'link.csv')

factory = generator.GeneratorFactory()
dicom_mask_batch_generator = factory.create(dicoms, masks)
your_keras_model.fit_generator(dicom_mask_batch_generator, steps_per_epoch=10, epochs=3)
```

Refer to the documentation in `DICOMBatchLoader.generator` and https://keras.io/preprocessing/image/
for more options!

If you've installed the package through `PIP` prepend your imports with a `DicomBatchLoader`. Note
this wasn't tested ;).

# Questions!

## Part 1

### How did you verify that you are parsing the contours correctly?

Due to time considerations I manually visualized the mask and to see if it made sense. I have documented
how I would go about creating automated unit tests for this sort of thing in the tests file.

### What changes did you make to the code, if any, in order to integrate it into our production code base?

Run `git diff 7dda6d0 7dda6d0^1` to see the changes in one commit.

Notable changes:
- Removed unneccessary try/except blocks and instead used the library `hasattr()` method to check DICOM image properties.
- Put a warning in the code stating we assume a polygon is inserted in to the `poly_to_mask()` function
- Put a warning stating linking to a stackoverflow post for code justification is just a plain bad idea. Instead research the library APIs and explain the code in readable comments
- Abstract out the awkward if statement into a readable function call `not_origin_and_not_horizontal()`, I may have misunderstood the code intentions but the idea was there :P

## Part 2

### Did you change anything from the pipelines built in Parts 1 to better streamline the pipeline built in Part 2? If so, what? If not, is there anything that you can imagine changing in the future?

Nope. I read in advance of what to prepare for, also I have worked with creating generators before with DICOM data a couple months ago so knew
what challenges to expect. One tiny thing I did have to change was figure out how to get the greyscale images working with the Keras generator.

### How do you/did you verify that the pipeline was working correctly?

View the tests for Keras to make sure there's sufficient code coverage here: https://github.com/fchollet/keras/blob/7f58b6fbe702c1936e88a878002ee6e9c469bc77/tests/keras/preprocessing/image_test.py

Also test out my generator with some sample code:
```
for e in range(epochs):
    print 'Epoch', e
    batches = 0
    for X_batch, Y_batch in my_generator.flow(X, y, batch_size=4):
        batches += 1
        if batches >= len(X_train) / 4:
            # break loop manually
            break
```

### Given the pipeline you have built, can you see any deficiencies that you would change if you had more time? If not, can you think of any improvements/enhancements to the pipeline that you could build in?

Right now for the generator to fit it needs to bring all images in to memory. This happens when you call the `GeneratorFactory.create()` method.

If I had more time I would also refactor my imports of `os` and the like to only import relevant methods. I would also actually write out
some tests instead of scaffolding out some, it was difficult to stay true to the 3 hour timeline but I feel like I accomplished a lot. 

I can see defincies with this pipeline when trying to use a huge dataset. After having the masks generated we should be saving them in a format
such as hdf5 for efficient storage. Whenever we would like to retrain this pipeline will have to regenerate the masks. Very expensive with a large
dataset!

This pipeline needs more tests!!!

Also this pipeline should ideally be deployed as a microservice and not embedded. You can do some pretty cool things with apache spark and
simultaneously training a variety of different models.



# NOTES:

Error when creating generator:
`ValueError: Input to .fit() should have rank 4. Got array with shape: (96, 256, 256)`

This is because the channels axis should have value 1 as per Keras documentation. Going to stay true to the time
and submit regardless.