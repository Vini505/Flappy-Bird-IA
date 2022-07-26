import pygame
import os

TELA_LARGURA = 1280
TELA_ALTURA = 500

IMG_CANO = pygame.image.load(os.path.join("imgs", "pipe.png"))
IMG_SOLO = pygame.image.load(os.path.join("imgs", "base.png"))
IMG_CEU = pygame.image.load(os.path.join("imgs", "bg1.png"))
IMG_NUVEM = pygame.image.load(os.path.join("imgs", "bg2.png"))
IMG_PREDIO = pygame.image.load(os.path.join("imgs", "bg3.png"))
IMG_ARVORE = pygame.image.load(os.path.join("imgs", "bg4.png"))
IMG_PASSARO = [
    (pygame.image.load(os.path.join("imgs", "bird1.png"))),
    (pygame.image.load(os.path.join("imgs", "bird2.png"))),
    (pygame.image.load(os.path.join("imgs", "bird3.png")))
]

VELOCIDADE_JOGO = 30
VELOCIDADE_BASE = 5