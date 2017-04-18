import os
import parser
import wrangler
from PIL import Image

def visualize(dicom, i_contour, o_contour, meta, show=False):
    """Creates a visualization of the original DICOM img, inner contour, and outer ontour
    in that order and saves it. Also shows the image if show=True.

    Will save the visualizations in a `visualized` folder in the current working directory.
    This folder is created if it doesn't already exist.

    :param dicom: numpy array representation of the DICOM img
    :param i_contour: list of inner contour points
    :param o_contour: list of outer contour points
    :param meta: meta data for the image, must be a dicionary containing original_id,
    patient_id and image_id. This is outputed by the wrangle method of the Wrangler module.
    :return: None
    """
    dicom_im = Image.fromarray(dicom)
    i_dicom_im = parser.draw_outline(dicom, i_contour)
    o_dicom_im = parser.draw_outline(dicom, o_contour)

    directory = 'visualized'
    filename = 'dicom_inner_outer_' + meta['original_id'] + '_' + meta['patient_id'] + '_' + meta['image_id'] + '.jpeg'

    # Create a canvas that is 3 images wide
    canvas_size = (i_dicom_im.size[0] * 3, i_dicom_im.size[1])
    visualization = Image.new(i_dicom_im.mode, canvas_size)

    # Paste the visualizations on to one canvas
    visualization.paste(dicom_im, (i_dicom_im.size[1] * 0, 0))
    visualization.paste(i_dicom_im, (i_dicom_im.size[1] * 1, 0))
    visualization.paste(o_dicom_im, (i_dicom_im.size[1] * 2, 0))

    if not os.path.exists(directory):
        os.makedirs(directory)
    visualization.convert('L').save(directory + '/' + filename, format='jpeg')

    if show:
        visualization.show(title=filename)
