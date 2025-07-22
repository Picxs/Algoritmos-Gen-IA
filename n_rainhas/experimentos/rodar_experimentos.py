import sys
import os
# Adiciona o diretório pai ao path para permitir imports dos módulos principais
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import csv
import random
from individuo import Individuo
from populacao import Populacao
from operadores import (
    selecao_roleta, selecao_torneio, selecao_truncamento, selecao_ranking,
    crossover_ponto_unico, crossover_ordem, crossover_pmx, crossover_uniforme,
    mutacao_swap, mutacao_deslocamento, mutacao_inversao, mutacao_scramble,
    elitismo_none, elitismo_fixo, elitismo_percentual, elitismo_threshold
)

# SEED: valor para inicializar o gerador aleatório, garantindo reprodutibilidade dos resultados
# Variantes clássicas de operadores
SELECOES = {
    'roleta': selecao_roleta,
    'torneio': selecao_torneio,
    'truncamento': selecao_truncamento,
    'ranking': selecao_ranking,
}
CROSSOVERS = {
    'ponto_unico': crossover_ponto_unico,
    'ordem': crossover_ordem,
    'pmx': crossover_pmx,
    'uniforme': crossover_uniforme,
}
MUTACOES = {
    'swap': mutacao_swap,
    'deslocamento': mutacao_deslocamento,
    'inversao': mutacao_inversao,
    'scramble': mutacao_scramble,
}
ELITISMOS = {
    'none': (elitismo_none, {}),
    'fixo': (elitismo_fixo, {'k': 2}),
    'percentual': (elitismo_percentual, {'taxa': 0.1}),
    'threshold': (elitismo_threshold, {'threshold': 0}),
}

# Parâmetros básicos fixos para todos experimentos
BASE_CONFIG = {
    'pop_size': 100,
    'max_gens': 500,
    'seed': None,
    'p_crossover': 0.8,
    'p_mutacao': 0.1,
}

# Tamanhos de tabuleiro a testar e quantidade de seeds
NS = [8, 16, 32, 64]
REPEATS = 10

# Garante diretório de resultados
os.makedirs('resultados', exist_ok=True)

def run_experiment(cfg):
    """
    Executa o AG com a configuração e retorna estatísticas:
    max_fitness, mean_fitness, min_fitness, gens_to_solve, solved
    """
    # Inicializa gerador aleatório com seed para reprodutibilidade
    if cfg.get('seed') is not None:
        random.seed(cfg['seed'])
    n = cfg['n']
    pop_size = cfg['pop_size']
    max_gens = cfg['max_gens']
    # Seleciona operadores
    selecao = SELECOES[cfg['selecao']]
    crossover = CROSSOVERS[cfg['crossover']]
    mutacao = MUTACOES[cfg['mutacao']]
    elitismo_func, elitismo_args = ELITISMOS[cfg['elitismo']]
    # Cria e avalia população inicial
    pop = Populacao(n, pop_size)
    pop.inicializa(); pop.avalia()
    max_pairs = n * (n - 1) // 2
    fitness_vals = [ind.fitness_value for ind in pop.individuos]
    # Checa solução na geração 0
    if max(fitness_vals) == max_pairs:
        return {
            'max_fitness': max_pairs,
            'mean_fitness': sum(fitness_vals)/len(fitness_vals),
            'min_fitness': min(fitness_vals),
            'gens_to_solve': 0,
            'solved': True
        }
    # Loop de gerações
    for gen in range(1, max_gens+1):
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
        if max(fitness_vals) == max_pairs:
            return {
                'max_fitness': max(fitness_vals),
                'mean_fitness': sum(fitness_vals)/len(fitness_vals),
                'min_fitness': min(fitness_vals),
                'gens_to_solve': gen,
                'solved': True
            }
    # Não solucionou
    return {
        'max_fitness': max(fitness_vals),
        'mean_fitness': sum(fitness_vals)/len(fitness_vals),
        'min_fitness': min(fitness_vals),
        'gens_to_solve': None,
        'solved': False
    }

if __name__ == '__main__':
    def sweep(component, variants, fixed_cfg):
        resultados = []
        for variant in variants:
            for n in NS:
                for seed in range(REPEATS):
                    cfg = BASE_CONFIG.copy()
                    cfg.update(fixed_cfg)
                    cfg['n'] = n
                    cfg['seed'] = seed
                    cfg[component] = variant
                    start = time.time()
                    stats = run_experiment(cfg)
                    duration = time.time() - start
                    entry = {
                        'component': component,
                        'variant': variant,
                        'n': n,
                        'seed': seed,
                        'tempo': duration,
                        **stats
                    }
                    resultados.append(entry)
        filename = f'resultados/{component}_sweep.csv'
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
            writer.writeheader()
            writer.writerows(resultados)
        print(f'Sweep para {component} salvo em {filename}')

    # Execução de sweeps para cada componente
    sweep('selecao', list(SELECOES.keys()),
          {'crossover': 'ponto_unico', 'mutacao': 'swap', 'elitismo': 'none'})
    sweep('crossover', list(CROSSOVERS.keys()),
          {'selecao': 'torneio', 'mutacao': 'swap', 'elitismo': 'none'})
    sweep('mutacao', list(MUTACOES.keys()),
          {'selecao': 'torneio', 'crossover': 'ponto_unico', 'elitismo': 'none'})
    sweep('elitismo', list(ELITISMOS.keys()),
          {'selecao': 'torneio', 'crossover': 'ponto_unico', 'mutacao': 'swap'})