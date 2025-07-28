import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import csv
from individuo import Individuo
from populacao import Populacao
from operadores import (
    elitismo_fixo, crossover_pmx, mutacao_swap, elitismo_percentual, selecao_torneio
)

# Configuração básica do experimento para 10 Rainhas
BASE_CONFIG = {
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


def experimenta_com_elitismo():
    elitismos = [elitismo_percentual, elitismo_fixo]  # Elitismo percentual e elitismo fixo
    resultados = []  # Para armazenar os resultados de cada experimento

    for elitismo_func in elitismos:
        cfg = BASE_CONFIG.copy()
        cfg['elitismo'] = elitismo_func  # Variando o elitismo
        
        for i in range(20):  # Repetir 20 vezes
            print(f"Executando experimento {i+1} com {elitismo_func.__name__}...")
            start = time.time()
            stats = run_experiment(cfg)  # Rodando o experimento
            duration = time.time() - start
            
            # Exibindo no console os resultados de cada execução
            print(f"Execução {i+1} - Tempo: {duration:.2f}s, Max Fitness: {stats['max_fitness']}, Solved: {stats['solved']}")
            
            # Armazenar os resultados de cada execução
            entry = {
                'elitismo': elitismo_func.__name__,
                'execucao': i + 1,
                'tempo': duration,
                **stats
            }
            resultados.append(entry)
    
  #Salvar os resultados em CSV
    filename = 'resultados_elitismo.csv'
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
        writer.writeheader()
        writer.writerows(resultados)
    print(f'Experimentos salvos em {filename}')

# Função para rodar o experimento com a configuração fornecida
def run_experiment(cfg):
    """
    Roda o experimento com a configuração fornecida e retorna as estatísticas.
    Essa função depende da implementação dos seus algoritmos genéticos.
    """
    n = cfg['n']  # Agora temos o valor de n para 10 rainhas
    pop_size = cfg['pop_size']
    max_gens = cfg['max_gens']
    selecao = cfg['selecao']
    crossover = cfg['crossover']
    mutacao = cfg['mutacao']
    elitismo_func = cfg['elitismo']
    
    if elitismo_func == elitismo_percentual:
        elitismo_args = {'taxa': 0.1}
    elif elitismo_func == elitismo_fixo:
        elitismo_args = {'k': 2}  # ou outro valor desejado para o número fixo de elites
    else:
        elitismo_args = {}


    # Criar a população
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
            'solved': True
        }
    
    # Evolução por gerações
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
        
        # Exibir o progresso ao final de cada geração
        max_fitness = max(fitness_vals)
        mean_fitness = sum(fitness_vals) / len(fitness_vals)
        min_fitness = min(fitness_vals)
        
        print(f"Geração {gen} - Máximo Fitness: {max_fitness}, Fitness Médio: {mean_fitness:.2f}, Mínimo Fitness: {min_fitness}")
        
        if max_fitness == max_pairs:
            return {
                'max_fitness': max_fitness,
                'mean_fitness': mean_fitness,
                'min_fitness': min_fitness,
                'gens_to_solve': gen,
                'solved': True
            }
    
    return {
        'max_fitness': max_fitness,
        'mean_fitness': mean_fitness,
        'min_fitness': min_fitness,
        'gens_to_solve': None,
        'solved': False
    }

# Rodar o experimento variando a seleção
experimenta_com_elitismo()  # Variando o operador de seleção