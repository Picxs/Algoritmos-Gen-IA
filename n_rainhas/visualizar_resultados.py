import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

# --- CONFIGURAÇÃO ---
RESULTS_DIR = os.path.join(os.getcwd(), 'results')
OUTPUT_DIR = RESULTS_DIR  # Salva gráficos na mesma pasta
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Lista de arquivos CSV gerados
csv_files = glob.glob(os.path.join(RESULTS_DIR, '*_sweep.csv'))

if not csv_files:
    print('Nenhum arquivo *_sweep.csv encontrado em', RESULTS_DIR)
    exit(1)

for csv_path in csv_files:
    comp = os.path.basename(csv_path).replace('_sweep.csv', '')
    df = pd.read_csv(csv_path)

    # ----- 1) Boxplot de max_fitness por variante -----
    plt.figure(figsize=(8, 5))
    df.boxplot(column='max_fitness', by='variant')
    plt.title(f"{comp.capitalize()} – Distribuição de Max Fitness")
    plt.suptitle("")
    plt.xlabel('Variante')
    plt.ylabel('Max Fitness')
    plt.tight_layout()
    boxplot_file = os.path.join(OUTPUT_DIR, f'{comp}_boxplot.png')
    plt.savefig(boxplot_file)
    plt.close()
    print('Gerado:', boxplot_file)

    # ----- 2) Linha de médias de gens_to_solve vs n (para runs bem-sucedidos) -----
    if 'gens_to_solve' in df.columns:
        df_solved = df[df['solved'] == True]
        if not df_solved.empty:
            summary_gens = df_solved.groupby(['n','variant'])['gens_to_solve'].mean().unstack()
            plt.figure(figsize=(8, 5))
            for var in summary_gens.columns:
                plt.plot(summary_gens.index, summary_gens[var], marker='o', label=var)
            plt.title(f"{comp.capitalize()} – Média de Gerações Até Solução vs n")
            plt.xlabel('Tamanho do tabuleiro (n)')
            plt.ylabel('Média de Gerações')
            plt.legend(title='Variante')
            plt.tight_layout()
            gens_line_file = os.path.join(OUTPUT_DIR, f'{comp}_gens_line.png')
            plt.savefig(gens_line_file)
            plt.close()
            print('Gerado:', gens_line_file)
        else:
            print(f'Nenhum run bem-sucedido para {comp}, pulando gráfico de gerações.')

    # ----- 3) Taxa de sucesso por variante e n -----
    if 'solved' in df.columns:
        success_rate = df.groupby(['n','variant'])['solved'].mean().unstack()
        plt.figure(figsize=(8, 5))
        for var in success_rate.columns:
            plt.plot(success_rate.index, success_rate[var], marker='o', label=var)
        plt.title(f"{comp.capitalize()} – Taxa de Sucesso vs n")
        plt.xlabel('Tamanho do tabuleiro (n)')
        plt.ylabel('Taxa de Solução (%)')
        plt.legend(title='Variante')
        plt.tight_layout()
        rate_line_file = os.path.join(OUTPUT_DIR, f'{comp}_success_rate.png')
        plt.savefig(rate_line_file)
        plt.close()
        print('Gerado:', rate_line_file)

print('Visualização concluída! Abra os PNGs em', OUTPUT_DIR)
