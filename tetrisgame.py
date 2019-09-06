# A TETRIS CLONE UTILIZING PYGAME WRITTEN AS A FIRST 'SIMPLE' GAME PROJECT BY LUKE CHILDS (STARTED 9/5/2019)
#------------------------------------------------------------------------------------------------------------
#
# So far, a tetris block will auto-generate which you can move. It will then sit on the bottom of the screen, and then auto-generate
# a new block. You can move left or right with the arrow keys, and increase downward velocity with the down arrow.
# ESCAPE quits.
#
# TODO: Collision Detection, Active block Rotation, Line Clearing, Main Menu & Game Over screens
# Possible fun bonuses: Allow player to vary speed & block size, introduce color variation & matching for bonus points
# (there are some icky hard-coded bits of yuck in here - sorry! This is my first real Python project ever)

import pygame

blockSize = 32
defaultVelocityFactor = 0.2
leftRightMovementFactor = 0.3


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
        if(self.position.y >= 600):
            self.downwardVelocity = 0
        self.boundingRectangle = pygame.Rect(self.position.x, self.position.y, blockSize, blockSize)

class TetrisBlock:
    blocks = []

    def generateNewTetrisBlock(self):
        # Generate 4 random blocks into this new Tetris block in random Tetris block ordering
        counter = 1
        self.blocks = []
        while(counter <= 4):
            self.blocks.append(Block(250 + counter*blockSize,0, (0,255,0)))
            counter += 1
        return
    
    def __init__(self):
        self.generateNewTetrisBlock()
        self.downwardVelocity = 1


def main():
    pygame.init()
    pygame.display.set_caption("Tetris Demo")
    gameSurface = pygame.display.set_mode((640, 640))

    # TODO: Main Menu screen
    
    # Here's where we start the game - should be its own
    # function to easily restart the game
    blocksOnScreen = []
    activeTetrisBlock = 0
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
    
        # Draw and update bounding box placement for all on-screen blocks in their position
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
        if allBlocksStopped:
            newTetrisBlock = TetrisBlock()
            for blockInNewTetrisBlock in newTetrisBlock.blocks:
                blocksOnScreen.append(blockInNewTetrisBlock)
            velocityFactor = defaultVelocityFactor  
            
        # Do code on the active Tetris block here
        # (since the new Tetris block is appended, we know the last 4 blocksOnScreen will always refer to the active Tetris block!)
        activeTetrisBlockCounter = 0
        # Here's the loop for all operations on the active Tetris block
        while activeTetrisBlockCounter < 4:
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
                if blocksOnScreen[currentWallTestIteration].position.x >= 600:
                    activeBlockAgainstRightWall = True
                    break
            
            if activeBlockAgainstLeftWall == False:
                if pressed[pygame.K_LEFT]:
                    blocksOnScreen[currentIteration].moveLeftorRight(-leftRightMovementFactor)
            if activeBlockAgainstRightWall == False:
                if pressed[pygame.K_RIGHT]:
                    blocksOnScreen[currentIteration].moveLeftorRight(leftRightMovementFactor)  
            
            # TODO: Space bar rotates active block (somehow...lol)
            # TODO: Do collision tests (ie stop entire active Tetris block if one of its blocks collides with one other block) 
        
            # Game over if active block intersects with top of screen
            if blocksOnScreen[currentIteration].position.y <= -5:
                gameRunning = False
                break


        # ESCAPE quits
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameRunning = False
                # Handling downward keyboard movement here too (don't ask why)
                if event.type == pygame.KEYDOWN:
                    if(event.key ==  pygame.K_ESCAPE):
                        gameRunning = False
                    if(event.key == pygame.K_DOWN):
                        velocityFactor += defaultVelocityFactor
                        

        pygame.display.flip()
        pygame.display.update()
        gameSurface.fill((0,0,0))

    # TODO: Game over screen - music/graphics/keypress to quit, play again, etc.


# This is where the fun starts...
if __name__ == "__main__":
    main()
