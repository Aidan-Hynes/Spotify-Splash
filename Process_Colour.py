from PIL import Image
import requests
from io import BytesIO
from operator import itemgetter
import math


def get_rgb_value(cover_info):
    if cover_info is not None:
        url = cover_info['url']
        height = cover_info['height']
        width = cover_info['width']
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        img.thumbnail((height, width))
        paletted = img.convert('P', palette=Image.ADAPTIVE)

        palette = paletted.getpalette()
        color_counts = sorted(paletted.getcolors(), reverse=True)

        colour_list = []
        for colour_index in color_counts:
            colour = palette[colour_index[1] * 3:colour_index[1] * 3 + 3]
            brightness = math.sqrt(0.299*colour[0]**2 + 0.587*colour[1]**2 + 0.114*colour[1]**2)
            if 180 > brightness > 50:
                colour.append(brightness)
                colour_list.append(colour)
            if len(colour_list) >= 3: break

        print(colour_list)
        colour_list = sorted(colour_list, key=itemgetter(3))
        print(colour_list)

        return colour_list[0]
