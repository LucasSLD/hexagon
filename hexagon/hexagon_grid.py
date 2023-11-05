import numpy as np

def flat_hex_to_pixel(q : float, r : float, size : int) -> tuple[float, float]:
    """
    Converts hexagonal coordinates (flat hexagon grid) to pixel coordinates
    Args:
        q (float): first hexagonal axis coordinate
        r (float): second hexagonal axis coordinate
        size (int): external radius of one hexagon in pixel

    Returns:
        tuple[float, float]: pixel coordinates of the center of the hexagon with hex coordinates (q,r)
    """
    x = size * 3/2 * q
    y = size * (np.sqrt(3)/2 * q  +  np.sqrt(3) * r)
    return (x,y)

def pixel_to_flat_hex(x : int, y : int, size : int) -> tuple[int, int]:
    """
    Get the coordinates (flat hexagon grid) from pixel coordinates (screen space)
    Args:
        x (int): pixel's horizontal coordinate
        y (int): pixel's vetical coordinate
        size (int): external radius of one hexagon in pixel

    Returns:
        tuple[int, int]: hexagonal coordinates (q,r)
    """
    q = 2/3 * x/size
    r = (-1/3 * x + np.sqrt(3)/3 * y)/size
    return axial_round(q,r)

def axial_round(q : float, r : float) -> tuple[int, int]:
    """
    Round the axial coordinates to the nearest hexagon
    Args:
        q (float): first axial coordinate
        r (float): second axial coordinate

    Returns:
        tuple[int, int]: axial coordinates of the nearest hexagon
    """
    cube = axial_to_cube(q,r)
    cube_rounded = cube_round(cube[0],cube[1],cube[2])
    return cube_to_axial(cube_rounded[0],cube_rounded[1],cube_rounded[2])

def axial_to_cube(q : float | int, r : float | int) -> tuple[float, float] | tuple[int, int]:
    """
    Converts axial coordinates to cube coordinates
    Args:
        q (float | int): first axial coordinate
        r (float | int): second axial coordinate

    Returns:
        tuple[float, float] | tuple[int, int]: cube coordinates 
    """
    return (q,r,-q-r)

def cube_to_axial(q : float | int, r : float | int, s : float | int) -> tuple[float, float] | tuple[int, int]:
    """
    Converts cube coordinates to axial coordinates
    Args:
        q (float | int): first cube coordinate
        r (float | int): second cube coordinate
        s (float | int): third cube coordinate

    Returns:
        tuple[float, float] | tuple[int, int]: 
    """
    return (q,r)

def cube_round(q_float : float, r_float : float, s_float : float) -> tuple[int, int, int]:
    """
    Rounds cube coordinates to the nearest hexagon
    Args:
        q_float (float): first cube coordinate
        r_float (float): second cube coordinate
        s_float (float): third cube coordinate

    Returns:
        tuple[int, int, int]: cube coordinates rounded to the nearest hexagon
    """
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

def map_value_from_ab_to_xy(value : float, a : float, b : float, x : float, y : float) -> float:
    """
    Maps a value from a source range [a,b] to a target range [x,y]
    Args:
        value (float): The value to map
        a (float): Lower bound of the source range
        b (float): Higher bound of the target range
        x (float): Lower bound of the target range
        y (float): Higher bound of the target range

    Returns:
        float: the value of "value" mapped from [a,b] to [x,y] 
    """
    assert a <= b
    assert x <= y
    assert value >= a and value <= b
    return (value-a)/(b-a) * (y-x) + x

def corners_from_hex_coordinates(q : float, r : float, size : int) -> list[int]:
    """
    Compute the pixel coordinates of the corners of the hexagon with coordinates (q,r)
    Args:
        q (float): first axial coordinate
        r (float): second axial coordinate
        size (int): external radius of one hexagon in pixel

    Returns:
        list[int]: pixel coordinates of each corner of the hexagon
    """
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
    assert r >= min_r
    assert q >= min_q
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
    assert i >= 0
    assert j >= 0
    return(i + min_q, j + min_r)

if __name__ == "__main__": # pragma: no cover
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