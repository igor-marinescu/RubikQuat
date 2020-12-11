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
class Action:
    """ Definition of an action """

    def __init__(self, key, keyMod, manager, method, args):
        self.key = key
        self.keyMod = keyMod
        self.manager = manager
        self.method = method
        self.args = args

    def execute(self):
        """ Execute the action """
        if((self.manager != None) and (self.method != None)):
            # check if there are arguments for the method
            if(self.args != None):
                getattr(self.manager, self.method)(*self.args)  # call method with arguments
                #getattr(btn.manager, btn.method)(btn.args)  # call method with arguments
            else:
                getattr(self.manager, self.method)()          # call method without arguments
            return True
        return False
        
#-------------------------------------------------------------------------------
class ActionList:
    """ Definition of a list of actions """

    def __init__(self):
        self.actList = []
    
    def add(self, key, keyMod, manager, method, args):
        """ Add button to the list of buttons """
        self.actList.append(Action(key, keyMod, manager, method, args))

    def execKeyDown(self, key, keyMod):
        """ Execute keydown """
        for act in self.actList:
            if(act.key == key):
                # Key match, check 
                if(act.keyMod == None):
                    if(keyMod == 0):
                        return act.execute()
                elif(act.keyMod & keyMod):
                        return act.execute()
        return False
        
    def get(self, idx):
        return self.actList[idx]
    
#-------------------------------------------------------------------------------
class Button:
    """ Definition of a button """

    def __init__(self, pos, imgIdx, action):
        self.pos = pos
        self.imgIdx = imgIdx
        self.action = action
        self.select = False     # Indicates if the button is selected

#-------------------------------------------------------------------------------
class ButtonList:
    """ Definition of a list of buttons """

    def __init__(self, resMan, selectColor):
        self.btnList = []
        self.resMan = resMan
        self.selectColor = selectColor
    
    def add(self, pos, imgIdx, action):
        """ Add button to the list of buttons """
        self.btnList.append(Button(pos, imgIdx, action))

    def draw(self, surface):
        """ Draw buttons on a surface """
        for b in self.btnList:
            if((b.pos != None) and (b.imgIdx != None)):
                # If button selected?
                special_flags = 0
                if(b.select):
                    surface.fill(self.selectColor, (b.pos[0], b.pos[1], 48, 48))
                    special_flags = pygame.BLEND_ADD
                self.resMan.draw(surface, b.imgIdx, b.pos[0], b.pos[1], None, special_flags)
    
    def isPosButton(self, idxBtn, pos):
        """ Check if the position is inside of a button 
        idxBtn - button index inside of btnList 
        pos - position to be checked (x, y) 
        returns True if the position (x, y) is inside the button with index idxBtn """
        b = self.btnList[idxBtn]
        if ((pos[0] >= b.pos[0]) and (pos[0] <= (b.pos[0] + 48)) 
        and (pos[1] >= b.pos[1]) and (pos[1] <= (b.pos[1] + 48))):
            return True
        return False

    def mclickSelect(self, pos):
        """ Check if a button was clicked and select it """
        for idx,b in enumerate(self.btnList):
            if((b.pos != None) and self.isPosButton(idx, pos)):
                b.select = True
                return idx
        return None
    
    def deselectAll(self):
        """ De-select all buttons """
        for b in self.btnList:
            b.select = False

    def execute(self, btnIdx):
        """ Execute the action of a button if assigned """
        btn = self.btnList[btnIdx]
        # check if button has an action assigned and execute it
        if(btn.action != None):
            btn.action.execute()
        
    