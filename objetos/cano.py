import pygame
import random

from constantes import *

class Cano:
    distancia = 200
    velocidade = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.posTopo = 0
        self.posBase = 0
        self.canoTopo = pygame.transform.flip(IMG_CANO, False, True)
        self.canoBase = IMG_CANO
        self.passou = False
        self.definirAltura()

    def definirAltura(self):
        self.altura = random.randrange(50, 450)
        self.posTopo = self.altura - self.canoTopo.get_height()
        self.posBase = self.altura + self.distancia

    def mover(self):
        self.x -= self.velocidade

    def desenhar(self, tela):
        tela.blit(self.canoTopo, (self.x, self.posTopo))
        tela.blit(self.canoBase, (self.x, self.posBase))

    def colidir(self, passaro):
        passaroMask = passaro.getMask()
        topoMask = pygame.mask.from_surface(self.canoTopo)
        baseMask = pygame.mask.from_surface(self.canoBase)

        distanciaTopo = (self.x - passaro.x, self.posTopo - round(passaro.y))
        distanciaBase = (self.x - passaro.x, self.posBase - round(passaro.y))

        basePonto = passaroMask.overlap(baseMask, distanciaBase)
        topoPonto = passaroMask.overlap(topoMask, distanciaTopo)


        if basePonto or topoPonto:
            return True
        else:
            return False
