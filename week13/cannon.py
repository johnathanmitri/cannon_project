import pygame as pg

pg.init()
pg.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

SCREEN_SIZE = (1280, 720)
screen = pg.display.set_mode((SCREEN_SIZE))
pg.display.set_caption("The gun of بغداد")

done = False
clock = pg.time.Clock()
frameCounter = 0
gameObjects = []

#Declaring the variable names of the images used in the program
targetImage = pg.image.load("target.png")
algorithmTankImage = pg.image.load("algorithmTankImage.png")

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

    def shootAt(self, x, y):
        '''
        Shoots a tank shell in the direction of the position (x, y)
        '''
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
        if self.y <= 0 or self.y >= SCREEN_SIZE[1]:
            self.vy = -self.vy

        if frameCounter % 90 == 0: # shoot every three seconds for now
            self.attack()

    '''FIX THIS LATER!!!!!!!'''
    def getCollisionRect(self):
        return pg.Rect(1,1,1,1) #pg.Rect(self.x - self.radius, self.y - self.radius, self.radius, self.radius) 

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

class Projectile(GameObject):

    def __init__(self, team, x, y, vx, vy, radius):
        super().__init__(team, x,y)
        self.vx = vx
        self.vy = vy
        self.radius = radius

    def getCollisionRect(self):
        return pg.Rect(self.x - self.radius, self.y - self.radius, self.radius, self.radius)

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

Target(1, 500, 100,-10,0,TARGET_RADIUS)

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