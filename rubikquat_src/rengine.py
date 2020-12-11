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
from . import rubikdef
from . import rubik
from . import axis
from .quaternion import Quaternion

class RubikEngine:
    """ Rubik Engine """
    
    def __init__(self, resMan, width_height, surface, backColor):
        """ Init """

        # Init resource manager
        self.resMan = resMan

        # Create rubik surface
        self.surface = pygame.Surface(width_height, 0, surface)
        (self.width, self.height) = width_height
        self.draw_offset = (self.width/2, self.height/2)
        self.backColor = backColor

        # Rotation axises
        self.x_axis_unit = (1, 0, 0)
        self.y_axis_unit = (0, 1, 0)
        self.z_axis_unit = (0, 0, 1)
        
        # Rubik rotation requests
        self.reqIncRad = 0.0    # Requested destination of incremental rotation [radians]
        self.reqIncAxs = ''     # Requested axis of incremental rotation
        
        self.actIncRad = 0.0    # Actual destination of incremental rotation [radians]
        self.actIncVal = 0.0    # Actual degree of incremental rotation [radians]
        self.actIncAxs = ''     # Actual axis of incremental rotation
        
        self.reqRelRad = (0.0, 0.0, 0.0)
        
        # Rubik flip request
        self.reqFlipIdx = -1
        self.reqFlipDir = 0
        
        # Rotation quaternions
        self.qflp = Quaternion.from_axisangle(0, self.z_axis_unit)  # Rotation of flipping set
        self.qrot = Quaternion.from_axisangle(0, self.z_axis_unit)  # Base rotation of entire rubik
        self.qinc = Quaternion.from_axisangle(0, self.z_axis_unit)  # Incremental rotation of entire rubik
        self.qrel = Quaternion.from_axisangle(0, self.z_axis_unit)  # Relative rotation of entire rubik
        
        # Define the rubik
        self.rubik = rubik.RubikExt(rubikdef.c3x3)
        self.rubik.out()
        
        # Define the set containing the entire rubik (used to display rubik in case of no flipping)
        self.rubSetAll = rubik.RubikSetDraw(self.rubik, (None, None, None, "Y", 1))
        self.rubSetAll.updateZorder()
    
        # Define sets for flipping 
        # During the flipping rubik is divided in two sets A and B
        # Set A is the dynamic set - which flips.
        # Set B is the static set which doesn't flip (rubSetFlipB = rubSetAll - rubSetFlipA)
        self.rubSetFlipA = None
        self.rubSetFlipB = None

        # Definitions for flipping sets
        self.rubFlipDef = []
        self.rubFlipDef.append(rubikdef.c3x3_front)  # 0 = Front Rubik layer
        self.rubFlipDef.append(rubikdef.c3x3_top)    # 1 = Top Rubik layer
        self.rubFlipDef.append(rubikdef.c3x3_left)   # 2 = Left Rubik layer
        self.rubFlipDef.append(rubikdef.c3x3_right)  # 3 = Right Rubik layer
        self.rubFlipDef.append(rubikdef.c3x3_ally)   # 4 = Entire Rubik flip on Y axis
        self.rubFlipDef.append(rubikdef.c3x3_allx)   # 5 = Entire Rubik flip on X axis
        self.rubFlipDef.append(rubikdef.c3x3_allz)   # 6 = Entire Rubik flip on Z axis
        
        # Index of flipping definition currently active (-1 no flipping currently active)
        self.actFlipIdx = -1
        # Index of flipping definition currently requested (-1 no flipping currently requested)
        self.reqFlipIdx = -1
        # Rotation degree of currently flipping set
        self.actFlipRad = 0.0
        # Requested DIrection of flipping
        self.reqFlipDir = 0
        
        # F-axis
        self.axisList = axis.AxisList(self.resMan)
        self.axisList.append(axis.Axis(0, (0.0, 0.0, -100.0), (0.0, 0.0, -150.0))) # F
        self.axisList.append(axis.Axis(1, (-100.0, 0.0, 0.0), (-150.0, 0.0, 0.0))) # L
        self.axisList.append(axis.Axis(2, ( 100.0, 0.0, 0.0), ( 150.0, 0.0, 0.0))) # R
        self.axisList.append(axis.Axis(3, (0.0, -100.0, 0.0), (0.0, -150.0, 0.0))) # T
    
    def divide(self, flipSetIdx = -1):
        """ Divide rubik in two sets:
                1. rubSetFlipA - is the flipping set defined in rubFlipDef
                2. rubSetFlipB - is the rest of rubik containing nodes not in flipping set
            flipSetIdx - index of flipping definition to be used for flipping set
                or -1 when rubik is not divided (rubSetFlipA = None) """
                
        self.actFlipDefIdx = flipSetIdx
        if(self.actFlipDefIdx < 0):
            self.rubSetFlipA = None
            self.rubSetFlipB = None
            return;
            
        # Create the dynamic flipping set A
        setFlipDef = self.rubFlipDef[self.actFlipDefIdx]
        self.rubSetFlipA = rubik.RubikSetDraw(self.rubik, setFlipDef)
        self.rubSetFlipA.updateZorder()
        
        # Create the static set B for the rest of rubik 
        # (which includes the cubelets from Rubik that are not part of dynamic flipping set A)
        restCubel = self.rubSetFlipA.diff()
        if(len(restCubel) > 0):
            self.rubSetFlipB = rubik.RubikSetDraw(self.rubik, (restCubel, None, None, "Y", 1))
            self.rubSetFlipB.updateZorder()
        else:
            self.rubSetFlipB = None
    
    def display(self, surface, offset):
        """ Draw the sets on the surface. """
        #self.surface.fill(self.backColor)
        self.resMan.draw(self.surface, 38, 0, 0)
        self.axisList.drawBack(self.surface, self.draw_offset);
        
        # In case both sets A and B defined
        if((self.rubSetFlipA != None) and (self.rubSetFlipB != None)):
            # Take care about the Z-Order of sets
            if(self.rubSetFlipA.getZcenter() < self.rubSetFlipB.getZcenter()):
                self.rubSetFlipB.draw(self.surface, self.draw_offset)
                self.rubSetFlipA.draw(self.surface, self.draw_offset)
            else:
                self.rubSetFlipA.draw(self.surface, self.draw_offset)
                self.rubSetFlipB.draw(self.surface, self.draw_offset)
        
        # In case only A set defined (flipping the entire rubik)
        elif(self.rubSetFlipA != None):
            self.rubSetFlipA.draw(self.surface, self.draw_offset)
        
        # In case if no set defined (no flipping)
        else:
            self.rubSetAll.draw(self.surface, self.draw_offset)
        
        self.axisList.drawFore(self.surface, self.draw_offset);

        # Draw Renfinge surface into main surface (applying offset)
        surface.blit(self.surface, offset)
    
    def rotate(self):
        """ rotate cubes with angle """
        
        # Init Rubik to initial position
        self.rubik.init0()
        self.axisList.init0()
        
        # Apply rotation to dynamic flipping layer A
        if(self.rubSetFlipA != None):
            self.rubSetFlipA.rotate(self.qflp)
            
        # Apply base rotation to entire rubik
        self.rubik.rotate(self.qrot)
        self.axisList.rotate(self.qrot)
        
        # Apply incremental rotation to entire rubik
        self.rubik.rotate(self.qinc)
        self.axisList.rotate(self.qinc)
        
        # Apply relative rotation to entire rubik
        self.rubik.rotate(self.qrel)
        self.axisList.rotate(self.qrel)
        
        # Update faces
        self.rubik.updateFaces()
        
        # Update Z-Order
        if(self.rubSetFlipA != None):
            self.rubSetFlipA.updateZorder()
        if(self.rubSetFlipB != None):
            self.rubSetFlipB.updateZorder()
        else:
            self.rubSetAll.updateZorder()
    
    def getAxisByName(self, axisName):
        """ Return axis by name """
        if(axisName == 'X'):
            return self.x_axis_unit
        elif(axisName == 'Y'):
            return self.y_axis_unit
        return self.z_axis_unit
    
    def process(self):
        """ Main process function, to be called cyclically 
            Returns True if display must be refreshed, if not returns False """
        
        # Incremental rotation requested?
        if(self.reqIncRad != 0.0):
            # Check if an incremental rotation is currently running
            # and apply it to base rotation
            if(self.actIncRad != 0.0):
                q = Quaternion.from_axisangle(self.actIncRad, self.getAxisByName(self.actIncAxs))
                self.qrot = q * self.qrot
            # Set new destination/axis for the incremental rotation and reset current value
            self.actIncRad = self.reqIncRad
            self.actIncAxs = self.reqIncAxs
            self.actIncVal = 0.0
            self.qinc = Quaternion.from_axisangle(0, self.z_axis_unit)
            # Clear the request
            self.reqIncRad = 0.0
            return True
        
        # Incremental rotation in process?
        if(self.actIncRad != 0.0):
            if(self.actIncVal < self.actIncRad):
                self.actIncVal += 0.1
                # Check if incremental rotation finished (reached destination)
                if(self.actIncVal >= self.actIncRad):
                    q = Quaternion.from_axisangle(self.actIncRad, self.getAxisByName(self.actIncAxs))
                    self.qrot = q * self.qrot
                    self.actIncRad = 0.0
                    self.qinc = Quaternion.from_axisangle(0, self.z_axis_unit)
                    return True
            if(self.actIncVal > self.actIncRad):
                self.actIncVal -= 0.1
                # Check if incremental rotation finished (reached destination)
                if(self.actIncVal <= self.actIncRad):
                    q = Quaternion.from_axisangle(self.actIncRad, self.getAxisByName(self.actIncAxs))
                    self.qrot = q * self.qrot
                    self.actIncRad = 0.0
                    self.qinc = Quaternion.from_axisangle(0, self.z_axis_unit)
                    return True
            self.qinc = Quaternion.from_axisangle(self.actIncVal, self.getAxisByName(self.actIncAxs))
            return True
        
        # Relative rotation requested
        if(self.reqRelRad != (0.0, 0.0, 0.0)):
            rx = Quaternion.from_axisangle(self.reqRelRad[0], self.x_axis_unit)
            ry = Quaternion.from_axisangle(self.reqRelRad[1], self.y_axis_unit)
            self.qrel = rx * ry
            self.reqRelRad = (0.0, 0.0, 0.0)
            return True
        
        # Flipping currently active?
        if(self.actFlipIdx != -1):
        
            # Rotate flipping set with one more step
            if(self.reqFlipDir < 0):
                self.actFlipRad -= 0.15
            elif(self.reqFlipDir > 0):
                self.actFlipRad += 0.15
                
            axis = self.getAxisByName(self.rubSetFlipA.axis)
            self.qflp = Quaternion.from_axisangle(self.actFlipRad, axis)
            
            # Flipping set rotated already ~90 degrees? 
            if((self.actFlipRad < -1.5) or (self.actFlipRad > 1.5)):
                # Flipping finished, flip the cubes inside the set
                if(self.rubSetFlipA != None):
                    self.rubSetFlipA.flip(-self.reqFlipDir)
                # Destroy the flipping sets
                self.qflp = Quaternion.from_axisangle(0, self.z_axis_unit)
                self.actFlipIdx = -1
                self.divide(-1)
            return True
        
        # Flip requested
        if(self.reqFlipIdx != -1):
            # Create the new flipping set (by dividing rubik)
            self.actFlipIdx = self.reqFlipIdx
            self.reqFlipIdx = -1
            self.divide(self.actFlipIdx)
            self.actFlipRad = 0.0
            return True
        
        # Idle, do nothing
        return False
    
    def reqIncRot(self, axis, degree):
        """ Request incremental rotation along one axis
            axis - axis along which the incremental rotation is requested
            degree - requested incremental rotation degree in radians  """
        self.reqIncAxs = axis
        self.reqIncRad = degree
        
    def reqRelRot(self, degree):
        """ Request Relative Rubik rotation along 3 axis (x, y, z)
            degree - rotation degree in radians  """
        self.reqRelRad = degree
    
    def appRelRot(self):
        """ Apply relative rotation to base rotation """
        self.qrot = self.qrel * self.qrot
        # Reset relative rotation
        self.qrel = Quaternion.from_axisangle(0, self.z_axis_unit)
    
    def reqFlip(self, flipIdx, flipDir):
        """ Request Flip of a set 
            flipIdx - Index of flipping definition 
            flipDir - flipping direction: 1 or -1 """
        self.reqFlipIdx = flipIdx
        self.reqFlipDir = flipDir
    
    def isFlipping(self):
        """ Return True if rubik is currently flipping or has a flipping request
        otherwise return False """
        return ((self.reqFlipIdx != -1) or (self.actFlipIdx != -1))
    
    def mclick(self, pos):
        """ mouse click, detect cubelet on which it was clicked """
        # search first cublet (based on z-order) which is at this pos
        return self.rubSetAll.mclick((pos[0] - self.draw_offset[0], pos[1] - self.draw_offset[1]))
