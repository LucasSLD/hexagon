from PIL import Image
from copy import deepcopy
import numpy as np

image = Image.open("img/hexagon.png")
px = image.load()
print(image.size)
        