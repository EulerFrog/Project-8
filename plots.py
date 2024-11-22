import matplotlib.pyplot as plt
import os
from PIL import Image, ImageSequence, ImageEnhance
import tifffile as tf
import numpy as np
from matplotlib.animation import FuncAnimation
from scipy.optimize import curve_fit
from compute_regions import compute_regions

DATA_DIR = 'data'
FILE = 'data/dish3.tif'
ROI_PATH = 'data/dish3_roi.zip'
CONTRAST_LEVEL = 2.0
SAVE_PREFIX = None

def normalize(data):
    '''
    Parameters:
        - Data: length 200 (for a specific cell or averaged dish)
    Function:
        - Normalize data between [1,2] in the style of Katie Lane
    Returns:
        - List of normalized data
    '''
    data_np = np.array(data)
    min_norm_avgs = data_np / np.mean(data_np[-5:])
    full_norm_avgs = ((min_norm_avgs - 1) / ((np.mean(min_norm_avgs[:5])) -1))+1
    return full_norm_avgs.tolist()

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


def plot_fluor_over_time(img_avgs, img_avgs_with_contrast):
    fig, axs = plt.subplots(2,1,figsize=(15,10))
    fig.suptitle(f"Fluorescence Over Time\n{FILE.split('.')[0].replace('_', ' ')}", fontsize=16)

    # Define x axis bounds (number of frames)
    x_axis_contrast = [x for x in range(len(img_avgs_with_contrast)*3) if x % 3 == 0]
    x_axis_no_contrast = [x for x in range(len(img_avgs)*3) if x % 3 == 0]

    subplot(axs[0], x_axis_no_contrast, img_avgs, False) # No Contrast
    subplot(axs[1], x_axis_contrast, img_avgs_with_contrast, True) # Contrast

    plt.tight_layout()

    if SAVE_PREFIX is None:
        plt.show()
    else:
        plt.savefig(f"{SAVE_PREFIX}_{FILE.split('.')[0]}_contrast{CONTRAST_LEVEL}_fluorescence_plots.png")


def truncate_decay(data : np.ndarray):
    '''
    data.shape = [cells,frames], contains average fluorescence values 
    '''
    # Truncate data so we only have decay information
    data = data.T
    data = data.tolist()
    for i in range(len(data)):
        max_value = np.max(data[i])
        max_index = len(data[i]) - 1 - data[i][::-1].index(max_value)
        data[i] = data[i][max_index:]
    return data


def plot_decay_over_time(data):

    def frames_to_seconds(frames):
        return [x for x in range(len(frames)*3) if x % 3 == 0]

    # Plot decays
    x_values = []
    y_values = []
    max_len = 0
    for i in range(len(data)):
        normalized_data = normalize(data[i])
        plt.scatter(frames_to_seconds(range(len(normalized_data)-1)), normalized_data[:-1], s=5, marker='o', c="black")
        plt.scatter((len(normalized_data)-1)*3, normalized_data[-1], c="cadetblue", marker='*', zorder=5)
        x_values.extend(range(len(normalized_data)))
        y_values.extend(normalized_data)
        max_len = len(normalized_data) if len(normalized_data) > max_len else max_len

    # Indicate equation governing line of best fit
    def exponential(t,a,b,c):
        return a * np.exp(b * t) + c

    # Fit exponential curve
    '''
    maxfev: maximum iterations to find line
    p0: initial guess; initialized to the sign of what the parameter should be
    popt: optimal parameters (a, b, c)
    '''
    popt, pcov = curve_fit(exponential, x_values, y_values, maxfev=5000, p0=[1, -1, 1])
    a,b,c = popt
    x_fitted = np.linspace(min(x_values), max(x_values), max_len)
    y_fitted = exponential(x_fitted, a, b, c)

    # Plot line of best fit
    plt.plot(frames_to_seconds(x_fitted), y_fitted, c = "red", linewidth=2, label=f"y = {a:.2f} * exp({b:.2f} * x) + {c:.2f}")
    plt.legend()
    plt.title("Fluorescence Decay Over Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Fluorescence (Normalized)")
    plt.show()


def main():
    #img_avgs = parse_frames()
    #img_avgs_with_contrast = parse_frames(contrast=CONTRAST_LEVEL)
    #plot_fluor_over_time(img_avgs, img_avgs_with_contrast)

    data = truncate_decay(compute_regions(FILE, ROI_PATH))
    plot_decay_over_time(data)


if __name__ == "__main__":
    main()
