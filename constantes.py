import pygame
import os

TELA_LARGURA = 1280
TELA_ALTURA = 500

IMG_CANO = pygame.image.load(os.path.join("imgs", "pipe.png"))
IMG_CHAO = pygame.image.load(os.path.join("imgs", "base.png"))
IMG_FUNDO = pygame.image.load(os.path.join("imgs", "bg.png"))
IMG_PASSARO = [
    (pygame.image.load(os.path.join("imgs", "bird1.png"))),
    (pygame.image.load(os.path.join("imgs", "bird2.png"))),
    (pygame.image.load(os.path.join("imgs", "bird3.png")))
]

VELOCIDADE = 5