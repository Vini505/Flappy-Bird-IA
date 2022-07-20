from constantes import *

class Solo:
    largura = IMG_SOLO.get_width()
    imagem = IMG_SOLO
    y = 450

    def __init__(self, x):
        self.x = x

    def mover(self):
        self.x -= VELOCIDADE_BASE

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))
