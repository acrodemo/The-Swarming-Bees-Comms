import pygame

black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
grey = (200,200,200)

class Grid():
    def __init__(self,screen,screen_width,screen_height,resWidth,resHeight,base,pixelToFeet=10):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        self.resWidth = resWidth
        self.resHeight = resHeight
        self.cellx = int(screen_width/resWidth) - 1
        self.celly = int(screen_height/resHeight) - 1
        self.basePosx = base.posx
        self.basePosy = base.posy
        self.font = pygame.font.SysFont("Arial",18)
        self.pixelToFeet = pixelToFeet

    def convertToFeet(self,pixX,pixY):
        absX = (pixX - self.basePosx)/self.resWidth * self.pixelToFeet
        absY = (-pixY + self.basePosy)/self.resHeight * self.pixelToFeet
        return(absX,absY)

    def convertToPixels(self,absX,absY):
        pixX = ((absX/self.pixelToFeet)*self.resWidth)+self.basePosx
        pixY = (((absY/self.pixelToFeet)*self.resHeight) - self.basePosy) * -1
        return (pixX,pixY)

    def drawGrid(self):
        for x in range(0,self.cellx):
            textSurface = self.font.render(str(self.pixelToFeet * (x+1-self.basePosx/self.resWidth)),False,(black))
            self.screen.blit(textSurface,((x+1)*self.resWidth-5,self.screen_height-self.resHeight))
            if(x==0):
                for y in range(0,self.celly):
                    textSurface = self.font.render(str(self.pixelToFeet * (-y-1+self.basePosy/self.resHeight)),False,(black))
                    self.screen.blit(textSurface,(self.resWidth/4,(y+1)*self.resHeight-10))

                continue
            for y in range(1,self.celly):
                pygame.draw.rect(self.screen,(grey),pygame.Rect(x*self.resWidth,y*self.resHeight,self.resWidth,self.resHeight),1)

