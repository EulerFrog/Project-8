import roifile
from roifile import roiread
import tifffile
import matplotlib
import argparse
from typing import Tuple, List


def import_roi(path: str) -> List[Tuple[int, int, float, float]]:
    '''
        Imports the regions defined in an roi zip file

        Parameters:
            path (str): the path to the ROI file

        Returns:
            List of tuples in the format:
                (x-coord, y-coord, width, height)
            Each tuple represents an ROI section

    '''
    rois = roiread(path)
    tuples = [(roi.top, roi.left, roi.widthd, roi.heightd) for roi in rois]
    return tuples


# This was used to better understand what an roi file has in it
# It lists out what each ImagejRoi object has as parameters
# Also lists out coordinates of the shapes and info about them.
if __name__ == "__main__":
    # Argument parsing so i can give it a filename
    parser = argparse.ArgumentParser(prog='readroi',
                                     description='Small reader for roi info')
    parser.add_argument(
        'filename', help='Path to roi file. Meant for zip file containing rois')
    args = parser.parse_args()

    # This img roi thing doesn't work with the tif files we got, but it is possible to embed roi info in tif files.
    # the .ome.tif extension is used when exporting from imagej's bio-tools plugin.
    img_rois = roiread('./240530_Dish1_ATP_1_MMStack_Pos0.ome.tif')
    file_rois = roiread(args.filename)
    print(f'img rois: {img_rois}')
    print(f'file rois: {file_rois}')

    # Outputs roi points
    for i, roi in enumerate(file_rois):
        print(f'ROI #{i}')
        print(f'ROI name: {roi.name}')
        print(f'ROI Dimensions: {(roi.widthd, roi.heightd)}')
        print(f'top-left: {(roi.top, roi.left)}')
        print(f'top-right: {(roi.top, roi.right)}')
        print(f'bottom-left: {(roi.bottom, roi.left)}')
        print(f'bottom-right: {(roi.bottom, roi.right)}')
        print('------------')
    print(
        f'Results of import_roi: {import_roi("240530_Dish1_ATP_1_MMStack_Pos0.ome.zip")}')
