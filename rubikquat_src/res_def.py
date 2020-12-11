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
# Resource definitions
# This definition is used by res_man.py (loadTiles) when extracting tiles
# from .\resources\images.png
#
#       Top-left location| Tile size  |Tile | Description
#          in images.png |width,height|index|
resDef = [ #(( x0,  y0), |  (w,  h)   |     |

            ((  0,   0),    (24, 24)),  # 0  (axis F)
            (( 24,   0),    (24, 24)),  # 1  (axis L)
            (( 48,   0),    (24, 24)),  # 2  (axis R)
            (( 72,   0),    (24, 24)),  # 3  (axis U)

            ((  0,  24),    (32, 32)),  # 4  (history F)
            ((  0, 120),    (32, 32)),  # 5  (history U)
            ((  0,  88),    (32, 32)),  # 6  (history L)
            ((  0,  56),    (32, 32)),  # 7  (history R)
            (( 64,  24),    (32, 32)),  # 8  (history Y)
            ((  0, 152),    (32, 32)),  # 9  (history X)
            (( 64,  88),    (32, 32)),  # 10 (history Z)

            (( 32,  24),    (32, 32)),  # 11 (history F')
            (( 32, 120),    (32, 32)),  # 12 (history U')
            (( 32,  88),    (32, 32)),  # 13 (history L')
            (( 32,  56),    (32, 32)),  # 14 (history R')
            (( 64,  56),    (32, 32)),  # 15 (history Y')
            (( 32, 152),    (32, 32)),  # 16 (history X')
            (( 64, 120),    (32, 32)),  # 17 (history Z')

            ((  0, 184),    (48, 48)),  # 18 (cmd F)
            ((  0, 328),    (48, 48)),  # 19 (cmd U)
            ((  0, 280),    (48, 48)),  # 20 (cmd L)
            ((  0, 232),    (48, 48)),  # 21 (cmd R)
            ((  0, 424),    (48, 48)),  # 22 (cmd Y)
            ((  0, 376),    (48, 48)),  # 23 (cmd X)
            ((  0, 472),    (48, 48)),  # 24 (cmd Z)

            (( 48, 184),    (48, 48)),  # 25 (cmd F')
            (( 48, 328),    (48, 48)),  # 26 (cmd U')
            (( 48, 280),    (48, 48)),  # 27 (cmd L')
            (( 48, 232),    (48, 48)),  # 28 (cmd R')
            (( 48, 424),    (48, 48)),  # 29 (cmd Y')
            (( 48, 376),    (48, 48)),  # 30 (cmd X')
            (( 48, 472),    (48, 48)),  # 31 (cmd Z')

            ((  0, 520),    (48, 48)),  # 32 (undo)
            (( 48, 520),    (48, 48)),  # 33 (redo)
            ((  0, 568),    (48, 48)),  # 34 (help)
            (( 48, 568),    (48, 48)),  # 35 (scramble)
            
            (( 100,  0),    (600, 600)),# 36 (help screen)
            (( 700,  0),    (600, 600)),# 37 (game screen)
            (( 748, 48),    (504, 504)) # 38 (rubik back)
            
        ]
#----------------------------------------------------------------------------------------------
