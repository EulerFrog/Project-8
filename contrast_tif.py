import tifffile as tf
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
import cv2
import numpy as np

FILE_PATH = 'video.tif'
CONTRAST_LEVEL = 5.0
SHOW_CONTOURS = False

# Parse frames
images = tf.imread(FILE_PATH)

# Display gif live, don't save

fig, ax = plt.subplots()
im = ax.imshow(images[0])
plt.subplots_adjust(bottom=0.2)
ax.axis('off')

ax2 = plt.axes([0.2,0.05, 0.6, 0.03])
slider = Slider(ax2, valmin=0, valmax=50, label='Contrast')

def update(frame):
    ax.set_title(frame)
    img = Image.fromarray(images[frame]).convert('L')
    enhancer = ImageEnhance.Contrast(img)
    img = np.array(enhancer.enhance(slider.val))

    if SHOW_CONTOURS:
        contours, pyramid = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        img = cv2.drawContours(img, contours, -1, (0,255,0), 3)

    im.set_array(img)
    return [im]

ani = FuncAnimation(fig, update, frames=len(images), interval=50, blit=True)
plt.show()
