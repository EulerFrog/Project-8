import tifffile as tf
import numpy as np
import readroi
import matplotlib.pyplot as plt

VIDEO_PATH = 'video.tif'
ROI_PATH = 'roi.zip'
HEIGHT = 5 # height in pixels of each region
WIDTH = 10 # width in pixels of each region

rois = np.array(readroi.import_roi(ROI_PATH)).astype(int)

background = rois[-1]
coords = rois[:-1]

images = np.array(tf.imread(VIDEO_PATH))
means = np.zeros(shape=(images.shape[0], coords.shape[0]))

background_mean = np.mean(
    images[
        :, 
        background[0]:(background[0] + background[2]),
        background[1]:(background[1] + background[3])
    ]
)


for i, coord in enumerate(coords):
    means[:, i] = np.mean(
        images[
            :, 
            coord[0]:coord[0] + np.round(coord[2]), 
            coord[1]:coord[1] + np.round(coord[3])
        ], axis = (1,2)
    )

    # subtract the background mean from every element
    means[:, i] -= background_mean

plt.scatter(range(means.shape[0]), means[:, 1])
plt.show()

np.save('means.npy', means)