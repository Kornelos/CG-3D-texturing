import tkinter # ui lib
import numpy as np
import math
import threading
from time import sleep

def draw_triangle(x1,y1,x2,y2,x3,y3,canvas):
    # canvas.create_line(x1, y1, x2, y2)
    # canvas.create_line(x2, y2, x3, y3)
    # canvas.create_line(x3, y3, x1, y1)
    canvas.create_polygon([x1,y1,x2,y2,x3,y3], outline='#f11',fill='#1f1', width=2)
    return canvas

window = tkinter.Tk()
width = 800
height = 800
window.geometry("800x800")
window.resizable(0, 0)

canva = tkinter.Canvas(window, width=width,height=height)
canva.pack()

# recangle
cube = [
    # SOUTH
    [np.array([0,0,0,1]),np.array([0,1,0,1]),np.array([1,1,0,1])],
    [np.array([0,0,0,1]),np.array([1,1,0,1]),np.array([1,0,0,1])],
    # EAST
    [np.array([1,0,0,1]),np.array([1,1,0,1]),np.array([1,1,1,1])],
    [np.array([1,0,0,1]),np.array([1,1,1,1]),np.array([1,0,1,1])],
    # NORTH
    [np.array([1,0,1,1]),np.array([1,1,1,1]),np.array([0,1,1,1])],
    [np.array([1,0,1,1]),np.array([0,1,1,1]),np.array([0,0,1,1])],
    # WEST
    [np.array([0,0,1,1]),np.array([0,1,1,1]),np.array([0,1,0,1])],
    [np.array([0,0,1,1]),np.array([0,1,0,1]),np.array([0,0,0,1])],
    # TOP
    [np.array([0,1,0,1]),np.array([0,1,1,1]),np.array([1,1,1,1])],
    [np.array([0,1,0,1]),np.array([1,1,1,1]),np.array([1,1,0,1])],
    # BOTTOM
    [np.array([1,0,1,1]),np.array([0,0,1,1]),np.array([0,0,0,1])],
    [np.array([1,0,1,1]),np.array([0,0,0,1]),np.array([1,0,0,1])],
]

# kuc tutorial
# [x,y,z,1]
a = width/height # aspect ratio
theta = math.pi / 2
fov = 1 / math.tan(theta/2) # field of view 
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

# rotation matrix
delta = 1 # changes in time
R_x = np.array([
    [1,0,0,0],
    [0,math.cos(delta),math.sin(delta),0],
    [0,-math.sin(delta),math.cos(delta),0],
    [0,0,0,1]
    ])
R_y = np.array([
    [math.cos(delta),0,-math.sin(delta),0],
    [0,1,0,0],
    [math.sin(delta),0,math.cos(delta),0],
    [0,0,0,1]
])
R_z = np.array([
    [math.cos(delta),-math.sin(delta),0,0],
    [math.sin(delta),math.cos(delta),0,0],
    [0,0,1,0],
    [0,0,0,1]
])

# first rotation
for tri in cube:
    # offset into the screen

    rotated1 = tri[0].dot(R_x).dot(R_x).dot(R_y)
    rotated2 = tri[1].dot(R_x).dot(R_x).dot(R_y)
    rotated3 = tri[2].dot(R_x).dot(R_x).dot(R_y)

    #Projection 3D -> 2D
    # for each point multiply times projection mateix and scale by division by z then normalise by adding one and dividing by 2
    rotated1[2] += 3
    rotated2[2] += 3
    rotated3[2] += 3
    proj1 = (rotated1.dot(M)/rotated1[2] + np.array([1,1,0,0]))/2
    proj2 = (rotated2.dot(M)/rotated2[2] + np.array([1,1,0,0]))/2
    proj3 = (rotated3.dot(M)/rotated3[2] + np.array([1,1,0,0]))/2
   
    proj1 = proj1.dot(S)
    proj2 = proj2.dot(S)
    proj3 = proj3.dot(S)
    
    draw_triangle(proj1[0],proj1[1],proj2[0],proj2[1],proj3[0],proj3[1],canva)
     
vCamera = np.zeros(3)
# redraw 
delta = 1 
def add_a(d):
    R_xn = np.array([
        [1,0,0,0],
        [0,math.cos(d),math.sin(d),0],
        [0,-math.sin(d),math.cos(d),0],
        [0,0,0,1]
        ])
    R_yn = np.array([
        [math.cos(d),0,-math.sin(d),0],
        [0,1,0,0],
        [math.sin(d),0,math.cos(d),0],
        [0,0,0,1]
    ])
    R_zn = np.array([
        [math.cos(d),-math.sin(d),0,0],
        [math.sin(d),math.cos(d),0,0],
        [0,0,1,0],
        [0,0,0,1]
    ])
    canva.delete("all")
    for tri in cube:
        rotated1 = tri[0].dot(R_zn).dot(R_xn).dot(R_yn)
        rotated2 = tri[1].dot(R_zn).dot(R_xn).dot(R_yn)
        rotated3 = tri[2].dot(R_zn).dot(R_xn).dot(R_yn)
        # offset
        rotated1[2] += 3
        rotated2[2] += 3
        rotated3[2] += 3
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


            proj1 = (rotated1.dot(M)/rotated1[2] + np.array([1,1,0,0]))/2
            proj2 = (rotated2.dot(M)/rotated2[2] + np.array([1,1,0,0]))/2
            proj3 = (rotated3.dot(M)/rotated3[2] + np.array([1,1,0,0]))/2
        
            proj1 = proj1.dot(S)
            proj2 = proj2.dot(S)
            proj3 = proj3.dot(S)
            #print(proj1[0],proj1[1],proj2[0],proj2[1],proj3[0],proj3[1])
            draw_triangle(proj1[0],proj1[1],proj2[0],proj2[1],proj3[0],proj3[1],canva)
    d += math.pi/60
    window.after(100,add_a,d)

window.after(500,add_a,delta)
window.mainloop()