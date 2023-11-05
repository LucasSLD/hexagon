import hexagon.hexagon_grid as hg
import numpy as np

def test_flat_hex_to_pixel():
    size = 10
    assert hg.flat_hex_to_pixel(0,0,size) == (0.,0.)
    assert hg.flat_hex_to_pixel(1,0,size) == (size*3/2, size*np.sqrt(3)/2)
    assert hg.flat_hex_to_pixel(0,1,size) == (0., size*np.sqrt(3))
    assert hg.flat_hex_to_pixel(1,1,size) == (size*3/2, size*(np.sqrt(3)/2 + np.sqrt(3)))

def test_cube_to_axial():
    q,r,s = np.random.randint(0,10), np.random.randint(0,10), np.random.randint(0,10)
    q_f,r_f,s_f = np.random.random() * 9, np.random.random() * 9, np.random.random() * 9
    assert hg.cube_to_axial(q,r,s) == (q,r)
    assert hg.cube_to_axial(q_f,r_f,s_f) == (q_f,r_f)

def test_axial_to_cube():
    assert hg.axial_to_cube(0,0) == (0, 0, 0)
    assert hg.axial_to_cube(1,0) == (1, 0, -1)
    assert hg.axial_to_cube(0,1) == (0, 1, -1)
    assert hg.axial_to_cube(1,1) == (1, 1, -2)
    assert hg.axial_to_cube(1.5,0.3) == (1.5, 0.3, -1.8)

def test_cube_round():
    assert hg.cube_round(0.5,0.1,0.1) == (0,0,0) 
    assert hg.cube_round(1.5,2.1,0.9) == (-3,2,1)
    assert hg.cube_round(3.1,2.5,0.9) == (3,-4,1)
    assert hg.cube_round(3.1,2.7,0.4) == (3,3,-6)

def test_axial_round():
    q = np.random.random() * np.random.randint(0,10)
    r = np.random.random() * np.random.randint(0,10)
    cube = hg.axial_to_cube(q,r)
    cube_rounded = hg.cube_round(cube[0],cube[1],cube[2])
    assert hg.axial_round(q,r) == hg.cube_to_axial(cube_rounded[0],cube_rounded[1],cube_rounded[2])

def test_pixel_to_flat_hex():
    size = 10
    assert hg.pixel_to_flat_hex(0,0,size) == hg.axial_round(0.,0.)
    assert hg.pixel_to_flat_hex(1,0,size) == hg.axial_round(2/3 / size,-1/3 / size)
    assert hg.pixel_to_flat_hex(0,1,size) == hg.axial_round(0.,np.sqrt(3)/3 / size)
    assert hg.pixel_to_flat_hex(1,1,size) == hg.axial_round(2/3 / size, (-1/3 + np.sqrt(3)/3)/size)

def test_map_value_from_ab_to_xy():
    assert hg.map_value_from_ab_to_xy(0.5,0,1,2,4) == 3
    assert hg.map_value_from_ab_to_xy(-1,-3,0,1,5) == 11/3

def test_corners_from_hex_coordinates():
    size = 10
    assert hg.corners_from_hex_coordinates(0,0,size) == [
        [size,0],
        [round(size*0.5),round(size*np.sqrt(3)/2)],
        [round(-size*0.5),round(size*np.sqrt(3)/2)],
        [round(-size),0],
        [round(-size*0.5),round(-size*np.sqrt(3)/2)],
        [round(size*0.5),round(-size*np.sqrt(3)/2)]
        ]

def test_array_indexes_from_hex_coordinates():
    assert hg.array_indexes_from_hex_coordinates(0,2,-3,2) == (3,0)
    assert hg.array_indexes_from_hex_coordinates(-5,1,-8,-4) == (3,5)

def test_hex_coordinates_from_array_indexes():
    assert hg.hex_coordinates_from_array_indexes(0,0,-3,5) == (-3,5)
    assert hg.hex_coordinates_from_array_indexes(0,0,0,7) == (0,7)
    assert hg.hex_coordinates_from_array_indexes(3,8,2,-4) == (5,4)