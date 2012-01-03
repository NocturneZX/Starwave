import os, pygame

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

def showTitle(screen, text,text2, size = None, pos = None):
    if size != None:
        bigfont = pygame.font.Font("font/plakosmos.ttf", size)
    else:
        bigfont = pygame.font.Font("font/plakosmos.ttf", 50)
    
    smallfont = pygame.font.Font("font/plakosmos.ttf", 15)
    
    bg = pygame.image.load("data/wallpaper.jpg")
    
    bigtext = bigfont.render(text, True, (255, 255, 255))
    bigtextS = bigfont.render(text2, True, (255,255,255))
    
    littletext = smallfont.render("Click anywhere to continue", True, (255, 255, 255))
    
    ypos = screen.get_height()/2
    
    if pos != None:
        if pos == "centre":
            xpos = screen.get_width()/2 - bigtext.get_width()/2
        elif pos == "left":
            xpos = 20
        elif pos == "right":
            xpos = screen.get_width()-bigtext.get_width()-20
        else:
            xpos = screen.get_width()/2 - bigtext.get_width()/2
    else:
        xpos = screen.get_width()/2 - bigtext.get_width()/2
    
        running = 1

        menu = load_sound("menu.ogg")

        screen.blit(bg, (0, 0))
        screen.blit(bigtext, (xpos, ypos))
        screen.blit(bigtextS, ((xpos),(ypos+50)))
        screen.blit(littletext, (screen.get_width()/2 - littletext.get_width()/2, screen.get_height() - 50))
        pygame.display.update()
    while running:
                menu.play()                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
                    if pygame.mouse.get_pressed()[0]:
                        running = False
                        pygame.time.delay(1000)
