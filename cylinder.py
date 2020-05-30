import tkinter
import numpy as np
from math import cos, sin, tan, pi

class Triangle:
    def __init__(self,p1,p2,p3):
        self.p = [p1,p2,p3]
    def draw(self):
        # to do
        pass
    def __repr__(self):
        return str(self.p)

class Cylinder:
    # h = 1
    # r = 1
    # n = 10 # number of the sides of the prism used to draw circle
    def __init__(self):
        h = 5
        r = 1
        n = 25 # number of the sides of the prism used to draw circle
        # points on the bottom and the top of the cylinder
        # n = 0..n
        p = [None] * (4*n+2)
        print(len(p))
        p_top = [np.array([0,h,0,1])] + [np.array([r*cos(2*pi*i/n),h,r*sin(2*pi*i/n),1]) for i in range(n)]
        
        print(len(range(0,n+1)),len(p_top))
        p[0:n+1] = p_top
        # n = 3n+1 ..4n+1
        p_bot =  [np.array([r*cos(2*pi*i/n),0,r*sin(2*pi*i/n),1]) for i in range(n)] + [np.array([0,0,0,1])]
        print(len(range(3*n+1,4*n+2)),len(p_bot))
        p[(3*n+1):(4*n+2)] = p_bot
        # construct triangles
        #print(len(p))
        # TODO: p insted of p_top etc
        top_tri = [Triangle(p_top[0],p_top[i+2],p_top[i+1]) for i in range(n-1)] + [Triangle(p_top[0],p_top[1],p_top[n])]
        bot_tri = [Triangle(p[4*n+1],p[i+1],p[i+2]) for i in range(3*n,4*n-1)] + [Triangle(p[4*n+1],p[4*n],p[3*n+1])]
        
        
        # sides
        # n = n+1 .. 2n and 2n+1 .. 3n
        p_sides = [np.array(p[i-n]) for i in range(n+1,2*n+1)] + [np.array(p[i+n]) for i in range(2*n+1,3*n+1)]
        print(len(range(n+1,3*n+1)),len(p_sides))
        p[(n+1):3*n+1] = p_sides
        # print(p)
        
        # side triangles n, ... 3n-1
        side_tri = [Triangle(p[i+1],p[i+2],p[i+1+n]) for i in range(n,2*n-1)] + \
                   [Triangle(p[2*n],p[n+1],p[3*n])] + \
                   [Triangle(p[i+1],p[i+2-n],p[i+2]) for i in range(2*n,3*n-1)] + \
                   [Triangle(p[3*n],p[n+1],p[2*n+1])]
        self.tris =  bot_tri + top_tri + side_tri




###---------------------------------------------------------------------------------------
# TESTING:
test = Cylinder()
window = tkinter.Tk()
width = 800
height = 800
window.geometry("800x800")
window.resizable(0, 0)

canva = tkinter.Canvas(window, width=width,height=height)
canva.pack()

a = width/height # aspect ratio
theta = pi / 3
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

# rotation matrix
delta = 1 # changes in time
R_x = np.array([
    [1,0,0,0],
    [0,cos(delta),sin(delta),0],
    [0,-sin(delta),cos(delta),0],
    [0,0,0,1]
    ])
R_y = np.array([
    [cos(delta),0,-sin(delta),0],
    [0,1,0,0],
    [sin(delta),0,cos(delta),0],
    [0,0,0,1]
])
R_z = np.array([
    [cos(delta),-sin(delta),0,0],
    [sin(delta),cos(delta),0,0],
    [0,0,1,0],
    [0,0,0,1]
])

def draw_triangle(x1,y1,x2,y2,x3,y3,canvas):
    canvas.create_line(x1, y1, x2, y2)
    canvas.create_line(x2, y2, x3, y3)
    canvas.create_line(x3, y3, x1, y1)
    #canvas.create_polygon([x1,y1,x2,y2,x3,y3], outline='#f11',fill='#1f1', width=2)
    #return canvas

cyl = Cylinder()
# first rotation
for tri in cyl.tris:
    # offset into the screen

    rotated1 = tri.p[0].dot(R_x).dot(R_x).dot(R_y)
    rotated2 = tri.p[1].dot(R_x).dot(R_x).dot(R_y)
    rotated3 = tri.p[2].dot(R_x).dot(R_x).dot(R_y)

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
    # temporary
    
    draw_triangle(proj1[0],proj1[1],proj2[0],proj2[1],proj3[0],proj3[1],canva)

vCamera = np.zeros(3)

def add_a(d):
    R_xn = np.array([
        [1,0,0,0],
        [0,cos(d),sin(d),0],
        [0,-sin(d),cos(d),0],
        [0,0,0,1]
        ])
    R_yn = np.array([
        [cos(d),0,-sin(d),0],
        [0,1,0,0],
        [sin(d),0,cos(d),0],
        [0,0,0,1]
    ])
    R_zn = np.array([
        [cos(d),-sin(d),0,0],
        [sin(d),cos(d),0,0],
        [0,0,1,0],
        [0,0,0,1]
    ])
    canva.delete("all")
    for tri in cyl.tris:
        rotated1 = tri.p[0].dot(R_zn).dot(R_xn).dot(R_yn)
        rotated2 = tri.p[1].dot(R_zn).dot(R_xn).dot(R_yn)
        rotated3 = tri.p[2].dot(R_zn).dot(R_xn).dot(R_yn)
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


            proj1 = (rotated1.dot(M)/rotated1[2] + np.array([1,1,0,0]))/2
            proj2 = (rotated2.dot(M)/rotated2[2] + np.array([1,1,0,0]))/2
            proj3 = (rotated3.dot(M)/rotated3[2] + np.array([1,1,0,0]))/2
        
            proj1 = proj1.dot(S)
            proj2 = proj2.dot(S)
            proj3 = proj3.dot(S)
            #print(proj1[0],proj1[1],proj2[0],proj2[1],proj3[0],proj3[1])
            draw_triangle(proj1[0],proj1[1],proj2[0],proj2[1],proj3[0],proj3[1],canva)
    d += pi/60
    window.after(100,add_a,d)

window.after(500,add_a,delta)
window.mainloop()
