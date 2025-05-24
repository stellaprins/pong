import pygame
from pathlib import Path
import os

# Colors
BLUE = (86, 156, 214)        
YELLOW = (229, 192, 123)     
GREEN = (152, 195, 121)     
PURPLE = (198, 120, 221)     
GREY = (127, 132, 142)      
WHITE = (255, 255, 255)
BLACK = (40, 44, 52)
AQUA = (97, 218, 251)          

# Settings
WIDTH, HEIGHT = 1200, 500
BAR_WIDTH, BAR_HEIGHT = 20, 350
OFFSET = 30
FPS = 60


####### SETUP ######
against_computer = True


def font_path():
    """By Riciery Leal, https://www.dafont.com/vcr-osd-mono.font"""
    root_dir = Path(__file__).parent.parent
    font_path = root_dir / "font" / "VCR_OSD_MONO_1.001.ttf"
    return font_path
