import pygame
import os
import random
import neat

aiJogando = False
geracao = 0

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

pygame.font.init()
fontePontos = pygame.font.SysFont("arial", 40)

class Passaro:
    IMGS = IMG_PASSARO

    ROTACAO_MAX = 25
    ROTACAO_VEL = 10
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
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

    def mover(self):
        self.tempo += 1
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


class Chao:
    velocidade = 5
    largura = IMG_CHAO.get_width()
    imagem = IMG_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.largura

    def mover(self):
        self.x1 -= self.velocidade
        self.x2 -= self.velocidade

        if self.x1 + self.largura < 0:
            self.x1 = self.x2 + self.largura
        if self.x2 + self.largura < 0:
            self.x2 = self.x1 + self.largura

    def desenha(self, tela):
        tela.blit(self.imagem, (self.x1, self.y))
        tela.blit(self.imagem, (self.x2, self.y))

def desenhaTela(tela, passaros, canos, chao, pontos):
    tela.blit(IMG_FUNDO, (0,0))
    for passaro in passaros:
        passaro.desenhar(tela)

    for cano in canos:
        cano.desenhar(tela)

    texto = fontePontos.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))

    if aiJogando:
        texto = fontePontos.render(f"Geração: {geracao}", 1, (255, 255, 255))
        tela.blit(texto, (10, 10))

    chao.desenha(tela)
    pygame.display.update()

def main(genomas, config):
    global geracao
    geracao += 1

    if aiJogando:
        redes = []
        listaGenomas = []
        passaros = []

        for _, genoma in genomas:
            rede = neat.nn.FeedForwardNetwork.create(genoma, config)
            redes.append(rede)
            genoma.fitness = 0
            listaGenomas.append(genoma)
            passaros.append(Passaro(230, 350))


    else:
        passaros = [Passaro(230, 350)]

    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()

            if not aiJogando:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        for passaro in passaros:
                            passaro.pular()

        indiceCano = 0
        if len(passaros) > 0:
            if len(canos) > 1 and passaros[0].x > (canos[0].x + canos[0].canoTopo.get_width()):
                indiceCano = 1
        else:
            rodando = False


        for i, passaro in enumerate(passaros):
            passaro.mover()

            if aiJogando:

                listaGenomas[i].fitness += 0.1
                output = redes[i].activate((passaro.y, abs(passaro.y - canos[indiceCano].altura), abs(passaro.y - canos[indiceCano].posBase)))

                if output[0] > 0.5:
                    passaro.pular()

        chao.mover()

        adicionarCano = False
        removerCanos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                    if aiJogando:
                        listaGenomas[i].fitness -= 1
                        listaGenomas.pop(i)
                        redes.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionarCano = True
            cano.mover()
            if cano.x + cano.canoTopo.get_width() < 0:
                removerCanos.append(cano)

        if adicionarCano:
            pontos += 1
            canos.append(Cano(600))
            if aiJogando:
                for genoma in listaGenomas:
                    genoma.fitness += 5
        for cano in removerCanos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)
                if aiJogando:
                    listaGenomas.pop(i)
                    redes.pop(i)

        desenhaTela(tela, passaros, canos, chao, pontos)

def rodar(caminhoConfig):
    config = neat.config.Config(neat.DefaultGenome
                                , neat.DefaultReproduction
                                , neat.DefaultSpeciesSet
                                , neat.DefaultStagnation
                                , caminhoConfig)
    populacao = neat.Population(config)
    populacao.add_reporter((neat.StdOutReporter(True)))
    populacao.add_reporter(neat.StatisticsReporter())

    if aiJogando:
        populacao.run(main)
    else:
        main(None, None)

if __name__ =="__main__":
    caminhoConfig = "config.txt"

    rodar(caminhoConfig)
