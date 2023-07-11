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
import flechitaSAque

#Info del juego y Pantalla #probando
WIDTH = 1280 
HEIGHT = 720
SCORE = 0
#Tupla = Letra que identifica a cada power up y su imagen
POWER_LARGE = 'L',"resources/imgLarge.png"
POWER_FUERZA = "F","resources/imgFuerza.png"
POWER_SMALL = "S","resources/imgSmall.png"
POWER_SHOOT = "M","resources/imgMissile.png"
POWER_MULTIBALL = "B","resources/imgPelotas.png"

SCR = pygame.display.set_mode((WIDTH,HEIGHT)) #inicializo la pantalla

BRICK_AMOUNT = 100
BRICKS_DISTANCE =10 

COLLISION_TOLARANCE = 10

POWERU_UP_LIST= [POWER_FUERZA,POWER_LARGE,POWER_SMALL,POWER_SHOOT,POWER_MULTIBALL]

BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = ( 255, 0, 0)
BLUE = (0,0,255)
GRAY = (64,64,64)
PURPLE=(148,0,211)

BACKGROUND = pygame.image.load('resources/bg1.jpg').convert()

#crea los ladrillos.
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
            redBrick = ld.normalBrick("resources/ladrilloRojo.png",posWidth,posHeight, 1,1)
            brickGroup.add([redBrick])
            del redBrick
        elif brickType == 1:
            greenBrick = ld.normalBrick("resources/ladrilloVerde.png",posWidth,posHeight, 2,2)
            brickGroup.add([greenBrick])
            del greenBrick
        elif brickType==2:
            num = rn.randrange(0,len(powerUps))
            violetBrick = ld.ladrillo_p("resources/ladrilloVioleta.png",posWidth,posHeight, 1,2,POWERU_UP_LIST[num][0],POWERU_UP_LIST[num][1])
            brickGroup.add([violetBrick])
            del violetBrick
            del num
        elif brickType == 3:
            blueBrick = ld.normalBrick("resources/ladrilloAzul.png",posWidth,posHeight, 3,3)
            brickGroup.add([blueBrick])
            del blueBrick
        elif brickType == 4:
            grayBrick = ld.fallingBrick("resources/ladrilloGris.png",posWidth,posHeight, 4,4)
            brickGroup.add([grayBrick])
            del grayBrick
        posWidth += ld.BRICK_SIZE[0] + BRICKS_DISTANCE
    return bricks

#suma los puntos al puntaje total.
def addScore(pts,SCORE):
    SCORE += pts






#Dibuja el puntaje en la pantalla.
def drawScore():
    text_surface, rect = GAME_FONT.render("Puntaje: " + str(SCORE), WHITE)
    rect.x = 0
    rect.y = HEIGHT / 1.15
    SCR.blit(BACKGROUND, rect, rect)
    SCR.blit(text_surface, rect)

#Dibuja el numero de vidas del jugador en la pantalla.
def drawLives():
    text_surface, rect = GAME_FONT.render("Vidas: " + str(lives), WHITE)
    rect.x = 0
    rect.y = HEIGHT / 1.05
    SCR.blit(BACKGROUND, rect, rect)
    SCR.blit(text_surface, rect, )

#Deja la pelota arriba del jugador, esperando al saque.
def serve(player,ball):
    SCR.blit(BACKGROUND, ball.rect, ball.rect) 
    ball.rect.midbottom = player.rect.midtop
    SCR.blit(ball.image, ball.rect) 
    ball.verticalSpeed = 0
    ball.horizontalSpeed = 0

#Texto de cuando el jugador pierde.
def gameOver():
    text_surface, rect = GAME_FONT.render("GAME OVER", WHITE, size = 100)
    rect.centerx = WIDTH / 2
    rect.centery = HEIGHT / 2
    SCR.blit(text_surface, rect )
    
    pygame.display.flip()
    time.sleep(3)
    sys.exit()

#Texto de cuando el jugador gana.
def win():
    text_surface, rect = GAME_FONT.render("GANASTE", WHITE, size = 100)
    rect.centerx = WIDTH / 2
    rect.centery = HEIGHT / 2
    SCR.blit(text_surface, rect )
    
    pygame.display.flip()
    time.sleep(3)
    sys.exit()

#Rompe al ladrillo cuando algo le pega (pelota o power up de los tiros).
def breakBrick(brk,proyectile):
    brk.setResistance(brk.getResistance()-proyectile.strenght)
    #Esto que comente hace que el ladrillo se rompa cuando todavia tiene 2 de vida
    #if brk.resistance <= proyectile.strenght: # 3 3
        #brk.resistance = 0
    if brk.resistance <= 0:
        brk.breakSound.play()
        return brk.points
    else:
        return 0

#Rebote vertical.
def bounceV(brk, b):
    SCR.blit(BACKGROUND, b.rect, b.rect)
    b.invertVSpeed()
    b.move()
    SCR.blit(b.image, b.rect)
    SCR.blit(brk.image, brk.rect)

#Rebote horizontal.
def bounceH(brk, b):
    SCR.blit(BACKGROUND, b.rect, b.rect)
    b.invertHSpeed()
    b.move()
    SCR.blit(b.image, b.rect)
    SCR.blit(brk.image, brk.rect)

#Agrega un power up al grupo de los power ups.
def addPowerUp(points,powerUpGroup,brick,SCR):
    if points > 0:
                SCR.blit(BACKGROUND, brick.rect, brick.rect)
                brickGroup.remove(brick)
                addScore(points,SCORE)
                if isinstance(brick, ld.ladrillo_p):
                    powerUpGroup.add([powerup.powerUp(brick.rect.x, brick.rect.y, brick.powerUp,brick.imagenPU)])

#Cambia el color de los ladrillos segun la resistencia que le queda.
def resistenceColor(brick,SCR):
    try:
        brick.resistanceColor()
        SCR.blit(BACKGROUND, brick.rect, brick.rect)
        SCR.blit(brick.image,brick.rect)
    except Exception as e:
            pass
    
#Verifica si un ladrillo es de la clase ladrillo flojo.
def isFallingBrick(SCR,proyectile,brick):
    #Verifica si el ladrillo es de la clase ladrillo flojo
    if isinstance(brick, ld.fallingBrick):
        SCR.blit(BACKGROUND, proyectile.rect, proyectile.rect)
        brick.setFalling(True)
        SCR.blit(proyectile.image,proyectile.rect)


def multiBall(SCR,ballGroup,b,num):
        for i in range(num):
            if not len(ballGroup)>=3:
                if i % 2 == 0:
                    ballGroup.add(t.Pelota((b.rect.x+b.rect.width),b.rect.y))
                else:
                    ballGroup.add(t.Pelota((b.rect.x-b.rect.width),b.rect.y))
        i = 0
        for ball in ballGroup: 
            ball.setSpeed(b.getSpeed()[0],b.getSpeed()[1])
            i +=1
            if i != 0:
                if i % 2 == 0:
                    ball.invertHSpeed()
                if i % 2 != 0:
                    ball.invertVSpeed()
            



def updateBallPosition(SCR,ball):
    SCR.blit(BACKGROUND, ball.rect, ball.rect)
    ball.move()
    SCR.blit(ball.image, ball.rect) 


pygame.init()

GAME_FONT = pygame.freetype.SysFont('roboto', 20, bold=False, italic=False)

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
angle = 0
flecha = flechitaSAque.FlechitaSaque(player.rect.centerx, player.rect.centery - ball.rect.height, 80, 10)
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
                ball.serve(flecha.angle)    
            elif (event.key == pygame.K_SPACE and not waitingServe and shootPU):
                missile = misil.Misille(player.rect.centerx,player.rect.y)                
                missileGroup.add([missile])
                
                player.setShoot(player.getShoot()-1)
                if player.getShoot() == 0:
                    shootPU = False

    joystick = pygame.key.get_pressed()

    #Movimiento del jugador
    if joystick[pygame.K_LEFT]:
        SCR.blit(BACKGROUND, player.rect, player.rect)
        player.moveLeft(0)
        SCR.blit(player.image, player.rect) 
    elif joystick[pygame.K_RIGHT]:
        SCR.blit(BACKGROUND, player.rect, player.rect)
        player.moveRight(WIDTH-10)
        SCR.blit(player.image, player.rect)
    
    #SAque del jugador. si el jugador saco, mueve la pelota
    if waitingServe == True:
        joystick = pygame.key.get_pressed()
        SCR.blit(BACKGROUND,(0,0))
        SCR.blit(player.image,player.rect)
        for brick in brickGroup:
            SCR.blit(brick.image,brick.rect)
        flecha.update(1,joystick)
        flecha.draw(SCR,player.rect.centerx, player.rect.centery - ball.rect.height)
        serve(player,ball)

    for ball in ballGroup:
        #Choque con el jugador
        if pygame.sprite.spritecollideany(ball, playerGroup):
            if abs(ball.rect.top - player.rect.bottom) < COLLISION_TOLARANCE and ball.verticalSpeed < 0:
                bounceV(player, ball)

            if abs(ball.rect.bottom - player.rect.top) < COLLISION_TOLARANCE and ball.verticalSpeed > 0:
                bounceV(player, ball)

            if abs(ball.rect.left - player.rect.right) < COLLISION_TOLARANCE and ball.horizontalSpeed < 0:
                bounceH(player, ball)

            if abs(ball.rect.right - player.rect.left) < COLLISION_TOLARANCE and ball.horizontalSpeed > 0:
                bounceH(player, ball)


    for ball in ballGroup:
        #Choque con limite de la pantalla
        if ball.rect.top <= 0 - COLLISION_TOLARANCE :
            ball.invertVSpeed()
        if ball.rect.left <= 0 or ball.rect.right >= WIDTH:
            ball.invertHSpeed()

    for ball in ballGroup:
        updateBallPosition(SCR,ball)

    for ball in ballGroup:  
        #Rebote de la pelota con los ladrillos 
        collisionedBricks = pygame.sprite.spritecollide(ball, brickGroup, False)
        if len(collisionedBricks) > 0:
            ball.bounce.play()  
            for brick in collisionedBricks:
                SCR.blit(brick.image, brick.rect)
                if ball.strenght > 1:
                    ball.strenght-= brick.resistance
                    points = breakBrick(brick,ball)    
                    if ball.strenght <= 0:
                        ball.strenght = 1
                    SCR.blit(BACKGROUND, ball.rect, ball.rect)
                    SCR.blit(ball.image, ball.rect)
                    SCR.blit(BACKGROUND, brick.rect, brick.rect)
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

                isFallingBrick(SCR,ball,brick)
                
            

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
            SCR.blit(BACKGROUND, brick.rect, brick.rect)
            brickGroup.remove(brick)
            del brick

    #tira los tiros
    if (shootPU or len(missileGroup)>0):
        try:        
            for m in missileGroup:    
                SCR.blit(BACKGROUND,m.rect,m.rect)
                m.lauch() 
                SCR.blit(m.image,m.rect)
                if m.rect.y < 0 - m.rect.height - 40:
                    missileGroup.remove(m)
                    del m      
        except Exception as e:
           pass

    

    #Choque de los tiros con los ladrillos
    for m in  missileGroup:   
        crashedBrick = pygame.sprite.spritecollideany(m, brickGroup)
        if crashedBrick:           
                points = breakBrick(crashedBrick,m)
                addPowerUp(points,powerUpGroup,crashedBrick,SCR)
                resistenceColor(crashedBrick,SCR)
                isFallingBrick(SCR,m,crashedBrick)
                if points > 0:
                    brickGroup.remove(crashedBrick)    
                SCR.blit(BACKGROUND, crashedBrick.rect, crashedBrick.rect)
                missileGroup.remove(m)
                SCR.blit(BACKGROUND,m.rect,m.rect)
                del m

    #hace caer al power up
    if len(powerUpGroup) > 0:
        for power in powerUpGroup:
            SCR.blit(BACKGROUND, power.rect, power.rect)
            power.fallDown()    
            SCR.blit(power.image, power.rect)
            for brick in brickGroup:
                SCR.blit(brick.image,brick.rect)

    #Verifica si el power up que cae choca con el jugador
    powerUpColisioned = pygame.sprite.spritecollide(player, powerUpGroup, True)
    #si choca, le da el power up al jugador
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
            elif powerUpColisioned[0].powerUp == POWER_MULTIBALL[0]:
                if not waitingServe:
                    multiBall(SCR,ballGroup,ball,3)
                    updateBallPosition(SCR,ball)
                else:
                    pass

            SCR.blit(BACKGROUND, power, power)
            powerUpGroup.remove(power)

            
            

    drawScore()
    drawLives()
    
    #Actualiza la pantalla
    pygame.display.flip()


    
    if len(ballGroup) == 0:
        lives -=1

    if len(ballGroup)>=2:
       for ball in ballGroup:
            if ball.rect.y > HEIGHT + 20:
                ballGroup.remove(ball)
                del ball

    #Si la pelota se cae por abajo el jugador pierde una vida. Si pierde todas las vidas pierde el juego.
    if len(ballGroup) == 1:
        for ball in ballGroup:
            if ball.rect.top > HEIGHT + 20:
                if lives > 1:
                    lives -=1
                    waitingServe = True   
                    serve(player,ball)
                    SCR.blit(BACKGROUND,flecha.rect,flecha.rect)
                else:
                    gameOver()
        
    #condicion para ganar el juego
    if len(brickGroup) == 0:
        win()

    if lives == 0:
            gameOver()
    
    
    
    clock.tick(60)

pygame.quit()