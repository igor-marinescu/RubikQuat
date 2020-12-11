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

#-------------------------------------------------------------------------------
# Axis
#-------------------------------------------------------------------------------
class Axis:

    def __init__(self, ridx, coord0A, coord0B):
        """ Initialize axis:
            ridx - resource index
            coord0A - initial coordinates point A - tuple (X,Y,Z)
            coord0B - initial coordinates point B - tuple (X,Y,Z) """
        self.ridx = ridx
        self.c0A = coord0A
        self.c0B = coord0B
        self.c1A = coord0A
        self.c1B = coord0B
    
    def init0(self):
        """ Initialize axis coordinates to init position 0 """
        self.c1A = self.c0A
        self.c1B = self.c0B

    def rotate(self, q):
        """ Rotate cubelet with a degree in reference to center """
        self.c1A = q * self.c1A
        self.c1B = q * self.c1B
        
    def draw(self, surface, offset):
        """ Draw cubelet's faces """
        pygame.draw.line(surface, (255, 255, 255),
                                 (offset[0] + self.c1A[0], offset[1] + self.c1A[1]), 
                                 (offset[0] + self.c1B[0], offset[1] + self.c1B[1]), 1)

#-------------------------------------------------------------------------------
# Axis List
#-------------------------------------------------------------------------------
class AxisList:
    
    def __init__(self, resMan):
        self.axisList = []
        self.resMan = resMan
        
    def append(self, a):
        self.axisList.append(a)
    
    def init0(self):
        for a in self.axisList:
            a.init0()
    
    def rotate(self, q):
        for a in self.axisList:
            a.rotate(q)
    
    def drawBack(self, surface, offset):
        for a in self.axisList:
            # Check Z coordinate, if bigger than 0 the axis is in the background
            if(a.c1A[2] > 0.0):
                a.draw(surface, offset)
                self.resMan.draw(surface, a.ridx, a.c1B[0] + offset[0] - 12, a.c1B[1] + offset[1] - 12)
    
    def drawFore(self, surface, offset):
        for a in self.axisList:
            # Check Z coordinate, if smaller than 0 the axis is in the foreground
            if(a.c1A[2] <= 0.0):
                a.draw(surface, offset)
                self.resMan.draw(surface, a.ridx, a.c1B[0] + offset[0] - 12, a.c1B[1] + offset[1] - 12)
