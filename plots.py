import os
import numpy as np
import tifffile as tf
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from compute_regions import compute_regions
from matplotlib.animation import FuncAnimation
from PIL import Image, ImageSequence, ImageEnhance
from utils.enums import NormalizationEnum

SAVE_DIR = None

def normalize(data, norm_type):
    if norm_type == "minmax":
        return NormalizationEnum.MINMAX(data)
    elif norm_type == "katielane":
        return NormalizationEnum.KATIELANE(data)

def frames_to_seconds(frames):
    return [x for x in range(len(frames)*3) if x % 3 == 0]


class Plotter:
    def __init__(self, tif_path, roi_zip_path, normalizer, desired_contrast=1.0):
        self.tif_path = tif_path
        self.roi_zip_path = roi_zip_path
        self.normalizer = normalizer
        self.img_avgs, self.imgs = parse_frames(self.tif_path, self.normalizer, desired_contrast) # list[float], len = num_frames; list[list[float]], images
        self.roi_vectors = compute_regions(self.tif_path, self.roi_zip_path) # list[list[float]], shape = (num_cells, num_frames)
        self.decay_data = truncate_decay(self.roi_vectors) # list[list[float]], shape = (num_cells, {cell's decay length})


    def plot_fluor_over_time(self, img_avgs=None, save=False):
        """Plot flourescence of entire movie"""

        if img_avgs is None:
            img_avgs = self.img_avgs

        plt.figure(figsize=(15,5))
        plt.xlabel("Time (s)")
        plt.ylabel("Fluorescence (Normalized)")
        plt.title(f"Fluorescence Over Time\n{self.tif_path.split('/')[-1].split('.')[0].replace('_', ' ')}", fontsize=16)

        x_axis = frames_to_seconds(range(len(img_avgs)))
        plt.scatter(x_axis, img_avgs, c='seagreen')
        plt.tight_layout()

        if not save:
            plt.show()
        else:
            plt.savefig(f"{SAVE_DIR}/{self.tif_path.split('/')[-1].split('.')[0]}_fluorescence.png")


    def plot_decay_over_time(self, want_best_fit=True, color_by_cell=False, save=False, data=None):
        """Plot fluorescence decay"""

        if data is None:
            data = self.decay_data

        # Define plot coloring
        if color_by_cell:
            colors = plt.cm.tab20.colors
            end_colors = colors
        else:
            colors = ['black' for _ in range(len(data))]
            end_colors = ['darkturquoise' for _ in range(len(data))]

        # Plot decays
        x_values = []
        y_values = []
        max_len = 0
        for i in range(len(data)):
            normalized_data = normalize(data[i], self.normalizer)
            plt.scatter(frames_to_seconds(range(len(normalized_data)-1)), normalized_data[:-1], s=5, marker='o', c=colors[i%len(colors)])
            plt.scatter((len(normalized_data)-1)*3, normalized_data[-1], c=end_colors[i%len(colors)], marker='*', zorder=5)
            x_values.extend(range(len(normalized_data)))
            y_values.extend(normalized_data)
            max_len = len(normalized_data) if len(normalized_data) > max_len else max_len

        # Fit exponential curve
        def exponential(t,a,b,c):
            return a * np.exp(b * t) + c
        popt, pcov = curve_fit(exponential, x_values, y_values, maxfev=5000, p0=[1, -1, 1])
        a,b,c = popt
        x_fitted = np.linspace(min(x_values), max(x_values), max_len)
        y_fitted = exponential(x_fitted, a, b, c)

        # Plot line of best fit
        if want_best_fit:
            plt.plot(frames_to_seconds(x_fitted), y_fitted, c = "red", linewidth=2, label=f"y = {a:.2f} * exp({b:.2f} * x) + {c:.2f}")
            plt.legend()

        plt.title(f"Fluorescence Decay Over Time\n{self.tif_path.split('/')[-1].split('.')[0].replace('_', ' ')}", fontsize=16)
        plt.xlabel("Time (s)")
        plt.ylabel("Fluorescence (Normalized)")

        if not save:
            plt.show()
        else:
            plt.savefig(f"{SAVE_DIR}/{self.tif_path.split('/')[-1].split('.')[0]}_decay.png")


    def display_gif(self, save=False):

        # Display gif live, don't save
        if not save:
            fig, ax = plt.subplots()
            im = ax.imshow(self.imgs[0], cmap='gray')
            ax.axis('off')
            def update(frame):
                print(frame)
                plt.title(frame)
                im.set_array(self.imgs[frame])
                return [im]
            ani = FuncAnimation(fig, update, frames=len(self.imgs), interval=50, blit=False)
            plt.show()

        # Save gif
        else:
            self.imgs[0].save(f"{SAVE_DIR}/{self.tif_path.split('/')[-1].split('.')[0]}.gif", save_all=True, append_images=self.imgs[1:], duration=50, loop=0)



def parse_frames(file, normalizer='katlielane', contrast=1.0):
    '''
        - Read frames from TIF file
        - Alter the contrast, 1.0 is no change
        - Average fluorescence of the whole image
    '''
    frames = tf.imread(file)
    parsed_frames = []

    # Adjust contrast and grayscale
    for frame in frames:
        image_pil = Image.fromarray(frame).convert('L')
        enhancer = ImageEnhance.Contrast(image_pil)
        image_enhanced = enhancer.enhance(contrast)
        np_image = np.array(image_enhanced)
        parsed_frames.append(np_image)

    # Average fluorescence of the frame
    frame_avgs = []
    for frame in parsed_frames:
        frame_avgs.append(np.average(frame))

    normalized_data = normalize(frame_avgs, normalizer)
    return normalized_data, parsed_frames


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


def make_plots(tif_path, roi_path, desired_norm='katielane', desired_contrast=5.0):
    SAVE_DIR = tif_path.split('/')[-2]

    plotter = Plotter(tif_path, roi_path, desired_norm, desired_contrast)
    plotter.plot_fluor_over_time()
    plotter.plot_decay_over_time(color_by_cell=True)
    plotter.display_gif()


if __name__ == "__main__":
    make_plots('data/dish3.tif', 'data/dish3_roi.zip')
