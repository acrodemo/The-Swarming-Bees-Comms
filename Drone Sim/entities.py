import pygame
import numpy as np
# from sympy import false
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
grey = (200,200,200)



class Base():
    def __init__(self,screen,posx,posy):
        self.screen = screen
        self.posx = posx
        self.posy = posy
        self.name = "Base Station"
        self.font = pygame.font.SysFont("Arial",16)
        self.ip = "192.0.0.0"
        self.textSurface = self.font.render("Base Station",False,(black))
    def draw(self):
        pygame.draw.rect(self.screen,(blue),pygame.Rect(self.posx-10,self.posy-10,20,20))
        self.screen.blit(self.textSurface,(self.posx-35,self.posy+10))

class Drone():
    def __init__(self,screen,posx,posy,name,ip):
        self.screen = screen
        self.posx = posx
        self.posy = posy
        self.font = pygame.font.SysFont("Arial",18)
        self.ip = ip
        self.name = name
        self.textSurface = self.font.render(name,False,(black))
        self.textSurface2 = self.font.render(ip,False,(black))
        self.conns = []

    def draw(self):
        pygame.draw.circle(self.screen,(black),(self.posx,self.posy),10)
        self.screen.blit(self.textSurface,(self.posx-25,self.posy-30))
        self.screen.blit(self.textSurface2, (self.posx-30,self.posy+10))


class Connection():
    def __init__(self,screen,droneA,droneB,color):
        self.screen = screen
        self.droneA = droneA
        self.droneB = droneB
        self.classColor = color
        self.active = True
        self.dist = 0
    def draw(self):
        if(self.active):
            pygame.draw.line(self.screen,(self.classColor),(self.droneA.posx,self.droneA.posy),(self.droneB.posx,self.droneB.posy),1)

class Swarm():
    def __init__(self,screen,swarm,base):
        self.screen = screen
        self.swarm = swarm
        self.base = base
        self.conns = []
        self.establishConn()

    def establishConn(self):
        self.conns = []
        drones = [] 
        for drone in self.swarm:
            drones.append(drone)
            c = Connection(self.screen,self.base,drone,blue)
            self.conns.append(c)
            drone.conns.append(c)
            for drone2 in self.swarm:
                if(drone2 not in drones):
                    c2 = Connection(self.screen,drone,drone2,red)
                    self.conns.append(c2)
                    drone.conns.append(c2)
                    drone2.conns.append(c2)

    def updateConns(self,threshold):
        for conn in self.conns:
            otoDist = np.sqrt((conn.droneA.posx-conn.droneB.posx)**2 + (conn.droneA.posy-conn.droneB.posy)**2)
            conn.dist = otoDist
            if(otoDist < threshold):
                conn.active = True
            else:
                conn.active = False


    def draw(self):
        for conn in self.conns:
            conn.draw()
        for drone in self.swarm:
            drone.draw()
        self.base.draw()

class Packet():
    def __init__(self,screen,start,swarm):
        self.swarm = swarm
        self.screen = screen
        self.startDrone = start
        self.posx = self.startDrone.posx
        self.posy = self.startDrone.posy
        self.active = True

        self.n = 0
        self.steps = 10
        self.graph = {}
        self.stops = []
        self.openList = []
        self.closedList = []
        self.current = start.name
        self.openList.append(self.current)
        self.map = {}
        self.finishedFindingForStep = False
        self.readyToMove = False
        self.classDict = {}
        self.classDict["Base Station"] = self.swarm.base
        for drone in self.swarm.swarm:
            self.classDict[drone.name] = drone
        


    def pathfind(self):
        if(self.openList):

            self.current = self.openList.pop()
            # print("Current Node: {}".format(self.current))
            if(self.current == "Base Station"):
                self.finishedFindingForStep = True
                # print("Pathfinding done for step")
                # print(self.map)
                return
            self.closedList.append(self.current)
            # print("Closed List: {}".format(self.closedList))
            unVisitedNeighbors = self.graph[self.current]
            # print("Neighbors: {}".format(unVisitedNeighbors))
            for neighbor in unVisitedNeighbors:
                if neighbor not in self.closedList:
                    # print("{} added to open list.".format(neighbor))
                    self.openList.append(neighbor)
                    if(self.current not in self.map):
                        self.map[self.current] = [neighbor]
                    else:
                        self.map[self.current].append(neighbor)
                    # print("Map looks like: {}".format(self.map))
        else:
            print("Stuck")
            self.finishedFindingForStep = True
            

        
        # print(self.graph)
        # currentConn = self.conn
        # if(currentConn.droneA == self.swarm.base or currentConn.droneB == self.swarm.base):
        #     print("Done")

    def update(self):
        if(self.active):
            if(not self.finishedFindingForStep):

                # print("Pathfinding")
                for drone in self.swarm.swarm:
                    self.graph[drone.name] = set(conn.droneA.name if conn.droneA is not drone else conn.droneB.name for conn in drone.conns if conn.active)
                self.pathfind()
                self.readyToMove = False
                # print(self.map)
            else:
                # map = {}
                # for key,val in self.map.items():
                #     if val not in map:
                #         map[val] = [key]
                #     else:
                #         map[val].append(key)
                # print(self.map)

                for key,val in self.map.items():
                    for v in val:
                        if v not in self.map and v != "Base Station":
                            val.remove(v)
                try:
                    if("Base Station" in self.map[self.startDrone.name]):
                        idx = "Base Station"
                    else:
                        idx = self.map[self.startDrone.name][0]
                except:
                    idx = self.startDrone.name
                self.targetDrone = self.classDict[idx]
                # print("StartDrone: {} TargetDrone: {}".format(self.startDrone.name,self.targetDrone.name))

                if(self.n != self.steps-1):
                    self.n += 1
                    aposx = self.startDrone.posx
                    aposy = self.startDrone.posy
                    bposx = self.targetDrone.posx
                    bposy = self.targetDrone.posy
                    self.posx = self.startDrone.posx
                    self.posy = self.startDrone.posy
                    self.vecDirection = (bposx - aposx + self.posx, bposy - aposy + self.posy)
                    self.stops = [((self.vecDirection[0]-self.posx)/self.steps * n + self.posx, (self.vecDirection[1]-self.posy)/self.steps * n + self.posy) for n in range(self.steps)]
                    self.readyToMove = True
                else:
                    if(self.targetDrone.name == "Base Station"):
                        self.startDrone = self.targetDrone
                        # print("Complete")
                        self.active = False
                    else:
                        # print("Resetting for Next Pathfinding")
                        self.n = 0
                        # self.active = False
                        self.startDrone = self.targetDrone
                        self.finishedFindingForStep = False
                        self.map = {}
                        self.graph = {}
                        self.stops = []
                        self.openList = []
                        self.closedList = []
                        self.current = self.startDrone.name
                        self.openList.append(self.current)
                        # print("StartDrone: {}".format(self.startDrone.name))

        # print(self.graph)
        # else:
        #     print(self.map)


        # if(self.active):



    def draw(self):
        # pass
        if(self.active and self.finishedFindingForStep):
            if(self.readyToMove):
                pygame.draw.circle(self.screen,(green),self.stops[self.n],6)
        else:
            pygame.draw.circle(self.screen,(green),(self.startDrone.posx,self.startDrone.posy),6)




