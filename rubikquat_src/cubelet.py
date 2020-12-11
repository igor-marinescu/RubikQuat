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
from . import rutils

#-------------------------------------------------------------------------------
# Cubelet is the miniature cube - an element of Rubik's Cube.
# Cubelet is defined by 8 nodes and 6 faces:
# 
#        Nodes (0..7):             Faces:        K back
#                                               /
#        5 +-------+ 6                    +-------+ 
#         /|      /|                     /  T    /|
#        / |     / |                    /  top  / |
#     1 +-------+ 2|            L ---> +-------+  | <--- R
#       |4 +----|--+ 7         left    |   F   |  +    right
#       | /     | /                    | front | /
#       |/      |/                     |       |/
#     0 +-------+ 3                    +-------+
#                                           ^
#                                        B bottom 
#-------------------------------------------------------------------------------
class CubeletFace:
    def __init__(self, nodes):
        self.nodes = nodes      # list of nodes which make this face (ex: [0,1,2,3])
        self.visible = False    # indicates if face is visible or not
        self.centerZ = 0.0      # Z coordinate of face's center (used to detect if face is visible)
        self.selected = False   # Inidcates if the face is currently selected

#-------------------------------------------------------------------------------
class Cubelet:

    # The following table defines the list of nodes for each face
    faceNodes = [[0, 1, 2, 3],  # 0-F front (nodes: 0-1-2-3)
                 [1, 5, 6, 2],  # 1-T top   (nodes: 1-5-6-2)
                 [1, 5, 4, 0],  # 2-L left  (nodes: 1-5-4-0)
                 [2, 6, 7, 3],  # 3-R right (nodes: 2-6-7-3)
                 [4, 5, 6, 7],  # 4-K back  (nodes: 4-5-6-7)
                 [0, 4, 7, 3]]  # 5-B bottom(nodes: 0-4-7-3)
                 
    # The following table defines the color for each face type
    faceType = [( 10, 10, 10),      # 0-None
                (0xde, 0x01, 0x01), # 1-Red
                (255,255, 10),      # 2-Yellow
                ( 15, 85,181),      # 3-Blue
                ( 13,112, 13),      # 4-Green
                (0xff, 0x81, 0x16), # 5-Orange
                (255,255,255)]      # 6-White

    def __init__(self, coordinates, facesDef, width):
        """ Initialize a cube:
            coordinates - tuple (X,Y,Z) coordinate of cubelet's center
            facesDef - list [F,T,L,R,K,B] color definition for every face of the cube 
                        (values in the list are index in faceType list)
            width - cubelet's width in pixels """

        # set center coordinates
        x, y, z = coordinates
        self.center0 = coordinates  # cubelet's center in init position 0
        self.center1 = coordinates  # cubelet's center after rotation
        # set faces colors
        self.faceColor = facesDef
        # add nodes
        hw = width / 2
        self.nodes0 = []
        self.nodes0.append((x - hw, y + hw, z - hw)) #0
        self.nodes0.append((x - hw, y - hw, z - hw)) #1
        self.nodes0.append((x + hw, y - hw, z - hw)) #2
        self.nodes0.append((x + hw, y + hw, z - hw)) #3
        self.nodes0.append((x - hw, y + hw, z + hw)) #4
        self.nodes0.append((x - hw, y - hw, z + hw)) #5
        self.nodes0.append((x + hw, y - hw, z + hw)) #6
        self.nodes0.append((x + hw, y + hw, z + hw)) #7
        self.nodes1 = self.nodes0.copy()
        # add faces
        self.faces = []
        for fNodes in self.faceNodes:
            self.faces.append(CubeletFace(fNodes))    # 0-Front
        self.updateFaces()

    def updateFaces(self):
        """ Update the visibility flag for every face, 
            face is visible if its center on axis Z < cube center on Z """
        for face in self.faces:
            sumZ = 0
            for node in face.nodes:
                sumZ += self.nodes1[node][2]                # 2 --> axisZ
            face.centerZ = sumZ / len(face.nodes)
            face.visible = (face.centerZ < self.center1[2]) # 2 --> axisZ

    def init0(self):
        """ Initialize cubelet's coordinates to init position 0 """
        self.nodes1 = self.nodes0.copy()
        self.center1 = self.center0

    def rotate(self, q):
        """ Rotate cubelet with a degree in reference to center """
        for idx,node in enumerate(self.nodes1):
            self.nodes1[idx] = q * node
        # rotate cube center
        self.center1 = q * self.center1
        
    def draw(self, surface, offset):
        """ Draw cubelet's faces on surface """
        for idx, face in enumerate(self.faces):
            if(face.visible):
                temp = []
                for node in face.nodes:
                    temp.append((offset[0] + self.nodes1[node][0], offset[1] + self.nodes1[node][1]))
                pygame.draw.polygon(surface, self.faceType[self.faceColor[idx]], temp, 0)
                if(face.selected):
                    pygame.draw.line(surface, (200, 200, 200), temp[0], temp[2])
                    pygame.draw.line(surface, (200, 200, 200), temp[1], temp[3])
    
    def isInsideXY(self, xyPos):
        """ Check if a point (xyPos) is inside of a cubelet (ignore Z-axis) """
        for face in self.faces:
            # Iterate only through visible faces
            if(face.visible):
                # For every face build a list of points with coordinates X,Y 
                temp = []
                for node in face.nodes:
                    temp.append((self.nodes1[node][0], self.nodes1[node][1]))
                # Check if xyPoint is inside of the parallelogram (temp)
                if(rutils.isPointInsideParallelogram(temp, xyPos)):
                    # toggle face
                    face.selected = not face.selected
                    return True
        return False

