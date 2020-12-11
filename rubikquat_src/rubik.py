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
from . import cubelet

#------------------------------------------------------------------------------
# Rubik's Data
# Rubik contains 27 elements (small cubes) called Cubelets.
# Every cubelet has 6 faces. Every face has a color.
#           +----+----+----+
#          / 0  / 1  / 2  /|                             K(4) back
#         / 3  / 4  / 5  / |                            /
#        / 6  / 7  / 8  /  |                      +-------+
#       +----+----+----+   |                     /  T(1) /|
#       |   ---------------+                    /  top  / |
#       |  / 9  / 10 / 11 /|           L(2)--> +-------+  | <--R(3) 
#       | / 12 / 13 / 14 / |           left    |  F(0) |  +    right
#       |/ 15 / 16 / 17 /  |                   | front | /
#       +----+----+----+   |                   |       |/
#       |   ---------------+                   +-------+
#       |  / 18 / 19 / 20 /                         ^
#       | / 21 / 22 / 23 /                       B(5) bottom   
#       |/ 24 / 25 / 26 /                        
#       +----+----+----+   
#------------------------------------------------------------------------------
class RubikData:
    """ RubikData is the main data storage of Rubik.
        It contains the list of cubelet. Where every cubelet is a list of colors 
        representing every face. """
    
    def __init__(self, rubikDef):
        """ Initialize rubik
            rubikdef - Rubik definition: Definition of cubelets and their face colors """
        self.rubikDef = rubikDef
        self.pos = []   # List of relative positions for every cubelet: tuple (x, y, z)
        self.data = []  # List of cubelets, every element is a list of faces for that cubelet
        self.count = 0  # Count of cubelets
        #add cubelets
        for cDef in self.rubikDef:
            self.pos.append(cDef[0])            # Relative position for every cubelet (x, y, z)
            self.data.append(cDef[1].copy())    # Faces definition for every cubelet [0, 2, 3, 0, 5, 0]
            self.count += 1
        
    def reset(self):
        """ Reset (reinitialize) Rubik to its default state/values """
        for idx,cDef in enumerate(self.rubikDef):
            self.pos[idx] = cDef[0]             # Relative position for every cubelet (x, y, z)
            for j,f in enumerate(cDef[1]):
                self.data[idx][j] = f           # Faces definition for every cubelet [0, 2, 3, 0, 5, 0]

    def out(self):
        for idx, c in enumerate(self.data):
            print(f'{idx:2d} : {c}')

    def flipX(self, cubeletIdx, direction):
        """ Flip the colors of one cubelet between faces on axis X
        direction - direction of fliping: < 0 = clockwise, > 0 = c.clockwise """
        c = self.data[cubeletIdx]
        col = c[0];
        if(direction < 0):
            c[0] = c[1]
            c[1] = c[4]
            c[4] = c[5]
            c[5] = col
        elif(direction > 0):
            c[0] = c[5]
            c[5] = c[4]
            c[4] = c[1]
            c[1] = col

    def flipY(self, cubeletIdx, direction):
        """ Flip the colors of one cubelet between faces on axis Y
        direction - direction of fliping: < 0 = clockwise, > 0 = c.clockwise """
        c = self.data[cubeletIdx]
        col = c[0];
        if(direction < 0):
            c[0] = c[3]
            c[3] = c[4]
            c[4] = c[2]
            c[2] = col
        elif(direction > 0):
            c[0] = c[2]
            c[2] = c[4]
            c[4] = c[3]
            c[3] = col

    def flipZ(self, cubeletIdx, direction):
        """ Flip the colors of one cubelet between faces on axis Z
        direction - direction of fliping: < 0 = clockwise, > 0 = c.clockwise """
        c = self.data[cubeletIdx]
        col = c[1];
        if(direction < 0):
            c[1] = c[2]
            c[2] = c[5]
            c[5] = c[3]
            c[3] = col
        elif(direction > 0):
            c[1] = c[3]
            c[3] = c[5]
            c[5] = c[2]
            c[2] = col

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class RubikExt(RubikData):
    """ RubikExt is the extended Rubik containing also the cubelets in 3D coordinates """
    
    def __init__(self, rubikDef):
        """ Initialize rubik 
            rubikDef - rubik definition """
        # initialize rubik's data
        RubikData.__init__(self, rubikDef)
        # initialize cubelets
        self.cubelet = []
        for pos, data in zip(self.pos, self.data):
            x, y, z = (pos)
            self.cubelet.append(cubelet.Cubelet((x * 60, y * 60, z * 60), data, 55))
        
    def init0(self):
        """ Init all cubelets to default position """
        for c in self.cubelet:
            c.init0()

    def rotate(self, q):
        """ Rotate all cubelet with a quaternion (in reference to center) """
        for c in self.cubelet:
            c.rotate(q)

    def updateFaces(self):
        """ Rotate all cubelet with a quaternion (in reference to center) """
        for c in self.cubelet:
            c.updateFaces()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class RubikSet:
    """ Rubik Set - is a set of cubelets defined in RubikData instance
        Rubik set is used to make operations (ex: flips) to a set of cubelets """

    def __init__(self, rubikData, rubikSetDef):
        """ Initialize Rubik Set 
            rubikData - the definition of the entire Rubik 
            rubikSetDef - the definition of this Rubik Set
                cubelIdx[] - list of cubelets in set (every element is an index to rubikData.data[])
                cubelIdx90[] - list of cubelets after fliping the set 90 degrees clockwise along axe 
                cubelIdxCenter - index (in rubikData.data[]) of the center cube for set 
                axis - axis on which the rotation/flipping of set takes place 
                axisDir - axis direction: 1=positive, -1=inversed/negative """
                
        self.rubikData = rubikData
        self.cubelIdx = rubikSetDef[0]
        self.cubelIdx90 = rubikSetDef[1]
        self.cubelIdxCenter = rubikSetDef[2]
        self.axis = rubikSetDef[3]
        self.axisDir = rubikSetDef[4]
        
        # if list of cubelets indexes is not defined, use the enire rubik
        if(self.cubelIdx == None):
            self.cubelIdx = range(rubikData.count)

        # set the index of center cubelet for this set
        # if not defined, use the middle cubelet from rubik
        if(self.cubelIdxCenter == None):
            self.cubelIdxCenter = int(rubikData.count/2)
        
    def out(self):
        for cidx in self.cubelIdx:
            print(f'{cidx:2d} : {self.rubikData.data[cidx]}')

    def flip(self, direction):
        """ Flip the set 
        direction - direction of fliping: < 0 = clockwise, > 0 = c.clockwise """
        
        if(self.cubelIdx90 == None):
            return

        # Copy the color of each face for every cubelet from rubik to a temp list:
        #   |<- Cub.0 ->| |<- Cub.1 ->|...
        # [ [F,T,L,R,K,B],[F,T,L,R,K,B]...]
        tempCubelet = []
        for c in self.rubikData.data:
            tempFaces = c.copy()
            tempCubelet.append(tempFaces)

        # Reassign the colors of each face for every cubelet
        # based on the order specified in self.cubelIdx90
        dst = None
        src = None
        if((direction * self.axisDir) > 0):
            dst = self.cubelIdx90
            src = self.cubelIdx
        elif((direction * self.axisDir) < 0):
            dst = self.cubelIdx
            src = self.cubelIdx90
        else:
            return
        
        for idx_dst,idx_src in zip(dst, src):
            c = self.rubikData.data[idx_dst]
            for i,val in enumerate(tempCubelet[idx_src]):
                c[i] = val
            # flip faces for every cubelets
            flipFunc = "flip" + self.axis
            getattr(self.rubikData, flipFunc)(idx_dst, direction)
            
    def diff(self):
        """ Return a list of indexes of cubelets that are present in rubik
            but not present in this set: range(rubikData.count) - cubelIdx[] """
        diffIdx = []
        for idx in range(self.rubikData.count):
            if idx not in self.cubelIdx:
                diffIdx.append(idx)
        return diffIdx

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class RubikSetDraw(RubikSet):
    """ Rubik Set Drawable - is a drawable set of cubelets """
    
    def __init__(self, rubikExt, rubikSetDef):
        """ Initialize Rubik Set (see RubikSet.__init__) """
        RubikSet.__init__(self, rubikExt, rubikSetDef)
        self.rubikExt = rubikExt
        
        # create a list of cubelet from rubik containing in this set
        self.cubelet = []
        self.zOrder = []        # list stores tulpes: (<index in self.cubes>, <z>)
        self.zDisplay = []      # list stores tulpes: (<index in self.cubes>, <z>)
        for idx in self.cubelIdx:
            c = rubikExt.cubelet[idx]
            self.cubelet.append(c)
            self.zOrder.append((len(self.cubelet) - 1, c.center1[2]))
            
        # set the center cubelet for this set
        self.cubelCenter = rubikExt.cubelet[self.cubelIdxCenter]
            
    def updateZorder(self):
        """ update zOrder for this set """
        # store the value of center.Z of every cubelets to be displayed in zOrder buffer
        for idx,c in enumerate(self.cubelet):
            self.zOrder[idx] = (idx, c.center1[2]) # 2 --> Z axis
        # sort the zOrder buffer by Z value in reverse, (cubelets in the background are first in the list)
        self.zDisplay = sorted(self.zOrder, key=lambda tup: tup[1], reverse = True)

    def getZcenter(self):
        """ Return the Z coordinate of the center cubelets for this set """
        return self.cubelCenter.center1[2]

    def draw(self, surface, offset):
        """ draw the set of cubelets on surface """
        for idx,z in self.zDisplay:
            c = self.cubelet[idx]
            c.draw(surface, offset)
            
    def rotate(self, q):
        """ rotate set with a quaternion """
        for c in self.cubelet:
            c.rotate(q)
    
    def mclick(self, pos):
        # Iterate through Z-order list in reverse: 
        # in this case first come cubelets in foreground, last come cubelets in background
        for idx, z in reversed(self.zDisplay):
            c = self.cubelet[idx]
            if(c.isInsideXY(pos)):
                # Found, get its index in entire Rubik
                # Iterate through Rubik and look for c cubelet
                for i2,cRegExt in enumerate(self.rubikExt.cubelet):
                    if(c is cRegExt):
                        print("Ok: ", i2)
                        return True
        return False