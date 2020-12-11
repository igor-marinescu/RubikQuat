# This file is part of the RubikQuat distribution.
# Copyright (c) 2020 Igor Marinescu (igor.marinescu@gmail.com).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------
import pygame
from cubelet import Cubelet
from quaternion import Quaternion

# ###############################################################################
# Test 
# ###############################################################################
class CubeletTest:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Cubelet Test')
        self.background = (10,10,50)

        self.x_axis_unit = (1, 0, 0)
        self.y_axis_unit = (0, 1, 0)
        self.z_axis_unit = (0, 0, 1)

        self.qflp = Quaternion.from_axisangle(0, self.z_axis_unit)
        self.qrot = Quaternion.from_axisangle(0, self.z_axis_unit)
        self.qrel = Quaternion.from_axisangle(0, self.z_axis_unit)

        self.zOrder = []        # list stores tulpes: (<index in self.cubes>, <z>)
        self.zDisplay = []      # list stores tulpes: (<index in self.cubes>, <z>)

        self.cubelet = [] 
        self.cubelet.append(Cubelet(((0 * 60), (0 * 60), (0 * 60)), [1, 2, 3, 4, 5, 0], 55))
        self.cubelet.append(Cubelet(((1 * 60), (1 * 60), (1 * 60)), [1, 2, 3, 4, 5, 0], 55))
        self.cubelet.append(Cubelet(((0 * 60), (1 * 60), (1 * 60)), [1, 2, 3, 4, 5, 0], 55))
        self.cubelet.append(Cubelet(((0 * 60), (1 * 60), (0 * 60)), [1, 2, 3, 4, 5, 0], 55))

        self.zOrder.append((0, self.cubelet[0].center1[2]))
        self.zOrder.append((1, self.cubelet[1].center1[2]))
        self.zOrder.append((2, self.cubelet[2].center1[2]))
        self.zOrder.append((3, self.cubelet[3].center1[2]))

    def updateZorder(self):
        """ update zOrder for this set """
        # store the value of center.Z of every cubelets to be displayed in zOrder buffer
        for idx,c in enumerate(self.cubelet):
            self.zOrder[idx] = (idx, c.center1[2]) # 2 --> Z axis
        # sort the zOrder buffer by Z value in reverse, (cubelets in the background are first in the list)
        self.zDisplay = sorted(self.zOrder, key=lambda tup: tup[1], reverse = True)
    
    def rotate(self):
        for cub in self.cubelet:
            # Copy nodes1 <- nodes0
            cub.init0()
            # Apply flip rotation
            if(cub == self.cubelet[1]):
                # Apply rotation
                cub.rotate(self.qflp)
            # Apply base rotation
            cub.rotate(self.qrot)
            # Apply relative rotation
            cub.rotate(self.qrel)
            # Update faces
            cub.updateFaces()

    def display(self):
        """ Draw the wireframes on the surface. """
        self.surface.fill(self.background)
        # display axis
        pygame.draw.aaline(self.surface, (50,50,50), (self.width/2, 0), (self.width/2, self.height), 1)
        pygame.draw.aaline(self.surface, (50,50,50), (0, self.height/2), (self.width, self.height/2), 1)
        self.updateZorder()
        for idx,z in self.zDisplay:
            c = self.cubelet[idx]
            c.draw(self.surface, (self.width/2, self.height/2))
    
    def run(self):
        """ Create a pygame surface until it is closed. """
        self.display()  
        pygame.display.flip()
        #print(f'X:{self.wireframe.node[0]:.3f} Y:{self.wireframe.node[1]:.3f} Z:{self.wireframe.node[2]:.3f}')
        #print(self.wireframe.q)
        
        msPos = (0, 0)
        flagDrag = False
        running = True
        
        qrel = Quaternion.from_axisangle(0, self.z_axis_unit)
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        ry = Quaternion.from_axisangle(0.1, self.y_axis_unit)
                        self.qrot = ry * self.qrot
                    elif event.key == pygame.K_RIGHT:
                        ry = Quaternion.from_axisangle(-0.1, self.y_axis_unit)
                        self.qrot = ry * self.qrot
                    elif event.key == pygame.K_DOWN:
                        rx = Quaternion.from_axisangle(0.1, self.x_axis_unit)
                        self.qrot = rx * self.qrot
                    elif event.key == pygame.K_UP:
                        rx = Quaternion.from_axisangle(-0.1, self.x_axis_unit)
                        self.qrot = rx * self.qrot
                    elif event.key == pygame.K_PAGEUP:
                        rz = Quaternion.from_axisangle(-0.1, self.z_axis_unit)
                        self.qrot = rz * self.qrot
                    elif event.key == pygame.K_PAGEDOWN:
                        rz = Quaternion.from_axisangle(0.1, self.z_axis_unit)
                        self.qrot = rz * self.qrot
                    elif event.key == pygame.K_q:
                        rx = Quaternion.from_axisangle(-0.1, self.x_axis_unit)
                        self.qflp = rx * self.qflp
                    elif event.key == pygame.K_a:
                        rx = Quaternion.from_axisangle(0.1, self.x_axis_unit)
                        self.qflp = rx * self.qflp
#                    elif event.key == pygame.K_1:
#                        self.wireframe.load_rot()
#                    elif event.key == pygame.K_r:
#                        self.wireframe.reset()
#                    elif event.key == pygame.K_s:
#                        self.wireframe.save_rot()
#                    elif event.key == pygame.K_l:
#                        self.wireframe.load_rot()
#                                    
                    self.rotate()
                    self.display()  
                    pygame.display.flip()
                    #print(f'X:{self.wireframe.node[0]:.3f} Y:{self.wireframe.node[1]:.3f} Z:{self.wireframe.node[2]:.3f}')
                    
                elif event.type == pygame.MOUSEBUTTONUP:
                    if(flagDrag):
                        self.qrot = self.qrel * self.qrot
                        self.qrel = Quaternion.from_axisangle(0, self.z_axis_unit)
                    flagDrag = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # start drag and drop, remember mouse position and rubik rotation degree
                    print('MDown')
                    msPos = pygame.mouse.get_pos()
                    flagDrag = True

                elif event.type == pygame.MOUSEMOTION:
                    if(flagDrag):
                        msPosNew = pygame.mouse.get_pos()
                        dx = (msPosNew[0] - msPos[0]) * 0.01
                        dy = (msPosNew[1] - msPos[1]) * 0.01
                        
                        rx = Quaternion.from_axisangle(dy, self.x_axis_unit)
                        ry = Quaternion.from_axisangle(-dx, self.y_axis_unit)
                        self.qrel = rx * ry;

                        self.rotate()
                        self.display()  
                        pygame.display.flip()
                        
if __name__ == '__main__':
    pv = CubeletTest(500, 500)
    pv.run()
    