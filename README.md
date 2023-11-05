# **Hexagon Project**

## **Hexagon PNG to SVG converter**
This repository provides a solution to convert an image of a hexagon gird in **png** format and **converts** it to a scalable version (**.svg** file).
### **Example :**
#### **Input**
![png](./img/hexagon.png)
#### **Output**
![svg](./outputs/output.svg)
## **Running this project**
- **Install poetry** on your machine (for detailed instructions click [here](https://python-poetry.org/docs/#installing-with-the-official-installer))
- **Dowload the source code** of this repository
- **Open a terminal** at the **root directory of the project**
- **For Linux user**, if poetry is installed but the command is not recognized, try typing this command in terminal (replace user by your user name): 
> **export PATH="/home/user/.local/bin:$PATH**
- Install project's dependencies
> **poetry install**
### **Using default parameters**
- The img folder contains a default image to test the project. You can run the hexagon/png_to_svg.py file without arguments. The image used as input is the one in the img folder, the output will be put in the output folder with the default name output.svg.
> **poetry run python hexagon/png_to_svg.py**
### **Using custom parameters**
- You can run the png_to_svg.py file with arguments to use your own image, give a specific name to the output file and give a size to the hexagon used in the hexagon grid.
> **poetry run python hexagon/png_to_svg.py *path_to_png_file* *name_of_the_output_file* *hexagon_size***

The output svg file will be stored in the output folder.
### Example
> **poetry run python hexagon/png_to_svg.py img/hexagon.png output_30.svg 30**
#### **Output**
![example output](./outputs/output_30.svg)
#
![coverage badge](./coverage.svg)