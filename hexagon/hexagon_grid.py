import numpy as np

def flat_hex_to_pixel(q,r,size):
    x = size * 3/2 * q
    y = size * (np.sqrt(3)/2 * q  +  np.sqrt(3) * r)
    return (x,y)

def pixel_to_flat_hex(x,y,size):
    q = 2/3 * x/size
    r = (-1/3 * x + np.sqrt(3)/3 * y)/size
    return axial_round(q,r)

def axial_round(q,r):
    cube = axial_to_cube(q,r)
    cube_rounded = cube_round(cube[0],cube[1],cube[2])
    return cube_to_axial(cube_rounded[0],cube_rounded[1],cube_rounded[2])

def axial_to_cube(q,r):
    return (q,r,-q-r)

def cube_to_axial(q,r,s):
    return (q,r)

def cube_round(q_float,r_float,s_float):
    q = int(round(q_float,0))
    r = int(round(r_float,0))
    s = int(round(s_float,0))

    q_diff = abs(q - q_float)
    r_diff = abs(r - r_float)
    s_diff = abs(s - s_float)

    if q_diff > r_diff and q_diff > s_diff:
        q = -r-s
    elif r_diff > s_diff:
        r = -q-s
    else:
        s = -q-r
    return (q,r,s)

def map_value_from_ab_to_xy(value,a,b,x,y):
    """
    Maps a value from a source range [a,b] to a target range [x,y]
    Args:
        value : The value to map
        a : Lower bound of the source range
        b : Higher bound of the target range
        x : Lower bound of the target range
        y : Higher bound of the target range

    Returns:
        _type_: the value of "value" mapped from [a,b] to [x,y] 
    """
    assert a <= b
    assert x <= y
    assert value >= a and value <= b
    return (value-a)/(b-a) * (y-x) + x

def corners_from_hex_coordinates(q,r,size):
    center = flat_hex_to_pixel(q,r,size)
    corners = []
    for i in range(6):
        angle = np.pi/3* i
        corner = [
            round(center[0] + size * np.cos(angle)), 
            round(center[1] + size * np.sin(angle))
        ]
        corners.append(corner)
    return corners


if __name__ == "__main__":
    from PIL import Image
    shape_0 = 500
    shape_1 = 500
    size = 50
    img = np.zeros(shape=(shape_0,shape_1,2),dtype=int)
    for x in range(shape_0):
        for y in range(shape_1):
            hex_coord = pixel_to_flat_hex(y,x,size) # careful about screen space coordinates (x and y are swapped) -> the element of indexes [x,y] in an array has pixel coordinates (y,x)
            img[x,y,0] = hex_coord[0]
            img[x,y,1] = hex_coord[1]
    

    img_rg = np.zeros(shape=(shape_0,shape_1,3),dtype=np.int16)
    min_q  = np.min(img[:,:,0])
    max_q  = np.max(img[:,:,0])
    min_r  = np.min(img[:,:,1])
    max_r  = np.max(img[:,:,1])
    for i in range(shape_0):
        for j in range(shape_1):
            img_rg[i,j,0] = map_value_from_ab_to_xy(img[i,j,0],min_q,max_q,0,255)
            img_rg[i,j,1] = map_value_from_ab_to_xy(img[i,j,1],min_r,max_r,0,255)

    print(img_rg)
    Image.fromarray(img_rg.astype(np.uint8)).show("hexagonal grid")