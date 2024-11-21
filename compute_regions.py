import tifffile as tf
import numpy as np
import readroi
import matplotlib.pyplot as plt

VIDEO_PATH = 'video.tif'
ROI_PATH = 'roi.zip'


def compute_regions(video_path = VIDEO_PATH, roi_path = ROI_PATH):
    rois = np.array(readroi.import_roi(roi_path)).astype(int)

    background = rois[-1]
    coords = rois[:-1]

    images = np.array(tf.imread(video_path))
    means = np.zeros(shape=(images.shape[0], coords.shape[0]))

    background_mean = np.mean(
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
        means[:, i] -= background_mean

    print(means[:20, 0])

    plt.scatter(range(means.shape[0]), means[:, 0])
    plt.show()

    return means

if __name__ == '__main__':
    np.save("means.npy", compute_regions())