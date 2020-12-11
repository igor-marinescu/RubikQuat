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

# Source from:
#http://www.petercollingridge.co.uk/tutorials/3d/pygame/basic-transformations/

# Source from: 
# https://stackoverflow.com/questions/47492663/how-can-i-determine-if-a-point-is-inside-a-certain-parallelogram-in-python/47508665

def isPointInsideParallelogram(parallelg, point):
    """ Check if point is inside of a parallelogram
        parallelog - definition of paralelogram as a list of 4 tulpes(xy-points) 
                        [(ax, ay), (bx, by), (cx, cy), (dx, dy)]
        point - definition of a xy-point in a tulpe (px, py)
        returns True if point is inside parallelogram else False """

    # 3 points from parallelogram are required to check
    if(len(parallelg) < 4):
        return False

    inside = False
    xb = parallelg[0][0] - parallelg[1][0]
    yb = parallelg[0][1] - parallelg[1][1]
    xc = parallelg[2][0] - parallelg[1][0]
    yc = parallelg[2][1] - parallelg[1][1]
    xp = point[0] - parallelg[1][0]
    yp = point[1] - parallelg[1][1]
    d = (xb * yc) - (yb * xc);
    if(d != 0):
        oned = 1.0 / d;
        bb = ((xp * yc) - (xc * yp)) * oned
        cc = ((xb * yp) - (xp * yb)) * oned
        inside = (bb >= 0) & (cc >= 0) & (bb <= 1) & (cc <= 1)
    return inside

def isPointInsideRect(rectPoint0, rectPoint1, point):
    """ Check if point is inside of a rectangle
        rectPoint0 - tulpe (x0, y0) contains the x and y coordinates of the upper-left corner
        rectPoint1 - tulpe (x1, y1) contains the x and y coordinates of the right-bottom corner
        returns True if point is inside of rectangle or False if otherwise """
    if((point[0] >= rectPoint0[0]) 
        and (point[0] <= rectPoint1[0])
        and (point[1] >= rectPoint0[1])
        and (point[1] <= rectPoint1[1])):
            return True
            
    return False
        
    