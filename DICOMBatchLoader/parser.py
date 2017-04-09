"""Parsing code for DICOMS and contour files"""

import dicom
from dicom.errors import InvalidDicomError

import numpy as np
from PIL import Image, ImageDraw

def parse_contour_file(filename):
    """Parse the given contour filename

    :param filename: filepath to the contourfile to parse
    :return: list of tuples holding x, y coordinates of the contour
    """

    coords_lst = []

    with open(filename, 'r') as infile:
        for line in infile:
            coords = line.strip().split()

            x_coord = float(coords[0])
            y_coord = float(coords[1])
            coords_lst.append((x_coord, y_coord))

    return coords_lst

def parse_dicom_file(filename):
    """Parse the given DICOM filename

    :param filename: filepath to the DICOM file to parse
    :return: dictionary with DICOM image data
    """

    try:
        dcm = dicom.read_file(filename)
        dcm_image = dcm.pixel_array

        if hasattr(dcm, 'RescaleIntercept'):
            intercept = dcm.RescaleIntercept
        else:
            intercept = 0.0

        if hasattr(dcm, 'RescaleSlope'):
            slope = dcm.RescaleSlope
        else:
            slope = 0.0

        if not_origin_and_not_horizontal(intercept, slope):
            dcm_image = dcm_image * slope + intercept

        return dcm_image

    except InvalidDicomError:
        return None

def not_origin_and_not_horizontal(intercept, slope):
    """Returns True iff the intercept and slope are both non zero"""
    return intercept != 0.0 and slope != 0.0

def poly_to_mask(polygon, width, height):
    """Convert polygon to mask

    :param polygon: list of pairs of x, y coords [(x1, y1), (x2, y2), ...]
     in units of pixels
    :param width: scalar image width
    :param height: scalar image height
    :return: Boolean mask of shape (height, width)
    """

    # http://stackoverflow.com/a/3732128/1410871
    # ^ A link to a stackoverflow is bad practise! Instead the code/documentation
    # should give a clear depiction of why it is written in such a way

    # Create a new 8-bit pixel black and white canvas
    img = Image.new(mode='L', size=(width, height), color=0)
    # Draw a polygon with the outline being False and filling being True
    ImageDraw.Draw(img).polygon(xy=polygon, outline=0, fill=1)
    # Convert the image to a boolean numpy array, most likely for easy Keras use
    mask = np.array(img).astype(bool)
    return mask
