import sys, math, pygame, os
#print (sys.version)
from pygame.locals import *
from random import randint

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (120,50) # posicion pantalla
ancho = 900
alto = 680

class Comida(pygame.sprite.Sprite):
	"""Clase para las naves"""
	def __init__(self,ancho,alto):
		pygame.sprite.Sprite.__init__(self)
		self.ImagenComida = pygame.image.load("Comida.png")
		self.rect = self.ImagenComida.get_rect()
		self.rect.bottom += randint(20,alto-20)
		self.rect.right += randint(20,ancho-20)

	def dibujar(self, superficie):
		superficie.blit(self.ImagenComida, self.rect)

class Cola(pygame.sprite.Sprite):
	def __init__(self,x,y):
		self.ImagenCola = pygame.image.load("SnakeTail.png")
		self.rect = self.ImagenCola.get_rect()
		self.rect.right = x
		self.rect.bottom = y

	def dibujar(self, superficie):
		superficie.blit(self.ImagenCola, self.rect)


class Cuerpo(pygame.sprite.Sprite):
	"""Clase para las naves"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.ImagenCabeza = pygame.image.load("SnakeHead.png")
		self.facing = "UP"

		self.rect = self.ImagenCabeza.get_rect()
		self.rect.bottom += 630
		self.rect.right +=25 
		self.velocidad = 27
		self.rotado = [0,0,0,0]
		self.tail = 0
		self.Cola = []
		#self.UltimaCola = 0


	def movimiento(self):

		#if ((self.rect.top>0 and self.rect.top<655) and (self.rect.right > 0 and self.rect.right <900)):
			if self.facing == "UP":
				self.rect.bottom -= self.velocidad
				if self.rotado[0] == 0:
					self.ImagenCabeza = pygame.image.load("SnakeHead.png")
					self.ImagenCabeza = pygame.transform.rotate(self.ImagenCabeza,0)
					self.rotado = [1,0,0,0]
			if self.facing == "RIGHT":
				self.rect.right += self.velocidad
				if self.rotado[1] == 0:
					self.ImagenCabeza = pygame.image.load("SnakeHead.png")
					self.ImagenCabeza = pygame.transform.rotate(self.ImagenCabeza,-90)
					self.rotado = [0,1,0,0]
			if self.facing == "LEFT":
				self.rect.right -= self.velocidad
				if self.rotado[2] == 0:
					self.ImagenCabeza = pygame.image.load("SnakeHead.png")
					self.ImagenCabeza = pygame.transform.rotate(self.ImagenCabeza,90)
					self.rotado = [0,0,1,0]
			if self.facing == "DOWN":
				self.rect.bottom += self.velocidad
				if self.rotado[3] == 0:
					self.ImagenCabeza = pygame.image.load("SnakeHead.png")
					self.ImagenCabeza = pygame.transform.rotate(self.ImagenCabeza,-180)
					self.rotado = [0,0,0,1]

	def right(self):
		self.facing = "RIGHT"
	def up(self):
		self.facing = "UP"
	def down(self):
		self.facing = "DOWN"
	def left(self):
		self.facing = "LEFT"
	
	def comer(self):
		newCola = Cola(self.rect.right, self.rect.bottom)
		self.Cola.append(newCola)		

	def dibujar(self, superficie):
		superficie.blit(self.ImagenCabeza, self.rect)

#------------------------------------------------------------

def Snake():
	venta = pygame.display.set_mode((ancho,alto))
	pygame.display.set_caption("Snake")
	ImagenFondo = pygame.image.load("Fondo.jpg")

	#Comida-------
	listaComidas=list()
	food = Comida(ancho, alto)
	listaComidas.append(food)
	#-----------

	serpiente = Cuerpo()
	reloj = pygame.time.Clock()
	mov = 0 #retraso para que se vea que avanza cada 25 pix [0-60]
	#colas = []

	while True:
		reloj.tick(60)
		mov +=1
		#jugador.movimiento()
		tiempo = pygame.time.get_ticks()/1000
		#------------------EVENTOS------------------------
		for evento in pygame.event.get():
			if evento.type == QUIT:
				pygame.quit()
				sys.exit()
			if evento.type == pygame.KEYDOWN:
				if evento.key == K_RIGHT:
					serpiente.right()
				if evento.key == K_LEFT:
					serpiente.left()
				if evento.key == K_UP:
					serpiente.up()
				if evento.key == K_DOWN:
					serpiente.down()
		
		venta.blit(ImagenFondo,(0,0)) #--Imagen fondo--
		#-------------Agregar y dibujar comida---------
		if len(listaComidas) > 0:
			for fod in listaComidas:
				if serpiente.rect.colliderect(fod.rect):
					serpiente.comer()
					listaComidas.remove(fod)
				else:
					fod.dibujar(venta)
		else:
			food = Comida(ancho,alto)
			listaComidas.append(food)
		#----------------- COLAS -----------------------------
		#print(serpiente.facing)

		serpiente.dibujar(venta)
		if (len(serpiente.Cola) >0) :
				for col in serpiente.Cola:
					col.dibujar(venta)
		#-------------retraso movimiento--------------------------
		if mov >15:
			x,y = serpiente.rect.right, serpiente.rect.bottom
			x1,y1 = 0,0
			if (len(serpiente.Cola) >0) :
					for col in serpiente.Cola:
						x1, y1 = col.rect.right , col.rect.bottom
						col.rect.right , col.rect.bottom = x,y
						x,y = x1,y1
			serpiente.movimiento() #esto debiera mover las colas, vamos para alla
			mov = 0
		#if serpiente.tail >0:
			#pygame.time.delay(100)
		pygame.display.update()

Snake()