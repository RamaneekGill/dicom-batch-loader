"""Reads data in a format such as final_data/ and matches contours to DICOM images"""

import os
import pandas as pd

def read_linker(filename):
    """Reads a linker CSV that matches Patient IDs to Original IDs/

    :param filename: filepath to the linker csv to parse
    :return: list of tuples holding Patient ID, Original ID of the data
    """

    return pd.read_csv(filename).values.tolist()

def get_contours(data_dir, original_id):
    """Get a list of filepaths to all contours belonging to an original ID"""
    contour_paths = []
    path = os.path.join(data_dir, 'contourfiles/' + original_id + '/i-contours')
    for (dirpath, _, filenames) in os.walk(path):
        for filename in filenames:
            contour_paths.append(os.path.join(dirpath, filename))
        break
    return contour_paths

def get_dicoms(data_dir, patient_id):
    """Get a list of filepaths to all DICOM images belonging to a patient ID"""
    dicom_paths = []
    path = os.path.join(data_dir, 'dicoms/' + patient_id)
    for (dirpath, _, filenames) in os.walk(path):
        for filename in filenames:
            dicom_paths.append(os.path.join(dirpath, filename))
        break
    return dicom_paths

def _get_id_of_contour(filename):
    """Returns the ID from the contour file, this is used to match to the corresponding DICOM.

    :param filename: filepath to a contour file
    :return: string representation of the ID
    """
    # The id is the 3 section of the filename
    contour_id = os.path.basename(filename).split('-')[2]
    # Remove leading zeros from the id
    return str(int(contour_id))

def _get_id_of_dicom(filename):
    """Gets the id of the dicom file"""
    # The id is the filename minus the file extension
    return os.path.basename(filename).split('.')[0]

def get_contour_dicom_pairs(contours, dicoms):
    """Creates a list of tuples, a contour filepath and dicom filepath for all
    dicoms that have an inner contour file for an Orignal ID and Patient ID pair.

    :param contours: list of contour filepaths
    :param dicoms: list of dicom filepaths
    :return: list of tuples with a matching dicom and inner countour filepaths
    """
    matches = []
    for contour in contours:
        contour_id = _get_id_of_contour(contour)
        for dicom in dicoms:
            dicom_id = _get_id_of_dicom(dicom)

            if contour_id == dicom_id:
                matches.append([contour, dicom])
                break

    return matches
    