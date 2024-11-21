import tifffile as tf
import numpy as np

FILE_PATH = 'video.tif'
HEIGHT = 5 # height in pixels of each region
WIDTH = 10 # width in pixels of each region

background = np.random.randint(0,1200, size=(2))
coords = np.random.randint(0, 1200, size=(10,2))
images = np.array(tf.imread(FILE_PATH))
means = np.zeros(shape=(images.shape[0], coords.shape[0]))

background_mean = np.mean(
    images[
        :, 
        background[0]:background[0] + WIDTH,
        background[1]:background[1] + HEIGHT
    ]
)

for i, coord in enumerate(coords):
    means[:, i] = np.mean(
        images[
            :, 
            coord[0]:coord[0] + WIDTH, 
            coord[1]:coord[1] + HEIGHT
        ], axis = (1,2)
    )

    # subtract the background mean from every element
    means[:, i] -= background_mean

np.save('means.npy', means)