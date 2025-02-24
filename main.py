import pygame as pg
from OpenGL.GL import *

class App:
    
    def __init__(self):
        # Initialize python
        pg.init()
        pg.display.set_mode((640, 480), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        # Initialize OpenGL
        glClearColor(0.1, 0.2, 0.2, 1)
        self.mainloop()
    
    def mainloop(self):
        running = True
        while running:
            # Check events
            for event in pg.event.get():
                if event.type == pg.QUIT:  # Correct event constant
                    running = False
            
            # Refresh screen
            glClear(GL_COLOR_BUFFER_BIT)
            pg.display.flip()
            
            # Timing
            self.clock.tick(60)
        self.quit()
    
    def quit(self):
        pg.quit()
  
if __name__ == "__main__":
    myApp = App()