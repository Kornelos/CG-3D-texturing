import pygame
import numpy as np
from math import cos, sin, tan, pi
from cylinder import Triangle, Cylinder
from pygame.locals import *
from PIL import Image

width = 1024
height = 1024
pygame.init()
screen = pygame.display.set_mode((width,height))
CLOCK = pygame.time.Clock()


a = width/height # aspect ratio

theta = pi / 2
fov = 1 / tan(theta/2) # field of view 
# viewing distance
fNear = 0.1
fFar = 1000.0

# projection matrix
M = np.array([[a*fov,0,0,0],[0,fov,0,0],[0,0,fFar/(fFar-fNear),1],[0,0,(-fFar*fNear)/(fFar-fNear),0]])
# print(M)
# scaling matrix
factor = 400
S = np.eye(4)
S[0,0] *= factor
S[1,1] *= factor


# draw line

def draw_triangle(x1,y1,x2,y2,x3,y3):
    pygame.draw.line(screen, pygame.color.THECOLORS['white'], (x1, y1), (x2, y2), 1)
    pygame.draw.line(screen, pygame.color.THECOLORS['white'], (x2, y2), (x3, y3), 1)
    pygame.draw.line(screen, pygame.color.THECOLORS['white'], (x3, y3), (x1, y1), 1)

cyl = Cylinder()


vCamera = np.zeros(4)
def rotate(d_x,d_y):
    R_xn = np.array([
        [1,0,0,0],
        [0,cos(d_x),sin(d_x),0],
        [0,-sin(d_x),cos(d_x),0],
        [0,0,0,1]
        ])
    R_yn = np.array([
        [cos(d_y),0,-sin(d_y),0],
        [0,1,0,0],
        [sin(d_y),0,cos(d_y),0],
        [0,0,0,1]
    ])
    R_zn = np.array([
        [cos(d_y),-sin(d_y),0,0],
        [sin(d_y),cos(d_y),0,0],
        [0,0,1,0],
        [0,0,0,1]
    ])
    
    for tri in cyl.tris:

        points = tri.get_points()
        tex_points = tri.get_texture()
      
        rotated1 = points[0].dot(R_yn).dot(R_xn)
        rotated2 = points[1].dot(R_yn).dot(R_xn)
        rotated3 = points[2].dot(R_yn).dot(R_xn)

        # offset
        rotated1[2] += 8
        rotated2[2] += 8
        rotated3[2] += 8
        ## hiding triangles that cannot be seen
        ## Use Cross-Product to get surface normal
        line1 = rotated2 - rotated1
        line2 = rotated3 - rotated1
        normal = np.zeros(4)
        normal[0] = line1[1] * line2[2] - line1[2] * line2[1]
        normal[1] = line1[2] * line2[0] - line1[0] * line2[2]
        normal[2] = line1[0] * line2[1] - line1[1] * line2[0]
        # normalise normal
        normal = normal / np.sqrt(np.sum(normal**2))
        if normal[0] * (rotated1[0] - vCamera[0]) + normal[1] * (rotated1[1] - vCamera[1]) + normal[2] * (rotated1[2] - vCamera[2]) < 0:
            # 3d -> 2d
            # for each point multiply times projection mateix and scale by division by z then normalise by adding one and dividing by 2

            ctr = np.array([2.5,1.5,0,0])
            proj1 = (rotated1.dot(M)/rotated1[2] + ctr)/2
            proj2 = (rotated2.dot(M)/rotated2[2] + ctr)/2
            proj3 = (rotated3.dot(M)/rotated3[2] +ctr)/2
        
            proj1 = proj1.dot(S)
            proj2 = proj2.dot(S)
            proj3 = proj3.dot(S)
            
            draw_triangle(proj1[0],proj1[1],proj2[0],proj2[1],proj3[0],proj3[1])
            scanline([[proj1[0],proj1[1]],[proj2[0],proj2[1]],[proj3[0],proj3[1]]],tex_points)
            # todo: fill
            # scanline()


# scanline ========================================
class Point:
    def __init__(self,p,t):
        self.x = p[0]
        self.y = p[1]
        self.u = t[0]
        self.v = t[1]

    def copy(self):
        return Point((self.x,self.y),(self.u,self.v))



# load texture image 
im = Image.open('texture.jpg')
im = Image.open('tex.gif')
rgb_im = im.convert('RGB')
texture_h = rgb_im.height
texture_w = rgb_im.width


# def horizline(start,end):
#     r,g,b =rgb_im.getpixel((100,100))
#     y = int(start.y)
#     v_rel = int(start.v * texture_h)%texture_h
#     u_start = int(start.u * texture_w)
#     for x in range(int(start.x), int(end.x)):
        
#         r,g,b = rgb_im.getpixel((u_start%texture_w,v_rel))
#         screen.set_at((x, y), pygame.Color(r,g,b))
#         u_start +=1

def putpixel(x,y,u,v):
        if(u <= 0 or v <= 0):
            return
        if u < 1:
            u_img = int(u * texture_w)
        else:
            u_img = int(u * texture_w)%texture_w
        if v < 1:
            v_img = int(v * texture_h)
        else:
            v_img = int(v * texture_h)%texture_h
        
        r,g,b = rgb_im.getpixel((u_img,v_img))
        screen.set_at((x, y), pygame.Color(r,g,b))

def scanline(points,texture_points):
    # source : http://www-users.mat.uni.torun.pl/~wrona/3d_tutor/tri_fillers.html
    t_ps = [Point(points[i],texture_points[i]) for i in range(len(points))]
    t_ps.sort(key = lambda p: p.y)
    A = t_ps[0]
    B = t_ps[1]
    C = t_ps[2]

    if (B.y-A.y > 0):
         dx1 = (B.x-A.x)/(B.y-A.y)
         du1 = (B.u-A.u)/(B.y-A.y)
         dv1 = (B.v-A.v)/(B.y-A.y)
    else: 
        dx1=du1=dv1=0
    if (C.y-A.y > 0):
         dx2 = (C.x-A.x)/(C.y-A.y)
         du2 = (C.u-A.u)/(C.y-A.y)
         dv2 = (C.v-A.v)/(C.y-A.y)
    else: 
        dx2=du2=dv2=0
    if (C.y-B.y > 0): 
        dx3 = (C.x-B.x)/(C.y-B.y)
        du3 = (C.u-B.u)/(C.y-B.y)
        dv3 = (C.v-B.v)/(C.y-B.y)
    else: 
        dx3=du3=dv3=0

    S=A.copy()
    E=A.copy()
    # calulate inner deltas
    if(dx2 != dx1):
        du = (du2 - du1)/(dx2-dx1)
        dv = (dv2 - dv1)/(dx2-dx1)
    else:
        du=dv=0
    if(dx1 > dx2):
        while(S.y<=B.y):
            u = S.u
            v = S.v
            for x in range(int(S.x),int(E.x)):
                putpixel(x,int(S.y),u,v)
                u += du
                v += dv
            
            S.u += du2
            E.u += du1
            S.v += dv2
            E.v += dv1
            S.y+=1
            E.y+=1
            S.x+=dx2
            E.x+=dx1
        E=B
        while(S.y<=C.y):
            u = S.u
            v = S.v
            for x in range(int(S.x),int(E.x)):
                putpixel(x,int(S.y),u,v)
                u += du
                v += dv
            
            S.u += du2
            E.u += du3
            S.v += dv2
            E.v += dv3
            S.x += dx2
            E.x += dx3
            S.y+=1
            E.y+=1
            
    else:
        while(S.y<=B.y):
            u = S.u
            v = S.v
            for x in range(int(S.x),int(E.x)):
                putpixel(x,int(S.y),u,v)
                u += du
                v += dv
            
            S.u += du1
            E.u += du2
            S.v += dv1
            E.v += dv2
            S.x += dx1
            E.x += dx2
            S.y+=1
            E.y+=1
        S=B
        while(S.y<=C.y):
            u = S.u
            v = S.v
            for x in range(int(S.x),int(E.x)):
                putpixel(x,int(S.y),u,v)
                u += du
                v += dv
            
            S.u += du3
            E.u += du2
            S.v += dv3
            E.v += dv2
            S.x += dx3
            E.x += dx2
            S.y+=1
            E.y+=1
        
# update screen
# Test of scanline alg
tri = [Point([100,150],[0,0]),Point([500,400],[0.5,0.5]),Point([600,200],[0.75,0.25])]

scanline([[100,150],[500,400],[600,200]],[[0,0],[0.5,1],[0.75,0.25]])
#rotate(0,0)
pygame.display.flip()
angle = 0
angle_x = 0
angle_y = 0
delta_ang = pi/60 # rate of rotation
left=right=up=down=False
# Main loop ------------------------------------------------------------
while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    up=True
                if event.key == K_DOWN:
                    down=True
                if event.key == K_LEFT:
                    left=True
                if event.key == K_RIGHT:
                    right=True
            if event.type == KEYUP:
                if event.key == K_UP:
                    up=False
                if event.key == K_DOWN:
                    down=False
                if event.key == K_LEFT:
                    left=False
                if event.key == K_RIGHT:
                    right=False
        
        # angle += pi/180
        if up:
            angle_x += delta_ang
        elif down:
            angle_x -= delta_ang
        if left:
            angle_y += delta_ang
        elif right:
            angle_y -= delta_ang

        if left or right or up or down:
            screen.fill((0,0,0))
            rotate(angle_x, angle_y)
            pygame.display.flip()
        CLOCK.tick(60)