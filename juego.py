import pygame
import jugador
import pelota as t
import ladrillo as ld
import pygame.freetype #Libreria que usamos para escribir en pantalla
import time #Sirve para determinar los FPS del juego
import sys #
import random as rn #generar numeros al azar
import powerup
#Info del juego y Pantalla
WIDTH = 1280 
HEIGHT = 720
SCORE = 0
#Tupla = Letra que identifica a cada power up y su imagen
POWER_LARGE = 'M',"resources/imgLarge.png"
POWER_FUERZA = "F","resources/imgFuerza.png"
POWER_SMALL = "S","resources/imgSmall.png"

SCR = pygame.display.set_mode((WIDTH,HEIGHT)) #inicializo la pantalla

BRICK_AMOUNT = 100
BRICKS_DISTANCE =10 

COLLISION_TOLARANCE = 10

POWERU_UP_LIST= [POWER_FUERZA,POWER_LARGE,POWER_SMALL]

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
        if posWidth + ld.BRICK_SIZE[0] + BRICKS_DISTANCE  > WIDTH:
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
            violetBrick = ld.ladrillo_p(PURPLE,posWidth,posHeight, 3,2,powerUps[num][0],powerUps[num][1])
            brickGroup.add([violetBrick])
            del violetBrick
            del num
        else:
            blueBrick = ld.Ladrillo(BLUE,posWidth,posHeight, 3,3)
            brickGroup.add([blueBrick])
            del blueBrick
        posWidth += ld.BRICK_SIZE[0] + BRICKS_DISTANCE
    return bricks

def addScore(pts):
    global SCORE
    SCORE += pts

def drawScore():
    text_surface, rect = GAME_FONT.render("Puntaje: " + str(SCORE), WHITE)
    rect.x = 0
    rect.y = HEIGHT / 1.15
    SCR.blit(BACKGROUND, rect, rect)
    SCR.blit(text_surface, rect)

def drawLives():
    text_surface, rect = GAME_FONT.render("Vidas: " + str(lives), WHITE)
    rect.x = 0
    rect.y = HEIGHT / 1.05
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
    rect.centerx = WIDTH / 2
    rect.centery = HEIGHT / 2
    SCR.blit(text_surface, rect, )
    
    pygame.display.flip()
    time.sleep(3)
    sys.exit()

def win():
    pass

def breakBrick(brk,proyectile):
    brk.resistance -= proyectile.strengh
    if brk.resistance <= proyectile.strengh: # 3 3
        brk.resistance = 0
    if brk.resistance <= 0:
        return brk.points
    else:
        return 0
def bounceV(brk, b):
    SCR.blit(BACKGROUND, b.rect, b.rect)
    b.invertVSpeed()
    b.move()
    SCR.blit(b.image, b.rect)
    SCR.blit(brk.image, brk.rect)
def bounceH(brk, b):
    SCR.blit(BACKGROUND, b.rect, b.rect)
    b.invertHSpeed()
    b.move()
    SCR.blit(b.image, b.rect)
    SCR.blit(brk.image, brk.rect)

pygame.init()
GAME_FONT = pygame.freetype.SysFont('roboto', 20, bold=False, italic=False)


#TODO:
    #Power Ups
    #Otros ladrillos <--ball
    #Mostrar Tiempo
    #Pantalla de inicio
    #Opcional Distintos niveles
    #Buscar pygame.draw.rect() parece que evite todo el problema de blit

SCR.blit(BACKGROUND, (0, 0))

brickGroup  = pygame.sprite.Group()
brickGroup.add( [createBricks(BRICK_AMOUNT,POWERU_UP_LIST)])
brickGroup.draw(SCR)

ballGroup = pygame.sprite.Group()
ball = t.Pelota(WIDTH /2,HEIGHT/2)
SCR.blit(BACKGROUND, ball.rect, ball.rect) 
ballGroup.add([ball])

playerGroup = pygame.sprite.Group()
player = jugador.Jugador((WIDTH /2),HEIGHT -50)
playerGroup.add([player])

powerUpGroup = pygame.sprite.Group()

clock = pygame.time.Clock()

lives = 3

waitingServe = True
playing = True


SCR.blit(player.image, player.rect)
#Bucle principal
while playing:

    #Eventos del juego
    for event in pygame.event.get():
        #Cierra el juego con la cruz
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            playing = False
        #Eventos de apretar una tecla
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE and waitingServe == True):
                waitingServe = False 

    joystick = pygame.key.get_pressed()
    if joystick[pygame.K_LEFT]:
        SCR.blit(BACKGROUND, player.rect, player.rect)
        player.moveLeft(0)
        SCR.blit(player.image, player.rect) 
    elif joystick[pygame.K_RIGHT]:
        SCR.blit(BACKGROUND, player.rect, player.rect)
        player.moveRight(WIDTH-10)
        SCR.blit(player.image, player.rect)
    if waitingServe == True:
        serve()
    else:
        SCR.blit(BACKGROUND, ball.rect, ball.rect) 
        ball.move()
        SCR.blit(ball.image, ball.rect) 
    #Choque con el jugador
    if pygame.sprite.spritecollideany(ball, playerGroup):
        SCR.blit(BACKGROUND, ball.rect, ball.rect)
        ball.invertVSpeed()
        ball.move()
        SCR.blit(ball.image, ball.rect)
        #porque aveces la pelota se come un pedazo de la paleta
        SCR.blit(BACKGROUND, player.rect, player.rect)
        SCR.blit(player.image, player.rect)
    if ball.rect.top <= 0 :
        ball.invertVSpeed()
    if ball.rect.left <= 0 or ball.rect.right >= WIDTH:
        ball.invertHSpeed()
    #Rebote de la pelota con los ladrillos 
    collisionedBricks = pygame.sprite.spritecollide(ball, brickGroup, False)
    if len(collisionedBricks) > 0:
        for brick in collisionedBricks:
            
            SCR.blit(brick.image, brick.rect)
            if ball.strengh > 1:
                ball.strengh-= brick.resistance
                points = breakBrick(brick,ball)    
                SCR.blit(BACKGROUND, brick.rect, brick.rect)
                if ball.strengh <= 0:
                    ball.strengh = 1
                SCR.blit(BACKGROUND, ball.rect, ball.rect)
                ball.move() 
                SCR.blit(ball.image, ball.rect)
            else:
                #si pelota fuerza == 1
                if abs(ball.rect.top - brick.rect.bottom) < COLLISION_TOLARANCE and ball.verticalSpeed < 0:
                    bounceV(brick, ball)
                    points = breakBrick(brick,ball)
                if abs(ball.rect.bottom - brick.rect.top) < COLLISION_TOLARANCE and ball.verticalSpeed > 0:
                    bounceV(brick, ball)
                    points = breakBrick(brick,ball)
                if abs(ball.rect.left - brick.rect.right) < COLLISION_TOLARANCE and ball.horizontalSpeed < 0:
                    bounceH(brick, ball)
                    points = breakBrick(brick,ball)
                if abs(ball.rect.right - brick.rect.left) < COLLISION_TOLARANCE and ball.horizontalSpeed > 0:
                    bounceH(brick, ball)
                    points = breakBrick(brick,ball)

            if points > 0:
                SCR.blit(BACKGROUND, brk.rect, brk.rect)
                brickGroup.remove(brk)
                addScore(points)
                if isinstance(brick, ld.ladrillo_p):
                    powerUpGroup.add([powerup.powerUp(brick.rect.x, brick.rect.y, brick.powerUp,brick.imagenPU)])

    if len(powerUpGroup) > 0:
        for power in powerUpGroup:
            SCR.blit(BACKGROUND, power.rect, power.rect)
            power.fallDown()    
            SCR.blit(power.image, power.rect)
            for brick in brickGroup:
                SCR.blit(brick.image,brick.rect)
    powerUpColisioned = pygame.sprite.spritecollide(player, powerUpGroup, True)

    if len(powerUpColisioned) > 0:
        for power in powerUpColisioned:
            SCR.blit(BACKGROUND, powerUpColisioned[0], powerUpColisioned[0])
            if powerUpColisioned[0].powerUp == POWER_LARGE[0]:
                SCR.blit(BACKGROUND, player.rect, player.rect)
                player.getBig()
                SCR.blit(player.image, player.rect)
            elif powerUpColisioned[0].powerUp == POWER_FUERZA[0]:
                ball.strengthUp()
            elif powerUpColisioned[0].powerUp == POWER_SMALL[0]:
                SCR.blit(BACKGROUND, player.rect, player.rect)
                player.getSmall()
                SCR.blit(player.image, player.rect)
            powerUpGroup.remove(power)

    drawScore()
    drawLives()
    
    #Actualiza la pantalla
    pygame.display.flip()

    #Actualiza la posicion de la pelota
    
    if len(brickGroup) == 0:
        win()
    
    #Si la pelota se cae por abajo el jugador pierde una vida. Si pierde todas las vidas pierde el juego.
    if ball.rect.top > HEIGHT + 20:
        if lives > 1:
            lives -=1
            waitingServe = True
            serve()
        else:
            gameOver()
    
    
    clock.tick(60)

pygame.quit()