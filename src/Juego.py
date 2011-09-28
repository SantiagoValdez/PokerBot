# -*- coding: utf-8 -*-
'''
Creado el Sep 26, 2011

@author: Nahuel Hernández
@author: Javier Pérez
@author: Carlos Bellino
@author: Vanessa Jannete Cañete
@author: Gabriela Gaona
'''

"""
Se supone que van a usar estas clases para abstraer todas las mierdas
de Pygame, como el tema de la musica, los sonidos, el manejo de sprites
el fondo, los eventos de teclado y mouse...By the way, esta es la manera
correcta de poner los comentarios, no como su sucio pydev pone...

En una carpeta datos dentro del mismo directorio pones las imagenes que
se van a usar.
"""

import os
import pygame
from pygame.locals import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Boton(pygame.sprite.Sprite):
    ''' Representa un boton '''
    def __init__(self, imagen, x, y, on_click=None):
        pygame.sprite.Sprite.__init__(self)
        (self.image, self.rect) = imagen
        self.rect.center = (x, y)
        self.posfinalx = x
        self.posfinaly = y
        
        ''' Asignacion de la funcion cuando se hace click en el boton '''
        if on_click :
            self.onclick = on_click
        else :
            self.onclick = self.funcionvacia
    
    def funcionvacia(self):
        return None
    
    def dentro(self, (x,y) ):
        if y >= self.rect.top and y <= self.rect.bottom :
            if x >= self.rect.left and x <= self.rect.right :
                return True
            else :
                return False
        else :
            return False
    ''' Se asignan las coord. de la pos.final, y en update se mueve'''
    def mover(self,(x,y)):
        self.posfinalx = x
        self.posfinaly = y
    
    ''' Movemos si es que no esta en su pos final '''
    def update(self):
        if self.posfinalx != self.rect.centerx or self.posfinaly != self.rect.centery :
            dx = self.posfinalx - self.rect.centerx
            dy = self.posfinaly - self.rect.centery
            if dx > 0:
                self.rect.centerx = self.rect.centerx + 1
            elif dx < 0:
                self.rect.centerx = self.rect.centerx - 1
            
            if dy > 0:
                self.rect.centery = self.rect.centery + 1
            elif dy < 0:
                self.rect.centery = self.rect.centery - 1
                
''' NO ANDA BIEN ESTE!!! Por algun motivo mas alla de la logica :O '''
class Campo(pygame.sprite.Sprite):
    ''' (DEBERIA)Representa una especie de textfield '''
    def __init__(self, imagen, x, y):
        pygame.sprite.Sprite.__init__(self)
        pygame.font.init()
        (self.image, self.rect) = imagen
        self.background = self.image.copy()
        self.rect.center = (x, y)
        self.posfinalx = x
        self.posfinaly = y
        self.text = ""
        self.screen = None
    
    def onclick(self,juego):
        fin = True
        cadena = ""
        clock = pygame.time.Clock()
        self.screen = juego.screen
        self.image = self.background.copy()
        print "entra while..."
        while fin:
            clock.tick(30)
            k = juego.get_tecla()
            if k:
                if k == "enter" or k == "esc":
                    fin = False
                elif k == "borrar":
                    cadena = cadena[ 0 : len(cadena)-1 ]
                else:
                    cadena += k
            self.text = cadena
            juego.actualizar()
        
        
    def dentro(self, (x,y) ):
        if y >= self.rect.top and y <= self.rect.bottom :
            if x >= self.rect.left and x <= self.rect.right :
                return True
            else :
                return False
        else :
            return False
    ''' Se asignan las coord. de la pos.final, y en update se mueve'''
    def mover(self,(x,y)):
        self.posfinalx = x
        self.posfinaly = y
    
    ''' Movemos si es que no esta en su pos final '''
    def update(self):
        if self.posfinalx != self.rect.centerx or self.posfinaly != self.rect.centery :
            dx = self.posfinalx - self.rect.centerx
            dy = self.posfinaly - self.rect.centery
            if dx > 0:
                self.rect.centerx = self.rect.centerx + 1
            elif dx < 0:
                self.rect.centerx = self.rect.centerx - 1
            
            if dy > 0:
                self.rect.centery = self.rect.centery + 1
            elif dy < 0:
                self.rect.centery = self.rect.centery - 1
        
        if len(self.text) > 0 :
            fuente = pygame.font.Font(None, 18)
            letra = (0, 0, 0)
            texto = fuente.render(self.text, 1, letra)
            self.image.blit(texto,(self.rect.left,self.rect.top))
        

class Juego():
    
    
    def cargar_imagen(self,name, colorkey=False):
        '''Genera una superficie a partir de una archivo de imagen.

        Retorna la imagen junto con su tamano en formato de tupla.'''

        fullname = os.path.join("datos", name)

        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            print 'No se puede cargar la imagen: ', fullname
            raise SystemExit, message

        image = image.convert()

        if colorkey:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)

        return (image, image.get_rect())


    def cargar_sonido(self,nombre):
        '''Carga un sonido a partir de un archivo.

        Si existe algun problema al cargar el sonido intenta crear
        un objeto Sound virtual.'''

        class NoneSound:
            def play(self):
                pass

        if not pygame.mixer or not pygame.mixer.get_init():
            return NoneSound()

        ruta = os.path.join("datos", nombre)

        try:
            sound = pygame.mixer.Sound(ruta)
        except pygame.error, message:
            print 'No se pudo cargar el sonido: ', ruta
            raise SystemExit, message

        return sound

    def cargar_musica(self,nombre):
        '''Carga una musica apartir de un archivo.'''
        ruta = os.path.join("datos", nombre)

        try:
            music = pygame.mixer.music.load(ruta)
        except pygame.error, message:
            print 'No se pudo cargar la musica: ', ruta
            raise SystemExit, message

        return music
        
    def iniciar(self):
        tamano = (SCREEN_WIDTH,SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(tamano)
        (self.background_image, _) = self.cargar_imagen("fondo.jpg")
        self.screen.blit(self.background_image, (0, 0))
        self.tecla = []
        self.click = []
        self.sprites = sprites = pygame.sprite.RenderClear()
    
    def actualizar(self):
        self.leer_click()
        self.leer_teclado()
        self.sprites.update()
        self.sprites.clear(self.screen, self.background_image)
        self.sprites.draw(self.screen)
        pygame.display.flip()
        pygame.event.clear()
        
    def leer_teclado(self):
        tecla = ""
        for event in pygame.event.get(KEYDOWN):
            if event.key == K_RETURN:
                tecla = "enter"
            elif event.key == K_ESCAPE:
                tecla = "esc"
            elif event.key ==  K_BACKSPACE:
                tecla = "borrar"
            elif event.key >= K_a and event.key <= K_z :
                tecla = chr(event.key)
            elif event.key >= K_0 and event.key <= K_9 :
                tecla = chr(event.key)
            if tecla != "":
                self.tecla.append(tecla)
        

    def leer_click(self):
        pos = (0,0)
        for event in pygame.event.get(MOUSEBUTTONDOWN):
            if event.button == 1 :
                pos = pygame.mouse.get_pos()
            if pos != (0,0):
                self.click.append(pos)
    
    def get_tecla(self):
        try:
            k = self.tecla.pop(0)
        except :
            k = False
        return k
    
    def get_click(self):
        try:
            k = self.click.pop(0)
        except :
            k = False
        return k
    
    def add_objeto(self,sprite):
        self.sprites.add(sprite)

def boton_1_onclick():
    '''Esto es una callback function, asi se personaliza un boton'''
    print "hola"

#----Pedazo de prueba-----

def main():
    pygame.init()
    game = Juego()
    game.iniciar()
    seguir = True
    imagen = game.cargar_imagen("otro.jpg")
    boton = Boton(imagen,600,400,boton_1_onclick)
    game.add_objeto(boton)
    clock = pygame.time.Clock()
    imagen = game.cargar_imagen("textfield.jpg")
    texto = Campo(imagen,100,100)
    game.add_objeto(texto)
    while seguir:
        clock.tick(30)
        c = game.get_click()
        k = game.get_tecla()
        
        if c :
            if boton.dentro(c) :
                boton.onclick()
                boton.mover((100,200))
            if texto.dentro(c) :
                texto.onclick(game)
            else :
                print c
        if k :
            if k == "esc" :
                exit()
            
        
        #---Despues de todos los calculos---
        game.actualizar()
if __name__ == '__main__':
    main()
