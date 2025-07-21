import argparse
import random
import json
import sys
from individuo import Individuo
from populacao import Populacao
from operadores import (
    selecao_roleta, selecao_torneio, selecao_truncamento, selecao_ranking,
    crossover_ponto_unico, crossover_ordem, crossover_pmx, crossover_uniforme,
    mutacao_swap, mutacao_deslocamento, mutacao_inversao, mutacao_scramble,
    elitismo_none, elitismo_fixo, elitismo_percentual, elitismo_threshold
)

# Mapeamento de nome para função
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
    'none': elitismo_none,
    'fixo': elitismo_fixo,
    'percentual': elitismo_percentual,
    'threshold': elitismo_threshold,
}

def print_tabuleiro(genes):
    """
    Imprime o tabuleiro n x n usando:
    'R' para rainha e '.' para casas vazias.
    genes[i] indica a linha da rainha na coluna i.
    """
    n = len(genes)
    for linha in range(n):
        linha_str = ''
        for col in range(n):
            if genes[col] == linha:
                linha_str += 'R '
            else:
                linha_str += '. '
        print(linha_str.rstrip())


def parse_args():
    parser = argparse.ArgumentParser(description='Algoritmo Genético para n-Rainhas')
    parser.add_argument('--config', required=True, help='Caminho para arquivo de configuração JSON')
    return parser.parse_args()


def load_config(path):
    with open(path) as f:
        return json.load(f)


def main():
    args = parse_args()
    config = load_config(args.config)

    # Fixar seed, se fornecida
    seed = config.get('seed')
    if seed is not None:
        random.seed(seed)

    n = config['n']
    pop_size = config['pop_size']
    max_gens = config['max_gens']

    # Seleção e operadores
    selecao = SELECOES[config.get('selecao', 'torneio')]
    crossover = CROSSOVERS[config.get('crossover', 'ponto_unico')]
    mutacao = MUTACOES[config.get('mutacao', 'swap')]
    elitismo = ELITISMOS[config.get('elitismo', 'none')]

    p_crossover = config.get('p_crossover', 0.8)
    p_mutacao = config.get('p_mutacao', 0.1)

    # Parâmetros extras para elitismo
    elitismo_args = None
    tipo = config.get('elitismo')
    if tipo == 'fixo':
        elitismo_args = {'k': config.get('elitismo_k', 1)}
    elif tipo == 'percentual':
        elitismo_args = {'taxa': config.get('elitismo_taxa', 0.1)}
    elif tipo == 'threshold':
        elitismo_args = {'threshold': config.get('elitismo_threshold', 0)}

    # Inicializa população
    pop = Populacao(n, pop_size)
    pop.inicializa()
    pop.avalia()

    max_pairs = n * (n - 1) // 2

    # Estatísticas e checagem da geração 0
    fitness_vals = [ind.fitness_value for ind in pop.individuos]
    print(f'Geração 0: f_max = {max(fitness_vals)}, f_medio = {sum(fitness_vals)/len(fitness_vals):.2f}, f_min = {min(fitness_vals)}')
    if max(fitness_vals) == max_pairs:
        best = pop.melhor()
        print('\nSolução encontrada na geração 0:')
        print_tabuleiro(best.genes)
        sys.exit(0)

    # Loop de gerações
    for gen in range(1, max_gens + 1):
        pop.gera_nova_geracao(
            selecao=selecao,
            crossover=crossover,
            p_crossover=p_crossover,
            mutacao=mutacao,
            p_mutacao=p_mutacao,
            elitismo=elitismo,
            elitismo_args=elitismo_args
        )
        fitness_vals = [ind.fitness_value for ind in pop.individuos]
        max_f = max(fitness_vals)
        min_f = min(fitness_vals)
        mean_f = sum(fitness_vals) / len(fitness_vals)
        print(f'Geração {gen}: f_max = {max_f}, f_medio = {mean_f:.2f}, f_min = {min_f}')

        if max_f == max_pairs:
            best = pop.melhor()
            print(f'\nSolução encontrada na geração {gen}:')
            print_tabuleiro(best.genes)
            break
    else:
        print('Nenhuma solução perfeita encontrada até o limite de gerações.')

if __name__ == '__main__':
    main()