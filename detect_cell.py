import torch, cv2, celldetection as cd
from skimage.data import coins
from matplotlib import pyplot as plt
import tifffile as tf
import numpy as np
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

FILE_PATH = 'video.tif'
CONTRAST_LEVEL = 7.0

# Parse frames
images = tf.imread(FILE_PATH)

# breakpoint()
img = images[0]
image_pil = Image.fromarray(img).convert('L') # Convert to grayscale
enhancer = ImageEnhance.Contrast(image_pil)
img = np.array(enhancer.enhance(CONTRAST_LEVEL))  # Factor > 1 increases contrast, < 1 decreases

# img = (img - img.min()) / (img.max() - img.min()) * 255  # Normalize to 0-255 range
# img = img.astype('uint8')




# Load input
# img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
print(img.dtype, img.shape, (img.min(), img.max()))

contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
img2 = cv2.drawContours(img, contours, -1, (0,255,0), 3)

fig, ax = plt.subplots()
im = ax.imshow(img2)
ax.axis('off')
plt.show()


breakpoint()
# Load pretrained model
# device = 'cuda' if torch.cuda.is_available() else 'cpu'
# # model = cd.fetch_model('ginoro_CpnResNeXt101UNet-fbe875f1a3e5ce2c', check_hash=True).to(device)
# # model = cd.models.ResNet34(in_channels=3, out_channels=1, nd=3)
# model = cd.models.ResNeXt101_32x8d(in_channels=3, pretrained=True).to(device)
# model.eval()
# # breakpoint()

# # Run model
# with torch.no_grad():
#     x = cd.to_tensor(img, transpose=True, device=device, dtype=torch.float32)
#     x = x / 255  # ensure 0..1 range
#     x = x[None]  # add batch dimension: Tensor[3, h, w] -> Tensor[1, 3, h, w]
#     y = model(x)

# # Show results for each batch item
# contours = y['contours']
# for n in range(len(x)):
#     cd.imshow_row(x[n],x[n], figsize=(16, 9), titles=('contours'))
#     cd.plot_contours(contours[n])
#     plt.show()