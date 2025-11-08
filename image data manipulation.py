from PIL import Image
from typing import List


def mirror(raw: List[List[List[int]]])-> None:
    """
    Assume raw is image data. Modifies raw by reversing all the rows
    of the data.

    >>> raw = [[[233, 100, 115], [0, 0, 0], [255, 255, 255]],
               [[199, 201, 116], [1, 9, 0], [255, 255, 255]]]
    >>> mirror(raw)
    >>> raw
    [[[255, 255, 255], [0, 0, 0], [233, 100, 115]],
     [[255, 255, 255], [1, 9, 0], [199, 201, 116]]]
    """
    for i in range(len(raw)):
        raw[i] = raw[i][::-1]



def grey(raw: List[List[List[int]]])-> None:
    """[p;
    Assume raw is image data. Modifies raw "averaging out" each
    pixel of raw. Specifically, for each pixel it totals the RGB
    values, integer divides by three, and sets the all RGB values
    equal to this new valuemm

    >>> raw = [[[233, 100, 115], [0, 0, 0], [255, 255, 255]],
               [[199, 201, 116], [1, 9, 0], [255, 255, 255]]]
    >>> grey(raw)
    >>> raw
    [[[149, 149, 149], [0, 0, 0], [255, 255, 255]],
     [[172, 172, 172], [3, 3, 3], [255, 255, 255]]]
    """
    for i in range(len(raw)):
        for j in range(len(raw[i])):
            total = 0
            for k in range(len(raw[i][j])):
                total += raw[i][j][k]           
            raw[i][j] = [total//3,total//3, total//3]


def invert(raw: List[List[List[int]]])-> None:
    """
    Assume raw is image data. Modifies raw inverting each pixel.
    To invert a pixel, you swap all the max values, with all the
    minimum values. See the doc tests for examples.

    >>> raw = [[[233, 100, 115], [0, 0, 0], [255, 255, 0]],
               [[199, 201, 116], [1, 9, 0], [255, 100, 100]]]
    >>> invert(raw)
    >>> raw
    [[[100, 233, 115], [0, 0, 0], [0, 0, 255]],
     [[199, 116, 201], [1, 0, 9], [100, 255, 255]]]
    """
    for i in range(len(raw)):
        for j in range(len(raw[i])):
            pixel = raw[i][j]
            max_value = max(pixel)
            min_value = min(pixel)
            new_pixel = []
            for x in pixel:
                if x == max_value:
                    new_pixel.append(min_value)
                elif x == min_value:
                    new_pixel.append(max_value)
                else:
                    new_pixel.append(x)
            raw[i][j] = new_pixel


def merge(raw1: List[List[List[int]]], raw2: List[List[List[int]]])-> List[List[List[int]]]:
    """
    Merges raw1 and raw2 into new raw image data and returns it.
    It merges them using the following rule/procedure.
    1) The new raw image data has height equal to the max height of raw1 and raw2
    2) The new raw image data has width equal to the max width of raw1 and raw2
    3) The pixel data at cell (i,j) in the new raw image data will be (in this order):
       3.1) a black pixel [0, 0, 0], if there is no pixel data in raw1 or raw2
       at cell (i,j)
       3.2) raw1[i][j] if there is no pixel data at raw2[i][j]
       3.3) raw2[i][j] if there is no pixel data at raw1[i][j]
       3.4) raw1[i][j] if i is even
       3.5) raw2[i][j] if i is odd
    """
    new_data = []
    height = max(len(raw1), len(raw2))
    width = max(len(raw1[0]), len(raw2[0]))
    for i in range(height):
        new_row = []
        for j in range(width):
            if i < len(raw1) and j < len(raw1[i]):
                p1 = raw1[i][j]
            else:
                p1 = None
            if i < len(raw2) and j < len(raw2[i]):
                p2 = raw2[i][j]
            else:
                p2 = None
                
            if p1 is None and p2 is None:
                new_row.append([0,0,0])
            elif p2 is None:
                new_row.append(p1)
            elif p1 is None:
                new_row.append(p2)
            else:
                if i % 2 == 0:
                    new_row.append(p1)
                else:
                    new_row.append(p2)
        new_data.append(new_row)
    return new_data


def compress(raw: List[List[List[int]]])-> List[List[List[int]]]:
    """
    Compresses raw by going through the pixels and combining a pixel with
    the ones directly to the right, below and diagonally to the lower right.
    For each RGB values it takes the average of these four pixels using integer
    division. If it is a pixel on the "edge" of the image, it only takes the
    relevant pixels to average across. See the second doctest for an example of
    this.

    >>> raw = [[[233, 100, 115], [0, 0, 0], [255, 255, 0], [3, 6, 7]],
               [[199, 201, 116], [1, 9, 0], [255, 100, 100], [99, 99, 0]],
               [[200, 200, 200], [1, 9, 0], [255, 100, 100], [99, 99, 0]],
               [[50, 100, 150], [1, 9, 0], [211, 5, 22], [199, 0, 10]]]
    >>> raw1 = compress(raw)
    >>> raw1
    [[[108, 77, 57], [153, 115, 26]],
     [[63, 79, 87], [191, 51, 33]]]

    >>> raw = [[[233, 100, 115], [0, 0, 0], [255, 255, 0]],
               [[199, 201, 116], [1, 9, 0], [255, 100, 100]],
               [[123, 233, 151], [111, 99, 10], [0, 1, 1]]]
    >>> raw2 = compress(raw)
    >>> raw2
    [[[108, 77, 57], [255, 177, 50]],
     [[117, 166, 80], [0, 1, 1]]]
    """
    height = len(raw)
    width = len(raw[0])
    new_data = []
    for i in range(0, height, 2):
        new_row = []
        for j in range(0, width, 2):
            pixels = [raw[i][j]]
            if j+1 < width:
                pixels.append(raw[i][j+1])
            if i+1 < height:
                pixels.append(raw[i+1][j])
                if j+1 < width:
                    pixels.append(raw[i+1][j+1])
                    
            total_r = 0
            total_g = 0
            total_b = 0
            for p in pixels:
                total_r += p[0]
                total_g += p[1]
                total_b += p[2]   
            avg_r = total_r // len(pixels)
            avg_g = total_g // len(pixels)
            avg_b = total_b // len(pixels)
            new_row.append([avg_r, avg_g, avg_b])
        new_data.append(new_row)
    return new_data


"""
**********************************************************

Do not worry about the code below. However, if you wish,
you can us it to read in images, modify the data, and save
new images.

**********************************************************
"""

def get_raw_image(name: str)-> List[List[List[int]]]:
    
    image = Image.open(name)
    num_rows = image.height
    num_columns = image.width
    pixels = image.getdata()
    new_data = []
    
    for i in range(num_rows):
        new_row = []
        for j in range(num_columns):
            new_pixel = list(pixels[i*num_columns + j])
            new_row.append(new_pixel)
        new_data.append(new_row)

    image.close()
    return new_data


def image_from_raw(raw: List[List[List[int]]], name: str)->None:
    image = Image.new("RGB", (len(raw[0]),len(raw)))
    pixels = []
    for row in raw:
        for pixel in row:
            pixels.append(tuple(pixel))
    image.putdata(pixels)
    image.save(name)

