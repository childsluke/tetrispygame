# A TETRIS CLONE UTILIZING PYGAME WRITTEN AS A FIRST 'SIMPLE' GAME PROJECT BY LUKE CHILDS (STARTED 9/5/2019)
#------------------------------------------------------------------------------------------------------------
#
# So far, a random tetris block will auto-generate which you can move. It will then move toward the bottom of the screen, and auto-generate
# a new block when it reaches the bottom. You can move left or right with the arrow keys, and increase downward velocity with the down arrow.
# ESCAPE quits.
# Movement speed has now been synced via an in-game clock
#
# TODO: Tetris 'bag' randomnisation algorithm, Collision Detection with other blocks, Active block Rotation, Line Clearing
# Possible fun bonuses: Main Menu & Game Over screens, Allow player to vary speed & block size, introduce color variation & matching for bonus points

#  COPYRIGHT 2019 - Luke Childs

import pygame
import random

blockSize = 32
defaultVelocityFactor = 0.25
leftRightMovementFactor = 1.0


class Block:
    position = pygame.Vector2()
    downwardVelocity = 0
    blockColor = (255, 0, 0)
    boundingRectangle = pygame.Rect(position.x, position.y, blockSize, blockSize)
    
    def moveDown(self, velocityFactorIn):
        self.downwardVelocity = velocityFactorIn
        self.position.y += velocityFactorIn
        
    def moveLeftorRight(self, amount):
            self.position.x += amount
    
    def __init__(self, startX, startY, *startColor):
        self.position = pygame.Vector2(startX, startY)
        self.blockColor = startColor
        self.downwardVelocity = defaultVelocityFactor

    def collisionTest(self, incomingBlock):
        return self.boundingRectangle.colliderect(incomingBlock.boundingRectangle)

    def updateBlock(self):
        if(self.position.y >= 640 - blockSize):
            self.downwardVelocity = 0
            self.position.y = 640 - blockSize
        self.boundingRectangle = pygame.Rect(self.position.x, self.position.y, blockSize, blockSize)

class TetrisBlock:
    blocks = []

    def generateNewTetrisBlock(self, blockChoice):
        # Gives us the chosen Tetris block variant (1 of 7)
        
        # 1 is this block: ####
        if blockChoice == 1:
            counter = 1
            self.blocks = []
            while(counter <= 4):
                self.blocks.append(Block(250 + counter*blockSize,0, (0,255,0)))
                counter += 1
            return
            
        
        # 2 is this block:##
        #                 ##
        if blockChoice == 2:
            counter = 1
            self.blocks = []
            while(counter <= 2):
                self.blocks.append(Block(250 + counter*blockSize,0, (255,0,0)))
                counter += 1
            counter = 1
            while(counter <= 2):
                self.blocks.append(Block(250 + counter*blockSize,blockSize, (255,0,0)))
                counter += 1
            return
        
        # 3 is this block: #
        #                  ###                 
        if blockChoice == 3:
            self.blocks = []
            counter = 1
            self.blocks.append(Block(250 + counter*blockSize,0, (255,255,0)))
            while(counter <= 3):
                self.blocks.append(Block(250 + counter*blockSize,blockSize, (255,255,0)))
                counter += 1
            return
                
        # 4 is this block:    #
        #                   ###
        if blockChoice == 4:
            self.blocks = []
            counter = 1
            self.blocks.append(Block(250 + blockSize*3,0, (255,0,0)))
            while(counter <= 3):
                self.blocks.append(Block(250 + counter*blockSize,blockSize, (255,0,0)))
                counter += 1
            return
        
        # 5 is this block:  ##
        #                  ##
        if blockChoice == 5:
            self.blocks = []
            counter = 2
            while counter <= 3:
                self.blocks.append(Block(250 + counter*blockSize,0, (0,255,255)))
                counter += 1
            counter = 1
            while counter <= 2:
                self.blocks.append(Block(250 + counter*blockSize,blockSize, (0,255,255)))
                counter += 1
            return
        
        # 6 is thie block: #
        #                 ###
        if blockChoice == 6:
            self.blocks = []
            self.blocks.append(Block(250 + 2*blockSize,0, (255,0,0)))
            counter = 1
            while counter <= 3:
                self.blocks.append(Block(250 + counter*blockSize,blockSize, (255,0,0)))
                counter += 1
            return
        
        # 7 is this block: ##
        #                   ##
        if blockChoice == 7:
            self.blocks = []
            counter = 1
            while counter <= 2:
                self.blocks.append(Block(250 + counter*blockSize,0, (255,0,255)))
                counter += 1
            counter = 2
            while counter <= 3:
                self.blocks.append(Block(250 + counter*blockSize,blockSize, (255,0,255)))
                counter += 1
            return

            

    
    def __init__(self, blockChoice = 1):
        self.generateNewTetrisBlock(blockChoice)
        self.downwardVelocity = 1

def main():
    
    pygame.init()
    pygame.display.set_caption("Tetris Demo")
    gameSurface = pygame.display.set_mode((640, 640))
    gameClock = pygame.time.Clock()
    # TODO: Main Menu screen
    
    # Here's where we start the game - should be its own
    # function to easily restart the game
    blocksOnScreen = []
    activeTetrisBlock = 0
    nextRandomBlockNumber = random.randint(1,7)
    currentRandomBlockNumber = nextRandomBlockNumber
    
    nextRandomBlock = TetrisBlock(nextRandomBlockNumber)
    nextRandomBlock.downwardVelocity = 0
    
    score = 0
    gameRunning = True
    allBlocksStopped = True
    velocityFactor = defaultVelocityFactor

    # Play the now infamous in-game music!
    pygame.mixer.music.load("Tetris.mp3")
    pygame.mixer.music.play(-1)

    #testBlock = Block(300, 300, (255,255,0)) 
    #blocksOnScreen.append( Block(0,0,(0,0,0)) )  

    while gameRunning:
    
        pressed = pygame.key.get_pressed()
        
        # Draw the next random block to appear
        for blockToDraw in nextRandomBlock.blocks:
            pygame.draw.rect(gameSurface, blockToDraw.blockColor, pygame.Rect(blockToDraw.position.x + 225, blockToDraw.position.y + 50, blockSize, blockSize ))
            pygame.draw.rect(gameSurface, (255,255,255), pygame.Rect(blockToDraw.position.x + 225, blockToDraw.position.y + 50, blockSize, blockSize ), 2)
           
        # Draw and update bounding box placement for all on-screen blocks in play in their position
        for blockToDraw in blocksOnScreen:
            blockToDraw.updateBlock()
            pygame.draw.rect(gameSurface, blockToDraw.blockColor, blockToDraw.boundingRectangle)
            pygame.draw.rect(gameSurface, (255,255,255), blockToDraw.boundingRectangle, 2)

            # Check if any blocks are still moving on-screen
            if blockToDraw.downwardVelocity == 0:
                allBlocksStopped = True
                
            else:
                allBlocksStopped = False                             
            
            # TODO: Clear line(s) if full & update score
            
        # If we have no moving block on screen, we need to make a new, active, moving block for the player to control      
        if allBlocksStopped or len(blocksOnScreen) == 0:
            
            # See if we've gotten here via a hold event or block dropping - if block dropping, let's re-enable hold usage
            
            newTetrisBlock = TetrisBlock(nextRandomBlockNumber)
            currentRandomBlockNumber = nextRandomBlockNumber
            
            nextRandomBlockNumber = random.randint(1,7)
            
            nextRandomBlock = TetrisBlock(nextRandomBlockNumber)
            nextRandomBlock.downwardVelocity = 0    
            justUsedHoldBlock = False
            
            for blockInNewTetrisBlock in newTetrisBlock.blocks:
                blocksOnScreen.append(blockInNewTetrisBlock)
            velocityFactor = defaultVelocityFactor 
            
        # Do code on the active Tetris block here
        # (since the new Tetris block is appended, we know the last 4 blocksOnScreen will always refer to the active Tetris block!)
        activeTetrisBlockCounter = 0
        # Here's the loop for all operations on the active Tetris block
        while activeTetrisBlockCounter < 4 and len(blocksOnScreen) > 0:
            activeTetrisBlockCounter += 1
            currentIteration = len(blocksOnScreen) - activeTetrisBlockCounter
            
            # Move the active block down the screen
            blocksOnScreen[currentIteration].moveDown(velocityFactor)
            
            # Check for left or right movement (if block is not already against the wall!)
            activeBlockAgainstLeftWall = False
            activeBlockAgainstRightWall = False
            
            wallTestCounter = 0
            currentWallTestIteration = 0
            while(wallTestCounter < 4):
                wallTestCounter += 1
                currentWallTestIteration = len(blocksOnScreen) - wallTestCounter
                if blocksOnScreen[currentWallTestIteration].position.x <= 0:
                    activeBlockAgainstLeftWall = True
                    break
                if blocksOnScreen[currentWallTestIteration].position.x >= 640 - blockSize:
                   activeBlockAgainstRightWall = True
                     

            if pressed[pygame.K_LEFT] and activeBlockAgainstLeftWall == False:
                    blocksOnScreen[currentIteration].moveLeftorRight(-leftRightMovementFactor)
            if pressed[pygame.K_RIGHT] and activeBlockAgainstRightWall == False:
                    blocksOnScreen[currentIteration].moveLeftorRight(leftRightMovementFactor)
         
            # TODO: Space bar rotates active block (somehow...lol)
            # TODO: Do collision tests (ie stop entire active Tetris block if one of its blocks collides with one other block) 
    
            # Game over if active block intersects with top of screen
            if blocksOnScreen[currentIteration].position.y <= -5:
                gameRunning = False
                break

        # Handle keyboard down arrow (increase speed & 'drop' block)
        if pressed[pygame.K_DOWN] and velocityFactor < 2.5:
            velocityFactor += defaultVelocityFactor
            if(velocityFactor > 2.5):
                velocityFactor = 2.5
                
        # ESCAPE quits
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameRunning = False
                # Handling downward keyboard movement here too (don't ask why)
                if event.type == pygame.KEYDOWN:
                    if(event.key ==  pygame.K_ESCAPE):
                        gameRunning = False
                        
        pygame.display.flip()
        pygame.display.update()
        gameSurface.fill((0,0,0))
        gameClock.tick(360)

    # TODO: Game over screen - music/graphics/keypress to quit, play again, etc.


# This is where the fun starts...
if __name__ == "__main__":
    main()
