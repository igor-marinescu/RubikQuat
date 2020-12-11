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
import random, pygame

# List of all flip commands
flipCmdList = ['f', 'F', 'u', 'U', 'l', 'L', 'r', 'R', 'y', 'Y', 'x', 'X', 'z', 'Z']

# Map contains definitions (layer, direction, image) for every flip command
#                 cmd   layer   dir.    img
flipCmdDefMap = { 'f':  (0,     +1,     4),   # F
                  'F':  (0,     -1,     11),  # F'
                  'u':  (1,     +1,     5),   # U
                  'l':  (2,     +1,     6),   # L
                  'L':  (2,     -1,     13),  # L'
                  'U':  (1,     -1,     12),  # U'
                  'r':  (3,     -1,     7),   # R
                  'R':  (3,     +1,     14),  # R'
                  'y':  (4,     +1,     8),   # Y
                  'Y':  (4,     -1,     15),  # Y'
                  'x':  (5,     +1,     9),   # X
                  'X':  (5,     -1,     16),  # X'
                  'z':  (6,     +1,     10),  # Z
                  'Z':  (6,     -1,     17)   # Z'
                }

class CmdManager:
    """ Command Manager """
    
    def __init__(self, resMan, width):
    
        # Init resource manager
        self.resMan = resMan
    
        # The list of flipping commands , where every element is a tuple: (flipLayer, flipDir, flipImg)
        self.cmdList = []
        self.cmdIdx = 0     # The current command index in the cmdList
        self.cmdTop = 0     # Index of the top of the list
        
        # The list of undo commands , where every element is a tuple: (flipLayer, flipDir)
        self.undList = []   # The undo-list: contains the commands for undo
        self.undIdx = 0     # The current command index in the cmdList
        
        # Create surface to draw undo-/redo-commands
        self.width = width
        self.surface = pygame.Surface((width, 32))
        #self.surface.fill((10, 10, 50))
        self.surface.fill((0, 0, 0))
        self.surface.set_colorkey((0, 0, 0))
    
    def flip(self, flipCmd):
        """ Add the command to flip a layer to command list
        flipCmd - flip command: an entry in flipMan dictionary """
        
        # In case the top is already pointing to the end the list:
        # just add the command at the end of list and move the top to the end
        if(self.cmdTop >= len(self.cmdList)):
            self.cmdList.append(flipCmdDefMap[flipCmd])
            self.cmdTop = len(self.cmdList)
        # Otherwise if top is not already pointing to the end of list (there are 'redo' commands):
        # add the command to the top and remove the rest of the list (delete 'redo' command)
        else:
            self.cmdList[self.cmdTop] = flipCmdDefMap[flipCmd]
            self.cmdList[self.cmdTop + 1 :] = []
            self.cmdTop = len(self.cmdList)
        #self.out()
    
    def scramble(self, cnt):
        """ Scramble Rubik 
        cnt - count: how many times to flip (scramble) """
        for i in range(cnt):
            self.flip(flipCmdList[random.randint(0, len(flipCmdList) - 1)])
        #self.out()
    
    def getNextCmd(self):
        """ Get the next command to be executed a tupple (flipLayer, flipDir), 
        the first priority has the undo-list (if it is not empty) 
        and after the commands list """
        
        # First check if undo list is not empty and retun next command from it
        if(self.undIdx < len(self.undList)):
            # Get next element from undo-list
            retVal = self.undList[self.undIdx]
            self.undIdx += 1
            return retVal
        
        # Check if command list not empty and return next command from it
        if((self.cmdIdx < self.cmdTop) and (self.cmdIdx < len(self.cmdList))):
            retVal = self.cmdList[self.cmdIdx]
            self.cmdIdx += 1
            return retVal
        
        # No commands to execute
        return None
    
    def undo(self):
        """ Undo the last movie """
        # Check if cmd list not empty
        if((self.cmdTop > 0) and (len(self.cmdList) > 0)):
            # Get element from top position and decrement top and index
            self.cmdTop -= 1
            (flipLayer, flipIdx, flipImg) = self.cmdList[self.cmdTop]
            if(self.cmdIdx > self.cmdTop):
                self.cmdIdx = self.cmdTop
            # Add element to undo-list (but inverse the direction)
            self.undList.append((flipLayer, -flipIdx))
            #self.out()
        pass
    
    def redo(self):
        """ Redo the move after an 'undo' operation """
        # Check if there are command between top index and end of the list
        # and increase the top pointer, getNextCmd will execute the command
        if(self.cmdTop < len(self.cmdList)):
            self.cmdTop += 1
    
    def updateSurface(self):
        """ Display command manager history (undo and redo moves) """
        #self.surface.fill((10, 10, 50))
        self.surface.fill((0, 0, 0))
        
        # display history
        x = self.width/2 - 32
        i = self.cmdTop - 1
        while(x > -32) and (i >= 0) and (i < len(self.cmdList)):
            self.resMan.draw(self.surface, self.cmdList[i][2], x, 0)
            i -= 1
            x -= 32
        
        # display redo
        x = self.width/2
        i = self.cmdTop
        while(x < self.width) and (i < len(self.cmdList)):
            self.resMan.draw(self.surface, self.cmdList[i][2], x, 0)
            i += 1
            x += 32
        
        pygame.draw.line(self.surface, (128, 128, 128),
                         (self.width/2, 0), (self.width/2, 32), 1)
    
    def draw(self, surface, pos):
        """ Draw history """
        surface.blit(self.surface, pos)

    def out(self):
        """ Display commands and history """
        print("cmd: len=", len(self.cmdList), " top=", self.cmdTop, " idx=", self.cmdIdx)
        for idx,cmd in enumerate(self.cmdList):
            print(idx, cmd)
        print("undo: len=", len(self.undList), " idx=", self.undIdx)
        for idx,cmd in enumerate(self.undList):
            print(idx, cmd)
    
