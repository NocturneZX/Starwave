import random
import os, pygame, intro
from pygame.locals import *

random.seed()

def loadImage(name, colorKey = None):
	completeName = os.path.join('data',name) # Get a full name
	image = pygame.image.load(completeName) # load the image
	image = image.convert() # Convert the image for speed
	if colorKey != None: # colorkey (transparency) calculation
		if colorKey == -1:
			colorKey = image.get_at((0,0))
		image.set_colorkey(colorKey)
	return image, image.get_rect()

#Load sounds
def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname) 
    except pygame.error, message:
        print 'Cannot load sound:', ogg
        raise SystemExit, message
    return sound

def startGame(screenX, screenY, caption, background, cursorVisible):
	pygame.init()
	global screen
	global background_image
	screen = pygame.display.set_mode((screenX, screenY))
	pygame.display.set_caption(caption)
	background_image, background_rect = loadImage(background)
	screen.blit(background_image, (0,0))
	pygame.mouse.set_visible(False)

##	dx = 768
##	active = 1
##	while active == True:
##                background_rect.right -= dx
##                if background_rect.right < 768:
##                        background_rect.right = 1024

class gameObject(pygame.sprite.Sprite):
	def __init__(self, name, image, x, y, maxX, maxY, colorKey = -1, minX = 0, minY = 0):
		pygame.sprite.Sprite.__init__(self) # Make a sprite
		self.image, self.rect = loadImage(image, colorKey) # Load the image
		self.rect.centerx = x # Place it
		self.rect.centery = y
		self.maxX = maxX
		self.maxY = maxY
		self.minX = minX
		self.minY = minY
	def update(self, xMove, yMove, boundsCheck):
		self.rect.move_ip((xMove,yMove)) # Move things

		# bounds checking
		if boundsCheck:
			if self.rect.left < self.minX:
				self.rect.left = self.minX
			if self.rect.right > self.maxX:
				self.rect.right = self.maxX
			if self.rect.top <= self.minY:
				self.rect.top = self.minY
			if self.rect.bottom >= self.maxY:
				self.rect.bottom = self.maxY
				
class SpaceShip(gameObject):
    def __init__(self, x, y):
        gameObject.__init__(self,'starship', 'starship.jpeg', x, y, 1024, 768) 

class bguy(gameObject):
    def __init__(self):
        y = random.randint(160, 660)
        gameObject.__init__(self,'bguy', 'bguy.png', 1004, y, 1024, 768)

        #random 1 - 160 determines enemy fire
##        fire = random.randint(1, 160)
##        if fire == 1 or fire == 3:
##                
##                
class meteor(gameObject):
    def __init__(self):
        y = random.randint(160, 660)
        gameObject.__init__(self,'meteor', 'meteor.gif', 1004, y, 1024, 768)        
class laser(gameObject):
        def __init__(self, x, y):
                gameObject.__init__(self, 'lazer', 'redLaserRay.png', x, y, 300, 300, colorKey = 0)
                
class enemy_fire(gameObject):
        def __init__(self, x, y):
                gameObject.__init__(self, 'lazer', 'redLaserRay.png', x, y, 300, 300, colorKey = 0)   
class Label(pygame.sprite.Sprite):
    """ Label Class (simplest version) 
        Attributes:
            font: any pygame font object
            text: text to display
            center: desired position of label center (x, y)
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont('font/plakosmos.ttf', 30)
        self.text = ""
        self.center = (320, 240)
                
    def update(self):
        self.image = self.font.render(self.text, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = self.center


def main():
        # Game Startup
        startGame(1024, 768, 'Starwave LOL by Ryan Belisle and Julio Jose Reyes III'
          , 'background.jpg', False)

        #Load Intro Screen
        #intro.showTitle(screen,"STARWAVE LOL","Horde Mode")

        #control how held keys are repeated
        pygame.key.set_repeat(1,15)

        #HUD
        lblOutput = Label()
        lblOutput.center = (100, 50)
        lblOutput.text = "KM: 20000"
        
        lblOutput2 = Label()
        lblOutput2.center = (300, 50)
        lblOutput2.text = "Score: 0"

        lblOutput3 = Label()
        lblOutput3.center = (500, 50)
        lblOutput3.text = "Health: 4"

        
        
        allSprites = pygame.sprite.Group(lblOutput, lblOutput2, lblOutput3)

        #Initial Player Health and Status
        global health
        km = 20000
        score = 0
        health = 4
        if health == 0:
                intro.showTitle(screen,"GAME OVER",("Final Score: " + str(score)))
                pygame.quit()

        
        #load sounds        
        normal = load_sound("normal.ogg")
        critical = load_sound("critical.ogg")
        normal.play(-1)

        #load ship and enemy objects
        ship = SpaceShip(300,275)
        shipSprites = pygame.sprite.RenderClear(ship)
        bguySprites = pygame.sprite.RenderPlain()
        bguySprites.add(bguy())
        laserSprites = pygame.sprite.RenderPlain()
        efireSprites = pygame.sprite.RenderPlain()


        #Laser Reload time
        lazy_reload = 0

        #initialize player movement
        x_movement = 0
        y_movement = 0

        clock = pygame.time.Clock()
        keepGoing = True
        while keepGoing:
                
                
                #Load Level
                #Issue 2 - can't successfully execute this module ->
                #level.Level.load()
                clock.tick(30)

                #Clear sprites
                bguySprites.clear(screen, background_image)
                shipSprites.clear(screen, background_image)
                laserSprites.clear(screen, background_image)
                allSprites.clear(screen, background_image)

                #Decrease distance
                km = km - 1
                pygame.time.delay(45)
                km_left = "KM: " + str(km)
                lblOutput.text = km_left
                respawn = random.randint(1,10)

                #Determine the speed of the enemies
                enemy_speed = random.randint(3, 15)
                
                #key Presses
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        keepGoing = False
                        pygame.quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == K_DOWN:
                                y_movement = 7
                        elif event.key == K_UP:
                                y_movement = -7
                        elif event.key == K_LEFT:
                                x_movement = -7
                        elif event.key == K_RIGHT:
                                x_movement = 7
                        elif event.key == pygame.K_SPACE:
                                if lazy_reload > 10:
                                        laserSprites.add(laser(ship.rect.x + 140, ship.rect.y + 75))
                                        lazy_reload = 0
                        elif event.key == K_p:
                                font = pygame.font.SysFont("Times", 24, bold=False, italic=False)
                                fontSurface = font.render("Paused. Press r to resume .", True, (0,0,0))
                                screen.blit(fontSurface, (0, 0))                
                    elif event.type == pygame.KEYUP:
                        if event.key == K_DOWN:
                                y_movement = 0
                        elif event.key == K_UP:
                                y_movement = 0
                        elif event.key == K_LEFT:
                                x_movement = 0
                        elif event.key == K_RIGHT:
                                x_movement = 0
                        if event.key == K_p:
                                paused = True
                                while paused:
                                        for event in pygame.event.get():
                                                if event.key == K_r:
                                                        paused = False
                                                        screen.blit(background_image, (0,0))
                                        pygame.time.delay(100)
                                        
                #auto respawn enemy
                if respawn == 1:
                        bguySprites.add(bguy())
                        
                #Update all sprites and HUD        
                shipSprites.update(x_movement, y_movement, False)
                shipSprites.draw(screen)
                laserSprites.update(10,0,False)
                laserSprites.draw(screen)
                efireSprites.update(-10,0,False)
                efireSprites.draw(screen)
                bguySprites.update(-enemy_speed, 0, False)
                bguySprites.draw(screen)
                allSprites.update()
                allSprites.draw(screen)

                #When laser hits badguys
                for hit in pygame.sprite.groupcollide(laserSprites, bguySprites, 0, 1):
                        score = score + 100
                        lblOutput2.text = "Score:" + str(score)
                        if respawn == 2:
                                pygame.time.delay(45)
                                bguySprites.add(bguy())
                                bguySprites.add(bguy())
                        if respawn == 3:
                                pygame.time.delay(45)
                                bguySprites.add(bguy())
                                bguySprites.add(bguy())
                                bguySprites.add(bguy())
                        enemy_speed = enemy_speed + 0.001
         
                        
                for sprite in laserSprites:
                        if sprite.rect.right < 0:
                                sprite.kill()
                                score = score - 100
                                lblOutput2.text = "Score:" + str(score)

                #When badguy ships hit player's ship        
                for hit in pygame.sprite.groupcollide(shipSprites,bguySprites, 0, 1):
                        health = health - 1
                        lblOutput3.text = "Health: " + str(health)
                        #Uses sound as an indicator for health 
                        if health == 2:
                                normal.stop()
                                critical.play(-1)
                        elif health == 0:
                                critical.stop()
                                intro.showTitle(screen,"GAMEOVER",("Final Score: " + str(score)))
                                pygame.quit()
                                
                                                
                pygame.display.flip()
                lazy_reload = lazy_reload + 1
        
if __name__ == "__main__":
    main()
