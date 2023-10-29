from PIL import Image
from copy import deepcopy
import numpy as np
import hexagon_grid as hg

with Image.open("img/hexagon.png") as image:
	px = image.load()
	print(image.size)

	width = image.size[0]
	height = image.size[1]

size = 10 # hexagons size

hex_coords = np.zeros(shape=(height,width,2),dtype=int)
for x in range(width): # x is the horizontal axis in screen coordinates
    for y in range(height): # y is the vertical axis in screen coordinates
        # (x,y) represents pixel's coodinates
        hex_coord = hg.pixel_to_flat_hex(x,y,size)
        hex_coords[y,x,0] = hex_coord[0]
        hex_coords[y,x,1] = hex_coord[1]
        
min_q = np.min(hex_coords[:,:,0])
max_q = np.max(hex_coords[:,:,0])
min_r = np.min(hex_coords[:,:,1])
max_r = np.max(hex_coords[:,:,1])

def array_indexes_from_hex_coordinates(q : int, r : int, min_q : int, min_r : int) -> tuple[int, int]:
	"""
	Map hexagon's coordinates to indexes of a 0-indexed array
	Args:
		q (int): first hexagonal coordinate
		r (int): second hexagonal coordinate
		min_q (int): min of q in the hexagonal grid
		min_r (int): min of r in the hexagonal grid 

	Returns:
		tuple[int, int]: array coordinates (i,j)
	"""
	return (q-min_q,r-min_r)

def hex_coordinates_from_array_indexes(i : int, j : int, min_q : int, min_r : int) -> tuple[int, int]:
	"""
	Map array indexes to the corresponding hexagonal coordinates with respect to the problem
	specific hexagonal grid in use
	Args:
		i (int): first dimension index
		j (int): second dimension index
		min_q (int): min of q in the hexagonal grid
		min_r (int): min of r in the hexagonal grid

	Returns:
		tuple[int, int]: hexagonal coordinates (q,r)
	"""
	return(i + min_q, j + min_r)


q_range = max_q - min_q + 1 # nb of integers between min_q and max_q
r_range = max_r - min_r + 1

hex_colors = np.zeros(shape=(q_range,r_range,3),dtype=int)
hex_corners = np.zeros(shape=(q_range,r_range,6),dtype=int)
hex_pixels_count = np.zeros(shape=(q_range,r_range),dtype=int)
with Image.open("img/hexagon.png") as img:
	px = img.load() # px[x,y] -> color of the pixel with screen coordinates (x,y)
	for x in range(width):
		for y in range(height):
			q, r = hex_coords[y,x] # for the pixel at position (x,y) we look at the coordinates of the hexagon it is on
			i, j = array_indexes_from_hex_coordinates(q,r,min_q,min_r)
			for k in range(3): hex_colors[i,j,k] += px[x,y][k]
			hex_pixels_count[i,j] += 1
	
	for i in range(hex_pixels_count.shape[0]):
		for j in range(hex_pixels_count.shape[1]):
			if(hex_pixels_count[i,j] > 0):
				hex_colors[i,j] =  hex_colors[i,j]/hex_pixels_count[i,j]

svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" height="{height}" width="{width}">\n"""

for i in range(hex_pixels_count.shape[0]):
	for j in range(hex_pixels_count.shape[1]):
		if(hex_pixels_count[i,j] > 0):
			q, r = hex_coordinates_from_array_indexes(i,j,min_q,min_r)
			corners = hg.corners_from_hex_coordinates(q,r,size)
			svg_content += '	<polygon points="'
			for n, corner in enumerate(corners):
				svg_content += f'{corner[0]} {corner[1]}'
				if n < len(corners) - 1: svg_content +=','
				else: svg_content += '" '
			svg_content += f'fill="rgb({hex_colors[i,j,0]},{hex_colors[i,j,1]},{hex_colors[i,j,2]})" />\n'

svg_content += "</svg>"

with open('outputs/output.svg','w') as f:
    f.write(svg_content)