import tkinter
import numpy as np
from math import cos, sin, tan, pi

class Triangle:
    def __init__(self,p1,p2,p3):
        self.verts = [p1,p2,p3]
    def draw(self):
        # to do
        pass
    def get_points(self):
        return [self.verts[0][0],self.verts[1][0],self.verts[2][0]]
    def get_texture(self):
        return [self.verts[0][2],self.verts[1][2],self.verts[2][2]]

    def __repr__(self):
        return str(self.verts)

class Cylinder:
    def __init__(self):
        h = 5 # height
        r = 3 # radius
        n = 10 # number of the sides of the prism used to draw circle

        # points on the bottom and the top of the cylinder
        # n = 0..n
        p = [None] * (4*n+2)

        # points on top
        p_top = [np.array([0,h,0,1])] + [np.array([r*cos(2*pi*i/n),h,r*sin(2*pi*i/n),1]) for i in range(n)]
        p[0:n+1] = p_top
        # normal vector top
        n_top = [np.array([0,1,0,0]) for _ in range(n+1)]
        # points on bottom
        p_bot =  [np.array([r*cos(2*pi*i/n),0,r*sin(2*pi*i/n),1]) for i in range(n)] + [np.array([0,0,0,1])]
        p[(3*n+1):(4*n+2)] = p_bot
        # normal vector bottom
        n_bot = [np.array([0,-1,0,0]) for _ in range(n+1)]

        
        
        # sides
        # n = n+1 .. 2n and 2n+1 .. 3n
        p_sides = [np.array(p[i-n]) for i in range(n+1,2*n+1)] + [np.array(p[i+n]) for i in range(2*n+1,3*n+1)]
        p[(n+1):3*n+1] = p_sides
        # sides norm
        n_sides = [np.array([p[i][0]/r,0,p[i][2]/r,0]) for i in range(n+1,3*n+1)]
        norms = n_top + n_sides + n_bot

        # texture coordinates:
        t = [np.array([0.25,0.25])] + \
            [np.array([0.25*(1+cos(2*pi*(i-1)/n)),0.25*(1+sin(2*pi*(i-1)/n))]) for i in range(1,n+1) ] + \
            [np.array([(i-1)/(n-1),1]) for i in range(1,n+1)] + \
            [np.array([(i-1)/(n-1),0.5]) for i in range(1,n+1)] + \
            [np.array([0.25*(3+cos(2*pi*(i-1)/n)),0.25*(1+sin(2*pi*(i-1)/n))]) for i in range(1,n+1) ] + \
            [np.array([0.75,0.25])]


        # create vertexes (Vi)
        verts = []
        for i in range(4*n+2):
            verts += [(p[i],norms[i],t[i])]
        

        top_tri = [Triangle(verts[0],verts[i+2],verts[i+1]) for i in range(n-1)] + [Triangle(verts[0],verts[1],verts[n])]
        bot_tri = [Triangle(verts[4*n+1],verts[i+1],verts[i+2]) for i in range(3*n,4*n-1)] + [Triangle(verts[4*n+1],verts[4*n],verts[3*n+1])]

        # side triangles n, ... 3n-1
        side_tri = [Triangle(verts[i+1],verts[i+2],verts[i+1+n]) for i in range(n,2*n-1)] + \
                   [Triangle(verts[2*n],verts[n+1],verts[3*n])] + \
                   [Triangle(verts[i+1],verts[i+2-n],verts[i+2]) for i in range(2*n,3*n-1)] + \
                   [Triangle(verts[3*n],verts[n+1],verts[2*n+1])]
        self.tris =  bot_tri + top_tri + side_tri
        



###---------------------------------------------------------------------------------------
# TESTING:
# window = tkinter.Tk()
# width = 800
# height = 800
# window.geometry("800x800")
# window.resizable(0, 0)

# canva = tkinter.Canvas(window, width=width,height=height)
# canva.pack()

# a = width/height # aspect ratio
# theta = pi / 3
# fov = 1 / tan(theta/2) # field of view 
# # viewing distance
# fNear = 0.1
# fFar = 1000.0

# # projection matrix
# M = np.array([[a*fov,0,0,0],[0,fov,0,0],[0,0,fFar/(fFar-fNear),1],[0,0,(-fFar*fNear)/(fFar-fNear),0]])
# # print(M)
# # scaling matrix
# factor = 400
# S = np.eye(4)
# S[0,0] *= factor
# S[1,1] *= factor

# # rotation matrix
# delta = 1 # changes in time
# R_x = np.array([
#     [1,0,0,0],
#     [0,cos(delta),sin(delta),0],
#     [0,-sin(delta),cos(delta),0],
#     [0,0,0,1]
#     ])
# R_y = np.array([
#     [cos(delta),0,-sin(delta),0],
#     [0,1,0,0],
#     [sin(delta),0,cos(delta),0],
#     [0,0,0,1]
# ])
# R_z = np.array([
#     [cos(delta),-sin(delta),0,0],
#     [sin(delta),cos(delta),0,0],
#     [0,0,1,0],
#     [0,0,0,1]
# ])

# def draw_triangle(x1,y1,x2,y2,x3,y3,canvas):
#     canvas.create_line(x1, y1, x2, y2)
#     canvas.create_line(x2, y2, x3, y3)
#     canvas.create_line(x3, y3, x1, y1)
#     #canvas.create_polygon([x1,y1,x2,y2,x3,y3], outline='#f11',fill='#1f1', width=2)
#     #return canvas

# cyl = Cylinder()
# # first rotation
# for tri in cyl.tris:
#     # offset into the screen

#     rotated1 = tri.p[0].dot(R_x).dot(R_x).dot(R_y)
#     rotated2 = tri.p[1].dot(R_x).dot(R_x).dot(R_y)
#     rotated3 = tri.p[2].dot(R_x).dot(R_x).dot(R_y)

#     #Projection 3D -> 2D
#     # for each point multiply times projection mateix and scale by division by z then normalise by adding one and dividing by 2
#     rotated1[2] += 3
#     rotated2[2] += 3
#     rotated3[2] += 3
#     proj1 = (rotated1.dot(M)/rotated1[2] + np.array([1,1,0,0]))/2
#     proj2 = (rotated2.dot(M)/rotated2[2] + np.array([1,1,0,0]))/2
#     proj3 = (rotated3.dot(M)/rotated3[2] + np.array([1,1,0,0]))/2
   
#     proj1 = proj1.dot(S)
#     proj2 = proj2.dot(S)
#     proj3 = proj3.dot(S)
#     # temporary
    
#     draw_triangle(proj1[0],proj1[1],proj2[0],proj2[1],proj3[0],proj3[1],canva)

# vCamera = np.zeros(3)

# def add_a(d):
#     R_xn = np.array([
#         [1,0,0,0],
#         [0,cos(d),sin(d),0],
#         [0,-sin(d),cos(d),0],
#         [0,0,0,1]
#         ])
#     R_yn = np.array([
#         [cos(d),0,-sin(d),0],
#         [0,1,0,0],
#         [sin(d),0,cos(d),0],
#         [0,0,0,1]
#     ])
#     R_zn = np.array([
#         [cos(d),-sin(d),0,0],
#         [sin(d),cos(d),0,0],
#         [0,0,1,0],
#         [0,0,0,1]
#     ])
#     canva.delete("all")
#     for tri in cyl.tris:
#         rotated1 = tri.p[0].dot(R_zn).dot(R_xn).dot(R_yn)
#         rotated2 = tri.p[1].dot(R_zn).dot(R_xn).dot(R_yn)
#         rotated3 = tri.p[2].dot(R_zn).dot(R_xn).dot(R_yn)
#         # offset
#         rotated1[2] += 8
#         rotated2[2] += 8
#         rotated3[2] += 8
#         ## hiding triangles that cannot be seen
#         ## Use Cross-Product to get surface normal
#         line1 = rotated2 - rotated1
#         line2 = rotated3 - rotated1
#         normal = np.zeros(4)
#         normal[0] = line1[1] * line2[2] - line1[2] * line2[1]
#         normal[1] = line1[2] * line2[0] - line1[0] * line2[2]
#         normal[2] = line1[0] * line2[1] - line1[1] * line2[0]
#         # normalise normal
#         normal = normal / np.sqrt(np.sum(normal**2))
#         if normal[0] * (rotated1[0] - vCamera[0]) + normal[1] * (rotated1[1] - vCamera[1]) + normal[2] * (rotated1[2] - vCamera[2]) < 0:
#             # 3d -> 2d
#             # for each point multiply times projection mateix and scale by division by z then normalise by adding one and dividing by 2


#             proj1 = (rotated1.dot(M)/rotated1[2] + np.array([1,1,0,0]))/2
#             proj2 = (rotated2.dot(M)/rotated2[2] + np.array([1,1,0,0]))/2
#             proj3 = (rotated3.dot(M)/rotated3[2] + np.array([1,1,0,0]))/2
        
#             proj1 = proj1.dot(S)
#             proj2 = proj2.dot(S)
#             proj3 = proj3.dot(S)
#             #print(proj1[0],proj1[1],proj2[0],proj2[1],proj3[0],proj3[1])
#             draw_triangle(proj1[0],proj1[1],proj2[0],proj2[1],proj3[0],proj3[1],canva)
#     d += pi/60
#     window.after(16,add_a,d)

# window.after(500,add_a,delta)
# window.mainloop()
