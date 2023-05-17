import pygame as pg
import random 
from my_colors import *

pg.init()
pg.font.init()

FONT = pg.font.SysFont("dejavusansmono", 25)
GAME_OVER_FONT = pg.font.SysFont("dejavusansmono", 75)
#global score
score = 0

#Declaring the variable names of the images used in the program
targetImage = pg.image.load("Target.png")
userTankImage = pg.image.load("userTank.png")
algorithmTankImage = pg.image.load("algorithmTankImage.png")
explosionImage = pg.image.load("explosion.png")

#Setting the sizes of the screen, the lower boundary for the targets to bounce off of, the widths and heights of the tanks and the radius of the targets.
SCREEN_SIZE = (1280, 720)
LOWER_BOUNDARY = 150
TANK_SPACE = 150

TANK_HALF_WIDTH = 25
TANK_HALF_HEIGHT = 50
ALGORITHM_TANK_HALF_WIDTH = 37.5
ALGORITHM_TANK_HALF_HEIGHT = 50

TARGET_RADIUS = 50

#Scaling the images that are being used in the game to fit our screen.
targetImage = pg.transform.scale(targetImage, (TARGET_RADIUS*2, TARGET_RADIUS*2))
algorithmTankImage = pg.transform.scale(algorithmTankImage,(ALGORITHM_TANK_HALF_WIDTH*2, ALGORITHM_TANK_HALF_HEIGHT*2))
userTankImage = pg.transform.scale(userTankImage, (TANK_HALF_WIDTH*2, TANK_HALF_HEIGHT*2))
explosionImage = pg.transform.scale(explosionImage, (TANK_HALF_WIDTH*5, TANK_HALF_HEIGHT*5))
smallExplosionImage = pg.transform.scale(explosionImage, (50, 50))

#using pygame to create a window with the title 
screen = pg.display.set_mode((SCREEN_SIZE))
pg.display.set_caption("The gun of بغداد")

#Initializing the global variables which are used later 
done = False
clock = pg.time.Clock()
frameCounter = 0
totalTargets = 0
gameObjects = []
bullets = []

#Setting the teams to ints 0 and 1 which is used later to determine destruction of the gameObject on collision 
PLAYER_TEAM = 0
ENEMY_TEAM = 1

#Making class Game Object that every class in the program is ultimately derived from
class GameObject:
        
     #Constructor that initializes the instance variables
    def __init__(self, team, x, y):
        #Setting position of the object
        self.x = x 
        self.y = y
        #Setting the objects velocity in x and y directions
        self.vx = 0 
        self.vy = 0
        self.team = team #Initializing the objects team
        gameObjects.append(self) #Adding the object to the list gameObjects to keep a track of the objects

    #Updates the position of the object on the screen by adding the velocities
    def update(self):
        self.x += self.vx
        self.y += self.vy

    #This removes the object from the gameObject list 
    def destroy(self):
        if self in gameObjects:
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
            #Shoots a tank shell in the direction of the position (x, y)
            pass
        
#Making class Enemy that is parent to both the Targets and the Algorithm Tank
class Enemy(GameObject):

    def __init__(self,x,y):
        super().__init__(ENEMY_TEAM, x, y) 
    def attack(self):
        pass

#Making class Target that determines the behaviour of targets 
class Target(Enemy):
    def __init__(self, x, y, vx, vy, radius):
        super().__init__(x, y)
        self.vx = vx
        self.vy = vy
        self.radius = radius
    
    def draw(self): #Function to draw the target to the screen
        screen.blit(targetImage, (self.x-self.radius, self.y-self.radius))

    #Function that makes the bombs drop out of the targets to attack the User tank 
    def attack(self):
        Projectile(self.team, self.x, self.y, 0, 10, 7)

    #Function that updates the location of the target  
    def update(self):
        super().update()
        # Make target bounce off of their boundaries when they hit the boundaries so they dont leave the screen
        if self.x <= TARGET_RADIUS or self.x >= (SCREEN_SIZE[0] - TARGET_RADIUS):
            self.vx = -self.vx #Reversing the direction of the target
        if self.y <= TANK_SPACE or self.y >= (SCREEN_SIZE[1] - LOWER_BOUNDARY):
            self.vy = -self.vy #Reversing the direction of the target 

        if frameCounter % 90 == 0: # Shoots bombs every three seconds 
            self.attack()

    def destroy(self):
        super().destroy() #destroys the target 
        global score
        score+=1 #When the target gets destroyed user score is incremeanted by 1 

    def getCollisionRect(self): #Sets the area in which collison gets detected in
        return pg.Rect(self.x-self.radius,self.y-self.radius,self.radius*2, self.radius*2) 

#Making class Algorithm tank that is a child of both Class Tank and class Enemy
class AlgorithmTank(Tank, Enemy):
    def __init__(self, x, y):
        super().__init__(x,y)
    
    def draw(self): #Function to draw the target to the screen
        screen.blit(algorithmTankImage, (self.x - ALGORITHM_TANK_HALF_WIDTH, self.y - ALGORITHM_TANK_HALF_HEIGHT))#, TANK_HALF_WIDTH*2, TANK_HALF_HEIGHT*2))

    def shootAt(self, x, y, bulletSpeed):

        #Calculating the direction the projectile is in 
        dirX = x - self.x
        dirY = y - self.y

        #Taking squareroot of the sum of the squares of direction X and direction y
        magnitude = (dirX ** 2 + dirY ** 2) ** 0.5
        dirX = dirX / magnitude #Finds the x component
        dirY = dirY / magnitude #Finds the y component

        velocity_x = dirX * bulletSpeed #velocity in x direction = x component * speed
        velocity_y = dirY * bulletSpeed #velocity in y direction = y component * speed
        #Sends a bullet to the position calculated
        Bullet(self.team, self.x, self.y, velocity_x, velocity_y, 6, 2)

    
    def update(self): #moves to dodge projectiles from the user
        super().update()
        for object in gameObjects:
            if isinstance(object, Projectile) and (object.team == PLAYER_TEAM): #If statement to check for if the object is a projectile and from the users team(PLAYER_TEAM)
                if object.y < 300: #If statement to check if it is close enough to hit the algorithm tank
                    if object.x < self.x and object.x >= self.x - ALGORITHM_TANK_HALF_WIDTH - 12: #If statement to check if it is between the center and the left end of the tank
                        self.x += 15 #Dodges to the right by 15 
                    elif object.x >= self.x and object.x <= self.x + ALGORITHM_TANK_HALF_WIDTH + 12:#If statement to check if it is between the center and the right end of the tank
                        self.x -= 15 #Dodges to the left by 15
                break

        if frameCounter % 60 == 0: # Shoots every two seconds 
            self.shootAt(userTank.x, userTank.y, 20)
        pass

    def getCollisionRect(self):
        ignoreTopPixelCount = 20 # Variable to ignore the blank space from the front of the tank up to the tip of the gun
        #Sets the area in which collison gets detected in
        return pg.Rect(self.x-ALGORITHM_TANK_HALF_WIDTH, self.y-ALGORITHM_TANK_HALF_HEIGHT, ALGORITHM_TANK_HALF_WIDTH*2, ALGORITHM_TANK_HALF_HEIGHT*2-ignoreTopPixelCount)

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

    def destroy(self):
        super().destroy()
        global gameOver
        gameOver = True

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
            yPos = 10
            if self.y > SCREEN_SIZE[1]:
                yPos = SCREEN_SIZE[1] - 10
            screen.blit(smallExplosionImage, (self.x-25, yPos-25))
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
            pg.draw.circle(screen, USER_COLORS[value], (self.x,self.y+6), self.radius)
            pg.draw.circle(screen, RED, (self.x,self.y), self.radius)
   
class Bullet(Projectile):
  
      def draw(self):
        if self.object == 1:
            value = random.randint(0,4)
            pg.draw.circle(screen, COLORS[value], (self.x,self.y), self.radius)
        else:
            value = random.randint(0,1)
            pg.draw.circle(screen, ALGORITHMTANK_COLORS[value], (self.x,self.y+7), self.radius)
            pg.draw.circle(screen, WHITE, (self.x,self.y), self.radius)

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
    frameCounter = 30
    global score
    score = 0
    gameObjects.clear()
    global totalTargets
    totalTargets = generateTargets()
    AlgorithmTank(SCREEN_SIZE[0]/2, 70)
    global userTank
    userTank = UserTank(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]-70)
    global gameOver
    gameOver = False

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
              
    if gameOver:
        for gameObject in gameObjects.copy():
            gameObject.draw()
            game_over = (GAME_OVER_FONT.render("GAME OVER", True, WHITE, BLACK))
            text_rect = game_over.get_rect(center=(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2))
            screen.blit(game_over, text_rect)

            restart_text = (FONT.render("Press R to restart", True, WHITE, BLACK))
            restart_text_rect = restart_text.get_rect(center=(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2+75))
            screen.blit(restart_text, restart_text_rect)
        
    else:
        # python stores references to objects in lists. we make a copy of the list, which is fast since they are just addresses.
        # this is necessary so that when removing items from the list in update(), it doesn't mess up the order.
        for gameObject in gameObjects.copy():
            gameObject.update()
            gameObject.draw()

        if score == totalTargets:
            totalTargets = totalTargets + generateTargets()
    pg.display.flip()
    frameCounter+=1

pg.quit()
