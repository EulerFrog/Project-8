import matplotlib.pyplot as plt
from PIL import Image, ImageSequence, ImageEnhance
import tifffile as tf
import numpy as np
from matplotlib.animation import FuncAnimation

FILE_PATH = 'dish2_ATP_1_MMStack_Pos0.ome.tif'
CONTRAST_LEVEL = 2.0
SAVE_PREFIX = 'contrast'

# Min/Max Normalization
def normalize(data):
    data_min = np.min(data)
    data_max = np.max(data)
    data_norm = (data - data_min) / (data_max - data_min)
    return data_norm

# Parse frames
images = tf.imread(FILE_PATH)
images_np = []
images_with_contrast = []
for img in images:
    # no contrast change
    image_pil = Image.fromarray(img).convert('L') # Convert to grayscale
    image_numpy = np.array(image_pil)
    images_np.append(image_numpy)

    # constrast change
    enhancer = ImageEnhance.Contrast(image_pil)
    image_enhanced = enhancer.enhance(CONTRAST_LEVEL) # Increase contrast
    image_numpy_with_contrast = np.array(image_enhanced)
    images_with_contrast.append(image_numpy_with_contrast)

# No contrast frame averages
img_avgs = []
for img in images_np:
    img_avgs.append(np.average(img))

# Constrast frame averages
img_avgs_with_contrast = []
for img in images_with_contrast:
    img_avgs_with_contrast.append(np.average(img))

fig, axs = plt.subplots(2,1,figsize=(15,10))
fig.suptitle(f"Fluorescence Over Time\n{FILE_PATH.split('.')[0].replace('_', ' ')}", fontsize=16)

# Define x axis bounds (number of frames)
x_axis_contrast = range(len(img_avgs_with_contrast))
x_axis_no_contrast = range(len(img_avgs))

# Draw subplot
def subplot(axis, x, y, contrast):
    axis.scatter(x, y, c='seagreen')
    axis.set_title(f"{'' if contrast else 'No'} Contrast Modification")
    axis.set_xlabel("Frame")
    axis.set_ylabel("Avg Fluorescence (Pixel Values)")

subplot(axs[0], x_axis_no_contrast, img_avgs, False) # No Contrast
subplot(axs[1], x_axis_contrast, img_avgs_with_contrast, True) # Contrast

plt.tight_layout()

if SAVE_PREFIX is None:
    plt.show()
else:
    plt.savefig(f"{SAVE_PREFIX}_{FILE_PATH.split('.')[0]}_contrast{CONTRAST_LEVEL}_fluorescence_plots.png")
