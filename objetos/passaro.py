import pygame

from constantes import *

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
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def cair(self):
        self.tempo += 1
        print()
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento += -2

        self.y += deslocamento

        if deslocamento < 0:
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
