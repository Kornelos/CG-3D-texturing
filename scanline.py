from pygame import Color


class Point:
    def __init__(self, p, t):
        self.x = p[0]
        self.y = p[1]
        self.u = t[0]
        self.v = t[1]

    def copy(self):
        return Point((self.x, self.y), (self.u, self.v))


class TextureFiller:

    def __init__(self, image, screen):
        self.screen = screen
        self.rgb_im = image.convert('RGB')
        self.texture_h = self.rgb_im.height
        self.texture_w = self.rgb_im.width

    def set_pixel(self, x, y, u, v):
        if u <= 0 or v <= 0:
            return
        if u < 1:
            u_img = int(u * self.texture_w)
        else:
            u_img = int(u * self.texture_w) % self.texture_w
        if v < 1:
            v_img = int(v * self.texture_h)
        else:
            v_img = int(v * self.texture_h) % self.texture_h

        r, g, b = self.rgb_im.getpixel((u_img, v_img))
        self.screen.set_at((x, y), Color(r, g, b))

    def scan_line(self, points, texture_points):
        # print(points)
        t_ps = [Point(points[i], texture_points[i]) for i in range(len(points))]
        t_ps.sort(key=lambda p: p.y)
        A = t_ps[0]
        B = t_ps[1]
        C = t_ps[2]

        dy1 = B.y - A.y
        dx1 = B.x - A.x
        dv1 = B.v - A.v
        du1 = B.u - A.u

        dy2 = C.y - A.y
        dx2 = C.x - A.x
        dv2 = C.v - A.v
        du2 = C.u - A.u

        dax_step = dbx_step = du1_step = dv1_step = du2_step = dv2_step = 0
        if dy1:
            dax_step = dx1 / abs(dy1)
            du1_step = du1 / abs(dy1)
            dv1_step = dv1 / abs(dy1)

        if dy2:
            dbx_step = dx2 / abs(dy2)
            du2_step = du2 / abs(dy2)
            dv2_step = dv2 / abs(dy2)

        if dy1:
            i = A.y
            while i <= B.y:
                ax = A.x + (i - A.y) * dax_step
                bx = A.x + (i - A.y) * dbx_step
                # start
                tex_su = A.u + (i - A.y) * du1_step
                tex_sv = A.v + (i - A.y) * dv1_step
                # end
                tex_eu = A.u + (i - A.y) * du2_step
                tex_ev = A.v + (i - A.y) * dv2_step

                if ax > bx:
                    # swap values to ensure going from smaller to larger
                    ax, bx = bx, ax
                    tex_su, tex_eu = tex_eu, tex_su
                    tex_sv, tex_ev = tex_ev, tex_sv

                tex_u = tex_su
                tex_v = tex_sv

                # step in the texture
                t_step = 0
                if ax != bx:
                    t_step = 1 / (bx - ax)
                t = 0

                j = int(ax)
                while j < bx:
                    tex_u = (1 - t) * tex_su + t * tex_eu
                    tex_v = (1 - t) * tex_sv + t * tex_ev
                    self.set_pixel(j, i, tex_u, tex_v)
                    t += t_step
                    j += 1

                # iterate loop
                i += 1

        dy1 = C.y - B.y
        dx1 = C.x - B.x
        dv1 = C.v - B.v
        du1 = C.u - B.u

        if dy1:
            dax_step = dx1 / abs(dy1)
            du1_step = du1 / abs(dy1)
            dv1_step = dv1 / abs(dy1)

        if dy2:
            dbx_step = dx2 / abs(dy2)

        if dy1:
            i = B.y
            while i <= C.y:
                ax = B.x + (i - B.y) * dax_step
                bx = A.x + (i - A.y) * dbx_step
                # start
                tex_su = B.u + (i - B.y) * du1_step
                tex_sv = B.v + (i - B.y) * dv1_step
                # end
                tex_eu = A.u + (i - A.y) * du2_step
                tex_ev = A.v + (i - A.y) * dv2_step

                if ax > bx:
                    # swap values to ensure going from smaller to larger
                    ax, bx = bx, ax
                    tex_su, tex_eu = tex_eu, tex_su
                    tex_sv, tex_ev = tex_ev, tex_sv

                tex_u = tex_su
                tex_v = tex_sv

                # step in the texture
                t_step = 0
                if ax != bx:
                    t_step = 1 / (bx - ax)
                t = 0

                j = int(ax)
                while j < bx:
                    tex_u = (1 - t) * tex_su + t * tex_eu
                    tex_v = (1 - t) * tex_sv + t * tex_ev
                    self.set_pixel(j, i, tex_u, tex_v)
                    t += t_step
                    j += 1

                # iterate loop
                i += 1

# Old scanline implementation
# def scan_line(points, texture_points):
#     # source : http://www-users.mat.uni.torun.pl/~wrona/3d_tutor/tri_fillers.html
#     t_ps = [Point(points[i], texture_points[i]) for i in range(len(points))]
#     t_ps.sort(key=lambda p: p.y)
#     A = t_ps[0]
#     B = t_ps[1]
#     C = t_ps[2]
#
#     if B.y - A.y > 0:
#         dx1 = (B.x - A.x) / (B.y - A.y)
#         du1 = (B.u - A.u) / (B.y - A.y)
#         dv1 = (B.v - A.v) / (B.y - A.y)
#     else:
#         dx1 = du1 = dv1 = 0
#     if C.y - A.y > 0:
#         dx2 = (C.x - A.x) / (C.y - A.y)
#         du2 = (C.u - A.u) / (C.y - A.y)
#         dv2 = (C.v - A.v) / (C.y - A.y)
#     else:
#         dx2 = du2 = dv2 = 0
#     if C.y - B.y > 0:
#         dx3 = (C.x - B.x) / (C.y - B.y)
#         du3 = (C.u - B.u) / (C.y - B.y)
#         dv3 = (C.v - B.v) / (C.y - B.y)
#     else:
#         dx3 = du3 = dv3 = 0
#
#     S = A.copy()
#     E = A.copy()
#     # calculate inner deltas
#     if dx2 != dx1:
#         du = (du2 - du1) / (dx2 - dx1)
#         dv = (dv2 - dv1) / (dx2 - dx1)
#     else:
#         du = dv = 0
#     if dx1 > dx2:
#         while S.y <= B.y:
#             u = S.u
#             v = S.v
#             for x in range(int(S.x), int(E.x)):
#                 putpixel(x, int(S.y), u, v)
#                 u += du
#                 v += dv
#
#             S.u += du2
#             E.u += du1
#             S.v += dv2
#             E.v += dv1
#             S.y += 1
#             E.y += 1
#             S.x += dx2
#             E.x += dx1
#         E = B
#         while S.y <= C.y:
#             u = S.u
#             v = S.v
#             for x in range(int(S.x), int(E.x)):
#                 putpixel(x, int(S.y), u, v)
#                 u += du
#                 v += dv
#
#             S.u += du2
#             E.u += du3
#             S.v += dv2
#             E.v += dv3
#             S.x += dx2
#             E.x += dx3
#             S.y += 1
#             E.y += 1
#
#     else:
#         while S.y <= B.y:
#             u = S.u
#             v = S.v
#             for x in range(int(S.x), int(E.x)):
#                 putpixel(x, int(S.y), u, v)
#                 u += du
#                 v += dv
#
#             S.u += du1
#             E.u += du2
#             S.v += dv1
#             E.v += dv2
#             S.x += dx1
#             E.x += dx2
#             S.y += 1
#             E.y += 1
#         S = B
#         while S.y <= C.y:
#             u = S.u
#             v = S.v
#             for x in range(int(S.x), int(E.x)):
#                 putpixel(x, int(S.y), u, v)
#                 u += du
#                 v += dv
#
#             S.u += du3
#             E.u += du2
#             S.v += dv3
#             E.v += dv2
#             S.x += dx3
#             E.x += dx2
#             S.y += 1
#             E.y += 1
