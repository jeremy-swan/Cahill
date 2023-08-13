import math


def circle_circle_intersect(x0, y0, r0, x1, y1, r1):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    d = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

    # non intersecting
    if d > r0 + r1:
        return None
    # One circle within other
    if d < abs(r0 - r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
    else:
        a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
        h = math.sqrt(r0 ** 2 - a ** 2)
        x2 = x0 + a * (x1 - x0) / d
        y2 = y0 + a * (y1 - y0) / d
        x3 = x2 + h * (y1 - y0) / d
        y3 = y2 - h * (x1 - x0) / d

        x4 = x2 - h * (y1 - y0) / d
        y4 = y2 + h * (x1 - x0) / d

        return (x3, y3), (x4, y4)


def circle_line_intersect(lx0, ly0, lx1, ly1, cx, cy, r):
    (p1x, p1y), (p2x, p2y), (cx, cy) = (lx0, ly0), (lx1, ly1), (cx, cy)
    (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
    dx, dy = (x2 - x1), (y2 - y1)
    dr = (dx ** 2 + dy ** 2) ** .5
    big_d = x1 * y2 - x2 * y1
    discriminant = r ** 2 * dr ** 2 - big_d ** 2

    if discriminant < 0:  # No intersection between circle and line
        return []
    else:  # There may be 0, 1, or 2 intersections with the segment
        intersections = [
            (cx + (big_d * dy + sign * (-1 if dy < 0 else 1) * dx * discriminant ** .5) / dr ** 2,
             cy + (-big_d * dx + sign * abs(dy) * discriminant ** .5) / dr ** 2)
            for sign in ((1, -1) if dy < 0 else (-1, 1))]  # This makes sure the order along the segment is correct
        if len(intersections) == 2:
            return [intersections[0]]
        else:
            return intersections


def reuleaux_width(r, d):
    h = math.sqrt((r ** 2 - (r / 2) ** 2))
    if d < h:
        # return 2 * math.sqrt(r ** 2 - d ** 2) - r
        return 2 * math.sqrt(r ** 2 - (h - d) ** 2) - r
    else:
        return 2 * math.sqrt((r ** 2 - d ** 2))


def trilinear_interpolation(c000, c001, c010, c011, c100, c101, c110, c111, x, y, z):
    # Interpolate along x-axis
    c00 = c000 * (1 - x) + c100 * x
    c01 = c001 * (1 - x) + c101 * x
    c10 = c010 * (1 - x) + c110 * x
    c11 = c011 * (1 - x) + c111 * x

    # Interpolate along y-axis
    c0 = c00 * (1 - y) + c10 * y
    c1 = c01 * (1 - y) + c11 * y

    # Interpolate along z-axis
    c = c0 * (1 - z) + c1 * z

    return c


def relief_lerp(point):
    _x, _y, _z = point
    x = _x / 255
    y = _y / 255
    z = _z / 255
    # return (max(trilinear_interpolation(0, 0.166, 0.5, 0.33, 0.833, 1, 0.66, 1, x, y, z), 0.5) - 0.5) * 2 * 255
    return trilinear_interpolation(0, 0.166, 0.5, 0.33, 0.833, 1, 0.66, 1, x, y, z) * 255


def constrained_exp(x, exp):
    return min((((x + 1) ** exp) - 1) / ((2 ** exp) - 1), 1)


def cubic_normalise(x):
    return ((((2 * x) - 1) ** 3) + 1) / 2

