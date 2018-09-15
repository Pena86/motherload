import pygame
import random
from collections import Counter

'''
Graphics downloaded from:

https://devilsworkshop.itch.io/big-pixel-isometric-block-pack-free-2d-sprites
2D Pixel Art - Isometric Blocks - Free Sprites
Low_Poly_Pixel_2D_Blocks_Devils_Garage_v04.zip

https://bakudas.itch.io/generic-platformer-pack
Generic Platformer Pack
generic_platformer_pack__bakudas.rar

https://vitalzigns.itch.io/war-platformer-tileset
War Platformer Tileset
WarTileset_VitalZigns.zip

https://raventale.itch.io/daily-doodles-pixelart-asset-pack
Daily Doodles Pixel Art Asset Pack #1
32x32pixelart_assets01_png.zip
32x32pixelart_assets02_weapons_png.zip
'''

MAX_SPEED = 20 #player movement

WORLDWIDTH = 20

DRILLTIMER = 10 # frames

BACKGROUNDCOLOR = (30,10,2)

def generateLevel(width, height, startHeight = 0):
    #print (height, startHeight)
    level = []
    for h in range(startHeight, startHeight + height):
        row  = []
        tileconut = 500
        chanceTreasure = 0 if h > 50 else -1
        chanceHardRock = h/2-2
        chanceRock = h/2+10 + (chanceHardRock if chanceHardRock >= 0 else 0)
        chanceMineral = 50 + chanceRock
        chanceCave = 20 + chanceMineral
        for w in range(width):
            tile = random.randint(0, tileconut)
            if tile == chanceTreasure:
                row.append('T')
            elif tile < chanceHardRock:
                row.append('H')
            elif tile < chanceRock:
                row.append('R')
            elif tile < chanceMineral:
                row.append('M')
            elif tile < chanceCave:
                row.append(' ')
            else: # Just dirt
                row.append('.')
        level.append(row)
        #print (' '.join(row), chanceHardRock, chanceRock)
    return level

class Player(pygame.sprite.Sprite):
    def __init__(self, startPosition):
        super().__init__()
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 40
        self.image = pygame.Surface([width, height])
        self.image.fill((200,50,50))

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
        self.rect.center = startPosition

        # Set speed vector of player
        self.speedX = 0
        self.speedY = 0

    def update(self):
        self.keyEvent()
        #gravity

        if self.speedX < 0.1 and self.speedX > -0.1:
            self.speedX = 0
        else:
            self.speedX -= self.speedX / 10


        if self.speedY < 0.1 and self.speedY > -0.1:
            self.speedY = 0
        else:
            self.speedY -= self.speedY / 10

        self.rect.x += self.speedX
        self.rect.y += self.speedY

        #collision detection now in Game -class


    def keyEvent(self):# Not an event anymore, but...
        pygame.event.pump()
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.speedX += MAX_SPEED / 10

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.speedX -= MAX_SPEED / 10

        if (keys[pygame.K_UP] or keys[pygame.K_w]):
            self.speedY -= MAX_SPEED / 10
        else:
            self.speedY += MAX_SPEED / 10

        #if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
        #    self.speedY += MAX_SPEED / 10

    def getPosition(self):
        return (self.rect.center)

    def setPosition(self, pos):
        self.rect.center = pos

    def drill(self):
        if self.speedY == 0 and self.speedX == 0:
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
                self.drillTimerY -= 1
                if self.drillTimerY < 0:
                    return (0,1)

            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
                self.drillTimerX -= 1
                if self.drillTimerX < 0:
                    return (1,0)

            elif (keys[pygame.K_LEFT] or keys[pygame.K_a]):
                self.drillTimerX -= 1
                if self.drillTimerX < 0:
                    return (-1,0)

        else:
            self.drillTimerY = DRILLTIMER
            self.drillTimerX = DRILLTIMER

        #print (self.speedX, self.speedY, self.drillTimerY, self.drillTimerX)

class Game:
    def __init__(self, windowSize):
        self.windowSize = pygame.Rect((0,0), windowSize)
        self.gameRunning = True
        self.loadTiles()
        self.tileSurfaces = []
        self.worldRect = None

        self.level = [[' '] * WORLDWIDTH] *5 # 5 laers of 'air' on top
        self.level.extend([['.'] * WORLDWIDTH]) # solid layer of dirt
        self.extendWorld()
        '''
        # dewWorld:
        self.level = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' '],
                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' '],
                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' '],
                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' '],
                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' '],
                    ['M', 'R', ' ', '.', '.', ' ', ' ', '.', '.', ' ', 'R','M'],
                    ['M', 'R', '.', '.', ' ', ' ', ' ', ' ', ' ', '.', 'R','M'],
                    ['M', 'R', '.', '.', ' ', ' ', ' ', ' ', ' ', '.', 'R','M'],
                    ['M', 'R', '.', 'R', '.', '.', '.', 'R', '.', '.', 'R','M']]

        print ('\n\n')
        print (Counter([item for sublist in self.level for item in sublist]))

        for line in self.level:
            self.tileSurfaces.append(self.generateTileSurface(line))
        self.worldRect = pygame.Rect(0,0, self.tileSurfaces[0].get_width(), len(self.tileSurfaces) * self.tileSize)
        '''
        self.cameraOffset = pygame.Rect((0,0), windowSize)

        # Level start at center when player on top of groud
        self.player = Player((self.tileSurfaces[0].get_width()/2, 4*self.tileSize)) # Player centered on screen
        self.active_sprite_list = pygame.sprite.Group()
        self.active_sprite_list.add(self.player)
        #print (self.player.getPosition(), self.tileSurfaces[0].get_width())

    def getRunningState(self):
        return self.gameRunning

    def loadTiles(self):
        self.tileSize = 64
        image = pygame.image.load('WarTileset_VitalZigns/Tileset/warTileset_64x64.png').convert()
        image_width, image_height = image.get_size()
        self.rock = image.subsurface((5*self.tileSize, 0*self.tileSize,
                                self.tileSize, self.tileSize))
        self.hardRock = image.subsurface((0*self.tileSize, 1*self.tileSize,
                                self.tileSize, self.tileSize))
        self.dirt = image.subsurface((3*self.tileSize, 1*self.tileSize,
                                self.tileSize, self.tileSize))
        self.gem01 = self.dirt.copy()
        self.gem01.blit(
                pygame.transform.scale(
                    pygame.image.load('32x32pixelart_assets01_png/gem01orange.png'), (64,64)),
                (0,0))
        self.treasure01 = self.dirt.copy()
        self.treasure01.blit(
                pygame.transform.scale(
                    pygame.image.load('32x32pixelart_assets02_weapons_png/weapon01crystalsword.png'), (64,64)),
                (0,0))

    def generateTileSurface(self, line):
        surface = pygame.Surface((len(line)*self.tileSize, self.tileSize))
        surface.fill(BACKGROUNDCOLOR)
        for x in range(len(line)):
            if (line[x]) == 'R':
                surface.blit(self.rock, (x*self.tileSize,0))
            elif (line[x]) == 'H':
                surface.blit(self.hardRock, (x*self.tileSize,0))
            elif (line[x]) == '.':
                surface.blit(self.dirt, (x*self.tileSize,0))
            elif (line[x]) == 'M':
                surface.blit(self.gem01, (x*self.tileSize,0))
            elif (line[x]) == 'T':
                surface.blit(self.treasure01, (x*self.tileSize,0))
        # print (line, surface)
        return (surface)

    def extendWorld(self, lines = 20):
        self.level.extend(generateLevel(WORLDWIDTH, lines, len(self.level)))
        for line in range(len(self.tileSurfaces), len(self.level)):
            self.tileSurfaces.append(self.generateTileSurface(self.level[line]))
        self.worldRect = pygame.Rect(0,0, self.tileSurfaces[0].get_width(), len(self.tileSurfaces) * self.tileSize)

    def gameEvent(self, event):
        if event.type == pygame.QUIT:
            self.gameRunning = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.gameRunning = False

    def gameLoop(self):
        self.active_sprite_list.update()

        # collision detection
        if not self.worldRect.contains(self.player.rect):
            # Put player back inside the world
            if self.worldRect.left > self.player.rect.left:
                self.player.rect.left = self.worldRect.left
                self.player.speedX = 0
            elif self.worldRect.right < self.player.rect.right:
                self.player.rect.right = self.worldRect.right
                self.player.speedX = 0
            if self.worldRect.top > self.player.rect.top:
                self.player.rect.top = self.worldRect.top
                self.player.speedY = 0
            elif self.worldRect.bottom < self.player.rect.bottom:
                self.player.rect.bottom = self.worldRect.bottom
                self.player.speedY = 0

        playerCenterOnTile = (int(self.player.rect.centery / self.tileSize), int(self.player.rect.centerx / self.tileSize))

        self.playerCollidesRects = []
        for mutation in [(1,0),(-1,0),(0,1),(0,-1)]:
            tile = (playerCenterOnTile[0] + mutation[0], playerCenterOnTile[1] + mutation[1])
            try:
                if self.level[tile[0]][tile[1]] != ' ':
                    self.playerCollidesRects.append(
                            pygame.Rect(
                            tile[1]*self.tileSize,
                            tile[0]*self.tileSize,
                            self.tileSize,self.tileSize
                            ))
            except:
                pass

        # tile on top
        try:
            if self.level[playerCenterOnTile[0]-1][playerCenterOnTile[1]] != ' ' and \
                    self.player.rect.top < (playerCenterOnTile[0])*self.tileSize:
                #print ('topCollision')
                self.player.rect.top = (playerCenterOnTile[0])*self.tileSize
                self.player.speedY = 0
        except:
            pass

        # tile on bottom
        try:
            if self.level[playerCenterOnTile[0]+1][playerCenterOnTile[1]] != ' ' and \
                    self.player.rect.bottom > (playerCenterOnTile[0]+1)*self.tileSize:
                #print ('bottomCollision')
                self.player.rect.bottom = (playerCenterOnTile[0]+1)*self.tileSize
                self.player.speedY = 0
        except:
            pass

        # tile on left
        try:
            if self.level[playerCenterOnTile[0]][playerCenterOnTile[1]-1] != ' ' and \
                    self.player.rect.left < (playerCenterOnTile[1])*self.tileSize:
                #print ('leftCollision')
                self.player.rect.left = (playerCenterOnTile[1])*self.tileSize
                self.player.speedX = 0
        except:
            pass

        # tile on right
        try:
            if self.level[playerCenterOnTile[0]][playerCenterOnTile[1]+1] != ' ' and \
                    self.player.rect.right > (playerCenterOnTile[1]+1)*self.tileSize:
                #print ('rightCollision')
                self.player.rect.right = (playerCenterOnTile[1]+1)*self.tileSize
                self.player.speedX = 0
        except:
            pass

        '''
        playerCollideMap = [False, False, False, False]
        playerCollideCorners = [self.player.rect.topleft, self.player.rect.topright, self.player.rect.bottomleft, self.player.rect.bottomright]
        for i in range(len(playerCollideMap)):
            for rect in self.playerCollidesRects:
                if rect.collidepoint(playerCollideCorners[i]):
                    playerCollideMap[i] = True
                    break
        if self.playerCollidesRects:
            if abs(self.player.rect.centery - self.playerCollidesRects[0].centery) > \
                abs(self.player.rect.centerx - self.playerCollidesRects[0].centerx):
                if self.player.speedY < 0:
                    #print ('topCollision')
                    self.player.rect.top = self.playerCollidesRects[0].bottom
                    self.player.speedY = 0
                else:
                    #print ('bototmCollision')
                    self.player.rect.bottom = self.playerCollidesRects[0].top -1
                    self.player.speedY = 0
            else:
                if self.player.speedX < 0:
                    #print ('leftCollision')
                    self.player.rect.left = self.playerCollidesRects[0].right
                    self.player.speedX = 0
                else:
                    #print ('rightCollision')
                    self.player.rect.right = self.playerCollidesRects[0].left -1
                    self.player.speedX = 0
        '''
        '''
        elif self.playerCollidesRects:
            if playerCollideMap[0] and playerCollideMap[1]:
                #print ('topCollision')
                self.player.rect.top = self.playerCollidesRects[0].bottom
                self.player.speedY = 0
            elif playerCollideMap[2] and playerCollideMap[3]:
                #print ('bototmCollision')
                self.player.rect.bottom = self.playerCollidesRects[0].top
                self.player.speedY = 0
            elif playerCollideMap[0] and playerCollideMap[2]:
                #print ('leftCollision')
                self.player.rect.left = self.playerCollidesRects[0].right
                self.player.speedX = 0
            elif playerCollideMap[1] and playerCollideMap[3]:
                #print ('rightCollision')
                self.player.rect.right = self.playerCollidesRects[0].left
                self.player.speedX = 0
        '''

        self.cameraOffset = (-self.player.rect.centerx + self.windowSize.width/2, -self.player.rect.top + self.windowSize.height/2)
        #print (self.player.getPosition(), self.player.rect.x, self.cameraOffset, playerCenterOnTile, self.playerCollidesRects)

        direction = self.player.drill()
        if direction:
            # try to drill direction of tuple
            try:
                tilePos = (playerCenterOnTile[0]+direction[1], playerCenterOnTile[1]+direction[0])
                tile = self.level[tilePos[0]][tilePos[1]]
                #print (direction)
                if tile == '.' or tile == 'M' or tile == 'T':
                    #print ('dirt drill', tile)
                    self.level[tilePos[0]][tilePos[1]] = ' '
                    self.tileSurfaces[tilePos[0]] = self.generateTileSurface(self.level[tilePos[0]])
            except:
                pass

        if playerCenterOnTile[0] + 10 > len(self.level):
            self.extendWorld()

    def draw(self, screen):
        screen.fill(BACKGROUNDCOLOR)

        # relative draw
        # screen.blit(self.tileSurfaces[0], (0,0))
        for y in range(len(self.tileSurfaces)):
            screen.blit(self.tileSurfaces[y],
                    (self.cameraOffset[0],
                    self.cameraOffset[1] + y*self.tileSize))

        #self.active_sprite_list.draw(screen)
        # Player
        #screen.blit(self.player.image, self.windowSize.center)
        screen.blit(self.player.image, (
                self.cameraOffset[0] + self.player.rect.x,
                self.cameraOffset[1] + self.player.rect.y))
        #/ relative draw

        '''
        # Absolute draw for debuggin
        for y in range(len(self.tileSurfaces)):
            screen.blit(self.tileSurfaces[y],
                    (0,
                    y*self.tileSize))

        for tile in self.playerCollidesRects: # Colision testing
            pygame.draw.rect(screen, (50,50,200), tile)

        self.active_sprite_list.draw(screen)
        #/ Absolute draw
        '''


if __name__ == "__main__" :
    print ('run: python main.py')
    #level = generateLevel(20, 100)
    #print ('\n\n')
    '''
    for r in level:
        for i in r:
            print ("{} ".format(i) ,end='')
        print ('')
    '''
    #print (Counter([item for sublist in level for item in sublist]))
