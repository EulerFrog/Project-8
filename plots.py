import matplotlib.pyplot as plt
import os
from PIL import Image, ImageSequence, ImageEnhance
import tifffile as tf
import numpy as np
from matplotlib.animation import FuncAnimation

DATA_DIR = 'data'
FILE = 'dish2_ATP_1_MMStack_Pos0.ome.tif'
CONTRAST_LEVEL = 2.0
SAVE_PREFIX = None 


def normalize(data):
    '''
    Min/Max Normalization
    '''
    data_min = np.min(data)
    data_max = np.max(data)
    data_norm = (data - data_min) / (data_max - data_min)
    return data_norm


def parse_frames(file=FILE, contrast=1.0):
    '''
        - Read frames from TIF file
        - Alter the contrast, 1.0 is no change
        - Average fluorescence of the whole image
    '''
    frames = tf.imread(os.path.join(DATA_DIR, file))
    parsed_frames = []
    for frame in frames:
        # Convert to grayscale
        image_pil = Image.fromarray(frame).convert('L')

        # Apply contrast
        enhancer = ImageEnhance.Contrast(image_pil)
        image_enhanced = enhancer.enhance(contrast)

        np_image = np.array(image_enhanced)
        parsed_frames.append(np_image)

    # Average fluorescence of the frame
    frame_avgs = []
    for frame in parsed_frames:
        frame_avgs.append(np.average(frame))
    return frame_avgs


def subplot(axis, x, y, contrast):
    '''
    Draw subplot
    '''
    axis.scatter(x, y, c='seagreen')
    axis.set_title(f"{'' if contrast else 'No'} Contrast Modification")
    axis.set_xlabel("Time (s)")
    axis.set_ylabel("Avg Fluorescence (Pixel Values)")


def plot_fluor_over_time():

    img_avgs = parse_frames()
    img_avgs_with_contrast = parse_frames(contrast=CONTRAST_LEVEL)

    fig, axs = plt.subplots(2,1,figsize=(15,10))
    fig.suptitle(f"Fluorescence Over Time\n{FILE.split('.')[0].replace('_', ' ')}", fontsize=16)

    # Define x axis bounds (number of frames)
    x_axis_contrast = range(len(img_avgs_with_contrast))
    x_axis_no_contrast = [x for x in range(len(img_avgs)*3) if x % 3 == 0]

    subplot(axs[0], x_axis_no_contrast, img_avgs, False) # No Contrast
    subplot(axs[1], x_axis_contrast, img_avgs_with_contrast, True) # Contrast

    plt.tight_layout()

    if SAVE_PREFIX is None:
        plt.show()
    else:
        plt.savefig(f"{SAVE_PREFIX}_{FILE.split('.')[0]}_contrast{CONTRAST_LEVEL}_fluorescence_plots.png")


if __name__ == "__main__":
    plot_fluor_over_time()
