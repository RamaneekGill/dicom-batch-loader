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
import visualizer

data_dir = '.../final_data/'
data = wrangler.wrangle(data_dir, data_dir + 'link.csv')

visualizer.visualize(data['dicoms'][0], data['inner_contours'][0], 
                     data['outer_contours'][0], data['meta'][0], show=True)

factory = generator.GeneratorFactory()
dicom_mask_batch_generator = factory.create(data['dicoms'], data['inner_contour_masks'])
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

## Part 3 Parsing Outer Contours

### Changes Made

Minimal changes were made to `wrangler.py`. Due to adequate code design in the previous phase.
Changes to note:
- Use a decorate pattern to parse inner OR outer contours with the same code. `get_i_contours()` and `get_o_contours()` call the private method `_get_contours()` since both inner and outer contour file paths have the same structure they can also reuse the `_get_contour_id()` private method as well.
- Needed to make changes to the matcher for inner contours and dicom images to fetch the right image id. This required another check with having a loop for finding the matching outer contour file. This is inefficient but the O(n^3) loop can be reduced to O(3) by using dictionaries to fetch a file path based on `patient_id`, and `image_id`
- The `wrangle()` method on the `Wrangler` module was augmented to return meta data as well as original contour vertice lists of inner and outer contours for visualization purposes. This method has potential to be parallelized easily due to loading multiple types of files at once all independently of one another.
- The `Wrangler` module would work better as a class due to its dependence on the `data_dir` parameter in many methods. TODO

## Part 4 Segmentation Approaches

### Can thresholding work?

Before diving into this question lets do a visualiztion. Go to the `DICOMBatchLoader/visualized` folder. Select all files, right click and click open. Now you can easily use arrow keys to animate a patient's images to view the outer and inner contours.

Note: The visualization is in order of original dicom, inner contour, outer contour. The contours are circled by a thing solid black line. TODO make this colored.

An overall trend one can visually inspect is that it is relatively easy to determine an inner contour if given an outer contour. The inner contour is the whiter smaller circle within the outer contour.

#### Some assumptions can be made here:
- The inner contour is always present
- The inner contour is always inside the outer contour
- Outer and inner contours are always circular in shape

#### Some considerations:
- We assume the data is annotated and always correct.
- Take a look at the image ![Image of incorrect outer circle](https://github.com/RamaneekGill/dicom-batch-loader/blob/master/visualized/dicom_inner_outer_SC-HF-I-6_SCD0000501_199.jpeg)
 - The outer circle seems like it is in the incorrect place but the inner circle seems correct. This could be an issue with the data or the visualization code. I'm going to put my bets on my code and say it is a problem with data since all other visualizations for a __different patient insteand of SCD0000501__ seem correct.
 - This is affecting all outer contours for patient `SCD0000501`
- The image ![not round inner contour](https://github.com/RamaneekGill/dicom-batch-loader/blob/master/visualized/dicom_inner_outer_SC-HF-I-2_SCD0000201_220.jpeg) does not have a round inner contour.

#### Accurate thresholding?

So can we create a simple thresholding algorithm that can __accurrately__ classify inner contours given an outer contour and the original image? 

I'm going to say yes but only to a certain extent. If the assumptions listed above can be made then the images that fit those assumptions can have a thresholding value on the intensity of the picture to label an circular-esque area of the inner contour.

#### Examples of good contours

Some great examples (from different patients are below)

![contour1](https://github.com/RamaneekGill/dicom-batch-loader/blob/master/visualized/dicom_inner_outer_SC-HF-I-2_SCD0000201_140.jpeg)

![contour2](https://github.com/RamaneekGill/dicom-batch-loader/blob/master/visualized/dicom_inner_outer_SC-HF-I-1_SCD0000101_159.jpeg)

![contour3](https://github.com/RamaneekGill/dicom-batch-loader/blob/master/visualized/dicom_inner_outer_SC-HF-I-5_SCD0000401_100.jpeg)

### Justification

I don't have any concrete statistic to support my assumption. Here is what I would do to confirm my hypothesis of a simple thresholding algorithm based on pixel intensities within an outer contour:
- Assume the following:
 - The inner contour is always present
 - The inner contour is always inside the outer contour
 - Outer and inner contours are always circular in shape
- Isolate inner contour pixels and outer contour pixels
- Create a histogram of pixel intensities for exclusive outer contour pixels and exclusive inner contour pixels
- Perform a comparison of two means (http://www.stat.yale.edu/Courses/1997-98/101/meancomp.htm) 
 - Given the dataset determine an appropriate threshold and whether tge threshold has a sufficient confidence on the data

TODO: get pixels only in outer contour not in inner contour, histogram them, visualize them

Histograms will give an overall picture of how pixel intensity distributions look like within an image. If given a mask
this is usually an effective technique
- https://arxiv.org/abs/1609.00096
- https://arxiv.org/abs/1703.04301 (uses ML but isn't fully supervised which may be the point of this)
- https://arxiv.org/abs/1302.1296
- A previous course I took http://www.cs.toronto.edu/~guerzhoy/320/lec/edgedetection.pdf
 - I did research with this professor in the past

### Non Machine Learning Segmentation

Convolutions! Kernels have historic significance in computer vision, especially for edge detection. Sobel filter
is great for edge detection.

Thresholds with image gradients actually may work very well since most inner contours are a clear distinction 
from the outer contour boundaries based on the pixel intensities changing quickly. A convolution

From the sample data in this exercise it seems like the problem is almost an edge detection challenge when
given an outer contour. Don't believe me? Just view the images in https://github.com/RamaneekGill/dicom-batch-loader/blob/master/visualized

I wouldn't go all out edge detection with an algorithm like canny edges since it seems like you'd have to constantly
tweak parameters and can pick up small artifacts.

First I would smooth them image, light gaussian smoothenning I've found works well in the past. Then use a watershed
algorithm to perform segmentation. Why watershed? Works on greyscale, seperates 'basins' seems almost like what
the task is at hand. I've found watershed to have problems with noisy images which seem like our case so tuning the
image smoothening would be key.

Having strict thresholds such as only one blob is allowed (the inner contour) and a minimum area size may help.

### Machine Learning Approach
- Fix generator issue in the Notes section
- Generate more images using Keras
 - Gives us more data to work with
- Take all pixels in inner contour, label as inner contour
- Take all pixels in outer contour that are NOT in inner contour, label as outer contour
- Becomes a classification problem
- Split data in to train and validation sets
    - Stratified k fold cross validation to maintain distributions between folds
- Test with simple logistic regression for AUC accuracy for baseline
- Test with CNN since convolutions are generally best when dealing with images
- Optimize parameters using a bayesian approach

# NOTES:

Error when creating generator:
`ValueError: Input to .fit() should have rank 4. Got array with shape: (96, 256, 256)`

This is because the channels axis should have value 1 as per Keras documentation. Going to stay true to the time
and submit regardless.

Added the method `draw_outline()` to the `Parser` module

Updated How To Use section to do visualizations.

Most time has been spent on research and understanding the problem, some docstrings may be out of date.