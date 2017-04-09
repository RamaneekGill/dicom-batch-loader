"""Reads data in a format such as final_data/ and matches contours to DICOM images"""

import pandas as pd

def read_linker(filename):
    """Reads a linker CSV that matches Patient IDs to Original IDs/

    :param filename: filepath to the linker csv to parse
    :return: list of tuples holding Patient ID, Original ID of the data
    """

    return pd.read_csv(filename).values.tolist()

def get_contours(original_id):
    """Get a list of filepaths to all contours belonging to an original ID"""
    pass

def get_dicoms(patient_id):
    """Get a list of filepaths to all DICOM images belonging to a patient ID"""
    pass

def _get_id_of_contour(filename):
    """Returns the ID from the contour file, this is used to match to the corresponding DICOM.

    :param filename: filepath to a contour file
    :return: string representation of the ID
    """

    print(filename)

def get_contour_dicom_pairs(contours, dicoms):
    """Creates a list of tuples, a contour filepath and dicom filepath for all
    dicoms that have an inner contour file for an Orignal ID and Patient ID pair.

    :param contours: list of contour filepaths
    :param dicoms: list of dicom filepaths
    :return: list of tuples with a matching dicom and inner countour filepaths
    """
    pass


