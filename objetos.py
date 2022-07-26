import pygame
import random

from constantes import *

class Cano:
    distanciaY = 150
    distanciaX = 250
    canoTopo = pygame.transform.flip(IMG_CANO, False, True)
    canoBase =IMG_CANO

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.posTopo = 0
        self.posBase = 0
        self.passou = False
        self.direcao = random.choice([-1, 1])
        self.velocidade = random.randrange(0, 8)
        self.definirAltura()

    def definirAltura(self):
        self.altura = random.randrange(50, 250)
        self.posTopo = self.altura - self.canoTopo.get_height()
        self.posBase = self.altura + self.distanciaY

    def mover(self):
        self.x -= VELOCIDADE_BASE
        self.posTopo -= self.velocidade
        self.posBase -= self.velocidade

        if(self.posTopo + self.canoTopo.get_height() < 50 or
           self.posTopo + self.canoTopo.get_height() > 250):
            self.velocidade = self.velocidade * -1

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

class Cenario:
    def __init__(self, x, y, img, velocidade):
        self.x = x
        self.y = y
        self.imagem = img
        self.velocidade = velocidade

    def mover(self):
        self.x -= self.velocidade

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))

class Solo(Cenario):
    imagem = IMG_SOLO
    largura = imagem.get_width()
    y = 450

    def __init__(self, x):
        super().__init__(x, self.y, self.imagem, VELOCIDADE_BASE)

class Ceu(Cenario):
    imagem = IMG_CEU
    largura = imagem.get_width()
    y = 0

    def __init__(self, x):
        super().__init__(x, self.y, self.imagem, 0)

class Nuvem(Cenario):
    imagem = IMG_NUVEM
    largura = imagem.get_width()
    y = 350

    def __init__(self, x):
        super().__init__(x, self.y, self.imagem, VELOCIDADE_BASE-4)

class Predios(Cenario):
    imagem = IMG_PREDIO
    largura = imagem.get_width()
    y = 375

    def __init__(self, x):
        super().__init__(x, self.y, self.imagem, VELOCIDADE_BASE-3)

class Arvore(Cenario):
    imagem = IMG_ARVORE
    largura = imagem.get_width()
    y = 400

    def __init__(self, x):
        super().__init__(x, self.y, self.imagem, VELOCIDADE_BASE-1)

class Passaro:
    IMGS = IMG_PASSARO

    ROTACAO_MAX = 25
    ROTACAO_VEL = 10
    TEMPO_ANIMACAO = 10

    def __init__(self, x, y):
        # TODO adicionar variavel pontos e implementar
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagemImagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -12
        self.tempo = 0
        self.altura = self.y

    def cair(self):
        self.tempo += 1
        self.velocidade = self.velocidade + 1

        if self.velocidade > 16:
            self.velocidade = 16

        self.y += self.velocidade

        if self.velocidade < 0:
            if self.angulo < self.ROTACAO_MAX:
                self.angulo = self.ROTACAO_MAX
        else:
            if self.angulo > -70:
                self.angulo -= self.ROTACAO_VEL

    def desenhar(self, tela):

        # TODO melhorar
        self.contagemImagem += 1

        if self.contagemImagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagemImagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagemImagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2 ]
        elif self.contagemImagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagemImagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagemImagem = 0

        if self.angulo <= -70:
            self.imagem = self.IMGS[1]
            self.contagemImagem = self.TEMPO_ANIMACAO*2

        imagemRotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        novoAngulo = imagemRotacionada.get_rect(
            center = self.imagem.get_rect(topleft=(self.x, self.y)).center)
        tela.blit(imagemRotacionada, novoAngulo.topleft)

    def getMask(self):
        return pygame.mask.from_surface(self.imagem)
