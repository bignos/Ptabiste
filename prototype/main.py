#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ptabiste import *
from startScreen import *


# -[ Main ]-
if __name__ == '__main__':
    exit = False
    while not exit:
        ptabiste    = Ptabiste()
        startScreen = StartScreen()
        startScreen.start()
        if startScreen.next == 'GAME':
            ptabiste.start()
            if ptabiste.next == 'EXIT':
                exit = True
        elif startScreen.next == 'EXIT':
            exit = True
            
