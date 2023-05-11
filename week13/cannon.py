import pygame as pg
import random 
from my_colors import *

pg.init()
pg.font.init()

FONT = pg.font.SysFont("dejavusansmono", 25)
#global score
score = 0

#Declaring the variable names of the images used in the program
targetImage = pg.image.load("Target.png")
userTankImage = pg.image.load("userTank.png")
algorithmTankImage = pg.image.load("algorithmTankImage.png")
explosionImage = pg.image.load("explosion.png")

SCREEN_SIZE = (1280, 720)
LOWER_BOUNDARY = 150
TANK_SPACE = 150

TARGET_RADIUS = 50
targetImage = pg.transform.scale(targetImage, (TARGET_RADIUS*2, TARGET_RADIUS*2))
TANK_HALF_WIDTH = 25
TANK_HALF_HEIGHT = 50
userTankImage = pg.transform.scale(userTankImage, (TANK_HALF_WIDTH*2, TANK_HALF_HEIGHT*2))
explosionImage = pg.transform.scale(explosionImage, (TANK_HALF_WIDTH*5, TANK_HALF_HEIGHT*5))

screen = pg.display.set_mode((SCREEN_SIZE))
pg.display.set_caption("The gun of بغداد")

done = False
clock = pg.time.Clock()
frameCounter = 0
totalTargets = 0
gameObjects = []

PLAYER_TEAM = 0
ENEMY_TEAM = 1

#Making class Game Object that every class in the program is derived from
class GameObject:
        
    def __init__(self, team, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.team = team
        gameObjects.append(self)

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def destroy(self):
        gameObjects.remove(self)

    def getCollisionRect(self):
         # return the rect that is used to check collisions by the Project update class
        pass

    def move(self):
        pass
        
    def draw(self):
        pass  

#Making class Tank that is parent to both User tank and Algorithm Tank
class Tank(GameObject):

    def shootAt(self, x, y, bulletSpeed):
            '''
            Shoots a tank shell in the direction of the position (x, y)
            '''
        #Projectile(self.team, self.x, self.y, 0, 10, 5)
#MAking class Enemy that is parent to both the Targets and the Algorithm Tank
class Enemy(GameObject):
    def __init__(self,x,y):
        super().__init__(ENEMY_TEAM, x, y)
    def attack(self):
        pass

class Target(Enemy):
    def __init__(self, x, y, vx, vy, radius):
        super().__init__(x, y)
        self.vx = vx
        self.vy = vy
        self.radius = radius
    def draw(self):
        screen.blit(targetImage, (self.x-self.radius, self.y-self.radius))

    def attack(self):
        Projectile(self.team, self.x, self.y, 0, 10, 5)

    def update(self):
        super().update()
        # Make target bounce off of their boundaries.
        if self.x <= TARGET_RADIUS or self.x >= (SCREEN_SIZE[0] - TARGET_RADIUS):
            self.vx = -self.vx
        if self.y <= TANK_SPACE or self.y >= (SCREEN_SIZE[1] - LOWER_BOUNDARY):
            self.vy = -self.vy

        if frameCounter % 90 == 0: # shoot every three seconds for now
            self.attack()
    def destroy(self):
        super().destroy()
        global score
        score+=1

        '''FIX THIS LATER!!!!!!!'''
    def getCollisionRect(self):
        return pg.Rect(self.x-self.radius,self.y-self.radius,self.radius*2, self.radius*2) #pg.Rect(self.x - self.radius, self.y - self.radius, self.radius, self.radius) 

class AlgorithmTank(Tank, Enemy):
        
    def draw(self):
        #*****cant use radius here because its not a circle 
        screen.blit(algorithmTankImage, (self.x-self.radius, self.y-self.radius))
    def update(self):
        #if pg.time.get_ticks() % 3000 == 0: # shoot every three seconds for now'''
        pass
    def moveTo(self):
        #this function moves the tank to a location such that it has a direct shot at the projectile 
        return super().move()
    def attack(self):
        return super().attack()

class UserTank(Tank):
    def __init__(self, x, y):
        super().__init__(PLAYER_TEAM,x,y)
        self.lastTimeShot = 0
            
    def update(self):
        keys=pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            if (self.x-TANK_HALF_WIDTH > 10):
                self.x-=10
        if keys[pg.K_RIGHT]:
            if (self.x+TANK_HALF_WIDTH < SCREEN_SIZE[0]-10):
                self.x+=10
        if keys[pg.K_SPACE]:
            if frameCounter-self.lastTimeShot >= 15:
                self.lastTimeShot = frameCounter
                Projectile(self.team, self.x, self.y, 0, -10, 5, object = 2)
                
    def draw(self):
        screen.blit(userTankImage, (self.x-TANK_HALF_WIDTH, self.y-TANK_HALF_HEIGHT))
        
    def getCollisionRect(self):
        # in order to ignore the blank space from the front of the tank up to the tip of the gun
        ignoreTopPixelCount = (150/500) * (TANK_HALF_HEIGHT * 2)
        return pg.Rect(self.x-TANK_HALF_WIDTH, self.y-TANK_HALF_HEIGHT+ignoreTopPixelCount, TANK_HALF_WIDTH*2, TANK_HALF_HEIGHT*2-ignoreTopPixelCount)


class Projectile(GameObject):

    def __init__(self, team, x, y, vx, vy, radius, object = 1):
        super().__init__(team, x,y)
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.object = object

    def getCollisionRect(self):
        return pg.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)

    def update(self):
        super().update() # call parent update
        rect = self.getCollisionRect()
        if self.y > SCREEN_SIZE[1] or self.y < 0:
            self.destroy()
        else:
            for gameObject in gameObjects:
                if gameObject == self or gameObject.team == self.team:
                    continue

                if rect.colliderect(gameObject.getCollisionRect()):
                    screen.blit(explosionImage, (self.x-TANK_HALF_WIDTH*2, self.y-TANK_HALF_HEIGHT*2))
                    gameObject.destroy()
                    self.destroy()

    def draw(self):
        if self.object == 1:
            value = random.randint(0,4)
            pg.draw.circle(screen, COLORS[value], (self.x,self.y), self.radius)
        else:
            value = random.randint(0,1)
            pg.draw.ellipse(screen, USER_COLORS[value], rect=(self.x,self.y+2,11,16))
            pg.draw.ellipse(screen, RED, rect=(self.x,self.y,11,9))

'''class Bombs(Projectile):

'''
def generateTargets():
    totalTargets = 0
    #Deciding the number of targets randomly to be between 7 - 10 targets
    numOfTargets = int(random.uniform(7,10))

    #Loops for having a random starting point and velocities for all the targets

    #Making random number of targets (between 2-4) that move horizontally
    numOfTargets = int(random.uniform(2,4))
    totalTargets = totalTargets + numOfTargets + 1
    for targets in range(numOfTargets + 1):
        #picking the velocity of each target randomly between -10 to -5 and 5 to 10
        vel = random.choice([-10, -9, -8, -7, -6, -5, 5, 6, 7, 8, 9, 10])
        #picking the starting point of the target randomly 
        x_axis = int(random.uniform(51,1200))
        y_axis = int(random.uniform(150,500))
        Target(x_axis, y_axis, vel, 0, TARGET_RADIUS)

    #Making random number of targets (between 2-4) that move vertically
    numOfTargets = int(random.uniform(2,4))
    totalTargets = totalTargets + numOfTargets + 1
    for targets in range(numOfTargets + 1):
        
        #picking the velocity of each target randomly between -10 to -5 and 5 to 10
        vel = random.choice([-10, -9, -8, -7, -6, -5, 5, 6, 7, 8, 9, 10])
        
        #picking the starting point of the target randomly 
        x_axis = int(random.uniform(51,1200))
        y_axis = int(random.uniform(150,500))
        Target(x_axis, y_axis, 0, vel, TARGET_RADIUS) #Moves target vertically

    #Making random number of targets (between 2-4) that move diagonally
    numOfTargets = int(random.uniform(2,4))
    totalTargets = totalTargets + numOfTargets + 1
    for targets in range(numOfTargets + 1):
        
        #picking the velocity of each target randomly between -10 to -5 and 5 to 10
        vel = random.choice([-10, -9, -8, -7, -6, -5, 5, 6, 7, 8, 9, 10])
        
        #picking the starting point of the target randomly 
        x_axis = int(random.uniform(51,1200))
        y_axis = int(random.uniform(150,500))
        Target(x_axis, y_axis, vel, vel, TARGET_RADIUS) 
    return totalTargets
    
def initializeGame():
    global frameCounter
    frameCounter = 0
    global score
    score = 0
    gameObjects.clear()
    global totalTargets
    totalTargets = generateTargets()
    UserTank(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]-70)

initializeGame()

while not done:
    clock.tick(30)
    screen.fill(BLACK)
    score_board = (FONT.render("Score: {}".format(score), True, WHITE))
    screen.blit(score_board, [10, 5])
    events = pg.event.get()
    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r: # restart is handled as KEYDOWN event so that it only runs once per click, instead of repeating as long as R is held. 
                initializeGame()
        if event.type == pg.QUIT:
                exit()
              
    for gameObject in gameObjects:
        gameObject.update()
        gameObject.draw()

    if score == totalTargets:
        totalTargets = totalTargets + generateTargets()
    pg.display.flip()
    frameCounter+=1
pg.quit()
