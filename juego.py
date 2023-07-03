import pygame
import jugador
import pelota as t
import ladrillo as ld
import pygame.freetype #Libreria que usamos para escribir en pantalla
import time #Sirve para determinar los FPS del juego
import sys #
import random as rn #generar numeros al azar
import powerup
import misil
#Info del juego y Pantalla
ANCHO = 1280 
ALTO = 720
SCORE = 0
#Tupla = Letra que identifica a cada power up y su imagen
POWER_LARGE = 'L',"resources/imgLarge.png"
POWER_FUERZA = "F","resources/imgFuerza.png"
POWER_SMALL = "S","resources/imgSmall.png"
POWER_SHOOT = "M","resources/imgMisille.png"

SCR = pygame.display.set_mode((ANCHO,ALTO)) #inicializo la pantalla

BRICK_AMOUNT = 100
SEPARACION_LADRILLOS =10 


POWERU_UP_LIST= [POWER_FUERZA,POWER_LARGE,POWER_SMALL,POWER_SHOOT]

BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = ( 255, 0, 0)
BLUE = (0,0,255)
PURPLE=(148,0,211)

BACKGROUND = pygame.image.load('resources/bg1.jpg').convert()


def createBricks(amount,powerUps): 
    posWidth = 20
    posHeight = 0   
    bricks = []
    #Genera los ladrillos
    for i in range(amount):
        brickType =rn.randrange(0,4)
        if posWidth + ld.BRICK_SIZE[0] + SEPARACION_LADRILLOS  > ANCHO:
            posWidth = 20
            posHeight += ld.BRICK_SIZE[1] + 20    
        if brickType == 1:
            redBrick = ld.Ladrillo(RED,posWidth,posHeight, 1,1)
            brickGroup.add([redBrick])
            del redBrick
        elif brickType == 2:
            greenBrick = ld.Ladrillo(GREEN,posWidth,posHeight, 2,2)
            brickGroup.add([greenBrick])
            del greenBrick
        elif brickType==3:
            num = rn.randrange(0,len(powerUps))
            violetBrick = ld.ladrillo_p(PURPLE,posWidth,posHeight, 1,2,POWERU_UP_LIST[num][0],POWERU_UP_LIST[num][1])
            brickGroup.add([violetBrick])
            del violetBrick
            del num
        else:
            blueBrick = ld.Ladrillo(BLUE,posWidth,posHeight, 3,3)
            brickGroup.add([blueBrick])
            del blueBrick
        posWidth += ld.BRICK_SIZE[0] + SEPARACION_LADRILLOS
    return bricks

def addScore(pts):
    global SCORE
    SCORE += pts


def drawScore():
    text_surface, rect = GAME_FONT.render("Puntaje: " + str(SCORE), WHITE)
    rect.x = 0
    rect.y = ALTO / 1.15
    SCR.blit(BACKGROUND, rect, rect)
    SCR.blit(text_surface, rect)

def drawLives():
    text_surface, rect = GAME_FONT.render("Vidas: " + str(lives), WHITE)
    rect.x = 0
    rect.y = ALTO / 1.05
    SCR.blit(BACKGROUND, rect, rect)
    SCR.blit(text_surface, rect, )

def serve():
    global ball
    global player
    SCR.blit(BACKGROUND, ball.rect, ball.rect) 
    ball.rect.midbottom = player.rect.midtop
    SCR.blit(ball.image, ball.rect) 

def gameOver():
    text_surface, rect = GAME_FONT.render("GAME OVER", WHITE, size = 100)
    rect.centerx = ANCHO / 2
    rect.centery = ALTO / 2
    SCR.blit(text_surface, rect, )
    
    pygame.display.flip()
    time.sleep(3)
    sys.exit()

def win():
    pass

def breakBrick(brick,proyectile):
    brick.resistance -= proyectile.strengh
    if brick.resistance <= proyectile.strengh: 
        brick.resistance = 0
    if brick.resistance <= 0:
        SCR.blit(BACKGROUND, brick.rect, brick.rect)
        brickGroup.remove(brick)
        return brick.points
    else:
        return 0

pygame.init()
GAME_FONT = pygame.freetype.SysFont('roboto', 20, bold=False, italic=False)


#TODO:
    #Power Ups
    #Otros ladrillos <--ball
    #Mostrar Tiempo
    #Pantalla de inicio
    #Opcional Distintos niveles

SCR.blit(BACKGROUND, (0, 0))

brickGroup  = pygame.sprite.Group()
brickGroup.add( [createBricks(BRICK_AMOUNT,POWERU_UP_LIST)])
brickGroup.draw(SCR)

ballGroup = pygame.sprite.Group()
ball = t.Pelota(ANCHO /2,ALTO/2)
SCR.blit(BACKGROUND, ball.rect, ball.rect) 
ballGroup.add([ball])

playerGroup = pygame.sprite.Group()
player = jugador.Jugador((ANCHO /2),ALTO -50)
playerGroup.add([player])


missileGroup = pygame.sprite.Group()

powerUpGroup = pygame.sprite.Group()

clock = pygame.time.Clock()

lives = 3
points = 0

waitingServe = True
playing = True
shootPU = False

SCR.blit(player.image, player.rect)
#Bucle principal
while playing:
    #Eventos del juego
    for event in pygame.event.get():
        #Cierra el juego con la cruz
        if event.type == pygame.QUIT:
            playing = False
        #Eventos de apretar una tecla
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE and waitingServe):
                waitingServe = False
            elif (event.key == pygame.K_SPACE and not waitingServe and shootPU):
                missile = misil.Misille(player.rect.centerx,player.rect.y)                
                missileGroup.add([missile])
                  
                player.setShoot(player.getShoot()-1)
                if player.getShoot() == 0:
                    shootPU = False

    if (shootPU or len(missileGroup)>0):
        try:        
            for m in missileGroup:    
                SCR.blit(BACKGROUND,m.rect,m.rect)
                m.lauch() 
                SCR.blit(m.image,m.rect)
                if m.rect.y < 0 - m.rect.height - 40:
                    missileGroup.remove(m)
            
            
                
                    
        except Exception as e:
           print(e)

    

    for m in  missileGroup:   
        crashedBrick = pygame.sprite.spritecollideany(m, brickGroup)
        if crashedBrick:
                points = breakBrick(crashedBrick,m)
                missileGroup.remove(m)
                SCR.blit(BACKGROUND,m.rect,m.rect)
                del m


    joystick = pygame.key.get_pressed()
    if joystick[pygame.K_LEFT]:
        SCR.blit(BACKGROUND, player.rect, player.rect)
        player.moveLeft(0)
        SCR.blit(player.image, player.rect) 
    elif joystick[pygame.K_RIGHT]:
        SCR.blit(BACKGROUND, player.rect, player.rect)
        player.moveRight(ANCHO-10)
        SCR.blit(player.image, player.rect)

    #Choque con el jugador
    if pygame.sprite.spritecollideany(ball, playerGroup):
        SCR.blit(BACKGROUND, ball.rect, ball.rect)
        ball.update(ANCHO,ALTO,True)
        SCR.blit(ball.image, ball.rect)
        #porque aveces la pelota se come un pedazo de la paleta
        SCR.blit(BACKGROUND, player.rect, player.rect)
        SCR.blit(player.image, player.rect)
    #Rebote de la pelota con los ladrillos o paredes.
    collisionedBricks = pygame.sprite.spritecollide(ball, brickGroup, False)
    if collisionedBricks:
        for brick in collisionedBricks:
            
            SCR.blit(brick.image, brick.rect)
            if ball.strengh > 1:
                ball.strengh-= brick.resistance
                points = breakBrick(brick,ball)    
                SCR.blit(BACKGROUND, brick.rect, brick.rect)
                if ball.strengh <= 0:
                    ball.strengh = 1
                SCR.blit(BACKGROUND, ball.rect, ball.rect)
                ball.update(ANCHO,ALTO) #this function moves ball
                SCR.blit(ball.image, ball.rect)
            else:
                points = breakBrick(brick,ball)
                
                #si pelota fuerza == 1
                if ball.rect.right <= brick.rect.left or ball.rect.left >= brick.rect.right:
                    SCR.blit(BACKGROUND, ball.rect, ball.rect)
                    ball.update(ANCHO,ALTO,False,True)
                    SCR.blit(ball.image, ball.rect)
                    SCR.blit(brick.image, brick.rect)

                elif brick.rect.left <= ball.rect.centerx and brick.rect.right  >= ball.rect.centerx:
                    SCR.blit(BACKGROUND, ball.rect, ball.rect)
                    ball.update(ANCHO,ALTO,True)
                    SCR.blit(ball.image, ball.rect)
                    SCR.blit(brick.image, brick.rect)
            
            
            if points > 0:
                SCR.blit(BACKGROUND, brick.rect, brick.rect)
                addScore(points)
                if isinstance(brick, ld.ladrillo_p):
                    powerUpGroup.add([powerup.powerUp(brick.rect.x, brick.rect.y, brick.powerUp,brick.imagenPU)])

    if powerUpGroup:
        for power in powerUpGroup:
            SCR.blit(BACKGROUND, power.rect, power.rect)
            power.fallDown()    
            SCR.blit(power.image, power.rect)
            for brick in brickGroup:
                SCR.blit(brick.image,brick.rect)
    powerUpColisioned = pygame.sprite.spritecollide(player, powerUpGroup, True)
    if powerUpColisioned:
        SCR.blit(BACKGROUND, powerUpColisioned[0], powerUpColisioned[0])
        if powerUpColisioned[0].powerUp == POWER_LARGE[0]:
            SCR.blit(BACKGROUND, player.rect, player.rect)
            player.getBig()
            SCR.blit(player.image, player.rect)
        elif powerUpColisioned[0].powerUp == POWER_FUERZA[0]:
            ball.masFuerza()
        elif powerUpColisioned[0].powerUp == POWER_SMALL[0]:
            SCR.blit(BACKGROUND, player.rect, player.rect)
            player.getSmall()
            SCR.blit(player.image, player.rect)
        elif powerUpColisioned[0].powerUp == POWER_SHOOT[0]:
            player.setShoot(5)
            shootPU = True

            

    drawScore()
    drawLives()
    

    #Actualiza la pantalla
    pygame.display.flip()

    #Actualiza la posicion de la pelota
    if waitingServe == True:
        serve()
    else:
        SCR.blit(BACKGROUND, ball.rect, ball.rect) 
        ball.update(ANCHO,ALTO)
        SCR.blit(ball.image, ball.rect) 
    if len(brickGroup) == 0:
        win()
    
    #Si la pelota se cae por abajo el jugador pierde una vida. Si pierde todas las vidas pierde el juego.
    if ball.rect.top > ALTO + 20:
        if lives > 1:
            lives -=1
            waitingServe = True
            serve()
        else:
            gameOver()
    
    
    clock.tick(60)

pygame.quit()