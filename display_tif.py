import tifffile as tf
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

FILE_PATH = 'dish2.tif'
SAVE_GIF = True 
SAVE_NAME = f"{FILE_PATH.split('.')[0]}.gif"
CONTRAST_LEVEL = 2.0

# Parse frames
images = tf.imread(FILE_PATH)
image_pil_list = []
for img in images:
    image_pil = Image.fromarray(img).convert('L') # Convert to grayscale
    enhancer = ImageEnhance.Contrast(image_pil)
    image_enhanced = enhancer.enhance(CONTRAST_LEVEL) # Increase contrast
    image_pil_list.append(image_enhanced)

# Display gif live, don't save
if not SAVE_GIF:
    fig, ax = plt.subplots()
    im = ax.imshow(image_pil_list[0], cmap='gray')
    ax.axis('off')
    def update(frame):
        print(frame)
        plt.title(frame)
        im.set_array(image_pil_list[frame])
        return [im]
    ani = FuncAnimation(fig, update, frames=len(image_pil_list), interval=50, blit=False)
    plt.show()

# Save gif
else:
    image_pil_list[0].save(SAVE_NAME, save_all=True, append_images=image_pil_list[1:], duration=50, loop=0)
