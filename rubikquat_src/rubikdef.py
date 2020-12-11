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
#----------------------------------------------------------------------------------------------
# Rubik's Cube Definition: 3x3x3=27 Cubelets (0..26)
#
#           +----+----+----+                             K back
#          / 0  / 1  / 2  /| Z=1                        /
#         / 3  / 4  / 5  / | Z=0                  +-------+
#        / 6  / 7  / 8  /  | Z=-1                /   T   /|
#  Y=-1 +----+----+----+   |                    /  top  / |
#       |   ---------------+             L --> +-------+  <-- R
#       |  / 9  / 10 / 11 /| Z=1         left  |   F   |  +   right
#       | / 12 / 13 / 14 / | Z=0               | front | /
#       |/ 15 / 16 / 17 /  | Z=-1              |       |/
#   Y=0 +----+----+----+   |                   +-------+
#       |   ---------------+                        ^
#       |  / 18 / 19 / 20 / Z=1                  B bottom   
#       | / 21 / 22 / 23 / Z=0   
#       |/ 24 / 25 / 26 / Z=-1      Colors:         
#   Y=1 +----+----+----+            0-None    3-Blue    6-White
#        X=-1  X=0  X=1             1-Red     4-Green
#                                   2-Yellow  5-Orange
#
#       | coordinates  |   faces/colors    | cubelet
#       |   X,  Y  Z,  | F, T, L, R, K, B  | index
c3x3 = [ ((-1, -1,  1), [0, 2, 3, 0, 5, 0]), # 0
         (( 0, -1,  1), [0, 2, 0, 0, 5, 0]), # 1
         (( 1, -1,  1), [0, 2, 0, 4, 5, 0]), # 2
         ((-1, -1,  0), [0, 2, 3, 0, 0, 0]), # 3
         (( 0, -1,  0), [0, 2, 0, 0, 0, 0]), # 4
         (( 1, -1,  0), [0, 2, 0, 4, 0, 0]), # 5
         ((-1, -1, -1), [1, 2, 3, 0, 0, 0]), # 6
         (( 0, -1, -1), [1, 2, 0, 0, 0, 0]), # 7
         (( 1, -1, -1), [1, 2, 0, 4, 0, 0]), # 8
         ((-1,  0,  1), [0, 0, 3, 0, 5, 0]), # 9
         (( 0,  0,  1), [0, 0, 0, 0, 5, 0]), # 10
         (( 1,  0,  1), [0, 0, 0, 4, 5, 0]), # 11
         ((-1,  0,  0), [0, 0, 3, 0, 0, 0]), # 12
         (( 0,  0,  0), [0, 0, 0, 0, 0, 0]), # 13
         (( 1,  0,  0), [0, 0, 0, 4, 0, 0]), # 14
         ((-1,  0, -1), [1, 0, 3, 0, 0, 0]), # 15
         (( 0,  0, -1), [1, 0, 0, 0, 0, 0]), # 16
         (( 1,  0, -1), [1, 0, 0, 4, 0, 0]), # 17
         ((-1,  1,  1), [0, 0, 3, 0, 5, 6]), # 18
         (( 0,  1,  1), [0, 0, 0, 0, 5, 6]), # 19
         (( 1,  1,  1), [0, 0, 0, 4, 5, 6]), # 20
         ((-1,  1,  0), [0, 0, 3, 0, 0, 6]), # 21
         (( 0,  1,  0), [0, 0, 0, 0, 0, 6]), # 22
         (( 1,  1,  0), [0, 0, 0, 4, 0, 6]), # 23
         ((-1,  1, -1), [1, 0, 3, 0, 0, 6]), # 24
         (( 0,  1, -1), [1, 0, 0, 0, 0, 6]), # 25
         (( 1,  1, -1), [1, 0, 0, 4, 0, 6])] # 26
#----------------------------------------------------------------------------------------------
# Top Layer Definition
#
#            Indexes of cubelets         After 90 grad rotation of layer
#           +----+----+----+            +----+----+----+
#          / 0  / 1  / 2  /            / 6  / 3  / 0  /
#         / 3  / 4  / 5  /            / 7  / 4  / 1  /
#        / 6  / 7  / 8  /            / 8  / 5  / 2  /
#       +----+----+----+            +----+----+----+
#       
c3x3_top = ([0, 1, 2, 3, 4, 5, 6, 7, 8],    # indexes of cubelets in this set
            [6, 3, 0, 7, 4, 1, 8, 5, 2],    # indexes of cubelets after rotating layer 90 degrees clocwise (facing the layer)
                                      4,    # index of center cubelet of this set
                                 "Y", 1)    # axis of the set, and direction (1 = normal/positive)
#----------------------------------------------------------------------------------------------
# Front Layer Definition
#
#            Indexes of cubelets        After 90 grad rotation of layer
#           +----+----+----+            +----+----+----+
#           | 6  | 7  | 8  |            | 24 | 15 | 6  |
#           | 15 | 16 | 17 |            | 25 | 16 | 7  |
#           | 24 | 25 | 26 |            | 26 | 17 | 8  |
#           +----+----+----+            +----+----+----+
#       
c3x3_front = ([ 6,  7,  8, 15, 16, 17, 24, 25, 26], # indexes of cubelets in this set
              [24, 15,  6, 25, 16,  7, 26, 17,  8], # indexes of cubelets after rotating layer 90 degrees clocwise (facing the layer)
                                                16, # index of center cubelet of this set
                                           "Z",  1) # axis of the set, and direction (1 = normal/positive)
#----------------------------------------------------------------------------------------------
# Left Layer Definition
#
#            Indexes of cubelets        After 90 grad rotation of layer
#           +----+----+----+            +----+----+----+
#           | 0  | 3  | 6  |            | 18 | 9  | 0  |
#           | 9  | 12 | 15 |            | 21 | 12 | 3  |
#           | 18 | 21 | 24 |            | 24 | 15 | 6  |
#           +----+----+----+            +----+----+----+
#       
c3x3_left = ([ 0,  3,  6,  9, 12, 15, 18, 21, 24],  # indexes of cubelets in this set
             [18,  9,  0, 21, 12,  3, 24, 15,  6],  # indexes of cubelets after rotating layer 90 degrees clocwise (facing the layer)
                                               12,  # index of center cubelet of this set
                                           "X", 1)  # axis of the set, and direction (1 = normal/positive)
#----------------------------------------------------------------------------------------------
# Right Layer Definition
#
#            Indexes of cubelets        After 90 grad rotation of layer
#           +----+----+----+            +----+----+----+
#           | 8  | 5  | 2  |            | 26 | 17 | 8  |
#           | 17 | 14 | 11 |            | 23 | 14 | 5  |
#           | 26 | 23 | 20 |            | 20 | 11 | 2  |
#           +----+----+----+            +----+----+----+
#       
c3x3_right = ([ 8,  5,  2, 17, 14, 11, 26, 23, 20], # indexes of cubelets in this set
              [26, 17,  8, 23, 14,  5, 20, 11,  2], # indexes of cubelets after rotating layer 90 degrees clocwise (facing the layer)
                                                14, # index of center cubelet of this set
                                           "X", -1) # axis of the set, and direction (-1 = inverse/negative)
#----------------------------------------------------------------------------------------------
# All - Y Axis Flip Definition:
#
#           +----+----+----+               +----+----+----+
#          / 0  / 1  / 2  /|              / 6  / 3  / 0  /| 
#         / 3  / 4  / 5  / |             / 7  / 4  / 1  / | 
#        / 6  / 7  / 8  /  |            / 8  / 5  / 2  /  | 
#       +----+----+----+   |           +----+----+----+   |  
#       |   ---------------+     ^     |   ---------------+  
#       |  / 9  / 10 / 11 /|     |     |  / 15 / 12 / 9  /|  
#       | / 12 / 13 / 14 / |     | Y   | / 16 / 13 / 10 / |  
#       |/ 15 / 16 / 17 /  |     |     |/ 17 / 14 / 11 /  |  
#       +----+----+----+   |     |     +----+----+----+   |  
#       |   ---------------+           |   ---------------+  
#       |  / 18 / 19 / 20 /            |  / 24 / 21 / 18 / 
#       | / 21 / 22 / 23 /             | / 25 / 22 / 19 / 
#       |/ 24 / 25 / 26 /              |/ 26 / 23 / 20 / 
#       +----+----+----+               +----+----+----+   
#
c3x3_ally = ([  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],    # indexes of cubelets in this set
             [  6,  3,  0,  7,  4,  1,  8,  5,  2, 15, 12,  9, 16, 13, 10, 17, 14, 11, 24, 21, 18, 25, 22, 19, 26, 23, 20],    # indexes of cubelets after rotating layer 90 degrees clocwise (facing the layer)
                13,         # index of center cubelet of this set
                "Y", 1)     # axis of the set, and direction (1 = normal/positive)
#----------------------------------------------------------------------------------------------
# All - X Axis Flip Definition:
#
#           +----+----+----+               +----+----+----+
#          / 0  / 1  / 2  /|              / 18 / 19 / 20 /| 
#         / 3  / 4  / 5  / |             / 9  / 10 / 11 / | 
#        / 6  / 7  / 8  /  |            / 0  / 1  / 2  /  | 
#       +----+----+----+   |           +----+----+----+   |  
#       |   ---------------+           |   ---------------+  
#       |  / 9  / 10 / 11 /|    X      |  / 21 / 22 / 23 /|  
#       | / 12 / 13 / 14 / |  ----->   | / 12 / 13 / 14 / |  
#       |/ 15 / 16 / 17 /  |           |/ 3  / 4  / 5  /  |  
#       +----+----+----+   |           +----+----+----+   |  
#       |   ---------------+           |   ---------------+  
#       |  / 18 / 19 / 20 /            |  / 24 / 25 / 26 / 
#       | / 21 / 22 / 23 /             | / 15 / 16 / 17 / 
#       |/ 24 / 25 / 26 /              |/ 6  / 7  / 8  / 
#       +----+----+----+               +----+----+----+   
#
c3x3_allx = ([  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],    # indexes of cubelets in this set
             [ 18, 19, 20,  9, 10, 11,  0,  1,  2, 21, 22, 23, 12, 13, 14,  3,  4,  5, 24, 25, 26, 15, 16, 17,  6,  7,  8],    # indexes of cubelets after rotating layer 90 degrees clocwise (facing the layer)
                13,         # index of center cubelet of this set
                "X", 1)     # axis of the set, and direction (1 = normal/positive)
#----------------------------------------------------------------------------------------------
# All - Z Axis Flip Definition:
#
#           +----+----+----+               +----+----+----+
#          / 0  / 1  / 2  /|              / 18 / 9  / 0  /| 
#         / 3  / 4  / 5  / |             / 21 / 12 / 3  / | 
#        / 6  / 7  / 8  /  |            / 24 / 15 / 6  /  | 
#       +----+----+----+   |           +----+----+----+   |  
#       |   ---------------+     _     |   ---------------+  
#       |  / 9  / 10 / 11 /|     /|    |  / 19 / 10 / 1  /|  
#       | / 12 / 13 / 14 / |    /      | / 22 / 13 / 4  / |  
#       |/ 15 / 16 / 17 /  |   / Z     |/ 25 / 16 / 7  /  |  
#       +----+----+----+   |  /        +----+----+----+   |  
#       |   ---------------+           |   ---------------+  
#       |  / 18 / 19 / 20 /            |  / 20 / 11 / 2  / 
#       | / 21 / 22 / 23 /             | / 23 / 14 / 5  / 
#       |/ 24 / 25 / 26 /              |/ 26 / 17 / 8  / 
#       +----+----+----+               +----+----+----+   
#
c3x3_allz = ([  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],    # indexes of cubelets in this set
             [ 18,  9,  0, 21, 12,  3, 24, 15,  6, 19, 10,  1, 22, 13,  4, 25, 16,  7, 20, 11,  2, 23, 14,  5, 26, 17,  8],    # indexes of cubelets after rotating layer 90 degrees clocwise (facing the layer)
                13,         # index of center cubelet of this set
                "Z", 1)     # axis of the set, and direction (1 = normal/positive)
#----------------------------------------------------------------------------------------------
