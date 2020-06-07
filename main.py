from math import cos, sin, tan, pi
import numpy as np
import pygame
from PIL import Image
from pygame.locals import *
from scanline import *
from cylinder import Cylinder
from sys import exit

# UI creation only set pixel and draw line is used from the framework
width = 1024
height = 1024
pygame.init()
pygame.display.set_caption('CG 3D textured cylinder -- Use arrows to rotate in X Y plane and {A Z} keys to rotate in Z plane')
screen = pygame.display.set_mode((width, height))
CLOCK = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 36)


# scene setup
a = width / height  # aspect ratio
theta = pi / 2
fov = 1 / tan(theta / 2)  # field of view

# viewing distance
fNear = 0.1
fFar = 1000.0

# projection matrix
M = np.array([
    [a * fov, 0, 0, 0],
    [0, fov, 0, 0],
    [0, 0, fFar / (fFar - fNear), 1],
    [0, 0, (-fFar * fNear) / (fFar - fNear), 0]
])

# scaling matrix
factor = 400
S = np.eye(4)
S[0, 0] *= factor
S[1, 1] *= factor


# draw line

def draw_triangle(x1, y1, x2, y2, x3, y3):
    pygame.draw.line(screen, pygame.color.THECOLORS['white'], (x1, y1), (x2, y2), 1)
    pygame.draw.line(screen, pygame.color.THECOLORS['white'], (x2, y2), (x3, y3), 1)
    pygame.draw.line(screen, pygame.color.THECOLORS['white'], (x3, y3), (x1, y1), 1)


cyl = Cylinder()

# translation matrix
T = np.eye(4)
T[3, 1] = -cyl.get_center_y()

T2 = np.eye(4)
T2[3, 1] = cyl.get_center_y()
T2[3, 2] = 5  # offset on Z axis (from screen)

# CAMERA
vCamera = np.zeros(3)

# load texture image
im = Image.open('tex.png')
im = im.rotate(180)
tex_filler = TextureFiller(im, screen)


# function which draws 3D triangles on screen and applies rotation and texturing
def rotate(d_x, d_y, d_z, texture_filler):
    R_xn = np.array([
        [1, 0, 0, 0],
        [0, cos(d_x), sin(d_x), 0],
        [0, -sin(d_x), cos(d_x), 0],
        [0, 0, 0, 1]
    ])
    R_yn = np.array([
        [cos(d_y), 0, -sin(d_y), 0],
        [0, 1, 0, 0],
        [sin(d_y), 0, cos(d_y), 0],
        [0, 0, 0, 1]
    ])
    R_zn = np.array([
        [cos(d_z), -sin(d_z), 0, 0],
        [sin(d_z), cos(d_z), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    # set rotation and translation matrix

    mat_world = np.eye(4).dot(T).dot(R_yn).dot(R_xn).dot(R_zn).dot(T2)

    for trg in cyl.tris:

        points = trg.get_points()
        tex_points = trg.get_texture()
        #print(tex_points)
        #

        for i in range(3):
            points[i] = points[i].dot(mat_world)

        line1 = points[1] - points[0]
        line2 = points[2] - points[0]

        normal = np.zeros(4)
        normal[0] = line1[1] * line2[2] - line1[2] * line2[1]
        normal[1] = line1[2] * line2[0] - line1[0] * line2[2]
        normal[2] = line1[0] * line2[1] - line1[1] * line2[0]
        # normalise
        normal = normal / np.sqrt(np.sum(normal ** 2))
        if normal[0] * (points[0][0] - vCamera[0]) + normal[1] * (points[0][1] - vCamera[1]) + normal[2] * (
                points[0][2] - vCamera[2]) < 0:
            # Convert World Space --> View Space for i in range(3): points[i] = points[i].dot(matView) 3d -> 2d for
            # each point multiply times projection matrix and scale by division by z then normalise by adding one and
            # dividing by 2

            ctr = np.array([2.5, 1.5, 0, 0])
            for i in range(3):
                points[i] = (points[i].dot(M) / points[i][2] + ctr) / 2
                points[i] = points[i].dot(S)

            # draw_triangle(points[0][0], points[0][1], points[1][0], points[1][1], points[2][0], points[2][1])
            texture_filler.scan_line([[int(points[0][0]), int(points[0][1])], [int(points[1][0]), int(points[1][1])],
                                      [int(points[2][0]), int(points[2][1])]],
                                     tex_points)



rotate(0, 0, pi, tex_filler)


pygame.display.flip()

angle_x = angle_y = 0
angle_z = pi
delta_ang = pi / 60  # rate of rotation
left = right = up = down = z_key = a_key = False
redraw = False
# Main loop ------------------------------------------------------------
on = True
while on:
    for event in pygame.event.get():
        if event.type == QUIT:
            on = False
            pygame.display.quit()
            pygame.quit()
            break

        if event.type == KEYDOWN:
            if event.key == K_UP:
                up = True
            if event.key == K_DOWN:
                down = True
            if event.key == K_LEFT:
                left = True
            if event.key == K_RIGHT:
                right = True
            if event.key == K_a:
                a_key = True
            if event.key == K_z:
                z_key = True
            # zoom in/out
            if event.key == K_s:
                if T2[3, 2] > cyl.h + 2:
                    T2[3, 2] -= 1
                    redraw = True
            if event.key == K_x:
                T2[3, 2] += 1
                redraw = True

        if event.type == KEYUP:
            if event.key == K_UP:
                up = False
            if event.key == K_DOWN:
                down = False
            if event.key == K_LEFT:
                left = False
            if event.key == K_RIGHT:
                right = False
            if event.key == K_a:
                a_key = False
            if event.key == K_z:
                z_key = False

    # X,Y,Z rotation
    if up:
        angle_x += delta_ang
    elif down:
        angle_x -= delta_ang
    if left:
        angle_y -= delta_ang
    elif right:
        angle_y += delta_ang
    if a_key:
        angle_z += delta_ang
    elif z_key:
        angle_z -= delta_ang

    if left or right or up or down or a_key or z_key or redraw:
        screen.fill((0, 0, 0))
        rotate(angle_x, angle_y, angle_z, tex_filler)
        pygame.display.flip()
        redraw = False
    CLOCK.tick(60)

exit(0)
