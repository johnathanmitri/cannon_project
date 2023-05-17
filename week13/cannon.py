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

SCREEN_SIZE = (1280, 720)
LOWER_BOUNDARY = 150
TANK_SPACE = 150

TARGET_RADIUS = 50
targetImage = pg.transform.scale(targetImage, (TARGET_RADIUS*2, TARGET_RADIUS*2))
TANK_HALF_WIDTH = 25
TANK_HALF_HEIGHT = 50

ALGORITHM_TANK_HALF_WIDTH = 37.5
ALGORITHM_TANK_HALF_HEIGHT = 50

algorithmTankImage = pg.transform.scale(algorithmTankImage,(ALGORITHM_TANK_HALF_WIDTH*2, ALGORITHM_TANK_HALF_HEIGHT*2))
userTankImage = pg.transform.scale(userTankImage, (TANK_HALF_WIDTH*2, TANK_HALF_HEIGHT*2))
explosionImage = pg.transform.scale(explosionImage, (TANK_HALF_WIDTH*5, TANK_HALF_HEIGHT*5))
smallExplosionImage = pg.transform.scale(explosionImage, (50, 50))

screen = pg.display.set_mode((SCREEN_SIZE))
pg.display.set_caption("The gun of بغداد")

done = False
clock = pg.time.Clock()
frameCounter = 0
totalTargets = 0
gameObjects = []
bullets = []

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
        Projectile(self.team, self.x, self.y, 0, 10, 7)

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

    def getCollisionRect(self):
        return pg.Rect(self.x-self.radius,self.y-self.radius,self.radius*2, self.radius*2) 

class AlgorithmTank(Tank, Enemy):
    def __init__(self, x, y):
        super().__init__(x,y)
    
    def draw(self):
        screen.blit(algorithmTankImage, (self.x - ALGORITHM_TANK_HALF_WIDTH, self.y - ALGORITHM_TANK_HALF_HEIGHT))#, TANK_HALF_WIDTH*2, TANK_HALF_HEIGHT*2))
    
    #def moveTo(self,x):
     #   self.moveX = x

    def shootAt(self, x, y, bulletSpeed):

        #object_x = object.x
        #object_y = object.y

        #Calculating the direction the projectile is in 
        dirX = x - self.x
        dirY = y - self.y

        #Someone Check my Physics/Math here
        magnitude = (dirX ** 2 + dirY ** 2) ** 0.5
        dirX = dirX / magnitude
        dirY = dirY / magnitude

        velocity_x = dirX * bulletSpeed
        velocity_y = dirY * bulletSpeed
        Bullet(self.team, self.x, self.y, velocity_x, velocity_y, 6, 2)

    
    def update(self): #moves to dodge and shoots at projectiles(x,y)location
        #make the tank move to dodge the first projectile released and then to shoot at it
        #if no projectile is left then make it shoot at the user tank by taking in its position
        #then go back and check for newer projectiles again 
        
        super().update()
        for object in gameObjects:
            if isinstance(object, Projectile) and (object.team == PLAYER_TEAM):
                if object.y < 300:
                    if object.x < self.x and object.x >= self.x - ALGORITHM_TANK_HALF_WIDTH - 12:
                        self.x += 15
                    elif object.x >= self.x and object.x <= self.x + ALGORITHM_TANK_HALF_WIDTH + 12:
                        self.x -= 15
                break

        if frameCounter % 60 == 0: # shoot every three seconds for now
            self.shootAt(userTank.x, userTank.y, 20)
        pass

#def getCollisionRect(self):
    def getCollisionRect(self):
        # in order to ignore the blank space from the front of the tank up to the tip of the gun
        ignoreTopPixelCount = 20
        return pg.Rect(self.x-ALGORITHM_TANK_HALF_WIDTH, self.y-ALGORITHM_TANK_HALF_HEIGHT, ALGORITHM_TANK_HALF_WIDTH*2, ALGORITHM_TANK_HALF_HEIGHT*2-ignoreTopPixelCount)



    '''
    def draw(self):
        #*****cant use radius here because its not a circle 
        screen.blit(algorithmTankImage, (self.x-TANK_HALF_WIDTH, self.y-TANK_HALF_HEIGHT))
    def update(self):
        #if pg.time.get_ticks() % 3000 == 0: # shoot every three seconds for now
        pass
    def moveTo(self):
        #this function moves the tank to a location such that it has a direct shot at the projectile 
        return super().move()
    def attack(self):
        Projectile(self.team, self.x, self.y, 0, 10, 5)
'''
class UserTank(Tank): 
    def __init__(self, x, y):
        super().__init__(PLAYER_TEAM,x,y)
        self.lastTimeShot = 0 #this code initializes an instance of the UserTank class with specified coordinates (x and y)
            
    def update(self):
        keys=pg.key.get_pressed() #keyboard inputs and updates the tank's position based on the left and right arrow keys. It also allows the tank to shoot projectiles at a specified rate.

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

    def destroy(self): #ends the game if user gets destroyed 
        super().destroy()
        global gameOver
        gameOver = True

class Projectile(GameObject): #projectile class with methods for initialization, collision detection, updating the projectile's state, and drawing it on the screen.

    def __init__(self, team, x, y, vx, vy, radius, object = 1):
        super().__init__(team, x,y) #coordinates and velocities for teams and object type
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.object = object

    def getCollisionRect(self):
        return pg.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)
		#collision detection between instances of this class and other objects in a game
    def update(self):
        super().update() 
        # call parent update
        rect = self.getCollisionRect() 
        # calls collision rectangle
        if self.y > SCREEN_SIZE[1] or self.y < 0: 
            yPos = 10
            # If it is either greater than the screen height (SCREEN_SIZE[1]) or less than 0, the code inside this block is executed.
            if self.y > SCREEN_SIZE[1]:
                yPos = SCREEN_SIZE[1] - 10
            screen.blit(smallExplosionImage, (self.x-25, yPos-25))
            self.destroy()
        else: #a loop that iterates over gameObjects, which is likely a list of other game objects.
            for gameObject in gameObjects:
                if gameObject == self or gameObject.team == self.team:
                    continue
                #This condition checks if the current gameObject is the same instance as self or if they belong to the same team.

                if rect.colliderect(gameObject.getCollisionRect()):
                    screen.blit(explosionImage, (self.x-TANK_HALF_WIDTH*2, self.y-TANK_HALF_HEIGHT*2))
                    gameObject.destroy()
                    self.destroy()
					#If a collision is detected, it displays an explosion image, destroys the colliding game object (gameObject), and destroys the current instance itself.
    def draw(self): 
        #method is responsible for rendering the current instance on the screen
        if self.object == 1:
            value = random.randint(0,4)
            pg.draw.circle(screen, COLORS[value], (self.x,self.y), self.radius)
        else:
            value = random.randint(0,1)
            pg.draw.circle(screen, USER_COLORS[value], (self.x,self.y+6), self.radius)
            pg.draw.circle(screen, RED, (self.x,self.y), self.radius)
			#Depending on the object attribute of the instance, it either draws a single colored circle or a combination of two concentric circles.
class Bullet(Projectile):
	#class inherits from the Projectile class and overrides the draw
      def draw(self):
        if self.object == 1:
            value = random.randint(0,4)
            pg.draw.circle(screen, COLORS[value], (self.x,self.y), self.radius)
            #method to provide specific drawing behavior for bullets.
        else:
            value = random.randint(0,1)
            pg.draw.circle(screen, ALGORITHMTANK_COLORS[value], (self.x,self.y+7), self.radius)
            pg.draw.circle(screen, WHITE, (self.x,self.y), self.radius)
			#method randomly chooses colors based on conditions and draws circles on the screen accordingly.
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
    global score #variable for score 
    score = 0 #score set to 0
    gameObjects.clear()
    global totalTargets
    totalTargets = generateTargets()
    AlgorithmTank(SCREEN_SIZE[0]/2, 70) #lass and initializes it with the x-coordinate SCREEN_SIZE[0]/2 and y-coordinate 70
    global userTank
    userTank = UserTank(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]-70)
    global gameOver
    gameOver = False
	#function sets up initial variables and game objects, including the frame counter, score, target count, tanks, and game over status.
initializeGame()

while not done:
    clock.tick(30) #This line limits the frame rate to 30 frames per second. It ensures that the loop doesn't execute more frequently than the specified frame rate.
    screen.fill(BLACK) #fills the screen with a black color
    score_board = (FONT.render("Score: {}".format(score), True, WHITE))
    screen.blit(score_board, [10, 5])
    events = pg.event.get()
    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r: # restart is handled as KEYDOWN event so that it only runs once per click, instead of repeating as long as R is held. 
                initializeGame()
        if event.type == pg.QUIT:
                exit()
              #continuously processes events, updates the game state, and handles specific events such as key presses ('R' key) for game restart and quit events to exit the program
    if gameOver:
        for gameObject in gameObjects.copy():
            gameObject.draw()
            game_over = (GAME_OVER_FONT.render("GAME OVER", True, WHITE, BLACK))
            text_rect = game_over.get_rect(center=(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2))
            screen.blit(game_over, text_rect)
			#when the game is over, this code snippet iterates over the game objects, draws them on the screen, and displays the "GAME OVER"
            restart_text = (FONT.render("Press R to restart", True, WHITE, BLACK))
            restart_text_rect = restart_text.get_rect(center=(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2+75))
            screen.blit(restart_text, restart_text_rect)
			#renders and displays the "Press R to restart" message on the screen. It utilizes text surfaces and blitting to render the message with the specified color and position.
    else:
        # python stores references to objects in lists. we make a copy of the list, which is fast since they are just addresses.
        # this is necessary so that when removing items from the list in update(), it doesn't mess up the order.
        for gameObject in gameObjects.copy():
            gameObject.update()
            gameObject.draw()

        if score == totalTargets: #This condition checks if the current score is equal to the total number of targets.
            totalTargets = totalTargets + generateTargets()
            #This line increments the totalTargets variable by generating a new set of targets using the generateTargets() function
    pg.display.flip()
    frameCounter+=1
	#if the score matches the total number of targets, and if so, generates additional targets. 
pg.quit()
