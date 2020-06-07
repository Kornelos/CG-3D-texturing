import numpy as np
from math import cos, sin, tan, pi


class Triangle:
    # class consist of 3 vertices V = (p,n,t) p - point (x,y,z,1) n - normal vector t - texture (u,v)
    def __init__(self, p1, p2, p3):
        self.verts = [p1, p2, p3]

    def draw(self):
        # to do
        pass

    def get_points(self):
        return [self.verts[0][0], self.verts[1][0], self.verts[2][0]]

    def get_texture(self):
        return [self.verts[0][2], self.verts[1][2], self.verts[2][2]]

    def get_norm(self):
        return self.verts[0][1]

    def __repr__(self):
        return str(self.verts)


class Cylinder:
    def __init__(self):
        h = 2  # height
        r = 1  # radius
        n = 40  # number of the sides of the prism used to draw circle

        self.h = h
        # points on the bottom and the top of the cylinder
        # n = 0..n
        p = [None] * (4 * n + 2)

        # points on top
        p_top = [np.array([0, h, 0, 1])] + [np.array([r * cos(2 * pi * i / n), h, r * sin(2 * pi * i / n), 1]) for i in
                                            range(n)]
        p[0:n + 1] = p_top
        # normal vector top
        n_top = [np.array([0, 1, 0, 0]) for _ in range(n + 1)]
        # points on bottom
        p_bot = [np.array([r * cos(2 * pi * i / n), 0, r * sin(2 * pi * i / n), 1]) for i in range(n)] + [
            np.array([0, 0, 0, 1])]
        p[(3 * n + 1):(4 * n + 2)] = p_bot
        # normal vector bottom
        n_bot = [np.array([0, -1, 0, 0]) for _ in range(n + 1)]

        # sides
        # n = n+1 .. 2n and 2n+1 .. 3n
        p_sides = [np.array(p[i - n]) for i in range(n + 1, 2 * n + 1)] + [np.array(p[i + n]) for i in
                                                                           range(2 * n + 1, 3 * n + 1)]
        p[(n + 1):3 * n + 1] = p_sides
        # sides norm
        n_sides = [np.array([p[i][0] / r, 0, p[i][2] / r, 0]) for i in range(n + 1, 3 * n + 1)]
        norms = n_top + n_sides + n_bot
        self.points = p
        # texture coordinates:
        t = [np.array([0.25, 0.25])] + \
            [np.array([0.25 * (1 + cos(2 * pi * (i - 1) / n)), 0.25 * (1 + sin(2 * pi * (i - 1) / n))]) for i in
             range(1, n + 1)] + \
            [np.array([(i - 1) / (n - 1), 1]) for i in range(1, n + 1)] + \
            [np.array([(i - 1) / (n - 1), 0.5]) for i in range(1, n + 1)] + \
            [np.array([0.25 * (3 + cos(2 * pi * (i - 1) / n)), 0.25 * (1 + sin(2 * pi * (i - 1) / n))]) for i in
             range(1, n + 1)] + \
            [np.array([0.75, 0.25])]

        # create vertexes (Vi)
        verts = []
        for i in range(4 * n + 2):
            verts += [(p[i], norms[i], t[i])]

        top_tri = [Triangle(verts[0], verts[i + 2], verts[i + 1]) for i in range(n - 1)] + [
            Triangle(verts[0], verts[1], verts[n])]
        bot_tri = [Triangle(verts[4 * n + 1], verts[i + 1], verts[i + 2]) for i in range(3 * n, 4 * n - 1)] + [
            Triangle(verts[4 * n + 1], verts[4 * n], verts[3 * n + 1])]

        # side triangles n, ... 3n-1
        side_tri = [Triangle(verts[i + 1], verts[i + 2], verts[i + 1 + n]) for i in range(n, 2 * n - 1)] + \
                   [Triangle(verts[2 * n], verts[n + 1], verts[3 * n])] + \
                   [Triangle(verts[i + 1], verts[i + 2 - n], verts[i + 2]) for i in range(2 * n, 3 * n - 1)] + \
                   [Triangle(verts[3 * n], verts[n + 1], verts[2 * n + 1])]
        self.tris = bot_tri + top_tri + side_tri

    def get_center_y(self):
        return self.h / 2


# ---------------------------------------------------------------------------------------
# TESTING:
t = Cylinder()
