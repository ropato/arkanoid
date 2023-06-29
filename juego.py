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
POWER_LARGE = 'M'
pantalla = pygame.display.set_mode((ANCHO,ALTO)) #inicializo la pantalla

SEPARACION_LADRILLOS =10 

BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = ( 255, 0, 0)
BLUE = (0,0,255)
PURPLE=(148,0,211)

BACKGROUND = pygame.image.load('resources/bg1.jpg').convert()
PELOTA_SPRITE = pygame.image.load("pelota.png").convert()

def generarLadrillos(cantidad): 
    ancho = 20
    alto = 0
    
    ladRojo = ld.Ladrillo(RED,ancho,0, 1, 1)
    ladVerde = ld.Ladrillo(GREEN,ancho,0, 2, 2)
    ladAzul = ld.Ladrillo(BLUE,ancho,0, 1, 1)
    #Genera los ladrillos
    for i in range(cantidad):
        lad = rn.randrange(0,4)
        if ancho + ladRojo.rect.width + SEPARACION_LADRILLOS  > ANCHO:
            ancho = 20
            alto += ladRojo.rect.height + 20    
        if lad == 1:
            ladRojo = ld.Ladrillo(RED,ancho,alto, 1,1)
            todos.add([ladRojo])
        elif lad == 2:
            ladVerde = ld.Ladrillo(GREEN,ancho,alto, 2,2)
            todos.add([ladVerde])
        elif lad==3:
            
            ladVioleta = ld.ladrillo_p(PURPLE,ancho,alto, 1,2,POWER_LARGE)
            todos.add([ladVioleta])
        else:
            ladAzul = ld.Ladrillo(BLUE,ancho,alto, 3,3)
            todos.add([ladAzul])
        ancho += ladRojo.rect.width + SEPARACION_LADRILLOS

def sumarPuntaje(puntos):
    global PUNTAJE
    PUNTAJE += puntos

def dibujarPuntaje():
    text_surface, rect = gameFont.render("Puntaje: " + str(PUNTAJE), (0, 0, 0))
    #pantalla.blit(text_surface, ( 0, ALTO / 1.15), ( 0, ALTO / 1.15))
    pantalla.blit(text_surface, ( 0, ALTO / 1.15))

def dibujarVidas():
    text_surface, rect = gameFont.render("Vidas: " + str(vidas), (0, 0, 0))
    #pantalla.blit(text_surface, ( 0, ALTO / 1.05), ( 0, ALTO / 1.05))
    pantalla.blit(text_surface, ( 0, ALTO / 1.05))

def saque():
    global p
    global j
    pantalla.blit(BACKGROUND, p.rect, p.rect) 
    p.rect.midbottom = j.rect.midtop
    pantalla.blit(p.image, p.rect) 

def perdio(jugando):
    fuente = pygame.font.Font(None,72)
    texto = fuente.render(f"GAME OVER",(0,0,0),(0,0,0))
    texto_rect = texto.get_rect()
    texto_rect.center = [ANCHO / 2  , ALTO / 2]
    pantalla.blit(texto,texto_rect)
    pygame.display.flip()
    time.sleep(3)
    jugando = False
    sys.exit()

def gano(jugando):
    pass

def romperLadrillo(ladrillo):
    ladrillo.resistencia -= 1
    if ladrillo.resistencia == 0:
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
    #Pantalla de fin
    #Opcional Distintos niveles

gameFont = pygame.freetype.SysFont('roboto', 16, bold=False, italic=False)



todos  = pygame.sprite.Group()

grupoPelota = pygame.sprite.Group()
p = t.Pelota(ANCHO /2,ALTO/2)
pantalla.blit(BACKGROUND, p.rect, p.rect) 
grupoPelota.add([p])

grupoJugador = pygame.sprite.Group()
j = jugador.Jugador(ANCHO /2,ALTO -50)
grupoJugador.add([j])
grupoPowerUp = pygame.sprite.Group()
reloj = pygame.time.Clock()
vidas = 3
generarLadrillos(30)

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

        if p.rect.centerx <= ladrillo.rect.left or p.rect.centerx >= ladrillo.rect.right:
            pantalla.blit(BACKGROUND, p.rect, p.rect)
            p.update(ANCHO,ALTO,False,True)
            pantalla.blit(p.image, p.rect)
        elif ladrillo.rect.left <= p.rect.centerx and ladrillo.rect.right  >= p.rect.centerx:
            pantalla.blit(BACKGROUND, p.rect, p.rect)
            p.update(ANCHO,ALTO,True)
            pantalla.blit(p.image, p.rect)
        
        puntos = romperLadrillo(listaLadrillos[0])
        if puntos > 0:
            pantalla.blit(BACKGROUND, p.rect, p.rect)
            p.update(ANCHO,ALTO,True)
            pantalla.blit(p.image, p.rect)
            sumarPuntaje(puntos)
            if isinstance(ladrillo, ld.ladrillo_p):
                grupoPowerUp.add({powerup.powerUp(ladrillo.rect.x, ladrillo.rect.y, ladrillo.powerUp)})
        #Si el centerx de la pelota es mas chico que la parte izquierda del ladrillo o mas grande que la parte derecha del ladrillo, es un rebote horizontal
    if grupoPowerUp:
        for power in grupoPowerUp:
            pantalla.blit(BACKGROUND, power.rect, power.rect)
            power.fallDown()    
            pantalla.blit(power.image, power.rect)
    powerUpColisioned = pygame.sprite.spritecollide(j, grupoPowerUp, True)
    if powerUpColisioned:
        pantalla.blit(BACKGROUND, powerUpColisioned[0], powerUpColisioned[0])
        if powerUpColisioned[0].powerUp == POWER_LARGE:
            pantalla.blit(BACKGROUND, j.rect, j.rect)
            j.getBig()
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
            perdio(jugando)
    
    
    reloj.tick(60)

pygame.quit()
    