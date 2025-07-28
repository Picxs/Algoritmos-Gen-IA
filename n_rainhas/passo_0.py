# parte_0.py

import time
import csv
import statistics
import random
from operadores import (
    selecao_torneio,
    crossover_pmx,
    mutacao_swap,
    elitismo_percentual
)
from populacao import Populacao
from individuo import Individuo


# --- CONFIGURAÇÕES DO EXPERIMENTO ---
N_RAINHAS = 25 
N_EXECUCOES = 5

# Parâmetros numéricos a serem testados
TAMANHOS_POP = [100, 150]
N_GERACOES_LISTA = [200, 500]
TAXAS_MUTACAO = [0.05, 0.1]
TAXAS_CROSSOVER = [0.8, 1.0]
TAXAS_ELITISMO = [0.02, 0.1]

def rodar_experimento_parte0():
    """Orquestra a execução, salva o CSV detalhado e imprime um resumo."""
    nome_arquivo_csv = 'resultados_parte0.csv'
    
    cabecalho_csv = [
        "componente", "variante", "n_rainhas", "semente", "tempo_s", 
        "fitness_maximo", "fitness_medio", "fitness_minimo", 
        "geracoes_para_solucao", "solucionado"
    ]

    melhor_config = None
    melhor_fitness_medio = float('-inf')  # Começa com o pior valor possível

    with open(nome_arquivo_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(cabecalho_csv)

        # Loop para testar diferentes combinações de parâmetros numéricos
        for tam_pop in TAMANHOS_POP:
            for n_geracoes in N_GERACOES_LISTA:
                for p_crossover in TAXAS_CROSSOVER:
                    for p_mutacao in TAXAS_MUTACAO:
                        for taxa_elitismo in TAXAS_ELITISMO:
                            
                            config_str = f"Pop={tam_pop}, Ger={n_geracoes}, pC={p_crossover}, pM={p_mutacao}, Elite%={taxa_elitismo}"
                            print(f"\n--- Testando Configuração: {config_str} ---")
                            
                            medias = []
                            
                            for i in range(N_EXECUCOES):
                                semente_atual = random.randint(0, 100000)
                                print(f" Execução {i+1}/{N_EXECUCOES} (Semente: {semente_atual})...")
                                
                                # Chama a função e recebe o dicionário de resultados
                                resultados = executar_ag(
                                    n_rainhas=N_RAINHAS, tam_pop=tam_pop, n_geracoes=n_geracoes,
                                    p_crossover=p_crossover, p_mutacao=p_mutacao,
                                    func_selecao=selecao_torneio, func_crossover=crossover_pmx,
                                    func_mutacao=mutacao_swap, func_elitismo=elitismo_percentual,
                                    elitismo_args={'taxa': taxa_elitismo},
                                    semente=semente_atual,
                                    verbose=True
                                )

                                medias.append(resultados['fitness_medio'])

                                # Escreve no CSV
                                writer.writerow([
                                    "Baseline",
                                    f"Torn.{p_crossover:.2f}C.{p_mutacao:.2f}M.{taxa_elitismo:.2f}E",
                                    N_RAINHAS,
                                    semente_atual,
                                    f"{resultados['tempo_s']:.4f}",
                                    resultados['fitness_maximo'],
                                    f"{resultados['fitness_medio']:.2f}",
                                    resultados['fitness_minimo'],
                                    resultados['geracoes_para_solucao'],
                                    resultados['solucionado']
                                ])

                            media_geral = statistics.mean(medias)

                            if media_geral > melhor_fitness_medio:
                                melhor_fitness_medio = media_geral
                                melhor_config = {
                                    'pop': tam_pop,
                                    'ger': n_geracoes,
                                    'p_crossover': p_crossover,
                                    'p_mutacao': p_mutacao,
                                    'taxa_elitismo': taxa_elitismo,
                                    'fitness_medio': media_geral
                                }
    
    print(f"\nExperimento concluído! Resultados detalhados salvos em '{nome_arquivo_csv}'")

    if melhor_config:
        print("\n🔝 Melhor configuração encontrada (com base no fitness médio):")
        print(f"  - Tamanho da população: {melhor_config['pop']}")
        print(f"  - Número de gerações: {melhor_config['ger']}")
        print(f"  - Taxa de crossover: {melhor_config['p_crossover']}")
        print(f"  - Taxa de mutação: {melhor_config['p_mutacao']}")
        print(f"  - Taxa de elitismo: {melhor_config['taxa_elitismo']}")
        print(f"  - Fitness médio: {melhor_config['fitness_medio']:.2f}")

def executar_ag(n_rainhas, tam_pop, n_geracoes, p_crossover, p_mutacao, func_selecao, func_crossover, func_mutacao, func_elitismo, elitismo_args, semente=None, verbose=True):
    """
    Executa uma rodada do AG e retorna um dicionário com métricas detalhadas.
    """
    if semente is not None:
        random.seed(semente)

    inicio = time.time()

    pop = Populacao(n=n_rainhas, tamanho=tam_pop)
    pop.inicializa()
    pop.avalia()

    max_fitness_possivel = n_rainhas * (n_rainhas - 1) // 2
    solucionado = False
    geracoes_para_solucao = -1
    
    for geracao in range(n_geracoes):
        pop.gera_nova_geracao(
            selecao=func_selecao,
            crossover=func_crossover,
            p_crossover=p_crossover,
            mutacao=func_mutacao,
            p_mutacao=p_mutacao,
            elitismo=func_elitismo,
            elitismo_args=elitismo_args
        )
        
        if verbose:
            fitness_geracao = [ind.fitness_value for ind in pop.individuos]
            print(f"  [Geração {geracao + 1:03d}] "
                  f"Melhor Fitness: {max(fitness_geracao)} | "
                  f"Fitness Médio: {statistics.mean(fitness_geracao):.2f} | "
                  f"Pior Fitness: {min(fitness_geracao)}")

        if not solucionado and pop.melhor().fitness_value == max_fitness_possivel:
            solucionado = True
            geracoes_para_solucao = geracao + 1
            if verbose:
                print(f"  Solução ótima encontrada na geração {geracao + 1}!")
            # Continua executando até o final para ter as métricas da última geração
    
    fim = time.time()
    
    # Coleta as métricas finais
    fitness_final_pop = [ind.fitness_value for ind in pop.individuos]
    
    return {
        "tempo_s": fim - inicio,
        "fitness_maximo": max(fitness_final_pop),
        "fitness_medio": statistics.mean(fitness_final_pop),
        "fitness_minimo": min(fitness_final_pop),
        "solucionado": "sim" if solucionado else "nao",
        "geracoes_para_solucao": geracoes_para_solucao
    }


if __name__ == '__main__':
    rodar_experimento_parte0()