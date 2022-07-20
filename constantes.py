import pygame
import os

TELA_LARGURA = 500
TELA_ALTURA = 800

IMG_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
IMG_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
IMG_FUNDO = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
IMG_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
]

VELOCIDADE = 5