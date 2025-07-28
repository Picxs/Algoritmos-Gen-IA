import pandas as pd
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, 'imgs_resultados')
os.makedirs(IMG_DIR, exist_ok=True)

# Gráficos simples (gerações e população)
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

# Gráficos por execução (crossover, selecao, etc)
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

# Gráficos a partir de resultados_variacoes.csv
variacoes_path = os.path.join(BASE_DIR, 'resultados_variacoes.csv')
if os.path.exists(variacoes_path):
    df = pd.read_csv(variacoes_path)

    # 1. Relação tamanho de n entre variações (fitness médio por n e variação)
    pivot = df.groupby(['n', 'variacao'])['mean_fitness'].mean().unstack()
    pivot.plot(marker='o')
    plt.xlabel('Tamanho de n')
    plt.ylabel('Fitness Médio')
    plt.title('Fitness Médio por n e Variação')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'variacoes_por_n.png'))
    plt.close()
    print('Gerado: variacoes_por_n.png')

    # 2. Taxa de sucesso por variação
    sucesso = df.groupby('variacao')['solved'].apply(lambda x: x.sum() / len(x))
    sucesso.plot(kind='bar', color='skyblue')
    plt.ylabel('Taxa de Sucesso')
    plt.title('Taxa de Sucesso por Variação')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'taxa_sucesso_variacoes.png'))
    plt.close()
    print('Gerado: taxa_sucesso_variacoes.png')

    # 3. Média de gerações até resolver (somente True)
    media_gens = df[df['solved'] == True].groupby('variacao')['gens_to_solve'].mean()
    media_gens.plot(kind='bar', color='orange')
    plt.ylabel('Média de Gerações até Resolver')
    plt.title('Gerações Médias por Variação (Somente Soluções)')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'geracoes_media_variacoes.png'))
    plt.close()
    print('Gerado: geracoes_media_variacoes.png')

    # 4. Fitness médio por valor de n
    media_n = df.groupby('n')['mean_fitness'].mean()
    media_n.plot(marker='o', color='green')
    plt.xlabel('n')
    plt.ylabel('Fitness Médio')
    plt.title('Fitness Médio por Valor de n')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'fitness_medio_por_n.png'))
    plt.close()
    print('Gerado: fitness_medio_por_n.png')
else:
    print('Arquivo resultados_variacoes.csv não encontrado')
