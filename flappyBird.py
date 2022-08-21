import pygame
import neat
from resources import populacao
from constantes import *
from objetos import Cano, Cenario, Passaro, Solo


aiJogando = True
geracao = 0
pause = True

pygame.font.init()
fontePontos = pygame.font.SysFont("arial", 40)

def desenhaTela(tela, passaros, canos, cenarios, solos, pontos):

    for lista in cenarios.values():
        for obj in lista:
            obj.desenhar(tela)

    for cano in canos:
        cano.desenhar(tela)

    for solo in solos:
        solo.desenhar(tela)

    for passaro in passaros:
        passaro.desenhar(tela)

    if pause == False:
        texto = fontePontos.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
        tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))

    if aiJogando and pause == False:
        texto = fontePontos.render(f"Geração: {geracao}", 1, (255, 255, 255))
        tela.blit(texto, (10, 10))

    pygame.display.update()

def gerarObjetos(genomas, config):

    if aiJogando:
        redes = []
        listaGenomas = []
        passaros = []

        for _, genoma in genomas:
            rede = neat.nn.FeedForwardNetwork.create(genoma, config)
            redes.append(rede)
            genoma.fitness = 0
            listaGenomas.append(genoma)
            passaros.append(Passaro(300, 250))
    else:
        passaros = [Passaro(300, 250)]


    cenarios = {
        "Ceu": [Cenario(0, 0, IMG_CEU, 0)]
        , "Nuvens": [Cenario(0, 320, IMG_NUVEM, VELOCIDADE_BASE-4)]
        , "Predios": [Cenario(0, 350, IMG_PREDIO, VELOCIDADE_BASE-3)]
        , "Arvores": [Cenario(0, 380, IMG_ARVORE, VELOCIDADE_BASE-2)]
        }

    solos = [Solo(0)]
    canos = [Cano(TELA_LARGURA)]
    
    return(cenarios, passaros, solos, canos, listaGenomas, redes)

def telaPause(relogio, cenarios, passaros, solos, pause):
    relogio.tick(VELOCIDADE_JOGO)

    for evento in pygame.event.get():
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pause = False

    for lista in cenarios.values():

        for obj in lista:
            obj.mover()

        if lista[0].x + lista[0].largura < 0:
            lista.pop(0)

        if lista[-1].x <= TELA_LARGURA:
            lista.append(Cenario(lista[-1].x + lista[-1].largura, lista[-1].y, lista[-1].imagem, lista[-1].velocidade))

    for passaro in passaros:
        passaro.pause()

    for solo in solos:
        solo.mover()

    if solos[0].x + solos[0].largura < 0:
            solos.pop(0)

    if solos[-1].x <= TELA_LARGURA:
        solos.append(Solo(solos[-1].x + solo.largura))

    return(pause)

def main(genomas, config, variaveis):
    global geracao
    global pause
    rodando = True
    
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    
    pontos = 0
    relogio = pygame.time.Clock()

    cenarios, passaros, solos, canos, listaGenomas, redes = gerarObjetos(genomas, config)

    while pause:
        pause = telaPause(relogio, cenarios, passaros, solos, pause)

        desenhaTela(tela, passaros, canos, cenarios, solos, pontos)
        pygame.display.update()


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
                listaGenomas[i].fitness += 0.1

                output = redes[i].activate((passaro.y
                                            , (passaro.x - canos[indiceCano].x)
                                            , (passaro.y - canos[indiceCano].posBase)
                                            , canos[indiceCano].velocidade))

                if output[0] > 0.5:
                    passaro.pular()

        for lista in cenarios.values():

            for obj in lista:
                obj.mover()

            if lista[0].x + lista[0].largura < 0:
                lista.pop(0)

            if lista[-1].x <= TELA_LARGURA:
                lista.append(Cenario(lista[-1].x + lista[-1].largura, lista[-1].y, lista[-1].imagem, lista[-1].velocidade))

        for solo in solos:
            solo.mover()

        if solos[0].x + solos[0].largura < 0:
                solos.pop(0)

        if solos[-1].x <= TELA_LARGURA:
            solos.append(Solo(solos[-1].x + solo.largura))

        removerCanos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                    if aiJogando:
                        listaGenomas[i].fitness -= 1
                        listaGenomas.pop(i)
                        redes.pop(i)
                if not cano.passou and passaro.x > cano.x + (cano.canoTopo.get_width()):
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

        desenhaTela(tela, passaros, canos, cenarios, solos, pontos)
        pygame.display.update()

def rodar(caminhoConfig):
    config = neat.config.Config(neat.DefaultGenome
                                , neat.DefaultReproduction
                                , neat.DefaultSpeciesSet
                                , neat.DefaultStagnation
                                , caminhoConfig)
    populacoes = populacao.Populacao(config)
    populacoes.add_reporter((neat.StdOutReporter(True)))
    populacoes.add_reporter(neat.StatisticsReporter())

    variaveis = populacoes.generation

    if aiJogando:
        populacoes.run(main, variaveis)
    else:
        main(None, None, None)

if __name__ =="__main__":
    caminhoConfig = "config.txt"

    rodar(caminhoConfig)
