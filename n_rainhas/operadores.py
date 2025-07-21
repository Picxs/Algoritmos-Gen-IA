import random
import math
from individuo import Individuo

# Seleção

def selecao_roleta(populacao):
    """
    (Clássico) Seleção por roleta (fitness-proporcional):
    cada indivíduo é sorteado com probabilidade proporcional ao seu valor de fitness.
    """
    soma = sum(ind.fitness_value for ind in populacao)
    def seleciona_um():
        ponto = random.uniform(0, soma)
        acumulado = 0
        for ind in populacao:
            acumulado += ind.fitness_value
            if acumulado >= ponto:
                return ind
        return populacao[-1]
    return seleciona_um(), seleciona_um()


def selecao_torneio(populacao, k=3):
    """
    (Clássico) Seleção por torneio:
    escolhe k competidores aleatórios e retorna o melhor. Repete para dois pais.
    """
    def torneio():
        competidores = random.sample(populacao, k)
        return max(competidores, key=lambda ind: ind.fitness_value)
    return torneio(), torneio()


def selecao_truncamento(populacao, taxa=0.5):
    """
    (Clássico) Seleção por truncamento (dizimação):
    descarta os piores (1-taxa)% e seleciona pais aleatoriamente
    entre os melhores taxa*100%.
    """
    k = max(2, int(len(populacao) * taxa))
    ordenados = sorted(populacao, key=lambda ind: ind.fitness_value, reverse=True)
    pool = ordenados[:k]
    return random.choice(pool), random.choice(pool)


def selecao_ranking(populacao):
    """
    (Clássico) Seleção por ranking:
    atribui probabilidade de seleção proporcional à posição no ranking,
    reduzindo viés de fitness extremos.
    """
    ordenados = sorted(populacao, key=lambda ind: ind.fitness_value)
    n = len(ordenados)
    soma_ranks = n * (n + 1) / 2
    def select_one():
        ponto = random.uniform(1, soma_ranks)
        acumulado = 0
        for rank, ind in enumerate(ordenados, start=1):
            acumulado += rank
            if acumulado >= ponto:
                return ind
        return ordenados[-1]
    return select_one(), select_one()

# Crossover

def crossover_ponto_unico(pai1, pai2):
    """
    (Clássico) Crossover de ponto único:
    seleciona um ponto e combine prefixo de um pai com sufixo do outro.
    """
    n = pai1.n
    ponto = random.randrange(1, n)
    g1 = pai1.genes[:ponto] + [g for g in pai2.genes if g not in pai1.genes[:ponto]]
    g2 = pai2.genes[:ponto] + [g for g in pai1.genes if g not in pai2.genes[:ponto]]
    return Individuo(n, g1), Individuo(n, g2)


def crossover_ordem(pai1, pai2):
    """
    (Clássico) Order Crossover (OX):
    preserva a ordem relativa de um segmento contínuo de genes.
    """
    n = pai1.n
    i, j = sorted(random.sample(range(n), 2))
    def ox(p1, p2):
        segmento = p1.genes[i:j]
        restante = [g for g in p2.genes if g not in segmento]
        return restante[:i] + segmento + restante[i:]
    return Individuo(n, ox(pai1, pai2)), Individuo(n, ox(pai2, pai1))


def crossover_pmx(pai1, pai2):
    """
    (Clássico) Partially Mapped Crossover (PMX):
    mapeia elementos de um segmento entre pais para manter consistência.
    """
    n = pai1.n
    i, j = sorted(random.sample(range(n), 2))
    def pmx(p1, p2):
        filho = [None] * n
        for idx in range(i, j):
            filho[idx] = p1.genes[idx]
        for idx in range(i, j):
            if p2.genes[idx] not in filho:
                val = p2.genes[idx]
                pos = idx
                while True:
                    val2 = p1.genes[pos]
                    pos = p2.genes.index(val2)
                    if filho[pos] is None:
                        filho[pos] = val
                        break
        for idx in range(n):
            if filho[idx] is None:
                filho[idx] = p2.genes[idx]
        return filho
    return Individuo(n, pmx(pai1, pai2)), Individuo(n, pmx(pai2, pai1))


def crossover_uniforme(pai1, pai2):
    """
    (Clássico) Crossover uniforme:
    para cada posição, escolhe aleatoriamente de qual pai virá o gene.
    """
    n = pai1.n
    mask = [random.random() < 0.5 for _ in range(n)]
    g1 = [None] * n
    g2 = [None] * n
    for idx in range(n):
        if mask[idx]:
            g1[idx] = pai1.genes[idx]
            g2[idx] = pai2.genes[idx]
    def fill(g, p):
        for gene in p.genes:
            if gene not in g:
                g[g.index(None)] = gene
    fill(g1, pai2)
    fill(g2, pai1)
    return Individuo(n, g1), Individuo(n, g2)

# Mutação

def mutacao_swap(individuo):
    """
    (Clássico) Mutação swap:
    troca aleatoriamente dois genes de lugar.
    """
    i, j = random.sample(range(individuo.n), 2)
    individuo.genes[i], individuo.genes[j] = individuo.genes[j], individuo.genes[i]


def mutacao_deslocamento(individuo):
    """
    (Clássico) Mutação por deslocamento:
    remove um gene e o reinsera em outra posição.
    """
    genes = individuo.genes
    i, j = random.sample(range(individuo.n), 2)
    gene = genes.pop(i)
    genes.insert(j, gene)
    individuo.genes = genes


def mutacao_inversao(individuo):
    """
    (Clássico) Mutação inversão:
    inverte a ordem de um segmento contínuo de genes.
    """
    genes = individuo.genes
    i, j = sorted(random.sample(range(individuo.n), 2))
    genes[i:j] = reversed(genes[i:j])
    individuo.genes = genes


def mutacao_scramble(individuo):
    """
    (Clássico) Mutação scramble:
    embaralha aleatoriamente os genes em um segmento selecionado.
    """
    genes = individuo.genes
    i, j = sorted(random.sample(range(individuo.n), 2))
    segment = genes[i:j]
    random.shuffle(segment)
    genes[i:j] = segment
    individuo.genes = genes

# Elitismo

def elitismo_none(populacao):
    """
    (Clássico) Nenhum elitismo:
    não preserva indivíduos entre gerações.
    """
    return []


def elitismo_fixo(populacao, k):
    """
    (Clássico) Elitismo rígido:
    preserva os k melhores indivíduos.
    """
    return sorted(populacao, key=lambda ind: ind.fitness_value, reverse=True)[:k]


def elitismo_percentual(populacao, taxa):
    """
    (Clássico) Elitismo percentual:
    preserva os melhores taxa*100% indivíduos.
    """
    k = max(1, math.ceil(len(populacao) * taxa))
    return elitismo_fixo(populacao, k)


def elitismo_threshold(populacao, threshold):
    """
    (Clássico) Elitismo por limiar:
    preserva indivíduos com fitness >= threshold.
    """
    return [ind for ind in populacao if ind.fitness_value >= threshold]