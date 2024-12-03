import tifffile as tf
import numpy as np
import readroi
import matplotlib.pyplot as plt
from typing import List
import os
import pandas as pd

VIDEO_PATH = 'data/240530_Dish1_ATP_1_MMStack_Pos0.ome.tif'
ROI_PATH = 'data/240530_Dish1_ATP_1_MMStack_Pos0.ome.zip'

# Save means so that we can export to csv without redoing work
SAVED_MEANS: List[np.array] = []
# Corresponding headers
SAVED_MEANS_HEADERS: List[List[str]] = []


def compute_regions(video_path=VIDEO_PATH, roi_path=ROI_PATH):
    '''
    Params:
        - video_path: path to tif file
        - roi_path: path to ROI zip
    Function:
        - Aligns ROIs to values in tif file
        - Averages pixels within background ROI box for each frame, retaining time dimension
        - Averages pixels within each 'cell' ROI box for each frame, retaining time dimension
        - Subtracts background ROI from 'cell' ROIs for each frame
    Returns:
        - Adjusted 'cell' ROIs for each frame (shape = (num_frames, num_cells))
    '''
    rois = np.array(readroi.import_roi(roi_path)).astype(int)

    background = rois[-1]  # background.shape=[4,] -> these are (x,y,h,w)
    # coords.shape=[# cells, 4] -> these are (x,y, h,w) for each cell
    coords = rois[:-1]

    images = np.array(tf.imread(video_path))  # images.shape =[200, 1200 ,1200]
    # means.shape = [200, # cells]
    means = np.zeros(shape=(images.shape[0], coords.shape[0]))

    background_means = np.mean(
        images[
            :,
            background[0]:(background[0] + background[2]),
            background[1]:(background[1] + background[3])
        ], axis=(1, 2)
    )

    for i, coord in enumerate(coords):
        means[:, i] = np.mean(
            images[
                :,
                coord[0]:(coord[0] + coord[2]),
                coord[1]:(coord[1] + coord[3])
            ], axis=(1, 2)
        )

        # subtract the background mean from every element
        means[:, i] -= background_means[i]

    # Store means for csv later
    SAVED_MEANS.append(means)
    # TODO: Sort of placeholder names, should consider updating
    # Index label
    headers = [f'\nVideo #{len(SAVED_MEANS_HEADERS) + 1} Frames']
    # Construct ROI labels
    headers.extend([f'ROI #{x}' for x in range(1, means.shape[1] + 1)])
    SAVED_MEANS_HEADERS.append(headers)

    # print(SAVED_MEANS_HEADERS)

    return means


def save_csv(file_name: str = 'means.csv', headers: List[str] = SAVED_MEANS_HEADERS):
    '''
        Saves recorded means as a CSV. All computed means go in one file. Headers included.
        Will overwrite file with same name

        Params:
            - file_name: Name to save file to
            - Headers: Optional header names. Defaults to numbering based on order of processing.
                       First header is used as index label.
        Preconditions:
            - compute_regions() has been ran at least one time
    '''
    if not SAVED_MEANS:
        print("Must run compute_regions before saving to csv")
        return

    # Remove old csv if it exists
    if os.path.exists(file_name):
        os.remove(file_name)

    # Start saving all means processed to csv
    for saved_header, array in zip(SAVED_MEANS_HEADERS, SAVED_MEANS):
        df = pd.DataFrame(array)
        df.to_csv(file_name, mode='a',
                  index_label=saved_header[0], header=saved_header[1:])


if __name__ == '__main__':
    print(compute_regions())
    print(SAVED_MEANS_HEADERS)
    save_csv('test_csv.csv')
    # np.save("means.npy", compute_regions())
