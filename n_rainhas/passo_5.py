import sys
import os
import time
import csv
import multiprocessing
from individuo import Individuo
from populacao import Populacao
from operadores import (
    crossover_pmx, mutacao_scramble, elitismo_percentual,
    selecao_torneio, mutacao_swap
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


BASE_CONFIG_CROSS = {
    'n': 10,  # Número de rainhas (10)
    'pop_size': 150,  # Tamanho da população
    'max_gens': 1000,  # Número de gerações
    'seed': None,      # Semente aleatória
    'p_crossover': 0.8,  # Taxa de crossover
    'p_mutacao': 0.05,  # Taxa de mutação
    'selecao': selecao_torneio,
    'crossover': crossover_pmx,  # Operador de crossover
    'mutacao': mutacao_swap,  # Operador de mutação
    'elitismo': elitismo_percentual,  # Operador de elitismo
}

BASE_CONFIG_ELITE = {
    'n': 10,  # Número de rainhas (10)
    'pop_size': 150,  # Tamanho da população
    'max_gens': 1000,  # Número de gerações
    'seed': None,      # Semente aleatória
    'p_crossover': 0.8,  # Taxa de crossover
    'p_mutacao': 0.05,  # Taxa de mutação
    'selecao': selecao_torneio,
    'crossover': crossover_pmx,  # Operador de crossover
    'mutacao': mutacao_swap,  # Operador de mutação
    'elitismo': elitismo_percentual,  # Operador de elitismo
}

BASE_CONFIG_MUTA = {
    'n': 10,  # Número de rainhas (10)
    'pop_size': 150,  # Tamanho da população
    'max_gens': 1000,  # Número de gerações
    'seed': None,      # Semente aleatória
    'p_crossover': 0.8,  # Taxa de crossover
    'p_mutacao': 0.05,  # Taxa de mutação
    'selecao': selecao_torneio,
    'crossover': crossover_pmx,  # Operador de crossover
    'mutacao': mutacao_scramble,  # Operador de mutação
    'elitismo': elitismo_percentual,  # Operador de elitismo
}
BASE_CONFIG_SELE = {
    'n': 10,  # Número de rainhas (10)
    'pop_size': 150,  # Tamanho da população
    'max_gens': 1000,  # Número de gerações
    'seed': None,      # Semente aleatória
    'p_crossover': 0.8,  # Taxa de crossover
    'p_mutacao': 0.05,  # Taxa de mutação
    'selecao': selecao_torneio,
    'crossover': crossover_pmx,  # Operador de crossover
    'mutacao': mutacao_swap,  # Operador de mutação
    'elitismo': elitismo_percentual,  # Operador de elitismo
}


# Função para criar uma cópia com valor n atualizado
def atualizar_config(base_cfg, n):
    cfg = base_cfg.copy()
    cfg['n'] = n
    return cfg

# Função para rodar o experimento e retornar os resultados
def run_experiment_wrapper(args):
    base_cfg, nome_base = args
    n = base_cfg['n']
    resultado_final = None

    while True:
        cfg = atualizar_config(base_cfg, n)
        result = run_experiment(cfg)
        salvar_resultado_em_csv({
            'variacao': nome_base,
            'n': n,
            **result
        })
        if result['solved'] or cfg['max_gens'] == result.get('gens_to_solve', cfg['max_gens']):
            n += 1

# Salvar resultados incrementalmente em CSV
def salvar_resultado_em_csv(dados, filename='resultados_variacoes.csv'):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=dados.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(dados)

# Função principal do experimento
def run_experiment(cfg):
    n = cfg['n']
    pop_size = cfg['pop_size']
    max_gens = cfg['max_gens']
    selecao = cfg['selecao']
    crossover = cfg['crossover']
    mutacao = cfg['mutacao']
    elitismo_func = cfg['elitismo']

    if elitismo_func == elitismo_percentual:
        elitismo_args = {'taxa': 0.1}
    else:
        elitismo_args = {}

    pop = Populacao(n, pop_size)
    pop.inicializa()
    pop.avalia()

    max_pairs = n * (n - 1) // 2
    fitness_vals = [ind.fitness_value for ind in pop.individuos]

    if max(fitness_vals) == max_pairs:
        return {
            'max_fitness': max(fitness_vals),
            'mean_fitness': sum(fitness_vals)/len(fitness_vals),
            'min_fitness': min(fitness_vals),
            'gens_to_solve': 0,
            'solved': True,
            'tempo_execucao': 0
        }

    start = time.time()
    for gen in range(1, max_gens + 1):
        pop.gera_nova_geracao(
            selecao=selecao,
            crossover=crossover,
            p_crossover=cfg['p_crossover'],
            mutacao=mutacao,
            p_mutacao=cfg['p_mutacao'],
            elitismo=elitismo_func,
            elitismo_args=elitismo_args
        )
        fitness_vals = [ind.fitness_value for ind in pop.individuos]
        max_fitness = max(fitness_vals)

        if max_fitness == max_pairs:
            duration = time.time() - start
            return {
                'max_fitness': max_fitness,
                'mean_fitness': sum(fitness_vals)/len(fitness_vals),
                'min_fitness': min(fitness_vals),
                'gens_to_solve': gen,
                'solved': True,
                'tempo_execucao': duration
            }

    duration = time.time() - start
    return {
        'max_fitness': max(fitness_vals),
        'mean_fitness': sum(fitness_vals)/len(fitness_vals),
        'min_fitness': min(fitness_vals),
        'gens_to_solve': None,
        'solved': False,
        'tempo_execucao': duration
    }

if __name__ == "__main__":
    # Configurações iniciais para as variações
    configs = [
        (BASE_CONFIG_CROSS, 'CROSSOVER'),
        (BASE_CONFIG_ELITE, 'ELITISMO'),
        (BASE_CONFIG_MUTA, 'MUTACAO'),
        (BASE_CONFIG_SELE, 'SELECAO')
    ]

    # Executar em paralelo
    with multiprocessing.Pool(processes=4) as pool:
        pool.map(run_experiment_wrapper, configs)


