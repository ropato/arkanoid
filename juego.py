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
WIDTH = 1280 
HEIGHT = 720
SCORE = 0
#Tupla = Letra que identifica a cada power up y su imagen
POWER_LARGE = 'L',"resources/imgLarge.png"
POWER_FUERZA = "F","resources/imgFuerza.png"
POWER_SMALL = "S","resources/imgSmall.png"
POWER_SHOOT = "M","resources/imgMisille.png"

SCR = pygame.display.set_mode((WIDTH,HEIGHT)) #inicializo la pantalla

BRICK_AMOUNT = 100
BRICKS_DISTANCE =10 

COLLISION_TOLARANCE = 10

POWERU_UP_LIST= [POWER_FUERZA,POWER_LARGE,POWER_SMALL,POWER_SHOOT]

BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = ( 255, 0, 0)
BLUE = (0,0,255)
GRAY = (64,64,64)
PURPLE=(148,0,211)

BACKGROUND = pygame.image.load('resources/bg1.jpg').convert()


def createBricks(amount,powerUps): 
    posWidth = 20
    posHeight = 0   
    bricks = []
    #Genera los ladrillos
    for i in range(amount):
        brickType =rn.randrange(0,5)
        if posWidth + ld.BRICK_SIZE[0] + BRICKS_DISTANCE  > WIDTH:
            posWidth = 20
            posHeight += ld.BRICK_SIZE[1] + 20    
        if brickType == 0:
            redBrick = ld.normalBrick(RED,posWidth,posHeight, 1,1)
            brickGroup.add([redBrick])
            del redBrick
        elif brickType == 1:
            greenBrick = ld.normalBrick(GREEN,posWidth,posHeight, 2,2)
            brickGroup.add([greenBrick])
            del greenBrick
        elif brickType==2:
            num = rn.randrange(0,len(powerUps))
            violetBrick = ld.ladrillo_p(PURPLE,posWidth,posHeight, 1,2,POWERU_UP_LIST[num][0],POWERU_UP_LIST[num][1])
            brickGroup.add([violetBrick])
            del violetBrick
            del num
        elif brickType == 3:
            blueBrick = ld.normalBrick(BLUE,posWidth,posHeight, 3,3)
            brickGroup.add([blueBrick])
            del blueBrick
        elif brickType == 4:
            grayBrick = ld.fallingBrick(GRAY,posWidth,posHeight, 4,4)
            brickGroup.add([grayBrick])
            del grayBrick
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
    SCR.blit(text_surface, rect )
    
    pygame.display.flip()
    time.sleep(3)
    sys.exit()

def win():
    text_surface, rect = GAME_FONT.render("GANASTE", WHITE, size = 100)
    rect.centerx = WIDTH / 2
    rect.centery = HEIGHT / 2
    SCR.blit(text_surface, rect )
    
    pygame.display.flip()
    time.sleep(3)
    sys.exit()

def breakBrick(brk,proyectile):
    brk.setResistance(brk.getResistance()-1)
    #if brk.resistance <= proyectile.strengh: # 3 3
        #brk.resistance = 0
    if brk.resistance <= 0:
        brk.breakSound.play()
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

def addPowerUp(points,powerUpGroup,brick,SCR):
    if points > 0:
                SCR.blit(BACKGROUND, brick.rect, brick.rect)
                brickGroup.remove(brick)
                addScore(points)
                if isinstance(brick, ld.ladrillo_p):
                    powerUpGroup.add([powerup.powerUp(brick.rect.x, brick.rect.y, brick.powerUp,brick.imagenPU)])


def resistenceColor(brick,SCR):
    try:
        brick.resistanceColor()
        SCR.blit(BACKGROUND, brick.rect, brick.rect)
        SCR.blit(brick.image,brick.rect)
    except Exception as e:
            pass
    

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
            pygame.quit()
            sys.exit()
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
        ball.bounce.play()  
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
        
            resistenceColor(brick,SCR)

            addPowerUp(points,powerUpGroup,brick,SCR)

            #Verifica si el ladrillo es de la clase ladrillo flojo
            if isinstance(brick, ld.fallingBrick):
                SCR.blit(BACKGROUND, ball.rect, ball.rect)
                brick.falling = True
                SCR.blit(brick.image,brick.rect)

    #Ladrillo flojo. si se choco una vez, se cae. Si le pega al jugador le resta una vida.
    #Si el ladrillo se va por abajo del jugador sin pegarle se elimina
    for brick in brickGroup:
        if isinstance(brick, ld.fallingBrick) and brick.falling:
                SCR.blit(BACKGROUND, brick.rect, brick.rect)
                brick.fall()
                SCR.blit(brick.image,brick.rect)   
        if pygame.sprite.spritecollideany(brick, playerGroup):
            lives -= 1
            SCR.blit(BACKGROUND, brick.rect, brick.rect)
            brickGroup.remove(brick)
        if brick.rect.y > HEIGHT + 10:
            brickGroup.remove(brick)
            del brick


    if (shootPU or len(missileGroup)>0):
        try:        
            for m in missileGroup:    
                SCR.blit(BACKGROUND,m.rect,m.rect)
                m.lauch() 
                SCR.blit(m.image,m.rect)
                if m.rect.y < 0 - m.rect.height - 40:
                    missileGroup.remove(m)        
        except Exception as e:
           pass

    

    for m in  missileGroup:   
        crashedBrick = pygame.sprite.spritecollideany(m, brickGroup)
        if crashedBrick:  
                       
                points = breakBrick(crashedBrick,m)
                addPowerUp(points,powerUpGroup,crashedBrick,SCR)
                resistenceColor(crashedBrick,SCR)
                if points > 0:
                    brickGroup.remove(crashedBrick)    
                SCR.blit(BACKGROUND, crashedBrick.rect, crashedBrick.rect)
                missileGroup.remove(m)
                SCR.blit(BACKGROUND,m.rect,m.rect)
                del m


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
            elif powerUpColisioned[0].powerUp == POWER_SHOOT[0]:
                player.setShoot(5)
                shootPU = True
            SCR.blit(BACKGROUND, powerUpColisioned[0], powerUpColisioned[0])
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
        
        
    if lives == 0:
            gameOver()
    
    
    clock.tick(60)

pygame.quit()