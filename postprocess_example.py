#!/usr/bin/env python3
import sys

from PIL import Image, ImageOps
import numpy as np


if __name__ == '__main__':
    assert len(sys.argv) == 2, "Image path must be passed!"
    path = sys.argv[1]

    # load image, discard alpha (if present)
    img = Image.open(path).convert("RGB")

    # remove menu and indicators
    data = np.array(img)
    menu_is_open = (data[40:1815, 40:1815] == 0).all()
    if not menu_is_open:
        # remove the entire menu, and the x in the top right corner
        data[:, :120, :] = 255
        data[40:81, 1324:1364, :] = 255
    else:
        # remove only the menu indicator circle
        data[40:81, 40:81, :] = 255

    # crop to the bounding box
    img = Image.fromarray(data).convert("RGB")
    bbox = ImageOps.invert(img).getbbox()
    img = img.crop(bbox)
    img=ImageOps.invert(img)

    # set alpha channel

    img= img.convert("RGBA")
    datas=img.getdata()

    newData = []
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(path)
