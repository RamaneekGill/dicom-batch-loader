"""Unit test for parsing methods"""

import sys
import os
# Add the project to system path
sys.path.append(os.path.join(os.getcwd(), 'DicomBatchLoader'))

# TODO fix the above, it is not production quality...

import unittest
import parsing

class TestParsing(unittest.TestCase):
    """Test the Parsing module"""

    def test_parse_contour_file(self):
        """Test if inner contour coordinates can be loaded correctly."""
        pass

    def test_parse_contour_file_invalid_file(self):
        """Test if an invalid contour file silently fails when parsing"""
        # Tests that aren't written need to be failing so they are not forgotten, TDD!
        self.fail("TODO, needs to be implemented")

    def test_parse_dicom_file(self):
        """Test if a DICOM image can be loaded correctly."""
        pass

    def test_parse_dicom_file_invalid_dicom(self):
        """Test if an invalid DICOM image silently fails when parsing"""
        self.fail("TODO, needs to be implemented")

    def test_poly_to_mask(self):
        """Test if a boolean mask can be correctly computed"""
        self.fail("TODO, needs to be implemented")

    def test_end_to_end_integration(self):
        """Test loading an inner contour, DICOM file and computing a mask"""
        # My gut would tell me this test needs to rely on a variety of unit tests first:
        # - What if the contour is invalid? There should a unit test for that...
        # - Time restrictions won't allow me to get the contours of the generated
        #   boolean mask and match with the parse_contour_file() output.
        # - Pillow documentation for outline=0 and fill=1 seems to have tests so perhaps
        #   a test showing that it doesn't fail may be sufficient.
        self.fail("TODO")

if __name__ == '__main__':
    unittest.main()
