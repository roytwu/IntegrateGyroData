import sys
import pygame
from operator import itemgetter
import Quaternions as qt

""" A class used for describing a point in 3D """
class Point3D:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = float(x), float(y), float(z)
        self.v = qt.Vector(self.x, self.y, self.z)

    """ Transforms this 3D point to 2D using a perspective projection """
    def project(self, win_width, win_height, fov, viewer_distance):
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, self.z)
    
    """ Apply rotation described by quaternion q to this 3D point """
    def rotateQ(self, q):
        v_rotated = qt.apply_rotation_on_vector(q, self.v)
        return Point3D(v_rotated.vx, v_rotated.vy, v_rotated.vz)


""" A class for rendering gyro integration as a 3D cube display. """
class RenderGyroIntegration:
    def __init__(self, GYR_Integration_Instance, win_width=640, win_height=480):
        self.GYR_Integration_Instance = GYR_Integration_Instance

        pygame.init()

        self.screen = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption("Rendering of 3D cube")

        self.clock = pygame.time.Clock()

        self.vertices = [
            Point3D(-1, 1, -1),
            Point3D(1, 1, -1),
            Point3D(1, -1, -1),
            Point3D(-1, -1, -1),
            Point3D(-1, 1, 1),
            Point3D(1, 1, 1),
            Point3D(1, -1, 1),
            Point3D(-1, -1, 1)
        ]

        # Define the vertices that compose each of the 6 faces.
        self.faces = [(0, 1, 2, 3), (1, 5, 6, 2), (5, 4, 7, 6),
                      (4, 0, 3, 7), (0, 4, 5, 1), (3, 2, 6, 7)]

        # Define colors for each face
        self.colors = [(255, 0, 255), (255, 0, 0), (0, 255, 0),
                       (0, 0, 255), (0, 255, 255), (255, 255, 0)]

        self.angle = 0


    """ Main Loop: run until window gets closed """
    def run(self):        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.clock.tick(50)
            self.screen.fill((0, 32, 0))

            #* It will hold transformed vertices.
            t = []

            #* perform one gyro integration: read, update quaternion
            self.GYR_Integration_Instance.perform_one_iteration()
            q = self.GYR_Integration_Instance.o

            for v in self.vertices:
                #* rotate point according to integrated gyro
                r = v.rotateQ(q)
                #* Transform the point from 3D to 2D
                p = r.project(self.screen.get_width(), self.screen.get_height(), 256, 4)
                #* Put the point in the list of transformed vertices
                t.append(p)

            #* Calculate the average Z values of each face.
            avg_z = []
            i = 0
            for f in self.faces:
                z = (t[f[0]].z + t[f[1]].z + t[f[2]].z + t[f[3]].z) / 4.0
                avg_z.append([i, z])
                i = i + 1

            #* Draw the faces using the Painter's algorithm:
            #* Distant faces are drawn before the closer ones.
            for tmp in sorted(avg_z, key=itemgetter(1), reverse=True):
                face_index = tmp[0]
                f = self.faces[face_index]
                pointlist = [(t[f[0]].x, t[f[0]].y), (t[f[1]].x, t[f[1]].y),
                             (t[f[1]].x, t[f[1]].y), (t[f[2]].x, t[f[2]].y),
                             (t[f[2]].x, t[f[2]].y), (t[f[3]].x, t[f[3]].y),
                             (t[f[3]].x, t[f[3]].y), (t[f[0]].x, t[f[0]].y)]
                pygame.draw.polygon(self.screen, self.colors[face_index], pointlist)

            self.angle += 1

            pygame.display.flip()
