"""Reads data in a format such as final_data/ and matches contours to DICOM images"""

import os
import parser
import numpy as np
import pandas as pd

def read_linker(filename):
    """Reads a linker CSV that matches Patient IDs to Original IDs/

    :param filename: filepath to the linker csv to parse
    :return: list of tuples holding Patient ID, Original ID of the data
    """
    csv = pd.read_csv(filename)
    patient_ids = csv['patient_id'].values.tolist()
    original_ids = csv['original_id'].values.tolist()
    return patient_ids, original_ids

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

def get_contour_dicom_path_pairs(contours, dicoms):
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

def wrangle(data_dir, linker_filepath):
    """Returns parsed tuple of DICOM images and their respective masks

    :param data_dir: path to the directory of data
    :param linker_filepath: path to the linker CSV file for the data
    :return: tuple of numpy array of DICOM images and a numpy array of its masks
    """
    contour_dicom_path_pairs = []
    patient_ids, original_ids = read_linker(linker_filepath)

    for i in range(len(patient_ids)):
        contours = get_contours(data_dir, original_ids[i])
        dicoms = get_dicoms(data_dir, patient_ids[i])
        contour_dicom_path_pairs += get_contour_dicom_path_pairs(contours, dicoms)

    dicoms = []
    masks = []
    for path_pair in contour_dicom_path_pairs:
        dicom = parser.parse_dicom_file(path_pair[1])
        if dicom is None: # Dicom failed to load correctly, skip the pair
            continue

        contour = parser.parse_contour_file(path_pair[0])
        mask = parser.poly_to_mask(contour, dicom.shape[1], dicom.shape[0])

        dicoms.append(dicom)
        masks.append(mask)


    return np.array(dicoms), np.array(masks)
