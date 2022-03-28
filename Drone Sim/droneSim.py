import numpy as np
import pygame
#Here we are importing classes written in the other two python files 
from entities import Base, Drone, Packet, Swarm
from grid import Grid
#Establishing color values for the GUI
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
grey = (200, 200, 200)

run_me = True
verbose = False
#All of this is pygame boilerplate
pygame.font.init()
screen_size = screen_width, screen_height = 1000, 1000
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('nodetest')

clock = pygame.time.Clock()
fps_limit = 60


amount = 4
#This is a simple list comprehension to instantiate the drones based on the "amount" value given before
#Drones are instantiated with completely random starting values here. This can be tweaked however you'd like.

swarmList = [Drone(screen, 50*n+150, 50 * n+150, "Drone " +
                   str(n), "192.0.0."+str(n)) for n in range(amount)]
'''
    A drone must be instantiated like this:
    Drone(screen,starting x position, starting y position, string representing IP address)
    Where screen is the pygame display object declared above
    After instantiating drones, they must be added to the swarm, shown below
'''

#A base station must be declared for the packets to head toward
base = Base(screen, 250, 850)
#Grid contains the grid lines and number values for display purposes
grid = Grid(screen, screen_width, screen_height, 50, 50, base)
#The swarm contains all the drones on the map currently. 
#Pass a list of drone objects to this constructor
swarm = Swarm(screen, swarmList, base)
#This is just our first packet. Many more will be instantiated
packet = Packet(screen, swarmList[1], swarm)
packets = [packet]

n = 0
while run_me:
    clock.tick(60)
    n += 1
    #More pygame boielerplate
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_me = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                #Here is where we instantiate our packets by pressing the spacebar
                #The second argument is a reference to where we'd like the packet to originate
                packets.append(Packet(screen, swarmList[0], swarm))

        keysPressed = pygame.key.get_pressed()
        
        if(keysPressed[pygame.K_LEFT]):
            swarmList[0].posx -= 50
        if(keysPressed[pygame.K_RIGHT]):
            swarmList[0].posx += 50   
        if(keysPressed[pygame.K_UP]):
            swarmList[0].posy -= 50
        if(keysPressed[pygame.K_DOWN]):
            swarmList[0].posy += 50   

    #This is where we define flightpaths of our drones.
    # You can see that all we are doing is updating the position of the
    # drones every tick. The n variable is incremented with every tick.
    # This is very janky currently, and I have plans to build out an actual
    # flightpath planning feature. 
    swarmList[1].posx = int(300 + 50 * np.sin(n*.01))
    swarmList[1].posy = int(300 + 50 * np.cos(n*.01))

    swarmList[2].posx = int(700 + 200 * np.sin(n*.05))
    swarmList[2].posy = int(700 + 150 * np.cos(n*.03)*np.sin(n*.01))

    swarmList[3].posx = int(250 + 150 * np.sin(n*.01))
    swarmList[3].posy = int(600 + 150 * np.cos(n*.03))

    screen.fill(white)
    #Here is another janky detail:
    # This is where we declare the max distance between drones 
    # before the connection is lost. Currently it's set at 500 
    # units for demonstration purposes. 
    swarm.updateConns(500)
    grid.drawGrid()
    swarm.draw()

    for packet in packets:
        packet.update()
        packet.draw()

    if(verbose):
        for conn in swarm.conns:
            if conn.active:
                print("{} is within viable comm distance of {}. Distance between is {} ft.".format(
                    conn.droneA.ip, conn.droneB.ip, conn.dist/5))
            else:
                print("{} is not within viable comm distance of {}. Distance between is {} ft. Recommend distance change of \
                {} ft.".format(conn.droneA.ip, conn.droneB.ip, conn.dist/5, conn.dist/5-100))

    pygame.display.flip()

pygame.quit()
