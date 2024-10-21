import pygame
import random
import pandas as pd
import numpy as np
pygame.init()



class Game:
    """
    To use this class simply initialize and instance and call the .loop() method
    inside of a pygame event loop (i.e while loop). Inside of your event loop
    you can call the .draw() and .move_paddle() methods according to your use case.
    Use the information returned from .loop() to determine when to end the
    game by calling
    .reset().
    """
    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BACKGROUND = WHITE


    scale = 5
    trace = 1
    cap = 5.5
    G = 0.011
    speeddivisor = 1.3

    def __init__(self, window, window_width,
        window_height,n,walls=False,consume=False):
        self.window_width = window_width
        self.window_height = window_height
        self.window = window
        self.n = n
        self.bodarr = np.zeros((n, 8))
        self.tracer = [[] for _ in range(n)]

        #customizable
        self.walls = walls
        self.consume = consume



        def rand():
            return random.randint(-min(self.window_width//4,self.window_height//4),min(self.window_width//4,self.window_height//4))
        def randf():
            return (random.random() - 0.5) /self.speeddivisor
        
        for bod in range(self.n):
            self.bodarr[bod][0] = self.window_width/2 + rand()
            self.bodarr[bod][1] = self.window_height/2 + rand()
            self.bodarr[bod][2] = randf()
            self.bodarr[bod][3] =randf()
            self.bodarr[bod][4] = (abs(rand()) + 30)//2.5
            dif = 130 // self.n
            spot = int(random.random() * 3)
            for i in range(3):
                self.bodarr[bod][5 + i] = 100
            self.bodarr[bod][5 + spot] = dif * bod




    #self.ball1xy = [self.window_width/2 + rand(),self.window_height/2 +rand(),randf(),randf(),10,(255, 0, 0)]
    def grav(self):
        bod = 0
        compbod = 0

        def mapt(bool):
            if bool:
                return -1
            return 1

        def grav(m1,m2,dist):
            if dist ==0:
                return 0
            top = self.G * m1 * m2
            bot = dist * dist + 0.4
            return top/bot
        def dist(x1,x2,y1,y2):
            p1 = abs(x1-x2) **2
            p2 = abs(y1-y2) **2
            fin =(p1+p2) **0.5
            return fin
        def force(x1,x2,y1,y2,ma,mb,xory,bod,compbod):
            distance = dist(x1,x2,y1,y2)
            if distance > 150:
                return 0
            if self.consume and distance <=(ma+mb)//15:
                biggerbod = compbod
                smallerbod = bod
                if self.bodarr[bod][4] > self.bodarr[compbod][4]:
                    biggerbod = bod
                    smallerbod = compbod
                self.bodarr[biggerbod][4] += self.bodarr[smallerbod][4]
                self.bodarr = np.delete(self.bodarr, smallerbod, axis=0)
                compbod -= 1
                bod -= 1
                self.tracer.pop(smallerbod)



            if xory == 0:
                p1 = abs(x1-x2)
                p2 = grav(ma,mb,distance)
                return p2 * (p1/distance)
            else:
                p1 = abs(y1-y2)
                p2 = grav(ma,mb,distance)
                return p2 * (p1/distance)


        while bod < self.bodarr.shape[0]:
            xforces = []
            yforces = []
            compbod = 0
            while compbod < self.bodarr.shape[0]:
                if compbod != bod and bod < self.bodarr.shape[0]:
                    xdir = mapt(self.bodarr[bod][0] > self.bodarr[compbod][0])
                    ydir = mapt(self.bodarr[bod][1] > self.bodarr[compbod][1])
                    xfor = force(self.bodarr[bod][0],self.bodarr[compbod][0],self.bodarr[bod][1],self.bodarr[compbod][1],self.bodarr[bod][4],self.bodarr[compbod][4],0,bod,compbod)
                    if compbod < self.bodarr.shape[0] and bod < self.bodarr.shape[0]:
                        yfor = force(self.bodarr[bod][0],self.bodarr[compbod][0],self.bodarr[bod][1],self.bodarr[compbod][1],self.bodarr[bod][4],self.bodarr[compbod][4],1,bod,compbod)
                        xforces.append(xdir * xfor)
                        yforces.append(ydir * yfor)
                compbod += 1
            ximp = sum(xforces)
            yimp = sum(yforces)
            if bod < self.bodarr.shape[0]:
                self.bodarr[bod][2] += ximp
                if self.bodarr[bod][2] > self.cap: self.bodarr[bod][2] = self.cap
                if self.bodarr[bod][2] < -self.cap: self.bodarr[bod][2] = -self.cap

                self.bodarr[bod][3] += yimp
                if self.bodarr[bod][3] > self.cap: self.bodarr[bod][3] = self.cap
                if self.bodarr[bod][3] < -self.cap: self.bodarr[bod][3] = -self.cap
            bod += 1

        for bod in range(self.bodarr.shape[0]):
            self.bodarr[bod][0] += self.bodarr[bod][2]
            self.bodarr[bod][1] += self.bodarr[bod][3]

            if self.walls:
                if self.bodarr[bod][0] < 0: 
                    self.bodarr[bod][0] = 0
                    self.bodarr[bod][2] *= -1 

                elif self.bodarr[bod][0] > self.window_width: 
                    self.bodarr[bod][0] = self.window_width 
                    self.bodarr[bod][2] *= -1 

                if self.bodarr[bod][1] < 0: 
                    self.bodarr[bod][1] = 0
                    self.bodarr[bod][3] *= -1 

                elif self.bodarr[bod][1] > self.window_height: 
                    self.bodarr[bod][1] = self.window_height 
                    self.bodarr[bod][3] *= -1






    def draw(self):
        self.window.fill(self.BACKGROUND)

        for bod in range(self.bodarr.shape[0]):
            pygame.draw.circle(self.window,(self.bodarr[bod][5],self.bodarr[bod][6],self.bodarr[bod][7]),(self.bodarr[bod][0], self.bodarr[bod][1]),self.bodarr[bod][4]/self.scale)

        i =0
        for list in self.tracer:
            for loca in list:
                pygame.draw.circle(self.window,(self.bodarr[i][5],self.bodarr[i][6],self.bodarr[i][7]), (loca),self.trace)
            self.tracer[i].append((self.bodarr[i][0], self.bodarr[i][1]))
            max_trace_length = 100 # Limit to the last 100 positions
            if len(self.tracer[i]) > max_trace_length:
                self.tracer[i].pop(0)
            i += 1



    def loop(self):
        """
        Executes a single game loop.

        :returns: GameInformation instance stating score
        and hits of each paddle.
        """
        self.grav()

    def reset(self):
        """Resets the entire game."""
        print("reset")
        self.window.fill(self.BLACK)
        def rand():
            return random.randint(-
            min(self.window_width//4,self.window_height//4),min(self.window_width//4,self.window_height//4))
        def randf():
            return (random.random() - 0.5) /self.speeddivisor
        self.bodarr = np.zeros((self.n, 8))
        self.tracer = [[] for _ in range(self.n)]
        for bod in range(self.n):
            self.bodarr[bod][0] = self.window_width/2 + rand()
            self.bodarr[bod][1] = self.window_height/2 + rand()
            self.bodarr[bod][2] = randf()
            self.bodarr[bod][3] =randf()
            self.bodarr[bod][4] = (abs(rand()) + 30)//2.5
            dif = 130 // self.n
            spot = int(random.random() * 3)
            for i in range(3):
                self.bodarr[bod][5 + i] = 100
            self.bodarr[bod][5 + spot] = dif * bod
