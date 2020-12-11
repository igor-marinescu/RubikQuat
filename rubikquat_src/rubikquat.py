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
from .rengine import RubikEngine
from .cmdman import CmdManager
from .resman import ResourceManager
from .buttons import ActionList
from .buttons import ButtonList
from .rutils import isPointInsideRect

# ##############################################################################
# Refresh Flags
# ##############################################################################
class RefreshArea:
    
    def __init__(self):
        self.rubik = False
        self.buttons = False
        self.history = False
        self.back = False

    def nothing(self):
        self.rubik = False
        self.buttons = False
        self.history = False
        self.back = False

    def all(self):
        self.rubik = True
        self.buttons = True
        self.history = True
        self.back = True

    def isRequested(self):
        return (self.rubik or self.buttons or self.history or self.back)

# ###############################################################################
# Main
# ###############################################################################
class RubikQuat:

    def __init__(self, width, height, path):
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption('RubikQuat')
        self.backColor = (10,10,50)
        self.quitFlag = False
        
        # create resource manager and load tiles
        self.resMan = ResourceManager(path)
        self.resMan.loadTiles()
        
        # create rubik engine
        self.reng = RubikEngine(self.resMan, (width - 96, height - 128), self.surface, self.backColor)
        
        # create command manager
        self.cmdMan = CmdManager(self.resMan, width)
        
        # create actions
        self.actList = ActionList()
        #                       key,        keyMod,             manager,        method,     args
        self.actList.add(pygame.K_l,        pygame.KMOD_SHIFT,  self.cmdMan,    'flip',     ['L'])     #0
        self.actList.add(pygame.K_l,        None,               self.cmdMan,    'flip',     ['l'])     #1
        self.actList.add(pygame.K_r,        None,               self.cmdMan,    'flip',     ['r'])     #2
        self.actList.add(pygame.K_r,        pygame.KMOD_SHIFT,  self.cmdMan,    'flip',     ['R'])     #3
        self.actList.add(pygame.K_UP,       pygame.KMOD_SHIFT,  self.cmdMan,    'flip',     ['X'])     #4
        self.actList.add(pygame.K_DOWN,     pygame.KMOD_SHIFT,  self.cmdMan,    'flip',     ['x'])     #5
        self.actList.add(pygame.K_f,        pygame.KMOD_SHIFT,  self.cmdMan,    'flip',     ['F'])     #6
        self.actList.add(pygame.K_f,        None,               self.cmdMan,    'flip',     ['f'])     #7
        self.actList.add(pygame.K_LEFT,     pygame.KMOD_SHIFT,  self.cmdMan,    'flip',     ['y'])     #8
        self.actList.add(pygame.K_RIGHT,    pygame.KMOD_SHIFT,  self.cmdMan,    'flip',     ['Y'])     #9
        self.actList.add(pygame.K_PAGEUP,   pygame.KMOD_SHIFT,  self.cmdMan,    'flip',     ['Z'])     #10
        self.actList.add(pygame.K_PAGEDOWN, pygame.KMOD_SHIFT,  self.cmdMan,    'flip',     ['z'])     #11
        self.actList.add(pygame.K_u,        pygame.KMOD_SHIFT,  self.cmdMan,    'flip',     ['U'])     #12
        self.actList.add(pygame.K_u,        None,               self.cmdMan,    'flip',     ['u'])     #13
        self.actList.add(pygame.K_y,        pygame.KMOD_CTRL,   self.cmdMan,    'undo',     None)      #14
        self.actList.add(pygame.K_z,        pygame.KMOD_CTRL,   self.cmdMan,    'redo',     None)      #15
        self.actList.add(pygame.K_LEFT,     None,               self.reng,      'reqIncRot',['Y',  0.6]) #16
        self.actList.add(pygame.K_RIGHT,    None,               self.reng,      'reqIncRot',['Y', -0.6]) #17
        self.actList.add(pygame.K_UP,       None,               self.reng,      'reqIncRot',['X', -0.6]) #18
        self.actList.add(pygame.K_DOWN,     None,               self.reng,      'reqIncRot',['X',  0.6]) #19
        self.actList.add(pygame.K_PAGEUP,   None,               self.reng,      'reqIncRot',['Z', -0.2]) #20
        self.actList.add(pygame.K_PAGEDOWN, None,               self.reng,      'reqIncRot',['Z',  0.2]) #21
        self.actList.add(pygame.K_s,        None,               self.cmdMan,    'scramble', [10])       #22
        self.actList.add(pygame.K_h,        None,               self.cmdMan,    'out',      None)       #23
        self.actList.add(pygame.K_F1,       None,               self,           'showHelp', None)       #24
        
        # create buttons
        h = height - 32
        w = width
        self.butList = ButtonList(self.resMan, (222, 158, 0))
        #                (posx, posy),      imgIdx, action
        self.butList.add((0, h/2 - 48),         27, self.actList.get(0))    # flip L'
        self.butList.add((0, h/2),              20, self.actList.get(1))    # flip L
        self.butList.add((0, h/2 - 120),        30, self.actList.get(4))    # flip X'
        self.butList.add((0, h/2 + 72),         23, self.actList.get(5))    # flip X

        self.butList.add((w - 48, h/2 - 48),    21, self.actList.get(2))    # flip R
        self.butList.add((w - 48, h/2),         28, self.actList.get(3))    # flip R'
        self.butList.add((w - 48, h/2 - 120),   30, self.actList.get(4))    # flip X'
        self.butList.add((w - 48, h/2 + 72),    23, self.actList.get(5))    # flip X

        self.butList.add((w/2 - 48, h - 48),    25, self.actList.get(6))    # flip F'
        self.butList.add((w/2, h - 48),         18, self.actList.get(7))    # flip F
        self.butList.add((w/2 - 120, h - 48),   22, self.actList.get(8))    # flip Y
        self.butList.add((w/2 + 72, h - 48),    29, self.actList.get(9))    # flip Y'
        self.butList.add((w/2 - 168, h - 48),   31, self.actList.get(10))   # flip Z'
        self.butList.add((w/2 + 120, h - 48),   24, self.actList.get(11))   # flip Z

        self.butList.add((w/2 - 48, 0),         26, self.actList.get(12))   # flip U'
        self.butList.add((w/2, 0),              19, self.actList.get(13))   # flip U
        
        self.butList.add((0, h - 48),           32, self.actList.get(14))   # undo
        self.butList.add((w - 48, h - 48),      33, self.actList.get(15))   # redo

        self.butList.add((0, 0),                34, self.actList.get(24))   # help
        self.butList.add((w - 48, 0),           35, self.actList.get(22))   # scramble
        
        # Refresh area
        self.refresh = RefreshArea()

    def display(self):
    
        """ Draw scene on the surface. """
        # display background
        if(self.refresh.back):
            self.resMan.draw(self.surface, 37, 0, 0)
        
        # display rubik
        if(self.refresh.rubik):
            self.reng.display(self.surface, (48, 48))
        
        # display cmd man
        if(self.refresh.history):
            self.cmdMan.draw(self.surface, (0, self.height - 32))
        
        # display buttons
        if(self.refresh.buttons):
            self.butList.draw(self.surface)
        
        self.refresh.nothing()
    
    def run(self):
        """ Create a pygame surface until it is closed. """
        
        self.showHelp()
        
        self.display()  
        pygame.display.flip()
        
        msPos = (0, 0)
        flagRubikMClick = False
        idxBtnMClick = None

        # Initialize clock
        clock = pygame.time.Clock()
        
        while not self.quitFlag:
            clock.tick(60)
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    self.quitFlag = True
                    
                elif(event.type == pygame.KEYUP):
                    if(event.key == pygame.K_ESCAPE):
                        self.quitFlag = True
                        
                elif(event.type == pygame.KEYDOWN):
                    if(not self.actList.execKeyDown(event.key, pygame.key.get_mods())):
                        pass
                                
                elif(event.type == pygame.MOUSEBUTTONDOWN):
                    idxBtnMClick = None
                    # Start drag and drop, remember mouse position
                    msPos = pygame.mouse.get_pos()
                    # Detect if rubik zone was clicked
                    flagRubikMClick = isPointInsideRect((48, 48), (self.width - 48, self.height - 48 - 32), msPos)
                    flagRubikMDragDrag = False
                    # is it mouse wheel (inside of the rubik zone)?
                    if(flagRubikMClick and ((event.button == 4) or (event.button == 5))):
                        flagRubikMClick = False
                        if(event.button == 4):
                            self.reng.reqIncRot('Z', -0.2)
                        else:
                            self.reng.reqIncRot('Z', 0.2)
                    # If not rubik zone, check if a button was clicked and select it
                    if(not flagRubikMClick):
                        idxBtnMClick = self.butList.mclickSelect(msPos)
                        if(idxBtnMClick != None):
                            self.refresh.buttons = True

                elif(event.type == pygame.MOUSEMOTION):
                    # Rubik clicked and moved?
                    if(flagRubikMClick):
                        flagRubikMDragDrag = True
                        msPosNew = pygame.mouse.get_pos()
                        dy = -(msPosNew[0] - msPos[0]) * 0.01
                        dx = (msPosNew[1] - msPos[1]) * 0.01
                        self.reng.reqRelRot((dx, dy, 0.0))
                
                elif(event.type == pygame.MOUSEBUTTONUP):
                    msPos = pygame.mouse.get_pos()
                    # Rubik clicked?
                    if(flagRubikMClick):
                        # Rubik moved?
                        if(flagRubikMDragDrag):
                            # End drag and drop, apply relative rotation to base rotation
                            self.reng.appRelRot()
                            flagRubikMDragDrag = False
                        # If Rubik not moved, check if a cubelet face was clicked and select it
                        else:
                            if(self.reng.mclick((msPos[0] - 48, msPos[1] - 48))):
                                self.refresh.rubik = True
                                
                        flagRubikMClick = False
                    # Button clicked?
                    if(idxBtnMClick != None):
                        # Mouse released on the same button it was clicked?
                        if(self.butList.isPosButton(idxBtnMClick, msPos)):
                            self.butList.execute(idxBtnMClick)
                        self.butList.deselectAll()
                        self.refresh.buttons = True

            # Check if Rubik not busy (not flipping) and execute next command
            if(not self.reng.isFlipping()):
                cmdNext = self.cmdMan.getNextCmd()
                if(cmdNext != None):
                    self.reng.reqFlip(cmdNext[0], cmdNext[1])
                    self.cmdMan.updateSurface()
                    self.refresh.all()
            
            # Process Rengine and refresh display if necessarily
            if(self.reng.process()):
                self.reng.rotate()
                self.refresh.rubik = True
                
            # Display to be refreshed?
            if(self.refresh.isRequested()):
                self.display()  
                pygame.display.flip()

    def showHelp(self):
        """ Show help screen """
        self.resMan.draw(self.surface, 36, 0, 0)
        pygame.display.flip()
        showingHelp = True

        while showingHelp:
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    self.quitFlag = True
                    showingHelp = False
                    
                if((event.type == pygame.KEYUP)
                or (event.type == pygame.MOUSEBUTTONUP)):
                    showingHelp = False
                    
        self.refresh.all();
