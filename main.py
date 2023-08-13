import math

from PIL import Image

from transformations import vertical_rescale, horizontal_flatten, reprojection, ramped_reprojection
from utils import cubic_normalise


def process(image_name, version):
    image = Image.open(image_name + ".jpg")
    image = image.resize((500, 500), Image.Resampling.LANCZOS)
    image = image.convert("RGB")
    in_pixels = image.load()
    in_width, in_height = image.size
    if in_width != in_height:
        raise Exception("expected input to be square")

    arc_length = in_height
    inner_triangle_height = int(math.sqrt((arc_length ** 2 - (arc_length / 2) ** 2)))

    v_scaled_image = Image.new("RGBA", (arc_length, inner_triangle_height), (0, 0, 0, 0))
    v_scaled_loaded = v_scaled_image.load()
    v_scaled_pixels = vertical_rescale(arc_length, inner_triangle_height, in_pixels, v_scaled_loaded)

    h_scaled_image = Image.new("RGBA", (arc_length, inner_triangle_height), (0, 0, 0, 0))
    h_scaled_loaded = h_scaled_image.load()
    h_scaled_pixels = (ramped_reprojection if version == "v4" else reprojection)\
                        (arc_length, inner_triangle_height, v_scaled_pixels, h_scaled_loaded)

    h_flattened_image = Image.new("RGBA", (arc_length, inner_triangle_height), (0, 0, 0, 0))
    h_flattened_loaded = h_flattened_image.load()
    h_flattened_pixels = horizontal_flatten(arc_length, inner_triangle_height, h_scaled_pixels, h_flattened_loaded)

    h_flattened_image.save(image_name + "_cahill.png")


# def preprocess():
#     bathy_image = Image.open("bathy.jpg")
#     bathy_image = bathy_image.convert("RGB")
#     bathy_pixels = bathy_image.load()
#     topo_image = Image.open("topo.jpg")
#     topo_image = topo_image.convert("RGB")
#     topo_pixels = topo_image.load()
#
#     width, height = bathy_image.size
#
#     output = Image.new("RGB", (width, height), (0, 0, 0))
#     output_pixels = output.load()
#
#     for y in range(height):
#         for x in range(width):
#             bathy = bathy_pixels[x, y][0]
#             topo = topo_pixels[x, y][0]
#             rescaled_topo = cubic_normalise(max(topo - 14, 0) / 255) * 255
#             val = int((bathy / 5) + (rescaled_topo + 64 if bathy < 50 else rescaled_topo))
#
#             output_pixels[x, y] = (val, val, val)
#
#     output.save("topobathy.jpg")


# preprocess()


# process("shaded/c1", "v4")

for i in range(1, 5):
    process("cahill/c" + str(i), "v3")
for i in range(5, 9):
    process("cahill/c" + str(i), "v3")






























