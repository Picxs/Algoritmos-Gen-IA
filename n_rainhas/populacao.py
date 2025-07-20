import random
from .individuo import Individuo

class Populacao:
    """Gerencia uma população de indivíduos/tabuleiros."""
    def __init__(self, n, tamanho):
        if n < 4:
            raise ValueError("Para n-rainhas, n deve ser >= 4")
        self.n = n
        self.tamanho = tamanho
        self.individuos = []

    def inicializa(self):
    """Gera a população inicial com indivíduos aleatórios."""
    self.individuos = []
    for _ in range(self.tamanho):
        novo = Individuo(self.n)
        self.individuos.append(novo)

    def avalia(self):
        """Avalia o fitness de todos os indivíduos da população."""
        for ind in self.individuos:
            ind.fitness()

    def melhor(self):
        """Retorna o indivíduo com maior fitness."""
        return max(
            self.individuos,
            key=lambda ind: ind.fitness_value if ind.fitness_value is not None else ind.fitness()
        )

    # Permite a duplicação dos mais aptos pelo elitismo e clonagem no crossover
    def gera_nova_geracao(
        self,
        selecao,
        crossover,
        p_crossover,
        mutacao,
        p_mutacao,
        elitismo
    ):
        """
        Aplica seleção, crossover, mutação e elitismo para formar a próxima geração.

        Parâmetros:
        - selecao: função(população) -> (pai1, pai2)
        - crossover: função(pai1, pai2) -> (filho1, filho2)
        - p_crossover: float, probabilidade de aplicar crossover
        - mutacao: função(ind) -> None (altera o indivíduo)
        - p_mutacao: float, probabilidade de mutação
        - elitismo: função(população) -> lista de indivíduos elitistas
        """
        # Seleciona elites e inicializa nova população
        elites = elitismo(self.individuos)
        nova_pop = elites.copy()

        # Geração de novos indivíduos
        while len(nova_pop) < self.tamanho:
            pai1, pai2 = selecao(self.individuos)
            # Crossover
            if random.random() < p_crossover:
                f1, f2 = crossover(pai1, pai2)
            else:
                # clones
                f1 = Individuo(self.n, pai1.genes)
                f2 = Individuo(self.n, pai2.genes)
            # Mutação
            if random.random() < p_mutacao:
                mutacao(f1)
            if random.random() < p_mutacao:
                mutacao(f2)
            nova_pop.extend([f1, f2])

        # Ajusta tamanho e avalia
        self.individuos = nova_pop[:self.tamanho]
        self.avalia()

    # Não permite a duplicação dos mais aptos pelo elitismo e clonagem no crossover, deixa apenas no elitismo
    def gera_nova_geracao2(
        self,
        selecao,
        crossover,
        p_crossover,
        mutacao,
        p_mutacao,
        elitismo
    ):
        """
        Aplica seleção, crossover, mutação e elitismo para formar a próxima geração.

        Parâmetros:
        - selecao: função(população) -> (pai1, pai2)
        - crossover: função(pai1, pai2) -> (filho1, filho2)
        - p_crossover: float, probabilidade de aplicar crossover
        - mutacao: função(ind) -> None (altera o indivíduo)
        - p_mutacao: float, probabilidade de mutação
        - elitismo: função(população) -> lista de indivíduos elitistas
        """
        # Seleciona elites e inicializa nova população
        elites = elitismo(self.individuos)
        new_pop = elites.copy()

        # Prepara pool de seleção sem os elites
        pool = [ind for ind in self.individuos if ind not in elites]
        if not pool:
            # Se todos são elites, volta para toda população
            pool = self.individuos.copy()

        # Gera novos indivíduos até preencher população
        while len(new_pop) < self.tamanho:
            pai1, pai2 = selecao(pool)
            # Crossover ou clonagem
            if random.random() < p_crossover:
                f1, f2 = crossover(pai1, pai2)
            else:
                f1 = Individuo(self.n, pai1.genes)
                f2 = Individuo(self.n, pai2.genes)
            # Mutação
            if random.random() < p_mutacao:
                mutacao(f1)
            if random.random() < p_mutacao:
                mutacao(f2)
            new_pop.extend([f1, f2])

        # Ajusta para o tamanho e avalia
        self.individuos = new_pop[:self.tamanho]
        self.avalia()
