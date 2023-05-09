import pygame as pg
import random 

pg.init()
pg.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

SCREEN_SIZE = (1280, 720)
LOWER_BOUNDARY = 150

screen = pg.display.set_mode((SCREEN_SIZE))
pg.display.set_caption("The gun of بغداد")

done = False
clock = pg.time.Clock()
frameCounter = 0
gameObjects = []

#Declaring the variable names of the images used in the program
targetImage = pg.image.load("target.png")
userTankImage = pg.image.load("userTank.png")
algorithmTankImage = pg.image.load("algorithmTankImage.png")

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

    def attack(self):
        pass

class Target(Enemy):
    def __init__(self, team, x, y, vx, vy, radius):
        super().__init__(team, x, y)
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
        if self.x <= 0 or self.x >= SCREEN_SIZE[0]:
            self.vx = -self.vx
        if self.y <= 0 or self.y >= (SCREEN_SIZE[1] - LOWER_BOUNDARY):
            self.vy = -self.vy

        if frameCounter % 90 == 0: # shoot every three seconds for now
            self.attack()

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
    def __init__(self, team, x, y):
        super().__init__(team,x,y)
        self.lastTimeShot = 0
    def update(self):
        keys=pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.x-=10
        if keys[pg.K_RIGHT]:
            self.x+=10
        if keys[pg.K_SPACE]:
            if frameCounter-self.lastTimeShot >= 15:
                self.lastTimeShot = frameCounter
                Projectile(self.team, self.x, self.y, 0, -10, 5)
            
    def draw(self):
        screen.blit(userTankImage, (self.x-TANK_HALF_WIDTH, self.y-TANK_HALF_HEIGHT))
    def getCollisionRect(self):
        # in order to ignore the blank space from the front of the tank up to the tip of the gun
        ignoreTopPixelCount = (150/500) * (TANK_HALF_HEIGHT * 2)
        return pg.Rect(self.x-TANK_HALF_WIDTH, self.y-TANK_HALF_HEIGHT+ignoreTopPixelCount, TANK_HALF_WIDTH*2, TANK_HALF_HEIGHT*2-ignoreTopPixelCount)



class Projectile(GameObject):

    def __init__(self, team, x, y, vx, vy, radius):
        super().__init__(team, x,y)
        self.vx = vx
        self.vy = vy
        self.radius = radius

    def getCollisionRect(self):
        return pg.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)

    def update(self):
        super().update() # call parent update
        rect = self.getCollisionRect()
        for gameObject in gameObjects:
            if gameObject == self or gameObject.team == self.team:
                continue

            if rect.colliderect(gameObject.getCollisionRect()):
                gameObject.destroy()
                self.destroy()

    def draw(self):
        pg.draw.circle(screen, RED, (self.x,self.y), self.radius)

'''class Bombs(Projectile):

'''

'''
class tankShells(Projectile):
    

'''

TARGET_RADIUS = 50
targetImage = pg.transform.scale(targetImage, (TARGET_RADIUS*2, TARGET_RADIUS*2))

TANK_HALF_WIDTH = 25
TANK_HALF_HEIGHT = 50
userTankImage = pg.transform.scale(userTankImage, (TANK_HALF_WIDTH*2, TANK_HALF_HEIGHT*2))

#Deciding the number of targets randomly to be between 7 - 10 targets
numOfTargets = int(random.uniform(7,10))

#A for loop for randomly assigning each of those targets directions to move in and also having a random starting point for all of them
for targets in range(numOfTargets + 1):
    
    #picking the velocity of each target randomly between -10 to -5 and 5 to 10
    vel = random.choice([-10, -9, -8, -7, -6, -5, 5, 6, 7, 8, 9, 10])
    
    #picking the starting point of the target randomly 
    x_axis = int(random.uniform(10,1200))
    y_axis = int(random.uniform(100,500))
    
    #randomly picking a number to make a choice as to which direction it moves in 
    dirToMove = int(random.uniform(1,4))
    if (dirToMove == 1):
        Target(1, x_axis, y_axis, vel, 0, TARGET_RADIUS) #Moves target horizontally
    elif (dirToMove == 2):
        Target(1, x_axis, y_axis, 0, vel, TARGET_RADIUS) #Moves target horizontally
    elif (dirToMove == 3):
        Target(1, x_axis, y_axis, vel, vel, TARGET_RADIUS) #Moves target diagonally

UserTank(PLAYER_TEAM, SCREEN_SIZE[0]/2, SCREEN_SIZE[1]-70)

while not done:
    clock.tick(30)
    screen.fill(BLACK)
    pg.event.get()
    for gameObject in gameObjects:
        gameObject.update()
        gameObject.draw()

    pg.display.flip()
    frameCounter+=1

pg.quit()