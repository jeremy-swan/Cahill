import math

from utils import reuleaux_width, relief_lerp, circle_circle_intersect, constrained_exp, cubic_normalise


def vertical_rescale(arc_length, inner_triangle_height, in_pixels, out_pixels):
    h_rescale = 1
    v_rescale = arc_length / inner_triangle_height

    for y in range(inner_triangle_height):
        for x in range(arc_length):
            out_pixels[x, y] = in_pixels[int(x * h_rescale), int(y * v_rescale)]

    return out_pixels


def reprojection(width, height, in_pixels, out_pixels):
    (P_x, P_y) = (width / 2, 0)
    (Q_x, Q_y) = (0, height)

    for y in range(height - 1):
        curr_width = int(reuleaux_width(width, y))
        offset = int((width - curr_width) / 2)
        for x in range(offset, width - offset):
            (Z_x, Z_y) = (x, y)
            (O_x, O_y) = (P_x, y - (math.sqrt(width ** 2 - (x - P_x) ** 2)))
            (A_x, A_y) = (P_x, O_y + width)

            ramp_ratio = (A_y - height) / (width - height)

            O_r = height * (1 + (1 / (1 - ramp_ratio))) ** 5
            (O_x, O_y) = (P_x, y - (math.sqrt(O_r ** 2 - (x - P_x) ** 2)))
            (A_x, A_y) = (P_x, O_y + O_r)

            (cci_1, cci_2) = circle_circle_intersect(Q_x, Q_y, width, O_x, O_y, O_r)
            (C_x, C_y) = cci_1 if cci_1[1] > cci_2[1] else cci_2
            A_O_Z = math.atan((Z_x - O_x) / (Z_y - O_y))
            A_O_C = math.atan((C_x - O_x) / (C_y - O_y))
            angle_ratio = (A_O_Z + A_O_C) / (A_O_C * 2)

            source_x = min(width * angle_ratio, width - 1)
            source_y = int(A_y)

            if A_y < 0:
                raise Exception('reverse indexing')
            out_pixels[x, y] = in_pixels[source_x, source_y]

    for x in range(width):
        out_pixels[x, height - 1] = in_pixels[x, height - 1]

    return out_pixels


def ramped_reprojection(width, height, in_pixels, out_pixels):
    (P_x, P_y) = (width / 2, 0)
    (Q_x, Q_y) = (0, height)

    for y in range(height):
        curr_width = int(reuleaux_width(width, y))
        offset = int((width - curr_width) / 2)
        for x in range(offset, width - offset):
            (Z_x, Z_y) = (x, y)
            (O_x, O_y) = (P_x, y - (math.sqrt(width ** 2 - (x - P_x) ** 2)))
            (A_x, A_y) = (P_x, O_y + width)
            O_r = width

            ramp_ratio = (A_y - height) / (width - height)

            adjusted_O_r = height * (1 + (1 / (1 - ramp_ratio))) ** 4
            (adjusted_O_x, adjusted_O_y) = (P_x, y - (math.sqrt(adjusted_O_r ** 2 - (x - P_x) ** 2)))
            (adjusted_A_x, adjusted_A_y) = (P_x, adjusted_O_y + adjusted_O_r)

            (cci_1, cci_2) = circle_circle_intersect(Q_x, Q_y, width, O_x, O_y, O_r)
            (C_x, C_y) = cci_1 if cci_1[1] > cci_2[1] else cci_2
            A_O_Z = math.atan((Z_x - O_x) / (Z_y - O_y))
            A_O_C = math.atan((C_x - O_x) / (C_y - O_y))
            angle_ratio = (A_O_Z + A_O_C) / (A_O_C * 2)

            source_x = min(width * angle_ratio, width - 1)

            distance_to_top_ratio = constrained_exp(math.sqrt((x - P_x) ** 2 + (y - P_y) ** 2) / height, 4)
            source_y = (A_y * (1 - distance_to_top_ratio)) + (adjusted_A_y * distance_to_top_ratio)

            if A_y < 0:
                raise Exception('reverse indexing')
            out_pixels[x, y] = in_pixels[source_x, source_y]

    return out_pixels


def horizontal_flatten(width, height, in_pixels, out_pixels):
    for y in range(height):
        curr_width = int(reuleaux_width(width, y))
        target_width = min(int(y * math.tan(math.radians(30)) * 2), width)
        offset = (width - target_width) / 2
        for x in range(target_width):
            factor = x / target_width
            reuleaux_offset = (width - curr_width) / 2

            source_x = int(reuleaux_offset + (curr_width * factor))

            r, g, b, a = in_pixels[source_x, y]
            # val = int(relief_lerp((r, g, b)))
            # val = int(cubic_normalise(cubic_normalise((r - 13) / 255)) * 255)
            out_pixels[x + offset, y] = (r, g, b, 255)

    return out_pixels
