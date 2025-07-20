import random

class Individuo:
    """
    Representa um indivíduo/tabuleiro para o problema das n-rainhas
    e o genes é uma lista de inteiros, onde o índice é a coluna e o valor 
    é a linha da rainha.
    """

    #TODO o n tem que ser maior ou igual a 4
    def __init__(self, n, genes=None):
        self.n = n
        if genes is None:
            # Gera uma permutação aleatória de 0 a n-1
            self.genes = list(range(n))
            random.shuffle(self.genes)
        else:
            if len(genes) != n:
                raise ValueError(f"Genes deve ter tamanho {n}")
        self.genes = genes.copy()
        self.conflitos = None
        self.fitness_value = None

    def calc_conflitos(self):
        """
        Calcula número de pares de rainhas em conflito.
        O conflito aceontece quando temos mais de uma rainha
        em uma mesma linha ou mesma diagonal.
        """
        n = self.n
        conflitos = 0
        for i in range(n):
            for j in range(i + 1, n):
                if self.genes[i] == self.genes[j] or abs(self.genes[i] - self.genes[j]) == abs(i - j):
                    conflitos += 1
        self.conflitos = conflitos
        return conflitos

    def fitness(self):
        """
        Fitness: número de pares sem conflito.
        Max pares = n*(n-1)/2.
        """
        if self.conflitos is None:
            self.calc_conflitos()
        max_pairs = self.n * (self.n - 1) // 2
        self.fitness_value = max_pairs - self.conflitos
        return self.fitness_value

    def __repr__(self):
        return f"Individuo(n={self.n}, genes={self.genes})"