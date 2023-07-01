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
ANCHO = 1280 
ALTO = 720
PUNTAJE = 0
#Tupla = Letra que identifica a cada power up y su imagen
POWER_LARGE = 'M',"resources/imgLarge.png"
POWER_FUERZA = "F","resources/imgFuerza.png"
POWER_SMALL = "S","resources/imgSmall.png"
pantalla = pygame.display.set_mode((ANCHO,ALTO)) #inicializo la pantalla

SEPARACION_LADRILLOS =10 

BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = ( 255, 0, 0)
BLUE = (0,0,255)
PURPLE=(148,0,211)

BACKGROUND = pygame.image.load('resources/bg1.jpg').convert()


def generarLadrillos(cantidad,listaPowerUP): 
    ancho = 20
    alto = 0   
    ladrilloAux = ld.Ladrillo(WHITE,0,0,0,0)
    #Genera los ladrillos
    for i in range(cantidad):
        lad =rn.randrange(0,4)
        if ancho + ladrilloAux.getAnchoLadrillo() + SEPARACION_LADRILLOS  > ANCHO:
            ancho = 20
            alto += ladrilloAux.rect.height + 20    
        if lad == 1:
            ladRojo = ld.Ladrillo(RED,ancho,alto, 1,1)
            todos.add([ladRojo])
        elif lad == 2:
            ladVerde = ld.Ladrillo(GREEN,ancho,alto, 2,2)
            todos.add([ladVerde])
        elif lad==3:
            num = rn.randrange(0,len(listaPowerUP))
            ladVioleta = ld.ladrillo_p(PURPLE,ancho,alto, 3,2,listaPowerUP[num][0],listaPowerUP[num][1])
            todos.add([ladVioleta])
        else:
            ladAzul = ld.Ladrillo(BLUE,ancho,alto, 3,3)
            todos.add([ladAzul])
        ancho += ladrilloAux.getAnchoLadrillo() + SEPARACION_LADRILLOS
    
    del ladrilloAux #Solamente sevia para te

def sumarPuntaje(puntos):
    global PUNTAJE
    PUNTAJE += puntos

def dibujarPuntaje():
    text_surface, rect = gameFont.render("Puntaje: " + str(PUNTAJE), WHITE)
    #pantalla.blit(text_surface, ( 0, ALTO / 1.15), ( 0, ALTO / 1.15))
    pantalla.blit(text_surface, ( 0, ALTO / 1.15))

def dibujarVidas():
    text_surface, rect = gameFont.render("Vidas: " + str(vidas), WHITE)
    #pantalla.blit(text_surface, ( 0, ALTO / 1.05), ( 0, ALTO / 1.05))
    pantalla.blit(text_surface, ( 0, ALTO / 1.05))

def saque():
    global p
    global j
    pantalla.blit(BACKGROUND, p.rect, p.rect) 
    p.rect.midbottom = j.rect.midtop
    pantalla.blit(p.image, p.rect) 

def perdio():
    fuente = pygame.font.Font(None, 72)
    texto = fuente.render("GAME OVER", True, WHITE)
    texto_rect = texto.get_rect()
    texto_rect.center = [ANCHO / 2  , ALTO / 2]
    pantalla.blit(BACKGROUND,(0,0))
    pantalla.blit(texto,texto_rect)
    pygame.display.flip()
    time.sleep(3)
    sys.exit()

def gano(jugando):
    pass

def romperLadrillo(ladrillo,pelota):
    ladrillo.resistencia -= pelota.fuerza
    if ladrillo.resistencia <= pelota.fuerza: # 3 3
        ladrillo.resistencia = 0
    if ladrillo.resistencia <= 0:

    
        pantalla.blit(BACKGROUND, ladrillo.rect, ladrillo.rect)
        todos.remove(ladrillo)
        return ladrillo.puntos
    else:
        return 0
pygame.init()


#TODO:
    #Power Ups
    #Otros ladrillos <--
    #Mostrar Tiempo
    #Pantalla de inicio
    #Opcional Distintos niveles

gameFont = pygame.freetype.SysFont('roboto', 20, bold=False, italic=False)

listaPowerUP= [POWER_FUERZA,POWER_LARGE,POWER_SMALL] 

todos  = pygame.sprite.Group()

grupoPelota = pygame.sprite.Group()
p = t.Pelota(ANCHO /2,ALTO/2)
pantalla.blit(BACKGROUND, p.rect, p.rect) 
grupoPelota.add([p])

grupoJugador = pygame.sprite.Group()
j = jugador.Jugador((ANCHO /2),ALTO -50)
grupoJugador.add([j])
grupoPowerUp = pygame.sprite.Group()
reloj = pygame.time.Clock()
vidas = 3
generarLadrillos(100,listaPowerUP)

esperando_saque = True
jugando = True

pantalla.blit(BACKGROUND, (0, 0))
pantalla.blit(j.image, j.rect)
#Bucle principal
while jugando:
    #Eventos del juego
    for event in pygame.event.get():
        #Cierra el juego con la cruz
        if event.type == pygame.QUIT:
            jugando = False
        #Eventos de apretar una tecla
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE and esperando_saque == True):
                esperando_saque = False        
    joystick = pygame.key.get_pressed()
    if joystick[pygame.K_LEFT]:
        pantalla.blit(BACKGROUND, j.rect, j.rect)
        j.izquierda(0)
        pantalla.blit(j.image, j.rect) 
    elif joystick[pygame.K_RIGHT]:
        pantalla.blit(BACKGROUND, j.rect, j.rect)
        j.derecha(ANCHO-10)
        pantalla.blit(j.image, j.rect)
    

    #Choque con el jugador
    if pygame.sprite.spritecollideany(p, grupoJugador):
        pantalla.blit(BACKGROUND, p.rect, p.rect)
        p.update(ANCHO,ALTO,True)
        pantalla.blit(p.image, p.rect)
        #porque aveces la pelota se come un pedazo de la paleta
        pantalla.blit(BACKGROUND, j.rect, j.rect)
        pantalla.blit(j.image, j.rect)
    #Rebote de la pelota con los ladrillos o paredes.
    listaLadrillos = pygame.sprite.spritecollide(p, todos, False)
    if listaLadrillos:
        ladrillo = listaLadrillos[0]
    
        if p.fuerza > 1:
            p.fuerza-= ladrillo.resistencia
            puntos = romperLadrillo(ladrillo,p)    
            if p.fuerza <= 0:
                p.fuerza = 1
            pantalla.blit(BACKGROUND, p.rect, p.rect)
            p.update(ANCHO,ALTO)
            pantalla.blit(p.image, p.rect)
        else:
            puntos = romperLadrillo(ladrillo,p)
            #si pelota fuerza == 1
            if p.rect.right <= ladrillo.rect.left or p.rect.left >= ladrillo.rect.right:
                pantalla.blit(BACKGROUND, p.rect, p.rect)
                p.update(ANCHO,ALTO,False,True)
                pantalla.blit(p.image, p.rect)
            elif ladrillo.rect.left <= p.rect.centerx and ladrillo.rect.right  >= p.rect.centerx:
                pantalla.blit(BACKGROUND, p.rect, p.rect)
                p.update(ANCHO,ALTO,True)
                pantalla.blit(p.image, p.rect)
        
        
        if puntos > 0:
            sumarPuntaje(puntos)
            if isinstance(ladrillo, ld.ladrillo_p):
                grupoPowerUp.add([powerup.powerUp(ladrillo.rect.x, ladrillo.rect.y, ladrillo.powerUp,ladrillo.imagenPU)])
      
    if grupoPowerUp:
        for power in grupoPowerUp:
            pantalla.blit(BACKGROUND, power.rect, power.rect)
            power.fallDown()    
            pantalla.blit(power.image, power.rect)
    powerUpColisioned = pygame.sprite.spritecollide(j, grupoPowerUp, True)
    if powerUpColisioned:
        pantalla.blit(BACKGROUND, powerUpColisioned[0], powerUpColisioned[0])
        if powerUpColisioned[0].powerUp == POWER_LARGE[0]:
            pantalla.blit(BACKGROUND, j.rect, j.rect)
            j.getBig()
            pantalla.blit(j.image, j.rect)
        elif powerUpColisioned[0].powerUp == POWER_FUERZA[0]:
            p.masFuerza()
        elif powerUpColisioned[0].powerUp == POWER_SMALL[0]:
            pantalla.blit(BACKGROUND, j.rect, j.rect)
            j.getSmall()
            pantalla.blit(j.image, j.rect)

    
    #Color de fondo de la pantalla
    #pantalla.fill((255,255,255))
    #Dibuja los objetos
    todos.draw(pantalla)
    #Dibuja la pelota en la pantalla
    #Dibuja al jugador en la pantalla

    dibujarPuntaje()
    dibujarVidas()

    #Actualiza la pantalla
    pygame.display.flip()

    #Actualiza la posicion de la pelota
    if esperando_saque == True:
        saque()
    else:
        pantalla.blit(BACKGROUND, p.rect, p.rect) 
        p.update(ANCHO,ALTO)
        pantalla.blit(p.image, p.rect) 
    if len(todos) == 0:
        ganaste()
    
    #Si la pelota se cae por abajo el jugador pierde una vida. Si pierde todas las vidas pierde el juego.
    if p.rect.top > ALTO + 20:
        if vidas > 1:
            vidas -=1
            esperando_saque = True
            saque()
        else:
            pantalla.fill((255,255,255))
            perdio()
    
    
    reloj.tick(60)

pygame.quit()
    