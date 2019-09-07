# A TETRIS CLONE UTILIZING PYGAME WRITTEN AS A FIRST 'SIMPLE' GAME PROJECT BY LUKE CHILDS (STARTED 9/5/2019)
#------------------------------------------------------------------------------------------------------------
#
# Left/Right arrows to move block. Down arrows to 'drop' block. Space bar to rotate block.
#
# ESCAPE quits.
# Movement speed has now been synced via an in-game clock
#
# TODO: Line Clearing, bug-fixing
# Possible fun bonuses: Main Menu & Game Over screens, Allow player to vary speed & block size, introduce color variation & matching for bonus points
#                       adjust random block-generation algorithm to have a 'bag' of 7 to choose from, and re-generate when depleted

#  COPYRIGHT 2019 - Luke Childs

import pygame
import random

blockSize = 32
defaultVelocityFactor = 0.125
leftRightMovementFactor = blockSize

class Block:
    position = pygame.Vector2()
    downwardVelocity = 0
    blockColor = (255, 0, 0)
    boundingRectangle = pygame.Rect(position.x, position.y, blockSize, blockSize)
    
    def moveDown(self, velocityFactorIn):
        #self.downwardVelocity = velocityFactorIn
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
        self.position.y += self.downwardVelocity
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
            
            
        
        # 2 is this block:##
        #                 ##
        elif blockChoice == 2:
            counter = 1
            self.blocks = []
            while(counter <= 2):
                self.blocks.append(Block(250 + counter*blockSize,0, (255,0,0)))
                counter += 1
            counter = 1
            while(counter <= 2):
                self.blocks.append(Block(250 + counter*blockSize,blockSize, (255,0,0)))
                counter += 1
            
        
        # 3 is this block: #
        #                  ###                 
        elif blockChoice == 3:
            self.blocks = []
            counter = 1
            self.blocks.append(Block(250 + counter*blockSize,0, (255,255,0)))
            while(counter <= 3):
                self.blocks.append(Block(250 + counter*blockSize,blockSize, (255,255,0)))
                counter += 1
            
                
        # 4 is this block:    #
        #                   ###
        elif blockChoice == 4:
            self.blocks = []
            counter = 1
            self.blocks.append(Block(250 + blockSize*3,0, (255,0,0)))
            while(counter <= 3):
                self.blocks.append(Block(250 + counter*blockSize,blockSize, (255,0,0)))
                counter += 1
            
        
        # 5 is this block:  ##
        #                  ##
        elif blockChoice == 5:
            self.blocks = []
            counter = 2
            while counter <= 3:
                self.blocks.append(Block(250 + counter*blockSize,0, (0,255,255)))
                counter += 1
            counter = 1
            while counter <= 2:
                self.blocks.append(Block(250 + counter*blockSize,blockSize, (0,255,255)))
                counter += 1
            
        
        # 6 is thie block: #
        #                 ###
        elif blockChoice == 6:
            self.blocks = []
            self.blocks.append(Block(250 + 2*blockSize,0, (255,0,0)))
            counter = 1
            while counter <= 3:
                self.blocks.append(Block(250 + counter*blockSize,blockSize, (255,0,0)))
                counter += 1
            
        
        # 7 is this block: ##
        #                   ##
        elif blockChoice == 7:
            self.blocks = []
            counter = 1
            while counter <= 2:
                self.blocks.append(Block(250 + counter*blockSize,0, (255,0,255)))
                counter += 1
            counter = 2
            while counter <= 3:
                self.blocks.append(Block(250 + counter*blockSize,blockSize, (255,0,255)))
                counter += 1    
    
    def __init__(self, blockChoice = 1):
        self.generateNewTetrisBlock(blockChoice)
        self.downwardVelocity = 1

def generateNewTetrisBag():
    # This function feeds a new bag of all 7 Tetris blocks in a random number back into the program (ready for each time the randomnisation needs to be re-run)
    tetrisBag = []
    tetrisBagNumbers = []
    tetrisBlockNumbers = [1,2,3,4,5,6,7]
    
    # While loop creates random Tetris block ordering
    while not len(tetrisBlockNumbers) == 0:
        randomNumber = random.randint(0,len(tetrisBlockNumbers) - 1)
        tetrisBag.append(TetrisBlock(randomNumber))
        tetrisBlockNumbers.pop(randomNumber)
        tetrisBagNumbers.append(randomNumber)
    return tetrisBag

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
    blocksOnLine = 0
    
    spaceAlreadyPressed = False
    leftOrRightPressed = False
    downAlreadyPressed = False
    
    nextRandomBlock = TetrisBlock(nextRandomBlockNumber)
    nextRandomBlock.downwardVelocity = 0
    rotationActive = False
    
    score = 0
    gameRunning = True
    allBlocksStopped = True
    velocityFactor = defaultVelocityFactor
    gameFont = pygame.font.SysFont("Arial", 22)
    scoreTitleText = gameFont.render("SCORE", True, (255,255,255)) 
    scoreText = gameFont.render(str(score), True, (255,255,255))
    nextText = gameFont.render("NEXT", True, (255,255,255))

    # Play the now infamous in-game music!
    pygame.mixer.music.load("Tetris.mp3")
    pygame.mixer.music.play(-1)
    blockToDrawIterator = 0
    #testBlock = Block(300, 300, (255,255,0)) 
    #blocksOnScreen.append( Block(0,0,(0,0,0)) )

    while gameRunning:

        pressed = pygame.key.get_pressed()
        
        # UI rendering
        gameSurface.blit(scoreTitleText, (545, 500))
        scoreText = gameFont.render(str(score), True, (255,255,255))
        gameSurface.blit(scoreText, (570, 550))
        gameSurface.blit(nextText, (550, 150))
        
        pygame.draw.line(gameSurface, (255,255,255), (508, 0), (508,640), 2)
        pygame.draw.line(gameSurface, (255,255,255), (20, 0), (20,640), 2)
        
        # Game rendering
        # Draw the next random block to appear
        if(not nextRandomBlockNumber == 1):
            for blockToDraw in nextRandomBlock.blocks:
                pygame.draw.rect(gameSurface, blockToDraw.blockColor, pygame.Rect(blockToDraw.position.x + 250, blockToDraw.position.y + 50, blockSize, blockSize ))
                pygame.draw.rect(gameSurface, (255,255,255), pygame.Rect(blockToDraw.position.x + 250, blockToDraw.position.y + 50, blockSize, blockSize ), 2)
        else:
            for blockToDraw in nextRandomBlock.blocks:
                pygame.draw.rect(gameSurface, blockToDraw.blockColor, pygame.Rect(blockToDraw.position.x + 225, blockToDraw.position.y + 50, blockSize, blockSize ))
                pygame.draw.rect(gameSurface, (255,255,255), pygame.Rect(blockToDraw.position.x + 225, blockToDraw.position.y + 50, blockSize, blockSize ), 2) 
        
        # Draw and update bounding box placement for all on-screen blocks in play in their position
        for blockToDraw in blocksOnScreen:
            blockToDraw.updateBlock()
            pygame.draw.rect(gameSurface, blockToDraw.blockColor, blockToDraw.boundingRectangle)
            pygame.draw.rect(gameSurface, (255,255,255), blockToDraw.boundingRectangle, 2)
            
            # TODO: Clear line if 15 or more blocks are on it and move any lines above it down

            # Check if any blocks are still moving on-screen
            if blockToDraw.downwardVelocity == 0:
                allBlocksStopped = True
                
            else:
                allBlocksStopped = False
            
            blockToDrawIterator += 1
            if(blockToDrawIterator == len(blocksOnScreen)): blockToDrawIterator = 0                             
            
        # If we have no moving block on screen, we need to make a new, active, moving block for the player to control      
        if allBlocksStopped or len(blocksOnScreen) == 0:
            score += 10
            # See if we've gotten here via a hold event or block dropping - if block dropping, let's re-enable hold usage
            
            newTetrisBlock = TetrisBlock(nextRandomBlockNumber)
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
            
            # Stop if we've reached the bottom!
            if(blocksOnScreen[currentIteration].position.y >= 640 - blockSize):
                collisionApplyCounter = 1
                while collisionApplyCounter <= 4:
                        blocksOnScreen[len(blocksOnScreen) - collisionApplyCounter].downwardVelocity = 0
                        blocksOnScreen[len(blocksOnScreen) - collisionApplyCounter].position.y -= velocityFactor / 2.0
                        collisionApplyCounter += 1
                allBlocksStopped = True
            
            # Check for left or right movement (if block is not already against the wall!)
            activeBlockAgainstLeftWall = False
            activeBlockAgainstRightWall = False
            
            # Do rotation if we've pressed Space
            if rotationActive:
                pivotX = blocksOnScreen[len(blocksOnScreen) - 1].position.x
                pivotY = blocksOnScreen[len(blocksOnScreen) - 1].position.y
                
                blocksOnScreen[currentIteration].position = (blocksOnScreen[currentIteration].position - pygame.Vector2(pivotX, pivotY)).rotate(90)
                blocksOnScreen[currentIteration].position += pygame.Vector2(pivotX, pivotY)
            
            wallTestCounter = 0
            currentWallTestIteration = 0
            while(wallTestCounter < 4):
                wallTestCounter += 1
                currentWallTestIteration = len(blocksOnScreen) - wallTestCounter
                if blocksOnScreen[currentWallTestIteration].position.x <= blockSize:
                    activeBlockAgainstLeftWall = True

                if blocksOnScreen[currentWallTestIteration].position.x >= 500 - blockSize:
                   activeBlockAgainstRightWall = True

            # Do collision tests (ie stop entire active Tetris block if one of its blocks collides with one other block)
            collisionTestCounter = 0
            while(collisionTestCounter < len(blocksOnScreen) - 4):
                if blocksOnScreen[currentIteration].collisionTest(blocksOnScreen[collisionTestCounter]):
                    collisionApplyCounter = 1
                    while collisionApplyCounter <= 4:
                        blocksOnScreen[len(blocksOnScreen) - collisionApplyCounter].downwardVelocity = 0
                        blocksOnScreen[len(blocksOnScreen) - collisionApplyCounter].position.y -= velocityFactor / 2.0
                        collisionApplyCounter += 1
                    allBlocksStopped = True
                    break
                collisionTestCounter += 1
    
            # Game over if last block placed intersects with top of screen
            if blocksOnScreen[len(blocksOnScreen) - 5].position.y <= blockSize:
                gameRunning = False
                break

        # Handle keyboard down arrow (increase speed & 'drop' block)
        if pressed[pygame.K_DOWN] and velocityFactor < 2.5 and not downAlreadyPressed:
            velocityFactor = 2.5
            downAlreadyPressed = True       
        
        rotationActive = False
        # ESCAPE quits
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameRunning = False
                # Handling downward keyboard movement here too (don't ask why)
                if event.type == pygame.KEYDOWN:
                    if(event.key ==  pygame.K_ESCAPE):
                        gameRunning = False
                    
                    #Space bar rotates active Tetris block 90 degrees
                    if event.key == pygame.K_SPACE and not spaceAlreadyPressed:
                        spaceAlreadyPressed = True
                        rotationActive = True
                   
                    # Left/Right moves active block left/right 
                    if((event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT)) and not leftOrRightPressed:
                        leftOrRightPressed = True
                        
                    moveCounter = 1
                    if event.key == pygame.K_LEFT and not activeBlockAgainstLeftWall:
                        while moveCounter <= 4:
                            blocksOnScreen[len(blocksOnScreen) - moveCounter].moveLeftorRight(-leftRightMovementFactor)
                            moveCounter += 1
                    elif event.key == pygame.K_RIGHT and not activeBlockAgainstRightWall:
                        while moveCounter <= 4:
                            blocksOnScreen[len(blocksOnScreen) - moveCounter].moveLeftorRight(leftRightMovementFactor)
                            moveCounter += 1
                        
                                
                if event.type == pygame.KEYUP:
                    if(event.key == pygame.K_SPACE):
                        spaceAlreadyPressed = False
                    if event.key == pygame.K_DOWN:
                        downAlreadyPressed = False
                    if(event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT):
                        leftOrRightPressed = False
               
        pygame.display.flip()
        pygame.display.update()
        gameSurface.fill((0,0,0))
        gameClock.tick(360)

    # TODO: Game over screen - music/graphics/keypress to quit, play again, etc.


# This is where the fun starts...
if __name__ == "__main__":
    main()
