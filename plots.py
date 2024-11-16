import matplotlib.pyplot as plt 
from PIL import Image, ImageSequence, ImageEnhance
import tifffile as tf
import numpy as np 
from matplotlib.animation import FuncAnimation

FILE_PATH = 'dish2.tif' 
# GIF_FILE = 'dish2.gif'
CONTRAST_LEVEL = 2.0
SAVE_PLT = True 

def normalization(data):
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


img_avgs = []
for img in images_np:
    img_avgs.append(np.average(img))

img_avgs_with_contrast = []
for img in images_with_contrast:
    img_avgs_with_contrast.append(np.average(img))

if not SAVE_PLT:
    # w/ normalization, w/ contrast
    plt.plot(normalization(img_avgs_with_contrast))
    plt.title("Normalization and Contrast Modification")
    plt.show()
    # w/out normalization, w/out contrast
    plt.plot(img_avgs)
    plt.title("No Normalization, No Contrast Modification")
    plt.show()
    # w/ normalization, w/out contrast
    plt.plot(normalization(img_avgs))
    plt.title("Normalization and No Contrast Modification")
    plt.show()
    # w/out normalization, w/ contrast
    plt.plot(img_avgs_with_contrast)
    plt.title("No Normalization, Contrast Modification")
    plt.show()

else:
    # w/ normalization, w/ contrast
    plt.plot(normalization(img_avgs_with_contrast))
    plt.title("Normalization and Contrast Modification")
    plt.savefig('norm_contrast.png')
    plt.close()
    # w/out normalization, w/out contrast
    plt.plot(img_avgs)
    plt.title("No Normalization, No Contrast Modification")
    plt.savefig('no_norm_no_contrast.png')
    plt.close()
    # w/ normalization, w/out contrast
    plt.plot(normalization(img_avgs))
    plt.title("Normalization and No Contrast Modification")
    plt.savefig('norm_only.png')
    plt.close()
    # w/out normalization, w/ contrast
    plt.plot(img_avgs_with_contrast)
    plt.title("No Normalization, Contrast Modification")
    plt.savefig('contrast_only.png')
    plt.close()