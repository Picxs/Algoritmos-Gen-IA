import random
from individuo import Individuo

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
        self.individuos = [Individuo(self.n) for _ in range(self.tamanho)]

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

    def gera_nova_geracao(
        self,
        selecao,
        crossover,
        p_crossover,
        mutacao,
        p_mutacao,
        elitismo,
        elitismo_args=None
    ):
        """
        Aplica seleção, crossover, mutação e elitismo para formar a próxima geração.

        Parâmetros:
        - selecao: função(população) -> (pai1, pai2)
        - crossover: função(pai1, pai2) -> (filho1, filho2)
        - p_crossover: float, probabilidade de aplicar crossover
        - mutacao: função(ind) -> None (altera o indivíduo)
        - p_mutacao: float, probabilidade de mutação
        - elitismo: função(população[, **args]) -> lista de indivíduos elitistas
        - elitismo_args: dict de parâmetros para elitismo (opcional)
        """
        # Obtém elites, passando args se houver
        if elitismo_args:
            elites = elitismo(self.individuos, **elitismo_args)
        else:
            elites = elitismo(self.individuos)
        nova_pop = elites.copy()

        while len(nova_pop) < self.tamanho:
            pai1, pai2 = selecao(self.individuos)
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
            nova_pop.extend([f1, f2])

        self.individuos = nova_pop[:self.tamanho]
        self.avalia()

    def gera_nova_geracao2(
        self,
        selecao,
        crossover,
        p_crossover,
        mutacao,
        p_mutacao,
        elitismo,
        elitismo_args=None
    ):
        """
        Variante sem permitir duplicação dos elitistas via seleção e clonagem.

        Parâmetros:
        - selecao: função(população) -> (pai1, pai2)
        - crossover: função(pai1, pai2) -> (filho1, filho2)
        - p_crossover: float, probabilidade de aplicar crossover
        - mutacao: função(ind) -> None (altera o indivíduo)
        - p_mutacao: float, probabilidade de mutação
        - elitismo: função(população[, **args]) -> lista de indivíduos elitistas
        - elitismo_args: dict de parâmetros para elitismo (opcional)
        """
        if elitismo_args:
            elites = elitismo(self.individuos, **elitismo_args)
        else:
            elites = elitismo(self.individuos)
        nova_pop = elites.copy()

        # Pool sem elites para seleção
        pool = [ind for ind in self.individuos if ind not in elites]
        if not pool:
            pool = self.individuos.copy()

        while len(nova_pop) < self.tamanho:
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
            nova_pop.extend([f1, f2])

        self.individuos = nova_pop[:self.tamanho]
        self.avalia()