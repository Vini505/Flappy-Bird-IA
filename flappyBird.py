import pygame
import neat

from constantes import *
from objetos import Arvore, Cano, Ceu, Nuvem, Passaro, Predios, Solo

aiJogando = True
geracao = 0

pygame.font.init()
fontePontos = pygame.font.SysFont("arial", 40)

def desenhaTela(tela, passaros, canos, cenarios, pontos):

    for lista in cenarios:
        for obj in lista:
            obj.desenhar(tela)

    for passaro in passaros:
        passaro.desenhar(tela)

    for cano in canos:
        cano.desenhar(tela)

    texto = fontePontos.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))

    if aiJogando:
        texto = fontePontos.render(f"Geração: {geracao}", 1, (255, 255, 255))
        tela.blit(texto, (10, 10))

    pygame.display.update()

def main(genomas, config):
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
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
            passaros.append(Passaro(200, 250))
    else:
        passaros = [Passaro(200, 250)]


    cenarios = [
        [Ceu(0)],
        [Nuvem(0)],
        [Predios(0)],
        [Arvore(0)],
        [Solo(0)]
        ]

    canos = [Cano(700)]

    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(VELOCIDADE_JOGO)

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
            passaro.cair()

            if aiJogando:
                # TODO passaro nao ta avancando
                listaGenomas[i].fitness += 0.1
                output = redes[i].activate((passaro.y
                                            , abs(passaro.y - canos[indiceCano].altura)
                                            , abs(passaro.y - canos[indiceCano].posBase)
                                            , canos[indiceCano].velocidade))

                # output = redes[i].activate((passaro.y
                #                             , abs(passaro.y - (canos[indiceCano].altura + Cano.distanciaY/2))
                #                             , canos[indiceCano].velocidade))

                if output[0] > 0.5:
                    passaro.pular()

        for lista in cenarios:

            for obj in lista:
                tipo = type(obj)
                obj.mover()

            if lista[0].x + lista[0].largura < 0:
                    lista.pop(0)

            if lista[-1].x <= TELA_LARGURA:
                lista.append(tipo(lista[-1].x + tipo.largura))

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
                    pontos += 1
                    if aiJogando:
                        for genoma in listaGenomas:
                            genoma.fitness += 5

            if cano.x + cano.canoTopo.get_width() < 0:
                removerCanos.append(cano)

            cano.mover()

        if canos[-1].x + canos[-1].distanciaX <= TELA_LARGURA:
            canos.append(Cano(canos[-1].x + canos[-1].distanciaX))

        for cano in removerCanos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > Solo.y or passaro.y < 0:
                passaros.pop(i)
                if aiJogando:
                    listaGenomas[i].fitness -= 10
                    listaGenomas.pop(i)
                    redes.pop(i)

        desenhaTela(tela, passaros, canos, cenarios, pontos)
        pygame.display.update()

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
