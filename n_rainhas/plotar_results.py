import pandas as pd
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, 'imgs_resultados')
os.makedirs(IMG_DIR, exist_ok=True)

arquivos_simples = {
    'resultados_geracoes.csv': ('max_gens', 'Gerações'),
    'resultados_populacao.csv': ('pop_size', 'População'),
}

for nome_arquivo, (eixo_x, titulo) in arquivos_simples.items():
    caminho = os.path.join(BASE_DIR, nome_arquivo)
    if not os.path.exists(caminho):
        print(f'Arquivo não encontrado: {caminho}')
        continue

    df = pd.read_csv(caminho).dropna(subset=['mean_fitness'])
    if df[eixo_x].dtype == object:
        df[eixo_x] = pd.to_numeric(df[eixo_x], errors='coerce')

    plt.figure(figsize=(8, 5))
    plt.plot(df[eixo_x], df['mean_fitness'], marker='o')
    plt.xlabel(eixo_x)
    plt.ylabel('Fitness Médio')
    plt.title(f'{titulo} – Fitness Médio')
    plt.grid(True)
    plt.tight_layout()
    nome_img = f'{titulo.lower()}_mean_fitness.png'.replace('ç', 'c')
    plt.savefig(os.path.join(IMG_DIR, nome_img))
    plt.close()
    print('Gerado:', nome_img)

arquivos_execucao = {
    'resultados_crossover.csv': ('crossover', 'Crossover'),
    'resultados_selecao.csv': ('selecao', 'Seleção'),
    'resultados_elitismo.csv': ('elitismo', 'Elitismo'),
    'resultados_mutacao.csv': ('mutacao', 'Mutação'),
}

for nome_arquivo, (coluna_categoria, titulo) in arquivos_execucao.items():
    caminho = os.path.join(BASE_DIR, nome_arquivo)
    if not os.path.exists(caminho):
        print(f'Arquivo não encontrado: {caminho}')
        continue

    df = pd.read_csv(caminho).dropna(subset=['mean_fitness'])

    plt.figure(figsize=(10, 6))
    for cat in df[coluna_categoria].unique():
        dados = df[df[coluna_categoria] == cat]
        plt.plot(dados['execucao'], dados['mean_fitness'], marker='o', label=str(cat))

    plt.xlabel('Execução')
    plt.ylabel('Fitness Médio')
    plt.title(f'{titulo} – Fitness Médio por Execução')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    nome_img = f'{titulo.lower()}_mean_fitness_linhas.png'.replace('ç', 'c')
    plt.savefig(os.path.join(IMG_DIR, nome_img))
    plt.close()
    print('Gerado:', nome_img)
