# python_programming_class
Python for programmers class
Group Members: Marc Cruz, Prerna Joshi, Johnathan Mitri, and Zack Wawi

The purpose of this assignment was to create a game and refactor the given file canon.py into a program with emphasis on modularization and object oriented programming. 
To run the game, you have to ensure you have downloaded pygame and have both files my_colors.py and cannon.py and then you run canon.py

How the game works: You keep shooting the targets and dodging until you die and your score is tracked. Everytime you kill all the targets that are on the screen, new targets respawn for you to shoot at and both tanks stay in the place where they were previously in. Note that the Algorithm tank is virtually impossible to kill because it is made to dodge whenever you shoot at it. Algorithm tank shoots once in every 2 seconds. 

Controls:
Left arrow key - Move left
Right arrow key - Move right
Space bar - Fire a bullet
R key - Restart game
The  x button at the top right corner of the game's window lets you close the game.

List of what we did:
1) Initially while deciding on how to proceed with the project we all collectively agreed that we would want to make it our own. So at that point we used the inital code given to us as a reference point and created our project from scratch. 
2) We planned out a general idea of how we wanted the game to look and how we wanted the game play to be.
3) We made it to be so that the user tank shoots staright upwards at targets and the targets drop bombs at certain time intervals. The user tank can move left or right to shoot at targets as required.
4) The targets are randomly generated and the number of targets is decided randomly (between 2-4 targets) that move in one particular direction atleast. So we made sure that we would have atleast 2 targets that move horizontally, vertically and diagonally each. The total number of targets can thus range anywhere between 6-12 targets.
5) We additionally added a moving algorithm tank to fulfill the requirements of having an algorithm based tank that shoots from the machines end. Our Algorithm tank not only shoots at the user tank and its projectiles but also dodges the projectiles that are fired from the user tank and moves as required.
6) Throughout the code we used polymorphism to make various classes that inherited according to their utility and type. Attached below you will find a UML Class Diagram Notation of the classes that you will see throughout our project. 

                        Class GameObject
                        /      |       \
                       /       |        \
                      /        |         \ 
                Class Tank     |      Class Projectile
                /  \      Class Enemy       \     
               /    \        /     \         \
              /      \      /       \       Class Bullet 
             /  Class AlgorithmTank  \
            /                         \
     Class UserTank               Class Target
    
    
7) And finally we have functions for initializing the game(initializeGame()) and generating targets(generateTargets()) as the 2 functions that are outside of these classes which are being called to run the game. 

Link to cannon.py:
