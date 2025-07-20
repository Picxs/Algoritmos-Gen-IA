import random
import matplotlib.pyplot as plt

def criar_individuo(n):
    """Cria um indivíduo aleatório garantindo 1 rainha por coluna"""
    individuo = list(range(n))  # uma rainha por coluna
    random.shuffle(individuo)  # embaralha as linhas
    return individuo

def contar_conflitos(individuo):
    """
    Conta o número de pares de rainhas que se atacam.
    Considera conflitos em linhas, colunas (já garantido), e diagonais.
    """
    n = len(individuo)
    conflitos = 0

    for i in range(n):
        for j in range(i + 1, n):
            # Conflito em linha
            if individuo[i] == individuo[j]:
                conflitos += 1
            # Conflito em diagonal
            elif abs(individuo[i] - individuo[j]) == abs(i - j):
                conflitos += 1
    return conflitos

def fitness(individuo):
    """
    Fitness inverso ao número de conflitos: quanto MENOS conflitos, MELHOR.
    Solução perfeita: fitness máximo = 1.0
    """
    conflitos = contar_conflitos(individuo)
    return 1 / (1 + conflitos)

#TODO MAIS UMA MANEIRA DE SELEÇÃO
def selecao(populacao, fitnesses):
    """Seleciona dois pais usando roleta proporcional ao fitness"""
    total_fit = sum(fitnesses)
    probs = [f / total_fit for f in fitnesses]
    pais = random.choices(populacao, weights=probs, k=2)
    return pais[0], pais[1]


#TODO MAIS UMA MANEIRA DE CROSSOVER
def crossover(pai1, pai2):
    """Crossover de ponto único"""
    n = len(pai1)
    ponto = random.randint(1, n - 2)
    filho = pai1[:ponto] + [gene for gene in pai2 if gene not in pai1[:ponto]]
    return filho

#TODO MAIS UMA MANEIRA DE MUTAÇÃO
def mutacao(individuo, taxa=0.2):
    """Troca a posição de duas rainhas com uma certa probabilidade"""
    if random.random() < taxa:
        i, j = random.sample(range(len(individuo)), 2)
        individuo[i], individuo[j] = individuo[j], individuo[i]
    return individuo

def imprimir_tabuleiro(individuo):
    """Mostra o tabuleiro em formato de matriz com Q para rainhas"""
    n = len(individuo)
    for linha in range(n):
        linha_str = ""
        for coluna in range(n):
            if individuo[coluna] == linha:
                linha_str += " Q "
            else:
                linha_str += " X "
        print(linha_str)
    print()  # Linha em branco no final


def algoritmo_genetico(n, tamanho_pop=200, taxa_mutacao=0.15, max_geracoes=10000):
    """
    Executa o Algoritmo Genético SEM elitismo até encontrar uma solução perfeita
    """
    populacao = [criar_individuo(n) for _ in range(tamanho_pop)]
    historico_melhores = []

    for geracao in range(1, max_geracoes + 1):
        fitnesses = [fitness(ind) for ind in populacao]
        melhor_fit = max(fitnesses)
        pior_fit = min(fitnesses)
        fitness_medio = sum(fitnesses) / len(fitnesses)

        melhor_indice = fitnesses.index(melhor_fit)
        melhor_individuo = populacao[melhor_indice]
        historico_melhores.append(melhor_fit)

        print(f"\n=== Geração {geracao} ===")
        print(f"🔝 Melhor fitness: {melhor_fit:.4f}")
        print(f"📉 Pior fitness:   {pior_fit:.4f}")
        print(f"📊 Fitness médio:  {fitness_medio:.4f}")
        print("Melhor indivíduo desta geração:")
        imprimir_tabuleiro(melhor_individuo)

        # Verifica se é uma solução perfeita (sem conflitos)
        if contar_conflitos(melhor_individuo) == 0:
            print("\n✅ Solução encontrada!")
            print(f"Solução em {geracao} gerações:\n")
            imprimir_tabuleiro(melhor_individuo)

            # Plot evolução
            plt.plot(historico_melhores)
            plt.title("Evolução do Melhor Fitness")
            plt.xlabel("Geração")
            plt.ylabel("Fitness")
            plt.show()
            return melhor_individuo

        # Cria nova população baseada no melhor indivíduo, mas SEM copiá-lo
        nova_populacao = []
        while len(nova_populacao) < tamanho_pop:
            # Sempre usa o melhor indivíduo como um dos pais
            pai1 = melhor_individuo
            pai2 = random.choice(populacao)
            filho = crossover(pai1, pai2)
            filho = mutacao(filho, taxa_mutacao)
            nova_populacao.append(filho)

        # Atualiza a população (não inclui o melhor_individuo atual)
        populacao = nova_populacao

    print("⚠️ Não foi encontrada uma solução perfeita no número máximo de gerações.")
    return None

if __name__ == "__main__":
    n = 3  # Tamanho do tabuleiro (n x n)
    if n < 4:
        print("selecione um n >= 4")
    else: 
        algoritmo_genetico(n)
