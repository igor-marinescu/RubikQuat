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
import pygame, os
import os.path
from . import res_def

class ResourceManager:
    """ Resource Manager """
    
    def __init__(self, path):
        self.imgList = []
        self.path = path
    
    def loadImage(self, name, colorkey=None, colorkeypos=None):
        fullname = os.path.join('', name)
        try:
            imgSurface = pygame.image.load(fullname)
        except pygame.error as message:
            print('Cannot load image:', name)
            raise SystemExit(message)

        imgSurface = imgSurface.convert()

        if (colorkey is not None):
            if colorkey is -1:
                colorkey = imgSurface.get_at((0, 0))
            imgSurface.set_colorkey(colorkey, pygame.RLEACCEL)
        elif (colorkeypos is not None):
            colorkey = imgSurface.get_at(colorkeypos)
            imgSurface.set_colorkey(colorkey, pygame.RLEACCEL)

        return imgSurface, imgSurface.get_rect()

    def loadTiles(self):
        """load all tiles in a list"""
        imgText, imgTextRect = self.loadImage(self.path + '/resources/images2.png', colorkeypos=(0, 0))
        #imgText, imgTextRect = self.loadImage('./resources/images2.png', colorkeypos=(0, 0))
        
        # extract images from texture image based on resource definition (resDef)
        for i,rDef in enumerate(res_def.resDef):
            src = rDef[0]
            size = rDef[1]
            self.imgList.append(pygame.Surface(size))
            self.imgList[i].blit(imgText, (0, 0), (src[0], src[1], size[0], size[1]))
            self.imgList[i].set_colorkey((0, 0, 0))

    def draw(self, surface, index, x, y, area = None, special_flags = 0):
        surface.blit(self.imgList[index], (x, y), area, special_flags)
