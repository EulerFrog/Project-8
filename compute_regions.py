import tifffile as tf
import numpy as np
import readroi
import matplotlib.pyplot as plt

VIDEO_PATH = 'dish2.tif'
ROI_PATH = 'roi.zip'


def compute_regions(video_path = VIDEO_PATH, roi_path = ROI_PATH):
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

    background = rois[-1] # background.shape=[4,] -> these are (x,y,h,w)
    coords = rois[:-1] # coords.shape=[# cells, 4] -> these are (x,y, h,w) for each cell

    images = np.array(tf.imread(video_path)) # images.shape =[200, 1200 ,1200]
    means = np.zeros(shape=(images.shape[0], coords.shape[0])) # means.shape = [200, # cells]

    background_means = np.mean(
        images[
            :, 
            background[0]:(background[0] + background[2]),
            background[1]:(background[1] + background[3])
        ], axis = (1,2)
    )


    for i, coord in enumerate(coords):
        means[:, i] = np.mean(
            images[
                :, 
                coord[0]:(coord[0] + coord[2]), 
                coord[1]:(coord[1] + coord[3])
            ], axis = (1,2)
        )

        # subtract the background mean from every element
        means[:, i] -= background_means[i]
    
    return means

if __name__ == '__main__':
    np.save("means.npy", compute_regions())