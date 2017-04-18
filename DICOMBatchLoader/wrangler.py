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

def get_i_contours(data_dir, original_id):
    """Get a list of filepaths to all inner contours belonging to an original ID"""
    return _get_contours(data_dir, original_id, 'inner')

def get_o_contours(data_dir, original_id):
    """Get a list of filepaths to all outer contours belonging to an original ID"""
    return _get_contours(data_dir, original_id, 'outer')

def _get_contours(data_dir, original_id, contour_type):
    """Get a list of filepaths to all contours belonging to an original ID"""
    if contour_type == 'i' or contour_type == 'inner':
        contour_folder = 'i-contours'
    elif contour_type == 'o' or contour_type == 'outer':
        contour_folder = 'o-contours'
    else:
        raise ValueError('Only inner or outer contours are supported.')

    contour_paths = []
    path = os.path.join(data_dir, 'contourfiles/' + original_id + '/' + contour_folder)
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

def get_contour_dicom_path_pairs(i_contours, o_contours, dicoms):
    """Creates a list of lists, an inner contour filepath, outer contour filepath
    and dicom filepath along with IDs. All inner lists have a matching Original ID and Patient ID pair.

    :param i_contours: list of inner contour filepaths
    :param o_contours: list of outer contour filepaths
    :param dicoms: list of dicom filepaths
    :return: list of dictionaries containing a matching dicom, inner countour, outer contour filepaths
    and patient id, image id, and original id
    """
    matches = []
    for i_contour in i_contours:
        i_contour_id = _get_id_of_contour(i_contour)
        for o_contour in o_contours:
            o_contour_id = _get_id_of_contour(o_contour)

            if i_contour_id == o_contour_id:
                for dicom in dicoms:
                    dicom_id = _get_id_of_dicom(dicom)

                    if i_contour_id == dicom_id:
                        matches.append({
                            'inner_contour': i_contour,
                            'outer_contour': o_contour,
                            'dicom': dicom,
                            'patient_id': os.path.basename(os.path.dirname(dicom)),
                            'image_id': dicom_id,
                            'original_id': os.path.basename(os.path.dirname(
                                os.path.dirname(i_contour)))})
                        break
                break

    return matches

def wrangle(data_dir, linker_filepath):
    """Returns parsed dictionary of DICOM images and their respective inner
     and outer masks in an numpy array.

    :param data_dir: path to the directory of data
    :param linker_filepath: path to the linker CSV file for the data
    :return: dictionary of numpy arrays containing DICOMs, inner contour, outer contour,
    inner masks, outer masks, and list of file paths used for lookup table uses
    """
    contour_dicom_path_pairs = []
    patient_ids, original_ids = read_linker(linker_filepath)

    for i in range(len(patient_ids)):
        i_contours = get_i_contours(data_dir, original_ids[i])
        o_contours = get_o_contours(data_dir, original_ids[i])
        dicoms = get_dicoms(data_dir, patient_ids[i])
        contour_dicom_path_pairs += get_contour_dicom_path_pairs(i_contours, o_contours, dicoms)

    dicoms = []
    i_contours = []
    o_contours = []
    i_masks = []
    o_masks = []
    for path_pair in contour_dicom_path_pairs:
        dicom = parser.parse_dicom_file(path_pair['dicom'])
        if dicom is None: # Dicom failed to load correctly, skip the pair
            continue

        i_contour = parser.parse_contour_file(path_pair['inner_contour'])
        o_contour = parser.parse_contour_file(path_pair['outer_contour'])

        i_mask = parser.poly_to_mask(i_contour, dicom.shape[1], dicom.shape[0])
        o_mask = parser.poly_to_mask(o_contour, dicom.shape[1], dicom.shape[0])

        dicoms.append(dicom)
        i_masks.append(i_mask)
        o_masks.append(o_mask)
        i_contours.append(i_contour)
        o_contours.append(o_contour)

    return {
        'dicoms': np.array(dicoms),
        'inner_contours': np.array(i_contours),
        'outer_contours': np.array(o_contours),
        'inner_contour_masks': np.array(i_masks),
        'outer_contour_masks': np.array(o_masks),
        'meta': contour_dicom_path_pairs
    }
