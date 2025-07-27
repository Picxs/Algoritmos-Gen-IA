import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import csv
from individuo import Individuo
from populacao import Populacao
from operadores import (
    selecao_torneio, selecao_ranking, selecao_roleta, selecao_truncamento,
    crossover_pmx, crossover_uniforme, crossover_ponto_unico, crossover_ordem,
    mutacao_swap, mutacao_deslocamento, mutacao_inversao, mutacao_scramble,
    elitismo_percentual, elitismo_fixo, elitismo_none, elitismo_threshold
)

BASE_CONFIG = {
    'pop_size': 100,  # Tamanho inicial da população
    'max_gens': 500,  # Número inicial de gerações
    'seed': None,     # Semente aleatória
    'p_crossover': 0.8,  # Taxa de crossover
    'p_mutacao': 0.05,  # Taxa de mutação
    'selecao': selecao_torneio,  # Operador de seleção inicial
    'crossover': crossover_pmx,  # Operador de crossover inicial
    'mutacao': mutacao_swap,  # Operador de mutação inicial
    'elitismo': elitismo_percentual,  # Operador de elitismo inicial
}

# Função para rodar o experimento com diferentes tamanhos de população
def experimenta_com_tamanho_populacao():
    tamanhos_populacao = [50, 100, 150, 200]
    
    resultados = []  # Para armazenar os resultados de cada experimento

    for pop_size in tamanhos_populacao:
        cfg = BASE_CONFIG.copy()
        cfg['pop_size'] = pop_size
        
        start = time.time()
        stats = run_experiment(cfg)  # Chama a função para rodar o experimento
        duration = time.time() - start
        
        # Armazenando os resultados
        entry = {
            'pop_size': pop_size,
            'tempo': duration,
            **stats
        }
        resultados.append(entry)
    
    # Salvar os resultados em CSV
    filename = 'resultados_populacao.csv'
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
        writer.writeheader()
        writer.writerows(resultados)
    print(f'Experimentos salvos em {filename}')

# Função para rodar o experimento com diferentes números de gerações
def experimenta_com_numero_de_geracoes():
    geracoes = [100, 500, 1000]
    
    resultados = []

    for max_gens in geracoes:
        cfg = BASE_CONFIG.copy()
        cfg['max_gens'] = max_gens
        
        start = time.time()
        stats = run_experiment(cfg)
        duration = time.time() - start
        
        entry = {
            'max_gens': max_gens,
            'tempo': duration,
            **stats
        }
        resultados.append(entry)
    
    # Salvar os resultados em CSV
    filename = 'resultados_geracoes.csv'
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
        writer.writeheader()
        writer.writerows(resultados)
    print(f'Experimentos salvos em {filename}')

# Função para rodar o experimento com diferentes taxas de crossover
def experimenta_com_taxa_crossover():
    taxas_crossover = [0.6, 0.8, 1.0]
    
    resultados = []

    for p_crossover in taxas_crossover:
        cfg = BASE_CONFIG.copy()
        cfg['p_crossover'] = p_crossover
        
        start = time.time()
        stats = run_experiment(cfg)
        duration = time.time() - start
        
        entry = {
            'p_crossover': p_crossover,
            'tempo': duration,
            **stats
        }
        resultados.append(entry)
    
    # Salvar os resultados em CSV
    filename = 'resultados_crossover.csv'
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
        writer.writeheader()
        writer.writerows(resultados)
    print(f'Experimentos salvos em {filename}')

# Função para rodar o experimento com diferentes taxas de mutação
def experimenta_com_taxa_mutacao():
    taxas_mutacao = [0.01, 0.05, 0.1]
    
    resultados = []

    for p_mutacao in taxas_mutacao:
        cfg = BASE_CONFIG.copy()
        cfg['p_mutacao'] = p_mutacao
        
        start = time.time()
        stats = run_experiment(cfg)
        duration = time.time() - start
        
        entry = {
            'p_mutacao': p_mutacao,
            'tempo': duration,
            **stats
        }
        resultados.append(entry)
    
    # Salvar os resultados em CSV
    filename = 'resultados_mutacao.csv'
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
        writer.writeheader()
        writer.writerows(resultados)
    print(f'Experimentos salvos em {filename}')

# Dentro da função run_experiment
def run_experiment(cfg):
    """
    Roda o experimento com a configuração fornecida e retorna as estatísticas.
    Essa função depende da implementação dos seus algoritmos genéticos.
    """
    n = cfg['pop_size']
    max_gens = cfg['max_gens']
    selecao = cfg['selecao']
    crossover = cfg['crossover']
    mutacao = cfg['mutacao']
    elitismo_func = cfg['elitismo']
    
    # Passando o argumento "taxa" se o elitismo for percentual
    if elitismo_func == elitismo_percentual:
        elitismo_args = {'taxa': 0.1}  # Exemplo de taxa de 10%
    else:
        elitismo_args = {}

    pop = Populacao(n, max_gens)
    pop.inicializa()
    pop.avalia()
    
    max_pairs = n * (n - 1) // 2
    fitness_vals = [ind.fitness_value for ind in pop.individuos]
    
    if max(fitness_vals) == max_pairs:
        return {
            'max_fitness': max_pairs,
            'mean_fitness': sum(fitness_vals)/len(fitness_vals),
            'min_fitness': min(fitness_vals),
            'gens_to_solve': 0,
            'solved': True
        }
    
    for gen in range(1, max_gens + 1):
        pop.gera_nova_geracao(
            selecao=selecao,
            crossover=crossover,
            p_crossover=cfg['p_crossover'],
            mutacao=mutacao,
            p_mutacao=cfg['p_mutacao'],
            elitismo=elitismo_func,
            elitismo_args=elitismo_args  # Passando elitismo_args aqui
        )
        fitness_vals = [ind.fitness_value for ind in pop.individuos]
        if max(fitness_vals) == max_pairs:
            return {
                'max_fitness': max(fitness_vals),
                'mean_fitness': sum(fitness_vals)/len(fitness_vals),
                'min_fitness': min(fitness_vals),
                'gens_to_solve': gen,
                'solved': True
            }
    
    return {
        'max_fitness': max(fitness_vals),
        'mean_fitness': sum(fitness_vals)/len(fitness_vals),
        'min_fitness': min(fitness_vals),
        'gens_to_solve': None,
        'solved': False
    }


# Rodar experimentos
experimenta_com_tamanho_populacao()  # Variar o tamanho da população
experimenta_com_numero_de_geracoes()  # Variar o número de gerações
experimenta_com_taxa_crossover()  # Variar a taxa de crossover
experimenta_com_taxa_mutacao()  # Variar a taxa de mutação